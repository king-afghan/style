#!/usr/bin/env python3
import os
import time
import sys

# ANSI رنګونه د متن لپاره
WHITE_TEXT = "\033[97m"
BOLD = "\033[1m"
RESET = "\033[0m"

# د بکس لاینونو لپاره رنګونه (طلایی او سرو زرو رنګونه)
GOLD_LINE = "\033[38;2;255;215;0m"      # طلایی (Gold)
DARK_GOLD = "\033[38;2;184;134;11m"     # تیاره طلایی (Dark Goldenrod)
LIGHT_GOLD = "\033[38;2;255;223;0m"     # روښانه طلایی

# د بکس شالید لپاره نرم طلایی رنګونه (بې له شالیده)
BOX1_BG = "\033[48;2;139;69;19m"        # نسواري-طلایی (SaddleBrown)
BOX1_BG_LIGHT = "\033[48;2;160;82;45m"  # سیینا (Sienna)
BOX2_BG = "\033[48;2;218;165;32m"       # طلایی (Goldenrod)
BOX2_BG_LIGHT = "\033[48;2;255;215;0m"  # روښانه طلایی

# د کرښو لپاره ځانګړي رنگین کوډونه
LINE_BOLD = "\033[1m"
LINE_RESET = "\033[0m"

logo = '''

 ███████╗ █████╗ █████╗░░░██████╗  ██████╗░░░██████╗░░░░░░░░░░██╗███╗░░██╗░█████╗░░░░░  
 ██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔═══██╗ ██╔═══██╗░░░░░░░░░██║████╗░██║██╔══██╗░░░░ 
 █████╗░ ███████║██████╔╝██║░░░██║██║░░░██║ ██║░░░██║░██████╗░██║██╔██╗██║██║░░╚═╝░░░░ 
 ██╔══╝░ ██╔══██║██╔══██╗██║░░░██║██║░░░██║ ██║▄▄░██║░╚═════╝░██║██║╚████║██║░░██╗░░░░  
 ██║░░░░ ██║░░██║██║░░██║╚██████╔╝╚██████╔╝░╚██████╔╝░░░░░░░░░██║██║░╚███║╚█████╔╝░░░░  
 ╚═╝░░░░ ╚═╝░░╚═╝╚═╝░░╚═╝░╚═════╝░░╚═════╝░░░╚══▀▀═╝░░░░░░░░░░╚═╝╚═╝░░╚══╝░╚════╝░░░░░  V2.7

'''

def print_centered_big(text):
    """متن د سنټر او لوی سایز سره چاپول"""
    # د ترمینل عرض ترلاسه کول
    try:
        terminal_width = os.get_terminal_size().columns
    except:
        terminal_width = 80
    
    # د متن اوږدوالی
    text_length = len(text)
    padding = (terminal_width - text_length) // 2
    if padding < 0:
        padding = 0
    
    # د متن لوی سایز (Bold + یو څه لوی ښکاره کېدو لپاره)
    # په ترمینل کې د لوی متن لپاره ځانګړی کوډ نشته، نو BOLD استفاده کوو
    spaces = " " * padding
    # نیم سور، نیم زرغون شالید (د متن رنګ سپین)
    mid = len(text) // 2
    first_half = text[:mid]
    second_half = text[mid:]
    
    # د سنټر لپاره فضایي خلا
    print(f"{spaces}", end="")
    # لومړی نیم: سور شالید، سپین متن، بولډ
    print(f"\033[41m\033[97m{BOLD}{first_half}{RESET}", end="")
    # دویم نیم: زرغون شالید، سپین متن، بولډ
    print(f"\033[42m\033[97m{BOLD}{second_half}{RESET}")

def clear():
    os.system("clear")

def banner():
    # لوګو د lolcat سره
    os.system(f"echo \"{logo}\" | lolcat -p 1.6")

def print_box1():
    """لومړی بکس - طلایی/نسواري رنګونه، د لاینونو سره بیل رنګ"""
    # پورتنۍ کرښه
    print(f"{LINE_BOLD}{DARK_GOLD}═══════════════════════╗ {GOLD_LINE}» ───── «◊•» ✠ • ◊ «─────» «================={RESET}")
    # د بکس مینځنی برخه
    print(f"{BOX1_BG}{WHITE_TEXT}│  {GOLD_LINE}Developer   >>{WHITE_TEXT} Faroooq Inc                                  {RESET}{BOX1_BG}│{RESET}")
    print(f"{BOX1_BG_LIGHT}{WHITE_TEXT}│  {GOLD_LINE}Tool Type   >>{WHITE_TEXT} FILExRANDOM                                  {RESET}{BOX1_BG_LIGHT}│{RESET}")
    print(f"{BOX1_BG}{WHITE_TEXT}│  {GOLD_LINE}Github      >>{WHITE_TEXT} github.com/porn-404                          {RESET}{BOX1_BG}│{RESET}")
    print(f"{BOX1_BG_LIGHT}{WHITE_TEXT}│  {GOLD_LINE}Version     >>{WHITE_TEXT} V2.7                                         {RESET}{BOX1_BG_LIGHT}│{RESET}")
    # ښکته کرښه
    print(f"{LINE_BOLD}{DARK_GOLD}╚═══════════════ ──•◆•── ────────────────•✦•───────────────────╝{RESET}")

def print_box2():
    """دویم بکس - طلایی/زعفراني رنګونه، د لاینونو سره بیل رنګ"""
    # پورتنۍ کرښه
    print(f"{LINE_BOLD}{LIGHT_GOLD}═══════════════════════╗ {GOLD_LINE}» ───── «◊•» ✠ • ◊ «─────» «================={RESET}")
    # د بکس مینځنی برخه
    print(f"{BOX2_BG}{WHITE_TEXT}│  {GOLD_LINE}Operator        >>{WHITE_TEXT} 0171                                     {RESET}{BOX2_BG}│{RESET}")
    print(f"{BOX2_BG_LIGHT}{WHITE_TEXT}│  {GOLD_LINE}Total Account   >>{WHITE_TEXT} 5000                                     {RESET}{BOX2_BG_LIGHT}│{RESET}")
    print(f"{BOX2_BG}{WHITE_TEXT}│  {GOLD_LINE}⚡ Use Airplane (Flight) Mode For Speed Up{WHITE_TEXT}                   {RESET}{BOX2_BG}│{RESET}")
    # ښکته کرښه
    print(f"{LINE_BOLD}{LIGHT_GOLD}╚═══════════════ ──•◆•── ────────────────•✦•───────────────────╝{RESET}")

def show_prompt():
    """ترمینل پرامپټ"""
    print(f"\n\033[93m┌─[h4ck3r@termux]-[~]\033[0m")
    print(f"\033[96m└──╼ ❯❯❯ \033[0m")

def welcome():
    print("\033[1;32mWelcome to FAROOQ Tool...\033[0m")
    time.sleep(1)

def main():
    clear()
    welcome()
    time.sleep(0.5)
    clear()
    
    # لوګو د lolcat سره
    banner()
    
    # ځانګړی متن - سنټر، لوی، نیم سور نیم زرغون
    print()
    print_centered_big("WELCOME TO FAROOOQ TOOLS")
    print()
    print()
    
    # بکسونه
    print_box1()
    print()
    print_box2()
    print()
    show_prompt()

if __name__ == "__main__":
    main()
