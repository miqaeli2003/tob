from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
import time
import sys

# ─── Config ───────────────────────────────────────────────────────────────────
URL            = "https://vinme.ge/"
MESSAGE        = "hello welcome to my site"
LOOP_DELAY     = 3        # seconds between "find next" cycles
MESSAGE_DELAY  = 1.5      # seconds after sending before moving on
HEADLESS       = True     # set False to watch the browser

# Selector candidates – first match wins
START_SELECTORS    = ["#startButton", "a:has-text('საუბრის დაწყება')",
                       "button:has-text('Start')", "[class*='start']"]
NEXT_SELECTORS     = ["#findNextButton", "a:has-text('მომიძებნე სხვა')",
                       "button:has-text('Next')", "[class*='next']",
                       "a[href*='next']"]
MESSAGE_SELECTORS  = ["#message", "textarea", "input[type='text']",
                       "[placeholder]", "[class*='message']"]
SUBMIT_SELECTORS   = ["#submit", "button[type='submit']",
                       "button:has-text('გაგზავნა')", "button:has-text('Send')",
                       "[class*='send']", "[class*='submit']"]
# ──────────────────────────────────────────────────────────────────────────────


def find_element(page, selectors: list, label: str, timeout: int = 5000):
    """Try each selector in order; return the first one that exists."""
    for sel in selectors:
        try:
            page.wait_for_selector(sel, timeout=timeout, state="visible")
            print(f"  ✓ [{label}] found via: {sel}")
            return sel
        except PWTimeout:
            continue
    raise RuntimeError(f"Could not find [{label}] with any selector: {selectors}")


def dump_page_selectors(page):
    """Helper – prints ids/classes on the page so you can tune selectors."""
    ids = page.evaluate("""
        () => [...document.querySelectorAll('[id]')]
              .map(e => '#' + e.id)
    """)
    print("\n── Element IDs on page ──")
    for i in ids:
        print(" ", i)

    buttons = page.evaluate("""
        () => [...document.querySelectorAll('button,a,input[type=button],input[type=submit]')]
              .map(e => e.outerHTML.slice(0, 120))
    """)
    print("\n── Buttons / links ──")
    for b in buttons:
        print(" ", b)
    print("────────────────────────\n")


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        )
        page = context.new_page()

        # ── Load site ─────────────────────────────────────────────────────────
        print(f"Opening {URL} …")
        page.goto(URL, wait_until="domcontentloaded", timeout=30_000)
        page.wait_for_load_state("networkidle", timeout=15_000)
        print("Page loaded.\n")

        # Uncomment the line below once to inspect real selectors:
        # dump_page_selectors(page)

        # ── Click Start ───────────────────────────────────────────────────────
        try:
            start_sel = find_element(page, START_SELECTORS, "Start button")
            page.click(start_sel)
            print("▶ Start clicked")
        except RuntimeError as e:
            print(f"⚠ Start button not found: {e}")
            dump_page_selectors(page)
            sys.exit(1)

        # Wait until chat UI is ready
        page.wait_for_timeout(2000)

        # ── Main loop ─────────────────────────────────────────────────────────
        MAX_CYCLES = 10
        cycle = 0
        while cycle < MAX_CYCLES:
            cycle += 1
            print(f"\n── Cycle {cycle}/{MAX_CYCLES} ──────────────────────")

            # Find next stranger
            try:
                next_sel = find_element(page, NEXT_SELECTORS, "Find Next")
                page.click(next_sel)
                print("⏭ Next clicked")
            except RuntimeError as e:
                print(f"⚠ Next button not found: {e}")
                time.sleep(LOOP_DELAY)
                continue

            # Type and send message as soon as partner connects
            try:
                msg_sel = find_element(page, MESSAGE_SELECTORS, "Message input")
                # Wait indefinitely until input is enabled (partner connected)
                page.wait_for_function(
                    "sel => !document.querySelector(sel).disabled",
                    arg=msg_sel
                )
                page.fill(msg_sel, MESSAGE)
                print(f"✉ Message filled: {MESSAGE!r}")

                submit_sel = find_element(page, SUBMIT_SELECTORS, "Submit button")
                page.click(submit_sel)
                print("✔ Message sent — finding next")

            except RuntimeError as e:
                print(f"⚠ Could not send message: {e}")


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\nStopped by user.")
