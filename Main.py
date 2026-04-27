#!/usr/bin/env python3
import os
import time
import sys

# ANSI رنګونه د متن لپاره
WHITE_TEXT = "\033[97m"
BOLD = "\033[1m"
RESET = "\033[0m"
UNDERLINE = "\033[4m"
GOLD_TEXT = "\033[38;2;255;215;0m"      # طلایی متن

# د بکس لاینونو لپاره رنګونه (طلایی او سرو زرو رنګونه)
GOLD_LINE = "\033[38;2;255;215;0m"      # طلایی (Gold)
DARK_GOLD = "\033[38;2;184;134;11m"     # تیاره طلایی (Dark Goldenrod)
LIGHT_GOLD = "\033[38;2;255;223;0m"     # روښانه طلایی
RED_GOLD = "\033[38;2;255;69;0m"        # سور-طلایی

# د لومړي بکس لپاره مختلف شالید رنګونه (نوي رنګونه)
BOX1_BG_COLORS = [
    "\033[48;2;128;0;32m",     # د چوغندر رنګ (Burgundy)
    "\033[48;2;75;0;130m",     # نیلي-بنفش (Indigo)
    "\033[48;2;0;0;128m",      # تیاره نیلي (Navy)
    "\033[48;2;0;64;128m",     # نیلي-خړ (Steel Blue)
    "\033[48;2;0;128;128m",    # تیل (Teal)
    "\033[48;2;0;128;64m",     # شنه (Green)
]

# د دویم بکس لپاره مختلف شالید رنګونه (نوي رنګونه)
BOX2_BG_COLORS = [
    "\033[48;2;128;0;128m",     # ارغواني (Purple)
    "\033[48;2;255;20;147m",    # ګلابي (Deep Pink)
    "\033[48;2;255;69;0m",      # سور-نارنجي (Orange Red)
    "\033[48;2;255;140;0m",     # نارنجي (Dark Orange)
    "\033[48;2;218;165;32m",    # طلایی (Goldenrod)
    "\033[48;2;255;215;0m",     # طلایی (Gold)
]

# د کرښو لپاره ځانګړي رنگین کوډونه
LINE_BOLD = "\033[1m"

# د پرامپټ درې مختلف رنګونه - د ❯ نښو لپاره
RED_ARROW = "\033[91m"      # سور رنګ
GREEN_ARROW = "\033[92m"    # شین رنګ
BLUE_ARROW = "\033[94m"     # نیلي رنګ

logo = '''

 ███████╗ █████╗ █████╗░░░██████╗  ██████╗░░░██████╗░░░░░░░░░░██╗███╗░░██╗░█████╗░░░░░  
 ██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔═══██╗ ██╔═══██╗░░░░░░░░░██║████╗░██║██╔══██╗░░░░ 
 █████╗░ ███████║██████╔╝██║░░░██║██║░░░██║ ██║░░░██║░██████╗░██║██╔██╗██║██║░░╚═╝░░░░ 
 ██╔══╝░ ██╔══██║██╔══██╗██║░░░██║██║░░░██║ ██║▄▄░██║░╚═════╝░██║██║╚████║██║░░██╗░░░░  
 ██║░░░░ ██║░░██║██║░░██║╚██████╔╝╚██████╔╝░╚██████╔╝░░░░░░░░░██║██║░╚███║╚█████╔╝░░░░  
 ╚═╝░░░░ ╚═╝░░╚═╝╚═╝░░╚═╝░╚═════╝░░╚═════╝░░░╚══▀▀═╝░░░░░░░░░░╚═╝╚═╝░░╚══╝░╚════╝░░░░░  V2.7

'''

def get_terminal_width():
    """د ترمینل عرض ترلاسه کول"""
    try:
        return os.get_terminal_size().columns
    except:
        return 80

def print_centered_big(text):
    """متن د سنټر او لوی سایز سره چاپول - دوه چنده لوی"""
    terminal_width = get_terminal_width()
    
    big_text = ""
    for char in text:
        if char.isupper() or char.islower() or char.isdigit():
            big_text += char + " "
        else:
            big_text += char
    
    if len(big_text) > terminal_width - 4:
        big_text = text
    
    text_length = len(big_text)
    padding = (terminal_width - text_length) // 2
    if padding < 0:
        padding = 0
    
    spaces = " " * padding
    mid = len(big_text) // 2
    first_half = big_text[:mid]
    second_half = big_text[mid:]
    
    print(f"{spaces}", end="")
    print(f"\033[41m\033[97m{BOLD}{UNDERLINE}{first_half}{RESET}", end="")
    print(f"\033[42m\033[97m{BOLD}{UNDERLINE}{second_half}{RESET}")

