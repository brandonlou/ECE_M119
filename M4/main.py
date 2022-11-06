import asyncio
import multiprocessing as mp
import struct
import time
from bleak import BleakScanner, BleakClient
from pong import run_pong

DEVICE_NAME = 'Arduino'
ACCEL_X_UUID = '00002101-0000-1000-8000-00805f9b34fb'
SCAN_INTERVAL_SEC = 5


async def connect_ble():
    address = None
    while True:
        print('Scanning...')
        devices = await BleakScanner.discover()
        for d in devices:
            print(f'{d.name}')
            if d.name == DEVICE_NAME:
                address = str(d.address)
                print(f'Found {DEVICE_NAME}! Address: {address}')
                break
        if address is not None:
            break
        time.sleep(SCAN_INTERVAL_SEC)

    manager = mp.Manager()
    ax_shared = manager.Value('d', 0.0) # Double precision float
    pong_proc = mp.Process(target=run_pong, args=(ax_shared,))

    async with BleakClient(address) as client:
        #print('Services:')
        #for s in client.services:
        #    print(s)
        pong_proc.start()
        while True:
            # Read acceleration values in the x, y, and z direction
            ax_bytes = await client.read_gatt_char(ACCEL_X_UUID)

            # Convert received 4 bytes into a float
            ax = struct.unpack('<f', ax_bytes)[0]

            # Update shared variable accessed by the pong process
            ax_shared.value = ax

            # print(f'ax: {ax}')
            # await asyncio.sleep(UPDATE_INTERVAL_SEC)

    print(f'Disconnected from {address}')
    pong_proc.join()


def main():
    asyncio.run(connect_ble())


if __name__ == '__main__':
    main()

