from colorama import Fore, Style, Back


def print_error(message):
    print(Fore.RED, message, Style.RESET_ALL, sep="")


def print_title(message):
    print(Fore.BLUE, message, Style.RESET_ALL, sep="")


def print_success(message):
    print(Back.GREEN, Fore.BLACK, ' УСПЕШНО ', Style.RESET_ALL, " ", sep="", end="")
    print(message)


def color_input(message: str) -> str:
    print(Fore.YELLOW, message, Fore.GREEN, sep="", end="")
    value = input()
    print(Style.RESET_ALL, sep="", end="")
    return value
