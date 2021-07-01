import pyautogui
from pyclick import HumanClicker
import python_imagesearch.imagesearch as imgsearch
import time
from pynput.keyboard import Key
from pynput.keyboard import Controller
import pynput.keyboard
import sys
import configparser


config = configparser.ConfigParser()
try:
    config.read('config.ini')
    print('config found')
    screen_mode = config['all']['screen-mode']
    debug = config['all']['debug_mode']
except Exception as e:
    print('config not found')
    screen_mode = '1920x1080'

print('screen_mode = ' + screen_mode)
print('debug mode = ' + debug)
time.sleep(2)
path = 'img\\'
hc = HumanClicker()
keyboard = Controller()
mode = 'moving'

def see(image):
    position = imgsearch.imagesearch(path + image + '.png')
    if position[0] != -1:
        if (debug == 'semi') or (debug == 'full'):
            print(f'SEE:    {image} {str(position)}')
        return True
    else:
        return False


def on_press(key):
    global mode
    if key == pynput.keyboard.Key.f10:
        mode = 'run'
        print(mode)
    if key == pynput.keyboard.Key.f11:
        mode = 'waiting_mode'
        print(mode)
    if key == pynput.keyboard.Key.f12:
        mode = 'coord_mode'
        print(mode)
    if key == pynput.keyboard.Key.f7:
        print('shutting down')
        sys.exit(1)

    if key == pynput.keyboard.Key.f9:
        # print('moving to the point of click')
        mode = 'moving'
        print(mode)
    

def run():
    
    global mode
    while True:
        if mode == 'run':
            if see('buy'+screen_mode):
                hc.click()
                mode = 'waiting_mode'
                if (debug == 'semi') or (debug == 'full'):
                    print('clicked on buy')
            else:
                if debug == 'full':
                    print('no buy image')

        if mode == 'moving':
            hc.move((642,109), duration=1)
            time.sleep(0.2)
            if (debug == 'semi') or (debug == 'full'):
                print('moved to point. Switching to run mode')
            mode = 'run'

        if mode == 'coord_mode':
            print(pyautogui.position())
            time.sleep(1)   

        if mode == 'waiting_mode':
            time.sleep(0.1)
            if debug == 'full':
                print('waited 0.1 secs')
def main():
    listener = pynput.keyboard.Listener(on_press=on_press)
    listener.start()
    run()

main()
