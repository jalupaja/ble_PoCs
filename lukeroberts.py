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

async def test(addr):
    client = await connect(addr)
    if not client:
        print("ERROR: connection failed")
        return

    # uuid = "44092844-0567-11e6-b862-0002a5d5c51b"
    # unknown. write_value = 00 -> 0x15

    # uuid = "44092848-0567-11e6-b862-0002a5d5c51b"
    # unknown. rsvd value: 2; write_value = 0x3200

    # unknown
    # uuid = "44092842-0567-11e6-b862-0002a5d5c51b"
    # write_value = 0x0200

    # value to nothing?
    # write_value = 0x648c0a00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

    # rsvd_value = await client.get_char(uuid)
    # if rsvd_value is not None:
    #     print(f"Characteristic value: {value}")

    await client.write_char(uuid, write_value, response=False)

    await client.disconnect()

async def new_profile(addr):
    client = await connect(addr)
    if not client:
        print("ERROR: connection failed")
        return

    # add new profile "NEW" with lamp turned off (handle = 27)
    uuid = "44092843-0567-11e6-b862-0002a5d5c51b"

    MAX_LEN = 40 # maximum length: 20 characters = 40 hex characters
    name = "new profile" # name of the new profile
    name_hex = name.lower().encode("utf-8").hex() # hex encode name
    name_hex += '0' * (MAX_LEN - len(name_hex)) # pad hex
    name_hex = name_hex[0:40] # ensure maximum length
    write_value = bytes.fromhex(f"01fe0001000000008c0a{'0' * 296}{name_hex}")

    await client.write_char(uuid, write_value, response=False)

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(new_profile("00:00:00:00:00:00"))

