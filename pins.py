from machine import Pin
import dht
import utime
import uasyncio
import json
import ujson
import logging

# Configure the logging module
logging.basicConfig(level=logging.DEBUG)


def read_pin_status():
    try:        
        with open('/files/pin_status.json', 'r') as file:
            status_data = json.load(file)
            logging.debug("File Content:\n%s", status_data)
        return status_data
    except OSError as e:
        logging.error("Error reading pin status file: %s", e)
        

def write_pin_status(status_data):    
    try:        
        with open('/files/pin_status.json', 'w') as file:
            json.dump(status_data, file)
        logging.debug("Updated data:/n", read_pin_status())
    except Eexcept as e:
        logging.error("Error try to write '/files/pin_status.json'- repr(e)")


def led_pin(user_input, pin_number=2):
    led = Pin(pin_number, Pin.OUT)
    led_status = None
    # Process the message and control the LED accordingly
    if "!on" == user_input:
        led_status = True
        #print("Turning LED ON")
        led.value(1)
    elif "!off" == user_input:
        led_status = False
        #print("Turning LED OFF")
        led.value(0)
        
    return led_status, pin_number


# Define global variables to store sensor data
temperature = 0
humidity = 0

async def temp_humid_task(_count=0):
    global temperature, humidity
    d = dht.DHT11(Pin(2))
    
    while True:
        try:           
            # Corrected import statement
            utime.sleep_ms(500)
            d.measure()

                       
            
            with open('/files/sensor_data.txt', 'a') as file:
                current_time = utime.localtime()
                formatted_time = '[{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}]'.format(
                    current_time[0], current_time[1], current_time[2],
                    current_time[3], current_time[4], current_time[5]
                )
                
                # Update global variables with the latest sensor data
                temperature = d.temperature()
                humidity = d.humidity() 
                message = {
                    'time': formatted_time,
                    'temp': temperature,
                    'hum': humidity
                }
                file.write(json.dumps(message) + '\n')
                print(message)
            

        except Exception as e:
            print("Error reading DHT sensor:", repr(e))

        # Sleep for a period before the next measurement
        await uasyncio.sleep_ms(2000)