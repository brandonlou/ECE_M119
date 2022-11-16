import asyncio
import struct
import time
from bleak import BleakScanner, BleakClient

GESTURE_UUID = '00002101-0000-1000-8000-00805f9b34fb'


async def connect_ble_internal(address, connected, gesture_shared):
    async with BleakClient(address) as client:
        print(f'Connected to {address}')
        connected.value = 1
        while client.is_connected:
            # Read acceleration values in the x, y, and z direction
            gesture_bytes = await client.read_gatt_char(GESTURE_UUID)

            # Convert received 4 bytes into an int
            gesture_local = struct.unpack('<i', gesture_bytes)[0]

            # Update shared variable accessed by the pong process
            gesture_shared.value = gesture_local

    connected.value = 0
    print(f'Disconnected from {address}')


def connect_ble(address, connected, gesture):
    asyncio.run(connect_ble_internal(address, connected, gesture))
