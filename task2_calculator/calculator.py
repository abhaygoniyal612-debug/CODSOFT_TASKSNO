"""
Zanpakuto Calculator - A Bleach-themed command line calculator
Channel your reiatsu into basic arithmetic operations!
"""

import sys

# ANSI color codes for that Soul Society aesthetic
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    BLACK_ROBE = "\033[90m"      # Shinigami robes
    HOLLOW_WHITE = "\033[97m"
    ICHIGO_ORANGE = "\033[38;5;208m"
    ZANGETSU_BLUE = "\033[38;5;39m"
    HITSUGAYA_CYAN = "\033[96m"
    RUKIA_PURPLE = "\033[95m"
    HOLLOW_RED = "\033[91m"
    SOUL_GOLD = "\033[93m"
    BANKAI_GREEN = "\033[92m"


BANNER = f"""{Colors.ICHIGO_ORANGE}{Colors.BOLD}
   ______              _                   
  |___  /             | |                  
     / /  __ _  _ __   | | __ _  _   _ | |_   ___  
    / /  / _` || '_ \\  | |/ _` || | | || __| / _ \\ 
   / /__| (_| || | | | | | (_| || |_| || |_ | (_) |
  /_____|\\__,_||_| |_| |_|\\__, | \\__,_| \\__| \\___/ 
                            __/ |                  
                           |___/                   
{Colors.RESET}{Colors.ZANGETSU_BLUE}  === ZANPAKUTO CALCULATOR :: Getsuga Tensho Edition ==={Colors.RESET}
"""

DIVIDER = f"{Colors.BLACK_ROBE}{'-' * 55}{Colors.RESET}"

OPERATION_FLAVOR = {
    "1": ("+", f"{Colors.BANKAI_GREEN}Combining reiatsu (Addition){Colors.RESET}"),
    "2": ("-", f"{Colors.HOLLOW_RED}Slashing away power (Subtraction){Colors.RESET}"),
    "3": ("*", f"{Colors.SOUL_GOLD}Bankai amplification (Multiplication){Colors.RESET}"),
    "4": ("/", f"{Colors.HITSUGAYA_CYAN}Splitting the soul (Division){Colors.RESET}"),
}

BANKAI_QUOTES = [
    "Bankai! The result manifests before you!",
    "Getsuga Tensho! Calculation cleaved clean!",
    "Your zanpakuto's spirit whispers the answer...",
    "The Soul Society approves this result.",
]


def print_banner():
    print(BANNER)


def print_menu():
    print(DIVIDER)
    print(f"{Colors.HOLLOW_WHITE}Choose your technique (operation):{Colors.RESET}")
    print(f"  {Colors.BANKAI_GREEN}1{Colors.RESET} - Addition       (+)  {Colors.BLACK_ROBE}Combine reiatsu{Colors.RESET}")
    print(f"  {Colors.HOLLOW_RED}2{Colors.RESET} - Subtraction    (-)  {Colors.BLACK_ROBE}Slash away power{Colors.RESET}")
    print(f"  {Colors.SOUL_GOLD}3{Colors.RESET} - Multiplication (*)  {Colors.BLACK_ROBE}Bankai amplify{Colors.RESET}")
    print(f"  {Colors.HITSUGAYA_CYAN}4{Colors.RESET} - Division      (/)  {Colors.BLACK_ROBE}Split the soul{Colors.RESET}")
    print(DIVIDER)


def get_number(prompt):
    while True:
        raw = input(f"{Colors.RUKIA_PURPLE}{prompt}{Colors.RESET}").strip()
        try:
            return float(raw)
        except ValueError:
            print(f"{Colors.HOLLOW_RED}That's not a valid number, Shinigami. Focus your reiatsu and try again.{Colors.RESET}")


def get_operation_choice():
    while True:
        choice = input(f"{Colors.HOLLOW_WHITE}Select technique (1-4): {Colors.RESET}").strip()
        if choice in OPERATION_FLAVOR:
            return choice
        print(f"{Colors.HOLLOW_RED}Unknown technique. Choose 1, 2, 3, or 4.{Colors.RESET}")


def calculate(a, op_symbol, b):
    if op_symbol == "+":
        return a + b
    if op_symbol == "-":
        return a - b
    if op_symbol == "*":
        return a * b
    if op_symbol == "/":
        if b == 0:
            raise ZeroDivisionError
        return a / b


def format_result(value):
    # Trim trailing .0 for whole numbers, keep decimals otherwise
    if value == int(value):
        return str(int(value))
    return f"{value:.6g}"


def run_calculator():
    print_banner()

    while True:
        print_menu()

        num1 = get_number("Enter your first reiatsu value: ")
        choice = get_operation_choice()
        num2 = get_number("Enter your second reiatsu value: ")

        symbol, flavor_text = OPERATION_FLAVOR[choice]
        print(f"\n{flavor_text}")

        try:
            result = calculate(num1, symbol, num2)
        except ZeroDivisionError:
            print(f"\n{Colors.HOLLOW_RED}{Colors.BOLD}HOLLOW ERROR: Division by zero rips a hole in reality!")
            print(f"Even a Captain-level Shinigami cannot divide by the void.{Colors.RESET}\n")
        else:
            import random
            quote = random.choice(BANKAI_QUOTES)
            print(f"\n{Colors.ZANGETSU_BLUE}{quote}{Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.SOUL_GOLD}>>> {format_result(num1)} {symbol} {format_result(num2)} "
                  f"= {format_result(result)} <<<{Colors.RESET}\n")

        again = input(f"{Colors.HOLLOW_WHITE}Draw your zanpakuto again? (y/n): {Colors.RESET}").strip().lower()
        if again != "y":
            print(f"\n{Colors.ICHIGO_ORANGE}{Colors.BOLD}Farewell, Shinigami. May your blade stay sharp.{Colors.RESET}")
            break


if __name__ == "__main__":
    try:
        run_calculator()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.HOLLOW_RED}Calculation interrupted... a Hollow must have appeared!{Colors.RESET}")
        sys.exit(0)