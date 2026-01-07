# NoIA

A webscraper that monitors DDR5 memories on Kabum and sends Telegram notifications when items are found below a specified price threshold.

## Features

- 🔍 Scrapes all pages from Kabum API until no more products are found
- 💰 Monitors products with `price` or `price_with_discount` below threshold
- 📱 Sends formatted Telegram messages to a group/channel
- 🔗 Provides direct product links in notifications

## Setup

### 1. Install Dependencies

```cmd
pip install -r requirements.txt
```

### 2. Configure Telegram Bot

You need to set up a Telegram bot and get your credentials:

#### Create a Telegram Bot:
1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Copy the **Bot Token** you receive

#### Get Your Chat ID:
1. Add your bot to your Telegram group
2. Send a message in the group
3. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Look for the `"chat":{"id":` field and copy the chat ID

### 3. Update Configuration

Edit `main.py` and replace these values:

```python
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Your bot token from BotFather
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"      # Your group chat ID
```

You can also adjust:
- `PRICE_THRESHOLD` - The price limit (default: 1500)
- `kabum_base_url` - The Kabum API endpoint to scrape

## Usage

Run the scraper:

```cmd
python main.py
```

The script will:
1. Start scraping from page 1
2. Check all products on each page
3. Send Telegram notifications for products below the threshold
4. Continue to the next page until no more products are found
5. Display a summary when complete

## Files

- `main.py` - Main scraper script
- `requirements.txt` - Python dependencies

## Notification Format

Each notification includes:
- 🚨 Alert header
- Product title
- 💰 Current price
- 🎯 Discount percentage (if applicable)
- 📦 Stock availability
- 🔗 Direct link to product page

## Scheduling

To run this periodically, you can adjust the `.github/workflows/scraper.yml` file at your desired cron.

---

<h5 align="center">
    <em>In favor of the failure of AI companies in a world that doesn't need their shitification and corporate greed. F*ck AI companies, long live PC building</em>
</h5>