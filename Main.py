#!/usr/bin/env python3
import os
import time
import sys

# ANSI رنګونه د متن لپاره
WHITE_TEXT = "\033[97m"
BOLD = "\033[1m"
RESET = "\033[0m"
UNDERLINE = "\033[4m"

# د بکس لاینونو لپاره رنګونه (طلایی او سرو زرو رنګونه)
GOLD_LINE = "\033[38;2;255;215;0m"      # طلایی (Gold)
DARK_GOLD = "\033[38;2;184;134;11m"     # تیاره طلایی (Dark Goldenrod)
LIGHT_GOLD = "\033[38;2;255;223;0m"     # روښانه طلایی
RED_GOLD = "\033[38;2;255;69;0m"        # سور-طلایی

# د بکس شالید لپاره رنګونه
# لومړی بکس (نسواري-طلایی)
BOX1_BG = "\033[48;2;139;69;19m"        # SaddleBrown
BOX1_BG_LIGHT = "\033[48;2;160;82;45m"  # Sienna

# دویم بکس (نیلي-شنه + طلایی ترکیب)
BOX2_BG = "\033[48;2;0;100;80m"         # Teal (نیلي-شنه)
BOX2_BG_LIGHT = "\033[48;2;0;128;128m"  # DarkCyan
BOX2_TEXT_HIGHLIGHT = "\033[38;2;255;215;0m"  # د متن لپاره طلایی

# د کرښو لپاره ځانګړي رنگین کوډونه
LINE_BOLD = "\033[1m"

logo = '''

 ███████╗ █████╗ █████╗░░░██████╗  ██████╗░░░██████╗░░░░░░░░░░██╗███╗░░██╗░█████╗░░░░░  
 ██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔═══██╗ ██╔═══██╗░░░░░░░░░██║████╗░██║██╔══██╗░░░░ 
 █████╗░ ███████║██████╔╝██║░░░██║██║░░░██║ ██║░░░██║░██████╗░██║██╔██╗██║██║░░╚═╝░░░░ 
 ██╔══╝░ ██╔══██║██╔══██╗██║░░░██║██║░░░██║ ██║▄▄░██║░╚═════╝░██║██║╚████║██║░░██╗░░░░  
 ██║░░░░ ██║░░██║██║░░██║╚██████╔╝╚██████╔╝░╚██████╔╝░░░░░░░░░██║██║░╚███║╚█████╔╝░░░░  
 ╚═╝░░░░ ╚═╝░░╚═╝╚═╝░░╚═╝░╚═════╝░░╚═════╝░░░╚══▀▀═╝░░░░░░░░░░╚═╝╚═╝░░╚══╝░╚════╝░░░░░  V2.7

'''

def print_centered_big(text):
    """متن د سنټر او لوی سایز سره چاپول - دوه چنده لوی"""
    try:
        terminal_width = os.get_terminal_size().columns
    except:
        terminal_width = 80
    
    # د متن دوه چنده لوی ښکاره کول
    # د ANSI د بلد او ځینې ترمینلونو کې د لیکو دوه چنده کولو لپاره
    big_text = ""
    for char in text:
        if char.isupper() or char.islower() or char.isdigit():
            big_text += char + " "
        else:
            big_text += char
    
    # که ډیر اوږد شو، نو عادي نسخه
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
    """لومړی بکس - نسواري/طلایی رنګونه"""
    # پورتنۍ کرښه - ډبل لاین
    print(f"{LINE_BOLD}{DARK_GOLD}╔═══════════════════════╗ {GOLD_LINE}» ───── «◊•» ✠ • ◊ «─────» «═══════════════════╗{RESET}")
    # د بکس مینځنی برخه - د کرښو سره
    print(f"{BOX1_BG}{WHITE_TEXT}{BOLD}║  {GOLD_LINE}Developer   >>{WHITE_TEXT} Faroooq Inc                                  {RESET}{BOX1_BG}{BOLD}║{RESET}")
    print(f"{BOX1_BG_LIGHT}{WHITE_TEXT}{BOLD}║  {GOLD_LINE}Tool Type   >>{WHITE_TEXT} FILExRANDOM                                  {RESET}{BOX1_BG_LIGHT}{BOLD}║{RESET}")
    print(f"{BOX1_BG}{WHITE_TEXT}{BOLD}║  {GOLD_LINE}Github      >>{WHITE_TEXT} github.com/porn-404                          {RESET}{BOX1_BG}{BOLD}║{RESET}")
    print(f"{BOX1_BG_LIGHT}{WHITE_TEXT}{BOLD}║  {GOLD_LINE}Version     >>{WHITE_TEXT} V2.7                                         {RESET}{BOX1_BG_LIGHT}{BOLD}║{RESET}")
    # ښکته کرښه
    print(f"{LINE_BOLD}{DARK_GOLD}╚═══════════════ ──•◆•── ────────────────•✦•───────────────────╝{RESET}")

