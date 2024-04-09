#! /home/matthew/Desktop/PythonProjects/data_processing.code-workspace/venv/bin/python3.12
#terminal_ai.py

from undetected_playwright.sync_api import Browser, Page, Playwright, sync_playwright

from browser import launch_browser
from chat_manager import ChatManager
from utils.file_utils import save_cookies_to_file
from utils.general_utils import clear_screen
from logs.logger import function_log, logger

class TerminalAIApp:
    def __init__(self, playwright: Playwright, ai: str):
        self.playwright: Playwright = playwright
        self.ai:str = ai
        self.page: Page = None
        self.browser: Browser = None
        self.chat_manager: ChatManager = None
           
    def run(self):
        clear_screen()
        self.page, self.browser = launch_browser(self.playwright, self.ai)
        self.chat_manager: ChatManager = ChatManager(self.page, self.ai)
        self.chat_manager.primary_screen()
        cookies = self.page.context.cookies()
        save_cookies_to_file(cookies)
        self.browser.close()
                                
def main() -> None:
    with sync_playwright() as playwright:
        terminal_ai: TerminalAIApp = TerminalAIApp(playwright, "chatGPT")
        terminal_ai.run()
        
if __name__ == "__main__":
    main() 