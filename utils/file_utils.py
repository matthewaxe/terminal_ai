#file_handlers.py

import json
from typing import Union
from os import path

from utils.constants import COOKIES_PATH

def get_root_directory() -> str:
    current_dir: str = path.abspath(path.dirname(__file__))
    while not path.isfile(path.join(current_dir, 'main.py')):
        if path.dirname(current_dir) == current_dir:
            raise FileNotFoundError("Root directory not found.")
        current_dir: str = path.dirname(current_dir)
    return current_dir

def load_cookies_from_file() -> Union[bool, str]:
        try:
            with open(f"{get_root_directory()}{COOKIES_PATH}", 'r') as file:
                return json.loads(file.read())
        except FileNotFoundError:
            return False
        
def save_cookies_to_file(cookies) -> None:
    with open(f"{get_root_directory()}{COOKIES_PATH}", 'w') as file:
        file.write(json.dumps(cookies))

def save_page_content(self, path: str, content) -> None:
        path = f"{path}.txt"
        with open(path, "w") as file:
                    file.write(content)

def write_responses_to_file(response) -> None:
    with open('successful_response_headers.txt', 'a') as f:
        for header, value in response.headers.items():
            f.write(f'\nURL: {response.url}\nHeader:{header}: {value}\n')
