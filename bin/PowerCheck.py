from tkinter import *
import os
import time
import psutil
import pystray
import PIL.Image
import sys
import datetime

icon_logo = 'PowerCheck.ico'
start_time = datetime.datetime.now()
background = '#000000'
bg = background
foreground_green = '#00FF00'
fg_green = foreground_green
foreground_red = '#FF0000'
fg_red = foreground_red

def window_configure_power_off():
    global window_power_off
    window_power_off = Tk()
    wide = window_power_off.winfo_screenwidth()
    high = window_power_off.winfo_screenheight()
    w = wide - 438
    h = high - 480
    window_power_off.attributes("-topmost",True)
    window_power_off.title("PowerCheck")
    window_power_off.attributes("-topmost",True)
    window_power_off.geometry(f"428x90+{w}+{h}")
    window_power_off.resizable(False, False)
    window_power_off.configure(bg=bg)
    txt = Label(text="Зарядка завершена!\n Отключите зарядку от ноутбука,\nчтобы сэкономить ресурс батареи!", 
                                background=bg, foreground=fg_green,
                                font=("Arial 18 bold")).place(x=0, y=0)
    window_power_off.iconbitmap(icon_logo)
    
def window_configure_power_on():
    global window_power_on
    window_power_on = Tk()
    wide = window_power_on.winfo_screenwidth()
    high = window_power_on.winfo_screenheight()
    w = wide - 438
    h = high - 480
    window_power_on.attributes("-topmost",True)
    window_power_on.title("PowerCheck")
    window_power_on.attributes("-topmost",True)
    window_power_on.geometry(f"428x70+{w}+{h}")
    window_power_on.resizable(False, False)
    window_power_on.configure(bg=bg)
    txt = Label(text="Батарея разряжена!\n Подключите зарядку к ноутбуку!", 
                                background=bg, foreground=fg_red,
                                font=("Arial 18 bold")).place(x=0, y=0)
    window_power_on.iconbitmap(icon_logo)

def start_power_off():
    window_configure_power_off()
    window_power_off.update()
    time.sleep(1.5)
    try:
        window_power_off.destroy()
    except:
        update()
    update()  
    
def start_power_on():
    window_configure_power_on()
    window_power_on.update()
    time.sleep(1.5)
    try:
        window_power_on.destroy()
    except:
        update()
    update()  

def pause_start():
    global start_time
    start_time = datetime.datetime.now()
   
def pause_finish():
    global start_time, check_pause
    elapsed_time = datetime.datetime.now() - start_time
    if elapsed_time.total_seconds() >= 200:
        check_pause = 0

def update():
    while True:
        global check_exit, check_pause
        if check_exit == 1:
            sys.exit()
        battery = psutil.sensors_battery()
        percent = int(battery.percent)
        pause_finish()
        if percent >= 70 and battery.power_plugged == True and check_pause == 0 :
            start_power_off()
        if percent <= 50 and battery.power_plugged == False and check_pause == 0 :
            start_power_on()
        time.sleep(1)
        
def tray(): 
    global check_exit
    global check_pause
    check_exit = 0
    check_pause = 0
    image = PIL.Image.open(icon_logo)
    def on_click(icon,item):
        global check_exit
        check_exit = 1
        icon.stop()
    def ok_click(icon,item):
        global check_pause
        if check_pause == 0:
            check_pause = 1
            pause_start()
    icon = pystray.Icon("PowerCheck", image, menu = pystray.Menu(pystray.MenuItem("Я понял!", ok_click), pystray.MenuItem("Выйти", on_click)))
    def run(icon):
        icon.visible = True
        update()
    icon.run(run) 
    
tray()
