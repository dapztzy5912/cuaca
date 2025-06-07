#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time
import sys
import os
from datetime import datetime
import random

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    PINK = '\033[95m'
    PURPLE = '\033[35m'
    YELLOW = '\033[33m'
    RED = '\033[31m'
    WHITE = '\033[37m'

WEATHER_EMOJIS = {
    'clear': '☀️',
    'sunny': '☀️',
    'partly': '⛅',
    'cloudy': '☁️',
    'overcast': '☁️',
    'rain': '🌧️',
    'drizzle': '🌦️',
    'snow': '❄️',
    'thunder': '⛈️',
    'fog': '🌫️',
    'mist': '🌫️',
    'wind': '💨',
    'default': '🌤️'
}

def clear_screen():
    """Clear screen untuk semua OS"""
    os.system('clear' if os.name == 'posix' else 'cls')

def print_banner():
    """Banner dengan ASCII art"""
    banner = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗
║  {Colors.BOLD}{Colors.YELLOW}██╗    ██╗███████╗ █████╗ ████████╗██╗  ██╗███████╗██████╗   {Colors.ENDC}{Colors.CYAN}║
║  {Colors.BOLD}{Colors.YELLOW}██║    ██║██╔════╝██╔══██╗╚══██╔══╝██║  ██║██╔════╝██╔══██╗  {Colors.ENDC}{Colors.CYAN}║
║  {Colors.BOLD}{Colors.YELLOW}██║ █╗ ██║█████╗  ███████║   ██║   ███████║█████╗  ██████╔╝  {Colors.ENDC}{Colors.CYAN}║
║  {Colors.BOLD}{Colors.YELLOW}██║███╗██║██╔══╝  ██╔══██║   ██║   ██╔══██║██╔══╝  ██╔══██╗  {Colors.ENDC}{Colors.CYAN}║
║  {Colors.BOLD}{Colors.YELLOW}╚███╔███╔╝███████╗██║  ██║   ██║   ██║  ██║███████╗██║  ██║  {Colors.ENDC}{Colors.CYAN}║
║  {Colors.BOLD}{Colors.YELLOW} ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝  {Colors.ENDC}{Colors.CYAN}║
║                                                              ║
║  {Colors.BOLD}{Colors.GREEN}🌟 Cek - Cuaca 🌟            {Colors.ENDC}{Colors.CYAN}║
║  {Colors.PINK}Made with ❤️  by XdpzQ                           {Colors.ENDC}{Colors.CYAN}║
╚══════════════════════════════════════════════════════════════╝{Colors.ENDC}
"""
    print(banner)

def loading_animation(text="Loading", duration=2):
    """Animasi loading"""
    animations = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    colors = [Colors.CYAN, Colors.GREEN, Colors.YELLOW, Colors.PINK, Colors.PURPLE]
    
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        color = random.choice(colors)
        print(f"\r{color}{animations[i % len(animations)]} {text}...{Colors.ENDC}", end="", flush=True)
        time.sleep(0.1)
        i += 1
    print(f"\r{Colors.GREEN}✅ {text} selesai!{Colors.ENDC}")

def get_weather_emoji(weather_desc):
    """Get emoji berdasarkan deskripsi cuaca"""
    weather_desc = weather_desc.lower()
    for key, emoji in WEATHER_EMOJIS.items():
        if key in weather_desc:
            return emoji
    return WEATHER_EMOJIS['default']

def format_weather_display(weather_data, city):
    """Format tampilan cuaca"""
    if not weather_data:
        return f"{Colors.RED}❌ Data cuaca tidak tersedia{Colors.ENDC}"
    
    # Parse data cuaca
    lines = weather_data.strip().split('\n')
    if len(lines) < 1:
        return f"{Colors.RED}❌ Format data tidak valid{Colors.ENDC}"
    
    weather_info = lines[0] if lines else "Data tidak tersedia"
    weather_emoji = get_weather_emoji(weather_info)
    
    # Box design dengan border keren
    box_width = 60
    
    result = f"""
{Colors.CYAN}╔{'═' * (box_width - 2)}╗{Colors.ENDC}
{Colors.CYAN}║{Colors.BOLD}{Colors.YELLOW}{city.upper().center(box_width - 2)}{Colors.ENDC}{Colors.CYAN}║{Colors.ENDC}
{Colors.CYAN}╠{'═' * (box_width - 2)}╣{Colors.ENDC}
{Colors.CYAN}║{Colors.ENDC} {weather_emoji} {Colors.BOLD}{Colors.WHITE}KONDISI CUACA{Colors.ENDC} {' ' * (box_width - 20)}{Colors.CYAN}║{Colors.ENDC}
{Colors.CYAN}║{Colors.ENDC}{' ' * (box_width - 2)}{Colors.CYAN}║{Colors.ENDC}
{Colors.CYAN}║{Colors.ENDC} {Colors.GREEN}{weather_info.ljust(box_width - 4)}{Colors.ENDC}{Colors.CYAN}║{Colors.ENDC}
{Colors.CYAN}║{Colors.ENDC}{' ' * (box_width - 2)}{Colors.CYAN}║{Colors.ENDC}
{Colors.CYAN}║{Colors.ENDC} 🕐 {Colors.PINK}Waktu: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}{Colors.ENDC}{' ' * (box_width - len(datetime.now().strftime('%d/%m/%Y %H:%M:%S')) - 12)}{Colors.CYAN}║{Colors.ENDC}
{Colors.CYAN}╚{'═' * (box_width - 2)}╝{Colors.ENDC}
"""
    return result

def get_detailed_weather(city):
    """Get cuaca detail dengan API wttr.in format JSON"""
    try:
        print(f"{Colors.YELLOW}🔍 Mencari data cuaca untuk {Colors.BOLD}{city}{Colors.ENDC}{Colors.YELLOW}...{Colors.ENDC}")
        loading_animation("Mengambil data", 1.5)
        
        # Format 3 untuk simple, format j untuk JSON detail
        simple_url = f"https://wttr.in/{city}?format=3"
        json_url = f"https://wttr.in/{city}?format=j1"
        
        # Get simple format
        simple_response = requests.get(simple_url, timeout=10)
        
        if simple_response.status_code == 200:
            weather_text = simple_response.text.strip()
            
            # Try to get detailed JSON data
            try:
                json_response = requests.get(json_url, timeout=5)
                if json_response.status_code == 200:
                    weather_json = json_response.json()
                    return format_detailed_weather(weather_json, city, weather_text)
                else:
                    return format_weather_display(weather_text, city)
            except:
                return format_weather_display(weather_text, city)
        else:
            return f"{Colors.RED}❌ Kota '{city}' tidak ditemukan atau server error{Colors.ENDC}"
            
    except requests.RequestException as e:
        return f"{Colors.RED}❌ Koneksi error: {str(e)}{Colors.ENDC}"
    except Exception as e:
        return f"{Colors.RED}❌ Error tidak terduga: {str(e)}{Colors.ENDC}"

def format_detailed_weather(weather_json, city, simple_text):
    """Format weather dengan data JSON detail"""
    try:
        current = weather_json['current_condition'][0]
        
        temp_c = current['temp_C']
        feels_like = current['FeelsLikeC']
        humidity = current['humidity']
        wind_speed = current['windspeedKmph']
        wind_dir = current['winddir16Point']
        visibility = current['visibility']
        weather_desc = current['weatherDesc'][0]['value']
        
        emoji = get_weather_emoji(weather_desc)
        box_width = 65
        
        result = f"""
{Colors.CYAN}╔{'═' * (box_width - 2)}╗{Colors.ENDC}
{Colors.CYAN}║{Colors.BOLD}{Colors.YELLOW}{city.upper().center(box_width - 2)}{Colors.ENDC}{Colors.CYAN}║{Colors.ENDC}
{Colors.CYAN}╠{'═' * (box_width - 2)}╣{Colors.ENDC}
{Colors.CYAN}║{Colors.ENDC} {emoji} {Colors.BOLD}{Colors.WHITE}KONDISI CUACA DETAIL{Colors.ENDC} {' ' * (box_width - 25)}{Colors.CYAN}║{Colors.ENDC}
{Colors.CYAN}╠{'─' * (box_width - 2)}╣{Colors.ENDC}
{Colors.CYAN}║{Colors.ENDC} 🌡️  {Colors.GREEN}Suhu         : {Colors.BOLD}{temp_c}°C{Colors.ENDC} {' ' * (box_width - len(f"Suhu         : {temp_c}°C") - 7)}{Colors.CYAN}║{Colors.ENDC}
{Colors.CYAN}║{Colors.ENDC} 🤔 {Colors.GREEN}Terasa seperti: {Colors.BOLD}{feels_like}°C{Colors.ENDC} {' ' * (box_width - len(f"Terasa seperti: {feels_like}°C") - 7)}{Colors.CYAN}║{Colors.ENDC}
{Colors.CYAN}║{Colors.ENDC} 💧 {Colors.GREEN}Kelembaban   : {Colors.BOLD}{humidity}%{Colors.ENDC} {' ' * (box_width - len(f"Kelembaban   : {humidity}%") - 7)}{Colors.CYAN}║{Colors.ENDC}
{Colors.CYAN}║{Colors.ENDC} 💨 {Colors.GREEN}Angin        : {Colors.BOLD}{wind_speed} km/h {wind_dir}{Colors.ENDC} {' ' * (box_width - len(f"Angin        : {wind_speed} km/h {wind_dir}") - 7)}{Colors.CYAN}║{Colors.ENDC}
{Colors.CYAN}║{Colors.ENDC} 👁️  {Colors.GREEN}Jarak pandang: {Colors.BOLD}{visibility} km{Colors.ENDC} {' ' * (box_width - len(f"Jarak pandang: {visibility} km") - 7)}{Colors.CYAN}║{Colors.ENDC}
{Colors.CYAN}║{Colors.ENDC} ☁️  {Colors.GREEN}Kondisi      : {Colors.BOLD}{weather_desc}{Colors.ENDC} {' ' * (box_width - len(f"Kondisi      : {weather_desc}") - 7)}{Colors.CYAN}║{Colors.ENDC}
{Colors.CYAN}╠{'─' * (box_width - 2)}╣{Colors.ENDC}
{Colors.CYAN}║{Colors.ENDC} 🕐 {Colors.PINK}Update: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}{Colors.ENDC} {' ' * (box_width - len(datetime.now().strftime('%d/%m/%Y %H:%M:%S')) - 12)}{Colors.CYAN}║{Colors.ENDC}
{Colors.CYAN}╚{'═' * (box_width - 2)}╝{Colors.ENDC}
"""
        return result
        
    except (KeyError, IndexError):
        # Fallback ke format simple jika JSON parsing gagal
        return format_weather_display(simple_text, city)

def show_quick_cities():
    """Tampilkan pilihan kota cepat"""
    cities = [
        "Jakarta", "Surabaya", "Bandung", "Medan", "Semarang",
        "Palembang", "Makassar", "Denpasar", "Padang", "Balikpapan"
    ]
    
    print(f"\n{Colors.CYAN}╔════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
    print(f"{Colors.CYAN}║{Colors.BOLD}{Colors.YELLOW}🏃‍♂️ QUICK ACCESS - KOTA POPULER{Colors.ENDC}{' ' * 28}{Colors.CYAN}║{Colors.ENDC}")
    print(f"{Colors.CYAN}╚════════════════════════════════════════════════════════════════╝{Colors.ENDC}")
    
    for i, city in enumerate(cities, 1):
        color = [Colors.GREEN, Colors.YELLOW, Colors.PINK, Colors.PURPLE, Colors.CYAN][i % 5]
        print(f"{color}[{i:2d}] {city}{Colors.ENDC}", end="  ")
        if i % 5 == 0:
            print()
    
    if len(cities) % 5 != 0:
        print()
    
    return cities

def interactive_menu():
    """Menu interaktif ultra modern"""
    while True:
        clear_screen()
        print_banner()
        
        print(f"\n{Colors.GREEN}🎯 Pilih opsi di bawah ini:{Colors.ENDC}")
        print(f"{Colors.YELLOW}[1] 🔍 Cari cuaca berdasarkan nama kota{Colors.ENDC}")
        print(f"{Colors.YELLOW}[2] ⚡ Quick access kota populer{Colors.ENDC}")
        print(f"{Colors.YELLOW}[3] 🌍 Cari cuaca berdasarkan koordinat{Colors.ENDC}")
        print(f"{Colors.YELLOW}[4] ❌ Exit{Colors.ENDC}")
        
        choice = input(f"\n{Colors.PINK}Masukkan pilihan (1-4): {Colors.ENDC}").strip()
        
        if choice == "1":
            print(f"\n{Colors.CYAN}═" * 60 + f"{Colors.ENDC}")
            city = input(f"{Colors.GREEN}🏙️  Masukkan nama kota: {Colors.ENDC}").strip()
            if city:
                result = get_detailed_weather(city)
                print(f"\n{result}")
                input(f"\n{Colors.PINK}Tekan ENTER untuk melanjutkan...{Colors.ENDC}")
            else:
                print(f"{Colors.RED}❌ Nama kota tidak boleh kosong!{Colors.ENDC}")
                time.sleep(1)
                
        elif choice == "2":
            cities = show_quick_cities()
            try:
                city_choice = input(f"\n{Colors.GREEN}Pilih nomor kota (1-{len(cities)}): {Colors.ENDC}").strip()
                city_idx = int(city_choice) - 1
                if 0 <= city_idx < len(cities):
                    result = get_detailed_weather(cities[city_idx])
                    print(f"\n{result}")
                    input(f"\n{Colors.PINK}Tekan ENTER untuk melanjutkan...{Colors.ENDC}")
                else:
                    print(f"{Colors.RED}❌ Pilihan tidak valid!{Colors.ENDC}")
                    time.sleep(1)
            except ValueError:
                print(f"{Colors.RED}❌ Masukkan nomor yang valid!{Colors.ENDC}")
                time.sleep(1)
                
        elif choice == "3":
            print(f"\n{Colors.CYAN}═" * 60 + f"{Colors.ENDC}")
            coords = input(f"{Colors.GREEN}🗺️  Masukkan koordinat (lat,lon): {Colors.ENDC}").strip()
            if coords:
                result = get_detailed_weather(coords)
                print(f"\n{result}")
                input(f"\n{Colors.PINK}Tekan ENTER untuk melanjutkan...{Colors.ENDC}")
            else:
                print(f"{Colors.RED}❌ Koordinat tidak boleh kosong!{Colors.ENDC}")
                time.sleep(1)
                
        elif choice == "4":
            print(f"\n{Colors.YELLOW}👋 Terima kasih telah menggunakan tools ini!{Colors.ENDC}")
            print(f"{Colors.GREEN}🌟 Tetap aman dan semoga harimu menyenangkan! 🌟{Colors.ENDC}")
            loading_animation("Exiting", 1)
            break
            
        else:
            print(f"{Colors.RED}❌ Pilihan tidak valid! Silakan pilih 1-4.{Colors.ENDC}")
            time.sleep(1)

def main():
    """Fungsi utama"""
    try:
        # Cek koneksi internet
        print(f"{Colors.YELLOW}🌐 Checking internet connection...{Colors.ENDC}")
        requests.get("http://google.com", timeout=5)
        
        interactive_menu()
        
    except requests.RequestException:
        print(f"{Colors.RED}❌ Tidak ada koneksi internet! Pastikan Anda terhubung ke internet.{Colors.ENDC}")
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}👋 Program dihentikan oleh user. Sampai jumpa!{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}❌ Error tidak terduga: {str(e)}{Colors.ENDC}")
        sys.exit(1)

if __name__ == "__main__":
    main()
