# Impor library yang diperlukan. Netmiko akan digunakan untuk koneksi SSH.
from netmiko import ConnectHandler
import csv
import re
import os
import sys # Digunakan untuk keluar dari skrip
import logging # Modul untuk debugging

# Mengaktifkan debug logging untuk Netmiko
logging.basicConfig(filename="netmiko.log", level=logging.DEBUG)
logging.getLogger("netmiko").setLevel(logging.DEBUG)

# Impor kredensial perangkat dari file terpisah.
# Pastikan file 'devices.py' berada di direktori yang sama.
from devices import DEVICES, JUMPHOST_1, JUMPHOST_2

# Nama file CSV output.
CSV_FILE_NAME = "cisco_device_info.csv"

# Fungsi untuk mengekstrak informasi yang dibutuhkan dari output perintah.
def parse_device_info(output):
    """
    Fungsi ini mengambil string output dari router dan mengurai informasi yang diperlukan.
    """
    data = {}

    # Ekstrak Hostname dari prompt router.
    # Regex yang diperbarui ini mencari frasa "hostname" diikuti oleh nama host.
    hostname_match = re.search(r"^hostname (\S+)", output, re.MULTILINE)
    data["hostname"] = hostname_match.group(1) if hostname_match else "N/A"

    # Ekstrak IP Address dari Loopback0.
    # Regex yang diperbarui ini mencari frasa "Internet address is"
    # diikuti oleh alamat IP dan subnet mask.
    loopback_match = re.search(r"Internet address is (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/\d{1,2}", output)
    data["loopback0_ip"] = loopback_match.group(1) if loopback_match else "N/A"

    # Ekstrak Platform
    # Mencari pola "Cisco XXXXX platform"
    platform_match = re.search(r"Cisco\s+(.+?)\s+platform", output)
    data["platform"] = platform_match.group(1) if platform_match else "N/A"

    # Ekstrak Versi
    # Mencari pola "Cisco IOS Software, ... Version X.X..."
    version_match = re.search(r"Cisco IOS Software, (.+?), Version (.+?),", output)
    if version_match:
        data["version"] = f"{version_match.group(1)}, Version {version_match.group(2)}"
    else:
        # Menangani versi Linux seperti di tangkapan layar
        linux_version_match = re.search(r"Linux Software\s+\((.+?)\), Version (.+?),", output)
        if linux_version_match:
             data["version"] = f"Linux Software ({linux_version_match.group(1)}), Version {linux_version_match.group(2)}"
        else:
             data["version"] = "N/A"

    return data

