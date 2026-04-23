#!/usr/bin/env python3
import os
import time

logo = '''

[+]
| ███████╗ █████╗ █████╗░░░██████╗  ██████╗░░░██████╗░░░░░░░░░░██╗███╗░░██╗░█████╗░░░░░  
| ██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔═══██╗ ██╔═══██╗░░░░░░░░░██║████╗░██║██╔══██╗░░░░ 
| █████╗░ ███████║██████╔╝██║░░░██║██║░░░██║ ██║░░░██║░██████╗░██║██╔██╗██║██║░░╚═╝░░░░ 
| ██╔══╝░ ██╔══██║██╔══██╗██║░░░██║██║░░░██║ ██║▄▄░██║░╚═════╝░██║██║╚████║██║░░██╗░░░░  
| ██║░░░░ ██║░░██║██║░░██║╚██████╔╝╚██████╔╝░╚██████╔╝░░░░░░░░░██║██║░╚███║╚█████╔╝░░░░  
| ╚═╝░░░░ ╚═╝░░╚═╝╚═╝░░╚═╝░╚═════╝░░╚═════╝░░░╚══▀▀═╝░░░░░░░░░░╚═╝╚═╝░░╚══╝░╚════╝░░░░░  V2.7


[+] Title    : AllHackingTools - Tool for hacking  -  ⁣ATTENTION! The author of this article is not respo-
[+] Github   : https://github.com/mishakorzik  -  nsi⁣ble responsible for any consequences of reading it. 
[+] Coded By : Misha Korzhik (Міша Коржик)  -  All materials are provided for educational purposes only! 
[+]———————-——-–————————-—-–———-——————-—–————-————-—–———————-——–—————–-——[+]

[01] Quick Start - on/off
[02] Servers Setting
[03] Extra Keys
[04] Add to Startup
[05] System Process Viewer
[06] Exit Tool
'''

def clear():
    os.system("clear")

def banner():
    os.system("echo \"{}\" | lolcat -p 1.6".format(logo))

def welcome():
    print("\033[1;32mWelcome to FAROOQ Tool...\033[0m")
    time.sleep(1)

def main():
    clear()
    welcome()
    time.sleep(0.5)
    clear()
    banner()

if __name__ == "__main__":
    main()
