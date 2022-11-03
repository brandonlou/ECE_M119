import asyncio
import matplotlib.pyplot as plt
import multiprocessing as mp
import pandas as pd
import struct
import time
from matplotlib.animation import FuncAnimation
from bleak import BleakScanner, BleakClient

DEVICE_NAME = 'Arduino'
ACCEL_SERVICE_UUID = '00001101-0000-1000-8000-00805f9b34fb'
ACCEL_X_UUID = '00002101-0000-1000-8000-00805f9b34fb'
ACCEL_Y_UUID = '00002102-0000-1000-8000-00805f9b34fb'
ACCEL_Z_UUID = '00002103-0000-1000-8000-00805f9b34fb'

SCAN_INTERVAL_SEC = 5
UPDATE_INTERVAL_SEC = 0.2
UPDATE_INTERVAL_MS = UPDATE_INTERVAL_SEC * 1000


async def connect_ble(ns):
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

    async with BleakClient(address) as client:
        #print('Services:')
        #for s in client.services:
        #    print(s)
        while True:
            # Read acceleration values in the x, y, and z direction
            ax_bytes = await client.read_gatt_char(ACCEL_X_UUID)
            ay_bytes = await client.read_gatt_char(ACCEL_Y_UUID)
            az_bytes = await client.read_gatt_char(ACCEL_Z_UUID)
            # Convert received 4 bytes into a float
            ax = struct.unpack('<f', ax_bytes)[0]
            ay = struct.unpack('<f', ay_bytes)[0]
            az = struct.unpack('<f', az_bytes)[0]
            # Create a new dataframe containing a single row and append it to the global dataframe
            data = {'time': [time.time()], 'ax': [ax], 'ay': [ay], 'az': [az]}
            row = pd.DataFrame(data)
            ns.df = pd.concat([ns.df, row], ignore_index=True)
            ns.df.reset_index()
            print(f'{ax}, {ay}, {az}')
            await asyncio.sleep(UPDATE_INTERVAL_SEC)


def update_plot(i, ns):
    time = ns.df.loc[:,'time']
    ax = ns.df.loc[:,'ax']
    ay = ns.df.loc[:,'ay']
    az = ns.df.loc[:,'az']
    plt.cla() # Clear axes
    plt.xlabel('Time')
    plt.ylabel('IMU value')
    plt.plot(time, ax, label='ax')
    #plt.plot(time, ay, label='ay')
    #plt.plot(time, az, label='az')
    plt.legend(loc='upper right')


def animate(ns):
    ani = FuncAnimation(plt.gcf(), update_plot, fargs=(ns,), interval=UPDATE_INTERVAL_MS)
    plt.show()


def main():
    manager = mp.Manager()
    ns = manager.Namespace()
    ns.df = pd.DataFrame(columns=['time', 'ax', 'ay', 'az'])
    p = mp.Process(target=animate, args=(ns,))
    p.start()
    asyncio.run(connect_ble(ns))
    p.join()


if __name__ == '__main__':
    main()

