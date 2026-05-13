from playwright.sync_api import sync_playwright
import time

print("Bot started")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto("http://vinme.ge/")
    time.sleep(5)

    try:
        page.click("#startButton")
        print("Start clicked")
    except:
        print("Start failed")

    time.sleep(5)

    while True:
        try:
            page.click("#findNextButton")
            print("Next clicked")

            time.sleep(2)

            page.fill("#message", "hello welcome to my site")
            page.click("#submit")

            print("Message sent successfully")

            time.sleep(5)

        except Exception as e:
            print("Error:", e)
            time.sleep(5)
