import json
from colorama import Fore, Style


def print_lambda(message, color=Fore.RESET):
    return lambda x: (print(color + message + json.dumps(x, indent=4, ensure_ascii=False) + Style.RESET_ALL), x)[1]
