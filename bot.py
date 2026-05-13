from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# -----------------------------
# CHROME OPTIONS (HEADLESS)
# -----------------------------
options = Options()

# Run without opening browser window
options.add_argument("--headless=new")

# Linux / Railway fixes
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")

# Optional
options.add_argument("--window-size=1920,1080")

# Chromium path for Railway/Linux
options.binary_location = "/usr/bin/chromium"

# Start browser
driver = webdriver.Chrome(options=options)

print("✅ Browser started")

# Open website
driver.get("http://vinme.ge/")

print("✅ Opened website")

time.sleep(5)

# -----------------------------
# START CHAT
# -----------------------------
try:
    start_btn = driver.find_element(By.ID, "startButton")
    start_btn.click()

    print("✅ Started chat")

except Exception as e:
    print("❌ Could not start chat:", e)

time.sleep(5)

# -----------------------------
# MAIN LOOP
# -----------------------------
while True:
    try:
        # Find next user
        next_btn = driver.find_element(By.ID, "findNextButton")
        next_btn.click()

        print("🔄 Searching for next user")

        time.sleep(2)

        # Message input
        msg_box = driver.find_element(By.ID, "message")

        # Send button
        send_btn = driver.find_element(By.ID, "submit")

        # First message
        msg_box.send_keys("privet")
        send_btn.click()

        time.sleep(2)

        # Second message
        msg_box.send_keys(
            "ზუსტად ესეთი გაცნობის საიტია ❤️ https://gaicani.online/"
        )
        send_btn.click()

        print("✅ Message sent successfully")

        # Wait before next cycle
        time.sleep(5)

    except Exception as e:
        print("❌ Error:", e)

        time.sleep(3)
