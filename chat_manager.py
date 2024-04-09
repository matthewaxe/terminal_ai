#chat_manager.py
from time import sleep

from colorama import Fore

from undetected_playwright.sync_api import Page

from logs.logger import function_log, logger
from utils.general_utils import robust_click, robust_type, clear_screen


class ChatManager:
    def __init__(self, page: Page, ai: str):
        self.page: Page = page
        self.ai: str = ai
        #chatGPT elements
        self.chatGPT_answer_output: Page = self.page.locator(r"div.markdown.prose.w-full.break-words.dark\:prose-invert")
        self.chatGPT_question_input: Page = self.page.get_by_placeholder("Message ChatGPT…")
        self.chatGPT_stop_generating: Page = self.page.get_by_role("button", name="Stop generating")
        self.chatGPT_chats: dict[str,str] = {}
        self.chatGPT_keys_to_remove: list[str] = [r"ChatGPT\nNew chat", "", r"Upgrade plan\nGet GPT-4, DALL·E, and more"]

        #claudeAI elements
        self.claude_initial_question_input: Page = self.page.locator("div.flex.items-center.flex-grow.break-words.min-w-0 > div.flex.flex-col.w-full > div.overflow-y-auto.w-full.max-h-96.break-words.py-4 > div.ProseMirror.break-words.max-w-\\[60ch\\]")
        self.claude_question_input: Page = self.page.get_by_text("Reply to Claude...")
        self.question_input_elements: list[Page] = [self.claude_initial_question_input, 
                                                    self.claude_question_input]
        self.claudeai_answer_output: Page = self.page.locator("whitespace-normal break-words")
        self.claude_answer_output: Page = self.page.locator("div[data-is-streaming='false'][class^='group ']")
        self.copy_button: Page = self.page.get_by_role("button", name=" Copy")


        self.elements: dict[str, dict[str,Page]] = {"chatGPT": {"answer_output": self.chatGPT_answer_output,
                                                                "question_input": self.chatGPT_question_input,
                                                                "response_finished_confirmation": self.chatGPT_stop_generating},

                                                    "ClaudeAI": {"answer_output": self.claudeai_answer_output}
                                                    }

    def primary_screen(self) -> None:
        user_input = input(f"{Fore.RESET}Type {Fore.BLUE}message{Fore.RESET}, type '{Fore.BLUE}c{Fore.RESET}' to see recent chats or type '{Fore.BLUE}e{Fore.RESET}' to exit):\n\n{Fore.YELLOW}")
        if user_input == "e":
            print(f"{Fore.RED}Exiting Terminal-AI.{Fore.RESET}")
            clear_screen(exit=True)
        elif user_input == "c":
            self.chat_screen()
            
        else:                
            self.input_question(user_input)
            self.get_response()
            self.primary_screen()

    def chat_screen(self):
        user_input: str = self.get_chat()
        
        if user_input == "b":
            clear_screen()
            self.primary_screen()
        
        else:
                href: str = self.chatGPT_chats[user_input]
                self.chat_options(href)

    def chat_options(self, href: str) -> None:
        self.page.goto(f"{self.url}{href}")
        user_input: str = input(f"{Fore.RESET}Press '{Fore.BLUE}f{Fore.RESET}' to see full chat, press '{Fore.BLUE}b{Fore.RESET}' to go back. Type a question to continue chat: ")
        if user_input == 'b':
            self.page.goto(self.url)
            self.primary_screen()
        if user_input == "f":
            previous_chat_responses = self.get_previous_chat_responses()
            for response in previous_chat_responses:
                print(response)
            self.primary_screen()
        else:
            self.input_question(user_input)
            self.get_response()
            self.primary_screen()  


    def input_question(self, question: str):
        match self.ai:
            case "ClaudeAI":
                question_input: Page = self.get_question_input()
                
            case "chatGPT":
                question_input: Page = self.elements[self.ai]["question_input"]
        
        robust_click(question_input)
        robust_type(question_input, f"{question}")
        self.page.keyboard.press("Enter")

    def get_question_input(self):
        for _ in range(10):
            for question_input in self.question_input_elements:
                if question_input.is_visible():
                    return question_input
                sleep(0.1)

    def get_previous_chats(self):
        chats: list[Page] = self.page.locator("a.flex").all()
        chatGPT_chats = {chat.inner_text():chat.get_attribute("href") for chat in chats}
        self.chatGPT_chats = {key:value for key, value in chatGPT_chats.items() if key not in self.chatGPT_keys_to_remove}

    def get_response(self):
        text = self.generated_text(self.elements[self.ai]["response_finished_confirmation"])
        print(f"\n{Fore.GREEN}Terminal-AI{Fore.RESET}: {text}\n")           
           
    def generated_text(self, element: Page):
        sleep(0.5)
        while True:
            if element.is_visible():
                pass
            else:
                response: list[Page] = self.elements[self.ai]["answer_output"].all()
                response: str = response[len(response)-1].inner_text()
                return response
                                                                    
    def get_chat(self) -> str:
        self.get_previous_chats()
        chat_keys: list[str] = [f"{i}. {key}" for i, key in enumerate(self.chatGPT_chats.keys())]
        for chat in chat_keys:
            print(f"{Fore.RESET}{chat}")
        
        user_input: str = input(f"\n{Fore.RESET}Select chat or press '{Fore.BLUE}b{Fore.RESET}' to go back: ")
        for key in chat_keys:
            if user_input in key:
                user_input = key.replace(f"{user_input}. ", "")
                clear_screen()
                return user_input
                
        return user_input
               
    def get_previous_chat_responses(self) -> list[str]:
        responses: list[Page] = self.elements[self.ai]["answer_output"].all()
        previous_chat_responses = [response.inner_text() for response in responses]
        return previous_chat_responses