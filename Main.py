#!/usr/bin/env python3
import os
import time
import sys

# ANSI رنګونه د متن لپاره
WHITE_TEXT = "\033[97m"
BOLD = "\033[1m"
RESET = "\033[0m"
UNDERLINE = "\033[4m"
BLINK = "\033[5m"
ITALIC = "\033[3m"

# د بکس لاینونو لپاره رنګونه (طلایی او سرو زرو رنګونه)
GOLD_LINE = "\033[38;2;255;215;0m"      # طلایی (Gold)
DARK_GOLD = "\033[38;2;184;134;11m"     # تیاره طلایی (Dark Goldenrod)
LIGHT_GOLD = "\033[38;2;255;223;0m"     # روښانه طلایی
RED_GOLD = "\033[38;2;255;69;0m"        # سور-طلایی
PURPLE_GOLD = "\033[38;2;255;215;0m"    # طلایی

# د بکس شالید لپاره رنګونه (غټ او ځلیدونکي)
# لومړی بکس (نسواري-طلایی غټ)
BOX1_BG = "\033[48;2;139;69;19m"        # SaddleBrown
BOX1_BG_LIGHT = "\033[48;2;205;133;63m" # Peru (روښانه)

# دویم بکس (نیلي-شنه + طلایی ترکیب غټ)
BOX2_BG = "\033[48;2;0;139;139m"        # DarkCyan (غټ)
BOX2_BG_LIGHT = "\033[48;2;0;206;209m"  # DarkTurquoise
BOX2_TEXT_HIGHLIGHT = "\033[38;2;255;215;0m"  # د متن لپاره طلایی

# د ویلکم بکس لپاره ځانګړی رنګونه
WELCOME_BG = "\033[48;2;88;41;0m"       # تیاره نسواري
WELCOME_BG2 = "\033[48;2;160;82;45m"    # Sienna

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

def print_welcome_in_box():
    """ویلکم متن په یوه ښکلې بکس کې - دوه چنده لوی سایز"""
    welcome_text = "WELCOME TO FAROOOQ TOOLS"
    
    # د متن لوی کول (د توریو ترمنځ فاصله)
    big_text = ""
    for char in welcome_text:
        big_text += char + "  "  # دوه فاصله هر توری ته
    
    # د بکس پورتنۍ برخه
    box_width = len(big_text) + 8
    print(f"{DARK_GOLD}{LINE_BOLD}╔{'═' * (box_width-2)}╗{RESET}")
    
    # خالي کرښه
    print(f"{DARK_GOLD}{LINE_BOLD}║{RESET}{WELCOME_BG}{' ' * (box_width-2)}{RESET}{DARK_GOLD}{LINE_BOLD}║{RESET}")
    
    # د متن کرښه (نیم سور، نیم زرغون)
    print(f"{DARK_GOLD}{LINE_BOLD}║{RESET}", end="")
    mid = len(big_text) // 2
    first_half = big_text[:mid]
    second_half = big_text[mid:]
    print(f"\033[41m\033[97m{BOLD}{first_half}{RESET}", end="")
    print(f"\033[42m\033[97m{BOLD}{second_half}{RESET}", end="")
    print(f"{DARK_GOLD}{LINE_BOLD}║{RESET}")
    
    # خالي کرښه
    print(f"{DARK_GOLD}{LINE_BOLD}║{RESET}{WELCOME_BG2}{' ' * (box_width-2)}{RESET}{DARK_GOLD}{LINE_BOLD}║{RESET}")
    
    # د بکس ښکته برخه
    print(f"{DARK_GOLD}{LINE_BOLD}╚{'═' * (box_width-2)}╝{RESET}")

def print_centered_big(text):
    """متن د سنټر او لوی سایز سره چاپول - درې چنده لوی"""
    try:
        terminal_width = os.get_terminal_size().columns
    except:
        terminal_width = 80
    
    # د متن درې چنده لوی ښکاره کول
    big_text = ""
    for char in text:
        if char.isupper() or char.islower() or char.isdigit():
            big_text += char + "  "  # دوه فاصله
        else:
            big_text += char
    
    text_length = len(big_text)
    padding = (terminal_width - text_length) // 2
    if padding < 0:
        padding = 0
    
    spaces = " " * padding
    mid = len(big_text) // 2
    first_half = big_text[:mid]
    second_half = big_text[mid:]
    
    print(f"{spaces}", end="")
    print(f"\033[41m\033[97m{BOLD}{UNDERLINE}{BLINK}{first_half}{RESET}", end="")
    print(f"\033[42m\033[97m{BOLD}{UNDERLINE}{BLINK}{second_half}{RESET}")

def clear():
    os.system("clear")

def banner():
    os.system(f"echo \"{logo}\" | lolcat -p 1.6")

