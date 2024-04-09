#general_utils.py

from colorama import Fore
from os import system 
from time import sleep
from typing import Optional

from undetected_playwright.sync_api import Page

from utils.constants import icon
from logs.logger import function_log, logger

def action(element: Page, action: str, input_: Optional[str] = None) -> None:
        element_not_visible = True
        i: int = 0
        while element_not_visible and i < 100:
            if element.is_visible():
                element_not_visible = False
                break
            sleep(0.1)
            i+=1

        if i < 100:
            match action:
                case "click":
                    element.click()
                case "type":
                    element.type(input_)
                case "fill":
                    element.fill(input_)
                case "wait":
                    pass
        else: 
            print(f"{Fore.RED}Element {element} not found after 100 attempts! Exiting program.{Fore.RESET}")
            exit()

def robust_click(element: Page):
    action(element, "click")

def robust_fill(element: Page, input: str):
    action(element, "fill", input)

def robust_type(element: Page, input: str):
    action(element, "type", input)

def robust_wait_for_element(element: Page):
    action(element)
            
def print_logo():
        _ = [print(f"{Fore.RESET}{line}") for line in icon]

def clear_screen(exit=False):
    system("clear")
    if not exit:
        print_logo()

def screenshot(self, path: str, page: Page):
    path = f"{path}.png"
    page.screenshot(path=path, full_page=True)

