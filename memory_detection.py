import pyautogui
from time import time, sleep
from ctypes import *
import pymem
import pymem.process
from pymem.ptypes import RemotePointer
import sys

PROCESS_NAME = sys.argv[1]

pm = pymem.Pymem(PROCESS_NAME)
def get_pointer_address(base, offsets):
    remote_pointer = RemotePointer(pm.process_handle, base)
    for offset in offsets:
        if offset != offsets[-1]:
            remote_pointer = RemotePointer(pm.process_handle, remote_pointer.value + offset)
        else:
            return remote_pointer.value + offset

hp_offsets = [0x90, 0x50, 0x48, 0x278]
HP_ADDRESS = get_pointer_address(pm.base_address+0x02C59698, offsets=hp_offsets)

print(f"HP_ADDRESS: 0x{HP_ADDRESS:X}")

loop_time = time()
while True:
    
    health = pm.read_uint(HP_ADDRESS)
    
    print(f"HP: {health}")
    if health < 500:
        print("LOW LIFE -- QUITTING!")
        pyautogui.hotkey("alt", "F4")
        exit()
    
    time_diff = time() - loop_time
    if time_diff < 0.006:
        sleep(0.016)
        time_diff = time() - loop_time
    print(f"FPS: {1 / (time_diff) : .2f}")
    loop_time = time()