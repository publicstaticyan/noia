import requests
import time
import os
from urllib.parse import urlencode

PRICE_THRESHOLD = 1500

kabum_base_url = "https://servicespub.prod.api.aws.grupokabum.com.br/catalog/v2/products-by-category/hardware/memoria-ram/ddr-5"

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print(f"Telegram notification sent successfully")
        return True
    except Exception as e:
        print(f"Error sending Telegram message: {e}")
        return False


def format_product_message(product):
    attrs = product.get('attributes', {})
    title = attrs.get('title', 'Unknown Product')
    product_id = product.get('id', 'N/A')
    price = attrs.get('price', 0)
    price_with_discount = attrs.get('price_with_discount', 0)
    discount_percentage = attrs.get('discount_percentage', 0)
    product_link = attrs.get('product_link', '')
    stock = attrs.get('stock', 0)

    final_price = price_with_discount if price_with_discount < price else price

    full_url = f"https://www.kabum.com.br/produto/{product_id}/{product_link}" if product_link else f"https://www.kabum.com.br/produto/{product_id}"

    message = f"🚨 <b>OFERTA ENCONTRADA!</b> 🚨\n\n"
    message += f"<b>{title}</b>\n\n"
    message += f"💰 Preço: R$ {final_price:.2f}\n"

    if discount_percentage > 0:
        message += f"🎯 Desconto: {discount_percentage}%\n"
        message += f"De: R$ {price:.2f}\n"

    message += f"📦 Estoque: {stock} unidades\n"
    message += f"\n🔗 <a href='{full_url}'>Ver produto</a>"

    return message


def scrape_kabum_page(page_number):
    params = {
        'page_number': page_number,
        'page_size': 50,
        'facet_filters': '',
        'sort': 'most_searched',
        'is_prime': 'false',
        'payload_data': 'products_category_filters',
        'include': 'gift'
    }

    url = f"{kabum_base_url}?{urlencode(params)}"

    try:
        print(f"Scraping page {page_number}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error scraping page {page_number}: {e}")
        return None


def check_product_price(product):
    attrs = product.get('attributes', {})

    price = attrs.get('price', float('inf'))
    price_with_discount = attrs.get('price_with_discount', float('inf'))
    title = attrs.get('title', 'Unknown Product')

    if (
            (price < PRICE_THRESHOLD or price_with_discount < PRICE_THRESHOLD)
            and 'ddr5' in title.lower()
            and '32' in title.lower()
            and 'sodimm' not in title.lower()
            and 'notebook' not in title.lower()
            and 'server' not in title.lower()):
        return True

    return False


def check_products(products, total_notifications_sent, total_products_found):
    for product in products:
        total_products_found += 1

        if check_product_price(product):
            product_id = product.get('id')
            attrs = product.get('attributes', {})
            title = attrs.get('title', 'Unknown')
            price = attrs.get('price')
            price_with_discount = attrs.get('price_with_discount')

            print(f"\n🎯 Found product below threshold:")
            print(f"   ID: {product_id}")
            print(f"   Title: {title[:50]}...")
            print(f"   Price: R$ {price:.2f}")
            print(f"   Price with discount: R$ {price_with_discount:.2f}")

            message = format_product_message(product)
            if send_telegram_message(message):
                total_notifications_sent += 1

            time.sleep(1)

    return total_notifications_sent, total_products_found


def scrape_all_pages():
    page_number = 1
    total_products_found = 0
    total_notifications_sent = 0

    print("=" * 60)
    print("Starting Kabum scraper...")
    print(f"Price threshold: R$ {PRICE_THRESHOLD:.2f}")
    print("=" * 60)

    while True:
        data = scrape_kabum_page(page_number)

        if not data:
            print("Error fetching data. Stopping.")
            break

        products = data.get('data', [])

        if not products:
            print(f"No more products found on page {page_number}. Scraping complete.")
            break

        print(f"Found {len(products)} products on page {page_number}")

        total_notifications_sent, total_products_found = (check_products(products, total_notifications_sent, total_products_found))

        meta = data.get('meta', {})
        total_pages = meta.get('total_pages_count', 1)

        if page_number >= total_pages:
            print(f"\nReached last page ({total_pages}). Scraping complete.")
            break

        page_number += 1
        time.sleep(1)

    print("\n" + "=" * 60)
    print("Scraping Summary:")
    print(f"Total products checked: {total_products_found}")
    print(f"Notifications sent: {total_notifications_sent}")
    print("=" * 60)

    return {
        "total_products_found": total_products_found,
        "total_notifications_sent": total_notifications_sent
    }


if __name__ == "__main__":
    scrape_all_pages()
