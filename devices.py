# Pastikan Anda menginstal Netmiko, Python, dan library pendukung lainnya.
# Pip install netmiko

DEVICES = [
    {
        "device_type": "cisco_ios",
        "host": "192.168.1.1",  # IP perangkat yang sebenarnya (diakses dari jumphost)
        "username": "admin",
        "password": "your_ssh_password",
        "secret": "your_enable_password"
    },
    {
        "device_type": "cisco_ios",
        "host": "192.168.1.2",
        "username": "admin",
        "password": "your_ssh_password",
        "secret": "your_enable_password"
    },
    # Tambahkan perangkat Cisco lainnya di sini
]

# Konfigurasi untuk Jumphost SSI
JUMPHOST_1 = {
    "device_type": "linux",
    "host": "10.0.0.1",
    "username": "jumphost1_user",
    "password": "jumphost1_password"
}

# Konfigurasi untuk Jumphost Telkom
JUMPHOST_2 = {
    "device_type": "linux",
    "host": "10.0.0.2",
    "username": "jumphost2_user",
    "password": "jumphost2_password"
}

# Perlu diingat:
# - Pastikan Anda mengganti IP, username, password, dan secret
# - Pastikan Jumphost SSI memiliki akses SSH ke Jumphost Telkom
# - Pastikan Jumphost Telkom memiliki akses SSH ke semua perangkat di atas