def clear():
    os.system("clear")

def banner():
    os.system(f"echo \"{logo}\" | lolcat -p 1.6")

def print_box1():
    """لومړی بکس - بشپړ شالید، عرض او عمق سره، سپین او طلایی متن"""
    width = get_terminal_width()
    box_width = min(width - 4, 70)
    
    # پورتنۍ کرښه د شالید سره
    bg_color = BOX1_BG_COLORS[0]
    print(f"{bg_color}{LINE_BOLD}{DARK_GOLD}{'═' * 20}{GOLD_LINE}» ───── «◊•» ✠ • ◊ «─────» «{DARK_GOLD}{'═' * 20}{RESET}{bg_color} {' ' * (box_width - 48)} {RESET}")
    
    # د معلوماتو کرښې - زیات عمق (۶ کرښې)
    info_lines = [
        f"  {GOLD_TEXT}╔════════════════════════════════════════╗{WHITE_TEXT}",
        f"  {GOLD_TEXT}║{WHITE_TEXT}          FAROOQ TOOL INFORMATION{WHITE_TEXT}          {GOLD_TEXT}║{WHITE_TEXT}",
        f"  {GOLD_TEXT}╠════════════════════════════════════════╣{WHITE_TEXT}",
        f"  {GOLD_TEXT}║{WHITE_TEXT}  {GOLD_TEXT}Developer{WHITE_TEXT}   >> Faroooq Inc{WHITE_TEXT}              {GOLD_TEXT}║{WHITE_TEXT}",
        f"  {GOLD_TEXT}║{WHITE_TEXT}  {GOLD_TEXT}Tool Type{WHITE_TEXT}     >> FILExRANDOM{WHITE_TEXT}                 {GOLD_TEXT}║{WHITE_TEXT}",
        f"  {GOLD_TEXT}║{WHITE_TEXT}  {GOLD_TEXT}Github{WHITE_TEXT}        >> github.com/porn-404{WHITE_TEXT}         {GOLD_TEXT}║{WHITE_TEXT}",
        f"  {GOLD_TEXT}║{WHITE_TEXT}  {GOLD_TEXT}Version{WHITE_TEXT}       >> V2.7{WHITE_TEXT}                        {GOLD_TEXT}║{WHITE_TEXT}",
        f"  {GOLD_TEXT}║{WHITE_TEXT}  {GOLD_TEXT}Status{WHITE_TEXT}        >> {GOLD_TEXT}ACTIVE{WHITE_TEXT}                       {GOLD_TEXT}║{WHITE_TEXT}",
        f"  {GOLD_TEXT}╚════════════════════════════════════════╝{WHITE_TEXT}"
    ]
    
    for i, info in enumerate(info_lines):
        bg_color = BOX1_BG_COLORS[i % len(BOX1_BG_COLORS)]
        # متن لا دمخه سپین او طلایی رنګونه لري
        print(f"{bg_color}{info}{' ' * (box_width - len(info))} {RESET}")
    
    # ښکته کرښه د شالید سره
    bg_color = BOX1_BG_COLORS[-1]
    print(f"{bg_color}{LINE_BOLD}{DARK_GOLD}╚{'═' * 20} ──•◆•── ────────────────•✦•───────────────────╝{RESET}{bg_color}{' ' * (box_width - 48)}{RESET}")

