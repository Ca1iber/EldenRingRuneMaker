import pyautogui
import time
from pynput import keyboard

time.sleep(3)
print('Running')

control=keyboard.Controller()

while True:
    #吃黄金角币
    control.press('r')
    time.sleep(3)
    control.release('r')

    #控制移动
    control.press('w')
    time.sleep(3)
    control.release('w')
    control.press('a')
    time.sleep(0.8)
    control.release('a')
    control.press('w')
    time.sleep(2.25)
    control.release('w')

    #黄金波动！
    control.press(keyboard.Key.ctrl)
    time.sleep(0.1)
    control.release(keyboard.Key.ctrl)
    time.sleep(2.5)

    #重新传送
    control.press('g')
    time.sleep(0.1)
    control.release('g')
    time.sleep(0.8)
    control.press('f')
    time.sleep(0.1)
    control.release('f')
    time.sleep(0.1)
    control.press('e')
    time.sleep(0.1)
    control.release('e')
    time.sleep(2.5)
    control.press('e')
    time.sleep(0.1)
    control.release('e')

    #传送读条
    time.sleep(7)