def run_automation():
    """
    Fungsi untuk menjalankan proses utama otomatisasi.
    """
    print("\n[+] Memulai proses pencarian informasi perangkat...")

    # Cek apakah file CSV sudah ada. Jika ada, hapus agar data baru bisa ditulis.
    if os.path.exists(CSV_FILE_NAME):
        os.remove(CSV_FILE_NAME)
        print(f"[*] File '{CSV_FILE_NAME}' yang lama telah dihapus.")

    # Menulis header ke file CSV
    with open(CSV_FILE_NAME, "a", newline="") as csvfile:
        fieldnames = ["hostname", "loopback0_ip", "platform", "version"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
    
    # Loop melalui setiap perangkat dalam daftar
    for device in DEVICES:
        host = device["host"]
        print(f"\n[+] Menghubungkan ke perangkat {host} melalui dua jumphost...")
        
        try:
            # 1. Membuat koneksi SSH ke jumphost pertama (SSI)
            jump1_connect = ConnectHandler(**JUMPHOST_1)
            print(f"[*] Berhasil terhubung ke jumphost pertama ({JUMPHOST_1['host']}).")

            # 2. Dari jumphost pertama, jalankan perintah SSH ke jumphost kedua (Telkom)
            print(f"[*] Menghubungkan ke jumphost kedua ({JUMPHOST_2['host']})...")
            jump2_connect_session = jump1_connect.send_command_expect(
                f"ssh {JUMPHOST_2['username']}@{JUMPHOST_2['host']}",
                expect_string=r"Password:"
            )
            jump2_connect_session += jump1_connect.send_command_expect(JUMPHOST_2['password'], expect_string=r"~$")
            
            print(f"[*] Berhasil terhubung ke jumphost kedua ({JUMPHOST_2['host']}).")

            # 3. Dari jumphost kedua, jalankan perintah SSH ke perangkat target (Node Telkor)
            print(f"[*] Menghubungkan ke perangkat target ({host})...")
            net_connect_session = jump1_connect.send_command_expect(
                f"ssh {device['username']}@{device['host']}",
                expect_string=r"Password:"
            )
            net_connect_session += jump1_connect.send_command_expect(device['password'], expect_string=r">")
            
            # Masuk ke privilege mode
            net_connect_session += jump1_connect.send_command_expect("enable", expect_string=r"Password:")
            net_connect_session += jump1_connect.send_command_expect(device['secret'], expect_string=r"#")
            
            print(f"[*] Berhasil terhubung ke perangkat {host}.")

            # Menjalankan perintah show
            print("[*] Mengambil informasi...")
            output_hostname = jump1_connect.send_command("show running-config | include hostname", use_textfsm=False)
            output_interface = jump1_connect.send_command("show ip interface loopback0", use_textfsm=False)
            output_platform = jump1_connect.send_command("show platform", use_textfsm=False)
            output_version = jump1_connect.send_command("show version", use_textfsm=False)
            
            # Gabungkan output menjadi satu string untuk diurai
            combined_output = f"{output_hostname}\n{output_interface}\n{output_platform}\n{output_version}"
            
            # Mengurai output untuk mendapatkan data yang diinginkan
            device_info = parse_device_info(combined_output)
            print("[*] Informasi perangkat berhasil diurai.")

            # Menulis data ke file CSV
            with open(CSV_FILE_NAME, "a", newline="") as csvfile:
                fieldnames = ["hostname", "loopback0_ip", "platform", "version"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow(device_info)
            
            print(f"[*] Data perangkat {host} telah disimpan ke file '{CSV_FILE_NAME}'.")
            
            # Tutup koneksi SSH
            jump1_connect.disconnect()

        except Exception as e:
            print(f"[-] Gagal terhubung atau mengambil data dari {host}: {e}")
            # Menulis entri error ke file CSV
            with open(CSV_FILE_NAME, "a", newline="") as csvfile:
                fieldnames = ["hostname", "loopback0_ip", "platform", "version"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({
                    "hostname": host,
                    "loopback0_ip": "ERROR",
                    "platform": "ERROR",
                    "version": "ERROR"
                })

    print("\n[+] Proses otomatisasi selesai. Silakan cek file cisco_device_info.csv.")

def show_menu():
    """
    Menampilkan menu interaktif kepada pengguna.
    """
    banner = """
 __          ___          _______        _     
 \ \        / (_)        |__   __|      | |    
  \ \  /\  / / _ _ __ ______| | ___  ___| |__  
   \ \/  \/ / | | '_ \______| |/ _ \/ __| '_ \ 
    \  /\  /  | | | | |     | |  __/ (__| | | |
     \/  \/   |_|_| |_|     |_|\___|\___|_| |_|
                                                    
           .:AdelwinNL FT NurSyafaq:.
    Skrip Otomasi Logging Perangkat Jaringan Cisco
"""
    print(banner)
    print("---------------------------------------------------------")
    print("Selamat datang di Skrip Otomasi Logging Cisco Router.")
    print("Pilih opsi di bawah ini:")
    print("---------------------------------------------------------")
    print("1. Mulai cari informasi perangkat")
    print("2. Keluar")
    print("---------------------------------------------------------")

def main():
    """
    Fungsi utama yang mengelola menu dan alur program.
    """
    while True:
        show_menu()
        choice = input("Masukkan pilihan Anda (1 atau 2): ")

        if choice == "1":
            run_automation()
            break
        elif choice == "2":
            print("Terima kasih, sampai jumpa!")
            sys.exit()
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            continue

if __name__ == "__main__":
    main()
