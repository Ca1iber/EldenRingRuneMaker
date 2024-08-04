import time
from pynput import keyboard
import pystray
import PIL.Image
import threading
import os

#加载系统托盘图标
image=PIL.Image.open("ER2.ico")

# 初始化控制变量
running = False

#系统托盘定义
def on_clicked(icon,item):
    global running
    if str(item)=="Say Hello":
        print("HelloWorld")
    elif str(item)=="Exit!":
        running = False
        icon.stop()
        os._exit(0)


#创建系统托盘
def setup_tray_icon():
    icon=pystray.Icon("Nude",image,menu=pystray.Menu(
        pystray.MenuItem("Say Hello",on_clicked),
        pystray.MenuItem("Exit!",on_clicked)
    ))
    icon.run()

# 在单独的线程中运行托盘图标
tray_thread = threading.Thread(target=setup_tray_icon)
tray_thread.daemon = True
tray_thread.start()


def on_press(key):
    global running
    try:
        if key == keyboard.Key.cmd_l or key == keyboard.Key.cmd_r:
            # 按下Win键时，监听下一次按键是否是'n'
            with keyboard.Listener(on_press=on_press_n) as listener:
                listener.join()
    except AttributeError:
        pass

def on_press_n(key):
    global running
    try:
        if key.char == 'n':
            running = not running
            if running:
                print('Started')
            else:
                print('Stopped')
    except AttributeError:
        pass
    return False  # 停止当前监听器

# 创建监听器
listener = keyboard.Listener(on_press=on_press)
listener.start()

print('Press Win+N to start/stop the loop')

while True:
    if running:
        # 吃黄金角币
        keyboard.Controller().press('r')
        time.sleep(3)
        keyboard.Controller().release('r')

        # 控制移动
        keyboard.Controller().press('w')
        time.sleep(3)
        keyboard.Controller().release('w')
        keyboard.Controller().press('a')
        time.sleep(0.8)
        keyboard.Controller().release('a')
        keyboard.Controller().press('w')
        time.sleep(2.25)
        keyboard.Controller().release('w')

        # 黄金波动！
        keyboard.Controller().press(keyboard.Key.ctrl)
        time.sleep(0.1)
        keyboard.Controller().release(keyboard.Key.ctrl)
        time.sleep(2.5)

        # 重新传送
        keyboard.Controller().press('g')
        time.sleep(0.1)
        keyboard.Controller().release('g')
        time.sleep(0.8)
        keyboard.Controller().press('f')
        time.sleep(0.1)
        keyboard.Controller().release('f')
        time.sleep(0.1)
        keyboard.Controller().press('e')
        time.sleep(0.1)
        keyboard.Controller().release('e')
        time.sleep(2.5)
        keyboard.Controller().press('e')
        time.sleep(0.1)
        keyboard.Controller().release('e')

        # 传送读条
        time.sleep(7)
    else:
        time.sleep(0.1)
