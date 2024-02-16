import asyncio
import ubinascii
import json
import config
import ws_server
import editiin_func
import pins
import uasyncio


async def main():
    try:
        # Set up WebSocket server    
        ws_server_instance = await uasyncio.start_server(ws_server.handle_websocket, config.SERVER_IP, 81)

        # Set up HTTP server
        http_server = await uasyncio.start_server(editiin_func.handle_http, config.SERVER_IP, 80)
        
        # Start the temperature and humidity measurement task
        temp_sensor = await uasyncio.create_task(pins.temp_humid_task())
        
        # Print server information
        print("WebSocket server listening on", config.SERVER_IP, 81)
        print("HTTP server listening on", config.SERVER_IP, 80)

        # Keep the event loop running
        while True:
            await asyncio.sleep(1)

    except Exception as e:
        print("An error occurred in the main function: %s", repr(e))
        raise

try:
    # Start the event loop
    uasyncio.run(main())  # Use uasyncio.run to start the event loop
except KeyboardInterrupt:
    print("Server stopped.")