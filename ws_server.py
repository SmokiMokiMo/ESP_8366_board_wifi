import asyncio
import ubinascii
import json
import hashlib
import pins
import config

def b64encode(s):
    return ubinascii.b2a_base64(s)[:-1].decode()

async def handle_websocket(reader, writer):
    try:
        # Read the client's handshake request
        request = await reader.read(1024)
        request_str = request.decode()

        # Extract the Sec-WebSocket-Key from the request
        key_start = request_str.find("Sec-WebSocket-Key: ") + len("Sec-WebSocket-Key: ")
        key_end = request_str.find("\r\n", key_start)
        key = request_str[key_start:key_end].strip()

        # Generate the Sec-WebSocket-Accept value
        accept_value = b64encode(hashlib.sha1((key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode()).digest())

        # Send the WebSocket upgrade response with the Sec-WebSocket-Accept header
        response = "HTTP/1.1 101 Switching Protocols\r\n" \
                   "Upgrade: websocket\r\n" \
                   "Connection: Upgrade\r\n" \
                   "Sec-WebSocket-Accept: {}\r\n" \
                   "\r\n".format(accept_value)

        await writer.awrite(response.encode())

        while True:
            # Read the WebSocket frame header
            try:
                header = await reader.read(2)
                b1, b2 = header
            except asyncio.CancelledError:
                break  # Task was cancelled, expected when the client closes the connection
            except Exception as e:
                print("Error reading WebSocket frame header:", repr(e))
                break  # Stop processing this connection if an error occurs

            fin = b1 & 0x80
            opcode = b1 & 0x0F
            mask = b2 & 0x80
            length = b2 & 0x7F

            if length == 126:
                try:
                    length_data = await reader.readexactly(2)
                    length = (length_data[0] << 8) + length_data[1]
                except asyncio.CancelledError:
                    break  # Task was cancelled, expected when the client closes the connection
                except Exception as e:
                    print("Error reading WebSocket frame length:", repr(e))
                    break  # Stop processing this connection if an error occurs
            elif length == 127:
                try:
                    length_data = await reader.readexactly(8)
                    length = int.from_bytes(length_data, "big")
                except asyncio.CancelledError:
                    break  # Task was cancelled, expected when the client closes the connection
                except Exception as e:
                    print("Error reading WebSocket frame length:", repr(e))
                    break  # Stop processing this connection if an error occurs

            mask_key = await reader.read(4) if mask else None

            try:
                frame_data = await reader.readexactly(length)
                
            except asyncio.CancelledError:
                break  
            except Exception as e:
                print("Error reading WebSocket frame data:", repr(e))
                break  

            if mask:
                frame_data = bytes(b ^ mask_key[i % 4] for i, b in enumerate(frame_data))

            try:
                message = frame_data.decode('utf-8')  
                print("Message to server:", message)

                if message.strip():
                    try:
                        message_json = json.loads(message)
                    except json.JSONDecodeError as e:
                        print(f"Error decoding message as JSON: {e}")
                        return

                    user_input = message_json.get("content", "")            
                    
                    led_status, pin_number = pins.led_pin(user_input, pin_number=2)                    

                    # Create a response message
                    response_message = {
                        "mssg_type": "response",
                        "content": user_input,
                        "pin_number": pin_number,
                        "status" : led_status,                        
                        "temp": pins.temperature,
                        "humid": pins.humidity,
                    }
                    
                    # Respond back to the client with the response message in JSON format
                    if response_message:
                        response_data = json.dumps(response_message)
                        try:
                            response_data = response_data.encode('utf-8')
                            header = bytearray([0b10000001, len(response_data)])
                            print("Message to client:", response_message)
                            await writer.awrite(header + response_data)
                        except Exception as e:
                            print("Error during sending response to client - {}".format(e))
            except UnicodeError:
                print("Error decoding message as UTF-8")
            except Exception as e:
                print("Error processing WebSocket data:", repr(e))

    except asyncio.CancelledError:
        pass  
    except Exception as e:
        print("Error processing WebSocket data:", repr(e))
    finally:
        await writer.aclose()