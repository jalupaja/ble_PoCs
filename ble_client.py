import asyncio
from bleak import BleakClient

class ble_client:
    def __init__(self, address):
        self.address = address
        self.client = BleakClient(self.address)

    def is_connected(self):
        if self.client and self.client.is_connected:
            return True
        else:
            return False

    async def connect(self):
        try:
            await self.client.connect()
            if self.client.is_connected:
                print("Connected!")
            else:
                print("Failed to connect!")
        except Exception as e:
            print(f"Exception during connection: {e}")

    async def disconnect(self):
        try:
            await self.client.disconnect()
            print("Disconnected.")
        except Exception as e:
            print(f"Exception during disconnection: {e}")

    def __del__(self):
        if self.client and self.client.is_connected:
            asyncio.create_task(self.client.disconnect())

    async def __ensure_connection(self):
        if not self.client.is_connected:
            await self.connect()
        return self.client.is_connected

    async def print_services(self):
        if not await self.__ensure_connection():
            print("Not connected.")
            return

        print("SERVICES:")
        for svc in self.client.services.services.values():
            print(f"{svc.uuid}: {svc.description} ({svc.handle})")
        print("\n")

        print("CHARACTERISTICS:")
        for char in self.client.services.characteristics.values():
            print(f"{char.uuid}: {char.description} ({char.handle}) - Properties: {', '.join(char.properties)}")
        print("\n")

        print("DESCRIPTORS:")
        for desc in self.client.services.descriptors.values():
            print(f"{desc.uuid}: {desc.description} ({desc.handle})")
        print("\n")

    def __dec_value(self, value):
        if not value:
            return None
        try:
            return value.decode('utf-8')
        except Exception:
            return value.hex()

    async def get_char(self, uuid):
        if not await self.__ensure_connection():
            print("Not connected; cannot read characteristic.")
            return None

        try:
            value = await self.client.read_gatt_char(uuid)
            return self.__dec_value(value)
        except Exception as e:
            print(f"Error reading characteristic {uuid}: {e}")
            return None

    async def write_char(self, uuid, data, response=False):
        if not await self.__ensure_connection():
            print("Not connected; cannot write characteristic.")
            return None

        try:
            await self.client.write_gatt_char(uuid, data, response=response)
            print(f"Successfully wrote to characteristic {uuid}.")
        except Exception as e:
            print(f"Error writing characteristic {uuid}: {e}")
            return None

