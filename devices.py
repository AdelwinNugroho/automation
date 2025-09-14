# Ini adalah file terpisah untuk menyimpan kredensial perangkat Anda.
# Pastikan Anda mengisinya dengan informasi yang benar.

JUMPHOST_1 = {
    "device_type": "windows",
    "host": "100.75.49.116",
    "username": "user1",
    "password": "sisindokom@sshd1",
}

JUMPHOST_2 = {
    "device_type": "terminal",
    "host": "10.62.170.56", 
    "username": "930435",
    "password": "Razor301412",
}

DEVICES = [
    {
        "device_type": "cisco_xr",
        "host": "R3.STA.PE-MOBILE.1",  # Ganti dengan IP atau hostname perangkat
        "username": "930435",
        "password": "12345Qwer",
    },
    {
        "device_type": "cisco_xr",
        "host": "R3.STA.PE-MOBILE.2",
        "username": "930435",
        "password": "12345Qwer"
    },
]