def print_box2():
    """دویم بکس - نیلي-شنه (Teal) او طلایی رنګونه"""
    # پورتنۍ کرښه
    print(f"{LINE_BOLD}{LIGHT_GOLD}╔═══════════════════════╗ {RED_GOLD}» ───── «◊•» ✠ • ◊ «─────» «═══════════════════╗{RESET}")
    # د بکس مینځنی برخه - د مختلف متن رنګ سره
    print(f"{BOX2_BG}{BOX2_TEXT_HIGHLIGHT}{BOLD}║  {WHITE_TEXT}Operator        >> {BOX2_TEXT_HIGHLIGHT}0171{WHITE_TEXT}                                     {RESET}{BOX2_BG}{BOLD}║{RESET}")
    print(f"{BOX2_BG_LIGHT}{BOX2_TEXT_HIGHLIGHT}{BOLD}║  {WHITE_TEXT}Total Account   >> {BOX2_TEXT_HIGHLIGHT}5000{WHITE_TEXT}                                     {RESET}{BOX2_BG_LIGHT}{BOLD}║{RESET}")
    print(f"{BOX2_BG}{BOX2_TEXT_HIGHLIGHT}{BOLD}║  {WHITE_TEXT}⚡ Use Airplane (Flight) Mode For Speed Up{WHITE_TEXT}                   {RESET}{BOX2_BG}{BOLD}║{RESET}")
    print(f"{BOX2_BG_LIGHT}{BOX2_TEXT_HIGHLIGHT}{BOLD}║  {WHITE_TEXT}[!] {BOX2_TEXT_HIGHLIGHT}Turn on Flight Mode for best results{WHITE_TEXT}               {RESET}{BOX2_BG_LIGHT}{BOLD}║{RESET}")
    # ښکته کرښه
    print(f"{LINE_BOLD}{LIGHT_GOLD}╚═══════════════ ──•◆•── ────────────────•✦•───────────────────╝{RESET}")

def show_prompt():
    """ترمینل پرامپټ"""
    print(f"\n\033[93m{BOLD}┌─[h4ck3r@termux]-[~]\033[0m")
    print(f"\033[96m{BOLD}└──╼ ❯❯❯ \033[0m")

def welcome():
    print(f"\033[1;32m{BOLD}Welcome to FAROOQ Tool...\033[0m")
    time.sleep(1)

def main():
    clear()
    welcome()
    time.sleep(0.5)
    clear()
    
    # لوګو د lolcat سره
    banner()
    
    # ځانګړی متن - سنټر، دوه چنده لوی، نیم سور نیم زرغون
    print()
    print_centered_big("WELCOME TO FAROOOQ TOOLS")
    print()
    print()
    
    # بکسونه د نوي شکل سره
    print_box1()
    print()
    print_box2()
    print()
    print(f"{GOLD_LINE}{BOLD}{'='*50}{RESET}")
    show_prompt()

if __name__ == "__main__":
    main() 
