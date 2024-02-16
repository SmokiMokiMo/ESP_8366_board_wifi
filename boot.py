import network
import config
import time
from modules import modules
from modules import ggsheet

station = network.WLAN(network.STA_IF)
station.active(True)
    
modules.do_connect()

config.SERVER_IP = station.ifconfig()[0]

print('\nConnection to Wi-Fi router successful.....')
print("SSID:", modules.ssid)
print("Password:", modules.password)
print("IP Address:", config.SERVER_IP,"\n") 
modules.synchronize_time()

ggsheet = ggsheet.MicroGoogleSheet()

# Update the data to a specific cell (Row,Column,Data)
ggsheet.updateCell(3,3,"H")