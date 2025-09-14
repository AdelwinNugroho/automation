# Pastikan Anda menginstal Netmiko, Python, dan library pendukung lainnya.
# Pip install netmiko

DEVICES = [
    {
        "device_type": "cisco_xr",
        "host": "R3.STA.PE-MOBILE.1",
        "username": "930435",
        "password": "12345Qwer"
    },
    {
        "device_type": "cisco_xr",
        "host": "R3.STA.PE-MOBILE.2",
        "username": "930435",
        "password": "12345Qwer"
    },
    # Tambahkan perangkat Cisco lainnya di sini
]

# Konfigurasi untuk Jumphost SSI
JUMPHOST_1 = {
    "device_type": "windows",
    "host": "100.75.49.116",
    "username": "user1",
    "password": "sisindokom@sshd1"
}

# Konfigurasi untuk Jumphost Telkom
JUMPHOST_2 = {
    "device_type": "terminal",
    "host": "10.62.170.56",
    "username": "930435",
    "password": "Razor301412"
}
