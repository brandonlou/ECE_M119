import asyncio
import struct
from bleak import BleakScanner, BleakClient

ADDRESS = '6C74ED05-4406-28D3-E8F6-A197DF99342B'
GESTURE_UUID = '00002101-0000-1000-8000-00805f9b34fb'


async def main():
    async with BleakClient(ADDRESS) as client:
        print(f'Connected to {ADDRESS}')
        prev_gesture = -1
        while client.is_connected:
            gesture_bytes = await client.read_gatt_char(GESTURE_UUID)
            gesture = struct.unpack('<i', gesture_bytes)[0]
            if gesture != prev_gesture:
                print(gesture)
                prev_gesture = gesture
        printf(f'Disconnected from {ADDRESS}')


if __name__ == '__main__':
    asyncio.run(main())

