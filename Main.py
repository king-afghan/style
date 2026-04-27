#!/usr/bin/env python3
import os
import time
import sys

# ANSI رنګونه
RED_BG = "\033[41m"
GREEN_BG = "\033[42m"
WHITE_TEXT = "\033[97m"
RESET = "\033[0m"

# د بکسونو رنګونه
ALMOND = "\033[48;2;205;133;63m"      # بادامي (Peru/SaddleBrown)
SAFFRON = "\033[48;2;255;153;51m"     # زعفراني (Orange)
CYAN_TEXT = "\033[96m"
YELLOW_TEXT = "\033[93m"

logo = '''

 ███████╗ █████╗ █████╗░░░██████╗  ██████╗░░░██████╗░░░░░░░░░░██╗███╗░░██╗░█████╗░░░░░  
 ██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔═══██╗ ██╔═══██╗░░░░░░░░░██║████╗░██║██╔══██╗░░░░ 
 █████╗░ ███████║██████╔╝██║░░░██║██║░░░██║ ██║░░░██║░██████╗░██║██╔██╗██║██║░░╚═╝░░░░ 
 ██╔══╝░ ██╔══██║██╔══██╗██║░░░██║██║░░░██║ ██║▄▄░██║░╚═════╝░██║██║╚████║██║░░██╗░░░░  
 ██║░░░░ ██║░░██║██║░░██║╚██████╔╝╚██████╔╝░╚██████╔╝░░░░░░░░░██║██║░╚███║╚█████╔╝░░░░  
 ╚═╝░░░░ ╚═╝░░╚═╝╚═╝░░╚═╝░╚═════╝░░╚═════╝░░░╚══▀▀═╝░░░░░░░░░░╚═╝╚═╝░░╚══╝░╚════╝░░░░░  V2.7

'''

def print_split_bg(text):
    """متن نیمایي سور او نیمایي زرغون شالید"""
    mid = len(text) // 2
    first_half = text[:mid]
    second_half = text[mid:]
    
    # لومړی نیم: سور شالید، سپین متن
    print(f"{RED_BG}{WHITE_TEXT}{first_half}{RESET}", end="")
    # دویم نیم: زرغون شالید، سپین متن
    print(f"{GREEN_BG}{WHITE_TEXT}{second_half}{RESET}")

def clear():
    os.system("clear")

def banner():
    # لوګو د lolcat سره
    os.system(f"echo \"{logo}\" | lolcat -p 1.6")

def print_box1():
    """لومړی بکس - بادامي رنګ"""
    box1 = f'''
{ALMOND}═══════════════════════╗ » ───── «◊•» ✠ • ◊ «─────» «================={RESET}
{ALMOND}│  Developer   >> Faroooq Inc                                  │{RESET}
{ALMOND}│  Tool Type   >> FILExRANDOM                                  │{RESET}
{ALMOND}│  Github      >> github.com/porn-404                          │{RESET}
{ALMOND}│  Version     >> V2.7                                         │{RESET}
{ALMOND}╚═══════════════ ──•◆•── ────────────────•✦•───────────────────╝{RESET}
'''
    print(box1)

def print_box2():
    """دویم بکس - زعفراني رنګ"""
    box2 = f'''
{SAFFRON}═══════════════════════╗ » ───── «◊•» ✠ • ◊ «─────» «================={RESET}
{SAFFRON}│  Operator        >> 0171                                     │{RESET}
{SAFFRON}│  Total Account   >> 5000                                     │{RESET}
{SAFFRON}│  ⚡ Use Airplane (Flight) Mode For Speed Up                   │{RESET}
{SAFFRON}╚═══════════════ ──•◆•── ────────────────•✦•───────────────────╝{RESET}
'''
    print(box2)

def show_prompt():
    """ترمینل پرامپټ"""
    print(f"\n{YELLOW_TEXT}┌─[h4ck3r@termux]-[~]{RESET}")
    print(f"{CYAN_TEXT}└──╼ ❯❯❯ {RESET}")

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
    
    # ځانګړی متن نیم سور نیم زرغون
    print_split_bg("          WELCOME TO FAROOOQ TOOLS          ")
    print()  # خالي کرښه
    
    # بکسونه
    print_box1()
    print()
    print_box2()
    print()
    show_prompt()

if __name__ == "__main__":
    main()
