# Pastikan Anda menginstal Netmiko, Python, dan library pendukung lainnya.
# Pip install netmiko

DEVICES = [
    {
        "device_type": "cisco_xr",
        "host": "",
        "username": "930435",
        "password": "12345Qwer"
    },
    {
        "device_type": "cisco_xr",
        "host": "",
        "username": "",
        "password": ""
    },
    # Tambahkan perangkat Cisco lainnya di sini
]

# Konfigurasi untuk Jumphost SSI
JUMPHOST_1 = {
    "device_type": "windows",
    "host": "",
    "username": "",
    "password": ""
}

# Konfigurasi untuk Jumphost Telkom
JUMPHOST_2 = {
    "device_type": "terminal",
    "host": "",
    "username": "",
    "password": ""
}