def print_box2():
    """دویم بکس - بشپړ شالید، عرض او عمق سره، سپین او طلایی متن"""
    width = get_terminal_width()
    box_width = min(width - 4, 70)
    
    # پورتنۍ کرښه د شالید سره
    bg_color = BOX2_BG_COLORS[0]
    print(f"{bg_color}{LINE_BOLD}{LIGHT_GOLD}{'═' * 20}{RED_GOLD}» ───── «◊•» ✠ • ◊ «─────» «{LIGHT_GOLD}{'═' * 21}{RESET}{bg_color} {' ' * (box_width - 49)} {RESET}")
    
    # د معلوماتو کرښې - زیات عمق (۷ کرښې)
    info_lines = [
        f"  {GOLD_TEXT}╔══════════════════════════════════════════╗{WHITE_TEXT}",
        f"  {GOLD_TEXT}║{WHITE_TEXT}           OPERATOR INFORMATION{WHITE_TEXT}              {GOLD_TEXT}║{WHITE_TEXT}",
        f"  {GOLD_TEXT}╠══════════════════════════════════════════╣{WHITE_TEXT}",
        f"  {GOLD_TEXT}║{WHITE_TEXT}  {GOLD_TEXT}Operator{WHITE_TEXT}        >> 0171{WHITE_TEXT}                         {GOLD_TEXT}║{WHITE_TEXT}",
        f"  {GOLD_TEXT}║{WHITE_TEXT}  {GOLD_TEXT}Total Account{WHITE_TEXT}   >> {GOLD_TEXT}5000{WHITE_TEXT}                           {GOLD_TEXT}║{WHITE_TEXT}",
        f"  {GOLD_TEXT}║{WHITE_TEXT}  {GOLD_TEXT}Speed{WHITE_TEXT}           >> {GOLD_TEXT}MAXIMUM{WHITE_TEXT}                        {GOLD_TEXT}║{WHITE_TEXT}",
        f"  {GOLD_TEXT}║{WHITE_TEXT}  {GOLD_TEXT}Connection{WHITE_TEXT}      >> {GOLD_TEXT}STABLE{WHITE_TEXT}                         {GOLD_TEXT}║{WHITE_TEXT}",
        f"  {GOLD_TEXT}║{WHITE_TEXT}  ⚡ Use Airplane Mode For Speed Up{WHITE_TEXT}          {GOLD_TEXT}║{WHITE_TEXT}",
        f"  {GOLD_TEXT}║{WHITE_TEXT}  [!] {GOLD_TEXT}Turn on Flight Mode{WHITE_TEXT} for best results{GOLD_TEXT}  ║{WHITE_TEXT}",
        f"  {GOLD_TEXT}╚══════════════════════════════════════════╝{WHITE_TEXT}"
    ]
    
    for i, info in enumerate(info_lines):
        bg_color = BOX2_BG_COLORS[i % len(BOX2_BG_COLORS)]
        # متن لا دمخه سپین او طلایی رنګونه لري
        print(f"{bg_color}{info}{' ' * (box_width - len(info))} {RESET}")
    
    # ښکته کرښه د شالید سره
    bg_color = BOX2_BG_COLORS[-1]
    print(f"{bg_color}{LINE_BOLD}{LIGHT_GOLD}╚{'═' * 20} ──•◆•── ────────────────•✦•───────────────────╝{RESET}{bg_color}{' ' * (box_width - 48)}{RESET}")

def show_prompt():
    """ترمینل پرامپټ - درې مختلف رنګونه لرونکې ❯❯❯ نښې"""
    print(f"\n\033[93m{BOLD}┌─[h4ck3r@termux]-[~]\033[0m")
    print(f"{BOLD}{RED_ARROW}└──╼{RESET} {BOLD}{RED_ARROW}❯{RESET}{BOLD}{GREEN_ARROW}❯{RESET}{BOLD}{BLUE_ARROW}❯{RESET} \033[0m", end="")

def welcome():
    """د ویلکم مسیج - لوی سایز"""
    width = get_terminal_width()
    welcome_text = "⚡ WELCOME TO FAROOQ TOOL ⚡"
    
    padding = (width - len(welcome_text)) // 2
    if padding < 0:
        padding = 0
    
    spaces = " " * padding
    
    print(f"\n{spaces}\033[1;33m{BOLD}{'=' * len(welcome_text)}{RESET}")
    print(f"{spaces}\033[1;32m{BOLD}{welcome_text}{RESET}")
    print(f"{spaces}\033[1;33m{BOLD}{'=' * len(welcome_text)}{RESET}\n")
    time.sleep(1)

def main():
    clear()
    welcome()
    time.sleep(0.5)
    clear()
    
    banner()
    
    print()
    print_centered_big("WELCOME TO FAROOOQ TOOLS")
    print()
    print()
    
    print_box1()
    print()
    print_box2()
    print()
    
    width = get_terminal_width()
    print(f"{GOLD_LINE}{BOLD}{'=' * 50}{RESET}")
    show_prompt()
    print()

if __name__ == "__main__":
    main()
