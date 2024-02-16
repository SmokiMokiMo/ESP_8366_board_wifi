import gc
import uos
import micropython


# gc.collect()

def mem_test():
    # Call this function to print memory information
    micropython.mem_info()

def ram_check():
    # mem_test()
    free_ram = gc.mem_free()
    total_ram = gc.mem_alloc() + free_ram
    print("Free RAM is:", free_ram, "Total RAM is:", total_ram)
ram_check()


def flash_check():
    fs_info = uos.statvfs("/")
    total_flash = fs_info[0] * fs_info[2]
    used_flash = fs_info[0] * (fs_info[2] - fs_info[3])
    print("Free FLASH is:", used_flash, "Total FLASH is:", total_flash)

flash_check()
async def handle_http(reader, writer):
    try:
        with open('server_page.html', 'r') as file:
            while True:
                chunk = file.read(1024)  # Read 1024 bytes at a time
                if not chunk:
                    break  # No more data to read
                await writer.awrite(chunk)

    except OSError:
        response = (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/plain\r\n"
            "Connection: close\r\n"
            "\r\n"
            "404 Not Found"
        )
        await writer.awrite(response)
    finally:
        await writer.aclose()