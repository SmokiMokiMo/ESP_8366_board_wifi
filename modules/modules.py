import ntptime
import utime
import machine
from machine import RTC


# Connect to Wi-Fi
#ssid = 'Boosteroid 2G'
#password='YourDeviceOurPower'
ssid = 'Smka'
password = '74617461smka'


def do_connect(ssid=ssid, password=password):
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('\n\nConnecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            pass
        
    print('Network config:', sta_if.ifconfig())
    
    
# Time synchronization
def synchronize_time():
    try:
        rtc = RTC()
        ntptime.settime()
        (year, month, day, weekday, hours, minutes, seconds, subseconds) = rtc.datetime()
        #print("UTC Time: \n", (year, month, day, hours, minutes, seconds))        

        sec = ntptime.time()
        timezone_hour = 2.0
        timezone_sec = timezone_hour * 3600
        sec = int(sec + timezone_sec)
        (year, month, day, hours, minutes, seconds, weekday, yearday) = utime.localtime(sec)
        print ("IST Time: [{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}]".format(
                   year, month, day, hours, minutes, seconds))
        rtc.datetime((year, month, day, 0, hours, minutes, seconds, 0))

    except Exception as e:
        print('Error synchronizing time:', e)
        
synchronize_time()
