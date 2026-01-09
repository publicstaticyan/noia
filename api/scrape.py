from http.server import BaseHTTPRequestHandler
import json
from main import scrape_all_pages


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            print("Vercel Cron: Starting scrape job...")
            result = scrape_all_pages()

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            response_data = {
                "status": "success",
                "message": "Scraping completed",
                "data": result
            }
            self.wfile.write(json.dumps(response_data).encode())

        except Exception as e:
            print(f"Error in Vercel cron job: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            error_data = {
                "status": "error",
                "message": str(e)
            }
            self.wfile.write(json.dumps(error_data).encode())
