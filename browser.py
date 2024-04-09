#browser.py

from undetected_playwright.sync_api import Browser, Page, Playwright

from utils.constants import URLS, CHANNEL, BROWSER_ARGS, VIEWPORT, HEADERS, USER_AGENT
from utils.file_utils import load_cookies_from_file, save_cookies_to_file

def launch_browser(playwright: Playwright, ai: str):
    ai: str = ai
    url: str = URLS[ai]
    cookies_saved = load_cookies_from_file()

    if cookies_saved:
        browser: Browser = playwright.chromium.launch(headless=True, channel=CHANNEL, args=BROWSER_ARGS)  
        context: Browser = browser.new_context(viewport=VIEWPORT, 
                                            extra_http_headers=HEADERS,
                                            user_agent=USER_AGENT)
        page: Page = context.new_page()
        page.context.add_cookies(cookies_saved)
        page.goto(url)
    
        return page, browser
    else:
        browser: Browser = playwright.chromium.launch(headless=False, channel=CHANNEL, args=BROWSER_ARGS)  
        context: Browser = browser.new_context(viewport=VIEWPORT, 
                                            extra_http_headers=HEADERS,
                                            user_agent=USER_AGENT)
        page: Page = context.new_page()
        page.goto(url)
        input("\n\nPlease log in manually in the new window and press any button to continue. You will only have to  do this once.")
        cookies = page.context.cookies()
        save_cookies_to_file(cookies)
        browser.close()
        launch_browser(playwright, ai)