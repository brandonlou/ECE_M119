import multiprocessing as mp
import time
from bluetooth import connect_ble
from pong import run_pong

ARDUINO_ADDRESS_1 = '6C74ED05-4406-28D3-E8F6-A197DF99342B' # Brandon
ARDUINO_ADDRESS_2 = '335AFBCA-F006-0B7A-1CB9-32A1739FF829' # Vani


def main():
    manager = mp.Manager()
    connected_1 = manager.Value('i', 0)
    connected_2 = manager.Value('i', 0)
    gesture_1 = manager.Value('i', 0)
    gesture_2 = manager.Value('i', 0)

    ble_proc_1 = mp.Process(target=connect_ble, args=(ARDUINO_ADDRESS_1, connected_1, gesture_1))
    ble_proc_2 = mp.Process(target=connect_ble, args=(ARDUINO_ADDRESS_2, connected_2, gesture_2))

    ble_proc_2.start()
    ble_proc_1.start()

    # Wait for both Arduinos to connect
    while True:
        if connected_1.value and connected_2.value:
            break
        time.sleep(2)

    run_pong(gesture_1, gesture_2)


if __name__ == '__main__':
    main()
