#constants.py

from platform import system

icon_0="████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗             █████╗ ██╗"
icon_1="╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║            ██╔══██╗██║"
icon_2="   ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║     █████╗ ███████║██║"
icon_3="   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║     ╚════╝ ██╔══██║██║"
icon_4="   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗       ██║  ██║██║"
icon_5="   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝       ╚═╝  ╚═╝╚═╝"

icon = [icon_0, icon_1, icon_2, icon_3, icon_4, icon_5]  

CHANNEL: str = "chrome"
BROWSER_ARGS: list[str] = ["--disable-blink-features=AutomationControlled"]
HEADERS: dict[str,str] = {"SEC-CH-PREFERS-COLOR-SCHEME":"dark",
           "Accept-Language":"en-GB,en;q=0.9,en-US;q=0.8"}
VIEWPORT: dict[str,int] = {"width":1280, "height":672}
USER_AGENT: str = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"
URLS: dict[str,str] = {"ClaudeAI": "httpe://claude.ai",
                    "chatGPT": "https://chat.openai.com"}

COOKIES_PATH_DICT: dict[str,str] = {"Linux":"/data/cookies.json",
                                    "Darwin":"/data/cookies.json",
                                    "Windows":r"\data\cookies.json"}
OS: str = system()
COOKIES_PATH: str = COOKIES_PATH_DICT[OS]

