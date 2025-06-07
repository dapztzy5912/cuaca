#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' 

print_banner() {
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║  ${YELLOW}🚀 Cek - Cuaca 🚀           ${CYAN}║${NC}"
    echo -e "${CYAN}║                                                              ║${NC}"
    echo -e "${CYAN}║  ${GREEN}✨ Menginstal dependensi untuk tampilan yang optimal           ${CYAN}║${NC}"
    echo -e "${CYAN}║  ${GREEN}   By : XdpzQ! ✨                             ${CYAN}║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

loading_dots() {
    local text="$1"
    local duration="$2"
    local chars="⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    local delay=0.1
    local end_time=$(($(date +%s) + duration))
    
    while [ $(date +%s) -lt $end_time ]; do
        for ((i=0; i<${#chars}; i++)); do
            echo -ne "\r${CYAN}${chars:$i:1} ${text}...${NC}"
            sleep $delay
        done
    done
    echo -e "\r${GREEN}✅ ${text} selesai!${NC}"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} ${WHITE}$1${NC}"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} ${WHITE}$1${NC}"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} ${WHITE}$1${NC}"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} ${WHITE}$1${NC}"
}

main() {
    clear
    print_banner
    
    echo -e "${PURPLE}🎯 Memulai instalasi...${NC}\n"
    
    print_step "Update package list..."
    if pkg update -y > /dev/null 2>&1; then
        loading_dots "Updating packages" 2
    else
        print_error "Gagal update packages!"
        exit 1
    fi
    
    print_step "Install Python..."
    if pkg install python -y > /dev/null 2>&1; then
        loading_dots "Installing Python" 3
    else
        print_error "Gagal install Python!"
        exit 1
    fi
    
    print_step "Install Python dependencies..."
    if pip install requests > /dev/null 2>&1; then
        loading_dots "Installing requests library" 2
    else
        print_error "Gagal install requests!"
        exit 1
    fi
    
    print_step "Setting up permissions..."
    chmod +x cuaca.py
    loading_dots "Setting permissions" 1
    
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  ${YELLOW}🎉 INSTALASI BERHASIL! 🎉                                  ${GREEN}║${NC}"
    echo -e "${GREEN}╠════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${GREEN}║  ${WHITE}Cek - Cuaca siap digunakan!                                   ${GREEN}║${NC}"
    echo -e "${GREEN}║                                                                ║${NC}"
    echo -e "${GREEN}║  ${CYAN}Cara menjalankan:                                          ${GREEN}║${NC}"
    echo -e "${GREEN}║  ${YELLOW}➤ python cuaca.py                                         ${GREEN}║${NC}"
    echo -e "${GREEN}║                                                                ║${NC}"
    echo -e "${GREEN}║  ${PURPLE}Fitur yang tersedia:                                       ${GREEN}║${NC}"
    echo -e "${GREEN}║  ${WHITE}• Cuaca detail dengan emoji 🌤️                           ${GREEN}║${NC}"
    echo -e "${GREEN}║  ${WHITE}• Interface Keren 🚀                              ${GREEN}║${NC}"
    echo -e "${GREEN}║  ${WHITE}• Quick access kota populer ⚡                           ${GREEN}║${NC}"
    echo -e "${GREEN}║  ${WHITE}• Pencarian berdasarkan koordinat 🗺️                    ${GREEN}║${NC}"
    echo -e "${GREEN}║  ${WHITE}• Animasi loading ✨                          ${GREEN}║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
    
    echo ""
    echo -e "${CYAN}🌟 Nikmati Fitur Cuaca Yang Fresh Ini! 🌟${NC}"
    echo -e "${YELLOW}💡 Tip: Jalankan 'python cuaca.py' untuk memulai!${NC}"
}

if [[ ! -d "/data/data/com.termux" ]]; then
    print_warning "Script ini dioptimalkan untuk Termux, tapi tetap bisa jalan di Linux lain."
    echo ""
fi

print_step "Checking internet connection..."
if ping -c 1 google.com > /dev/null 2>&1; then
    loading_dots "Testing connection" 1
else
    print_error "Tidak ada koneksi internet! Pastikan Anda terhubung ke internet."
    exit 1
fi

main