def print_box1():
    """لومړی بکس - نسواري/طلایی رنګونه (غټ سایز)"""
    print(f"{LINE_BOLD}{DARK_GOLD}╔{'═' * 55}╗{RESET}")
    print(f"{LINE_BOLD}{DARK_GOLD}║{RESET}{BOX1_BG}{WHITE_TEXT}{BOLD}  {GOLD_LINE}◆ {WHITE_TEXT}Developer   : {GOLD_LINE}Faroooq Inc{WHITE_TEXT}{' ' * 20}{RESET}{DARK_GOLD}{LINE_BOLD}║{RESET}")
    print(f"{LINE_BOLD}{DARK_GOLD}║{RESET}{BOX1_BG_LIGHT}{WHITE_TEXT}{BOLD}  {GOLD_LINE}◆ {WHITE_TEXT}Tool Type   : {GOLD_LINE}FILExRANDOM{WHITE_TEXT}{' ' * 23}{RESET}{DARK_GOLD}{LINE_BOLD}║{RESET}")
    print(f"{LINE_BOLD}{DARK_GOLD}║{RESET}{BOX1_BG}{WHITE_TEXT}{BOLD}  {GOLD_LINE}◆ {WHITE_TEXT}Github      : {GOLD_LINE}github.com/porn-404{WHITE_TEXT}{' ' * 11}{RESET}{DARK_GOLD}{LINE_BOLD}║{RESET}")
    print(f"{LINE_BOLD}{DARK_GOLD}║{RESET}{BOX1_BG_LIGHT}{WHITE_TEXT}{BOLD}  {GOLD_LINE}◆ {WHITE_TEXT}Version     : {GOLD_LINE}V2.7{WHITE_TEXT}{' ' * 30}{RESET}{DARK_GOLD}{LINE_BOLD}║{RESET}")
    print(f"{LINE_BOLD}{DARK_GOLD}╚{'═' * 55}╝{RESET}")

def print_box2():
    """دویم بکس - نیلي-شنه او طلایی (غټ سایز)"""
    print(f"{LINE_BOLD}{LIGHT_GOLD}╔{'═' * 55}╗{RESET}")
    print(f"{LINE_BOLD}{LIGHT_GOLD}║{RESET}{BOX2_BG}{BOX2_TEXT_HIGHLIGHT}{BOLD}  ⚡ {WHITE_TEXT}Operator        : {BOX2_TEXT_HIGHLIGHT}0171{WHITE_TEXT}{' ' * 27}{RESET}{LIGHT_GOLD}{LINE_BOLD}║{RESET}")
    print(f"{LINE_BOLD}{LIGHT_GOLD}║{RESET}{BOX2_BG_LIGHT}{BOX2_TEXT_HIGHLIGHT}{BOLD}  ⚡ {WHITE_TEXT}Total Account   : {BOX2_TEXT_HIGHLIGHT}5000{WHITE_TEXT}{' ' * 26}{RESET}{LIGHT_GOLD}{LINE_BOLD}║{RESET}")
    print(f"{LINE_BOLD}{LIGHT_GOLD}║{RESET}{BOX2_BG}{BOX2_TEXT_HIGHLIGHT}{BOLD}  ⚡ {WHITE_TEXT}Mode            : {BOX2_TEXT_HIGHLIGHT}Airplane/Flight{WHITE_TEXT}{' ' * 20}{RESET}{LIGHT_GOLD}{LINE_BOLD}║{RESET}")
    print(f"{LINE_BOLD}{LIGHT_GOLD}║{RESET}{BOX2_BG_LIGHT}{BOX2_TEXT_HIGHLIGHT}{BOLD}  ⚡ {WHITE_TEXT}Speed Up        : {BOX2_TEXT_HIGHLIGHT}Enable Flight Mode{WHITE_TEXT}{' ' * 16}{RESET}{LIGHT_GOLD}{LINE_BOLD}║{RESET}")
    print(f"{LINE_BOLD}{LIGHT_GOLD}╚{'═' * 55}╝{RESET}")

def show_prompt():
    """ترمینل پرامپټ (غټ سایز)"""
    print(f"\n\033[93m{BOLD}{ITALIC}┌─[h4ck3r@termux]-[~]\033[0m")
    print(f"\033[96m{BOLD}{ITALIC}└──╼ ❯❯❯ \033[0m")

def welcome():
    print(f"\033[1;32m{BOLD}{UNDERLINE}Welcome to FAROOQ Tool...\033[0m")
    time.sleep(1)

def main():
    clear()
    welcome()
    time.sleep(0.5)
    clear()
    
    # لوګو د lolcat سره
    banner()
    
    # ویلکم متن په بکس کې (نوی اضافه شوی)
    print()
    print_welcome_in_box()
    print()
    
    # بکسونه د نوي غټ شکل سره
    print_box1()
    print()
    print_box2()
    print()
    print(f"{GOLD_LINE}{BOLD}{'=' * 55}{RESET}")
    show_prompt()

if __name__ == "__main__":
    main() 
