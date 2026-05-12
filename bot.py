from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# ----------------------------
# HEADLESS CHROME SETUP
# ----------------------------
options = Options()
options.add_argument("--headless=new")          # no window
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

# Open site
driver.get("http://vinme.ge/")

time.sleep(5)

# ----------------------------
# START CHAT
# ----------------------------
try:
    start_btn = driver.find_element(By.ID, "startButton")
    start_btn.click()
    print("✅ Started chat")
except:
    print("❌ Start button not found")

time.sleep(5)

# ----------------------------
# MAIN LOOP
# ----------------------------
while True:
    try:
        # Find next user
        next_btn = driver.find_element(By.ID, "findNextButton")
        next_btn.click()
        print("🔄 Clicked Find Next")

        time.sleep(2)

        # Message box + send button
        msg_box = driver.find_element(By.ID, "message")
        send_btn = driver.find_element(By.ID, "submit")

        # First message
        msg_box.send_keys("hi")
        send_btn.click()

        time.sleep(2)

        # Second message
        msg_box.send_keys(
            "ზუსტად ესეთი გაცნობის საიტია, ამას ბევრად ჯობია ❤️ https://gaicani.online/"
        )
        send_btn.click()

        print("✅ Message sent successfully")

        time.sleep(5)

    except Exception as e:
        print("❌ Error:", e)
        time.sleep(3)