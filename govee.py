from ble_client import ble_client
import asyncio

async def connect(addr):
    client = ble_client(addr)
    await client.connect()
    if not client.is_connected():
        return None
    return client

async def print_svc(addr):
    client = await connect(addr)
    if not client:
        print("ERROR: connection failed")
        return

    await client.print_services()

    await client.disconnect()

async def showcase(addr, second_lamp = False):
    if second_lamp:
        await asyncio.sleep(1)

    client = await connect(addr)
    if not client:
        print("ERROR: connection failed")
        return

    uuid = "00010203-0405-0607-0809-0a0b0c0d2b11" # (handle: 16)

    # handle: 0011 (=16)
    val_keepalive = "aa010000000000000000000000000000000000ab"
    val_off = "3301000000000000000000000000000000000032"
    val_red = "33050dff0d2d00000000000000000000000000e4"
    val_purple = "33050d8b00ff000000000000000000000000004f"
    val_orange = "33050dff7f0000000000000000000000000000bb"
    val_yellow = "33050dffff00000000000000000000000000003b"
    val_green = "33050d00ff0000000000000000000000000000c4"
    val_blue = "33050d0000ff00000000000000000000000000c4"

    val_100 = "3304640000000000000000000000000000000053"
    val_94 = "33045E0000000000000000000000000000000069"
    val_85 = "3304550000000000000000000000000000000062"
    val_75 = "33044B000000000000000000000000000000007c"
    val_64 = "3304400000000000000000000000000000000077"
    val_50 = "3304320000000000000000000000000000000005"
    val_20 = "3304140000000000000000000000000000000023"
    val_1 = "3304010000000000000000000000000000000036"

    async def send(value):
        write_value = bytes.fromhex(value)
        await client.write_char(uuid, write_value, response=False)

    showcase_colors = [val_red, val_green, val_orange, val_blue, val_yellow, val_purple, val_off]
    if second_lamp:
        showcase_colors2 = [val_orange, val_blue, val_yellow, val_purple, val_red, val_green, val_off]
    showcase_brightness = [val_100, val_20, val_94, val_64, val_1, val_50, val_50]
    for i in range(len(showcase_colors)):
        if i % 2: # every 2 seconds 2 keep alives
            await send(val_keepalive)
            await send(val_keepalive)
        await send(showcase_colors[i])
        await send(showcase_brightness[i])

        print("wait...")
        await asyncio.sleep(1)

    await client.disconnect()

async def turn_off(addr):
    client = await connect(addr)
    if not client:
        print("ERROR: connection failed")
        return

    uuid = "00010203-0405-0607-0809-0a0b0c0d2b11" # (16) ???

    val_off = "3301000000000000000000000000000000000032" # off

    write_value = bytes.fromhex(val_off)
    await client.write_char(uuid, write_value, response=False)

    await client.disconnect()

def calc_brightness(brightness):
    """this function is doesn't work above brightness 64. The last_byte value changes weirdly and I don't want to use elif for every 16? steps"""
    if brightness <= 55:
        last_byte = format(0x37 - brightness, '02X')
    elif brightness <= 63:
        last_byte = format(0xb7 - brightness, '02X')
        last_byte = f"0{last_byte[1]}"
    else:
        # TODO not correct
        last_byte = format(0x77 + 0x20 * (((brightness // 16)) // 2) - brightness, '02X')
    # elif brightness <= 87:
    #     last_byte = format(0xb7 - brightness, '02X')
    # else:
    #     last_byte = format(0xc7 - brightness, '02X')
    return f"3304{format(brightness, '02X')}00000000000000000000000000000000{last_byte}"

async def run_showcase(addr1, addr2):
    await asyncio.gather(showcase(addr1), showcase(addr2, True))

if __name__ == "__main__":
    pass

