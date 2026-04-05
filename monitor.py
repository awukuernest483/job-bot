from playwright.sync_api import sync_playwright
import os
import time
import requests

os.system("playwright install --with-deps")

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)

# Test message
send_telegram("✅ Test message")

URL = "https://marketplace.inv.tech/invi/explore"

def get_job_titles():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state="auth.json")
        page = context.new_page()

        page.goto(URL)

        if "login" in page.url.lower():
            send_telegram("⚠️ Bot logged out! Please refresh session.")
            browser.close()
            return []

        page.wait_for_timeout(5000)

        # Extract ONLY job titles
        jobs = page.locator("p.text-\\[18px\\].font-medium").all_text_contents()

        browser.close()
        return jobs


previous_jobs = []

while True:
    print("🔍 Checking for new jobs...")

    current_jobs = get_job_titles()

    # Find new ones
    new_jobs = [job for job in current_jobs if job not in previous_jobs]

    if new_jobs:
        for job in new_jobs:
            message = f"🚨 New Job: {job}"
            print(message)
            send_telegram(message)

    previous_jobs = current_jobs

    time.sleep(60)
