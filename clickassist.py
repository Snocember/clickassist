#!/usr/bin/python3
# (c) Snocember 2020, github.com/snocember

import threading
from time import sleep
from locale import getdefaultlocale
import sys

gelb = '\033[30;103m'
gruen = "\033[42m"
cyan = "\033[96m"
rst = "\033[0m"

class lang:
    class de:
        class ModuleNotFoundError:
            txt1 = "Die erforderliche Python-Bibliothek 'pynput' ist nicht installiert."
            txt2 = "Möchten sie die Bibliothek installieren? (y/n): "
            y1  =  "Ok. Sie müssen die fehlende Bibliothek 'pynput' nachinstallieren"
            y2  =  "Geben sie diese Zeile in die Kommandozeile ein."
            y3  =  "$ sudo pip3 install pynput"
            y4  =  "Sie müssen ihr Passwort eingeben, wenn sie Sudo-Berechtigungen haben."
            y5  =  "Starten sie danach dieses Programm neu."
            n1  =  "Ohne diese Bibliothek wird das Programm abgebrochen."
        class ThreadError:
            txt = "Error: Konnte Thread nicht starten."
        class ValueError:
            txt = "Error: Du musst eine Zahl eintragen."
        class ButtonSelected:
            txt = "] wurde ausgewählt."
        class Autoclicker:
            on = "Autoclicker -aktiviert-"
            off = "Autoclicker deaktiviert"
        class ProgramEnd:
            txt = "Programm beendet."
        class Start:
            txt1 = "Drücke bitte die Aktivierungstaste einmal, um sie festzulegen."
            txt2 = "Wie viele Clicks pro Sekunde (cps) möchstest du haben? : "
            txt3 = "Welchen Modus möchtest du haben?"
            txt4 = "Clickassist:"
            txt5 = "- (1) Hold&Press - beim halten der Aktivierungstaste ist der AC aktiviert, linke/rechte Maustaste muss mit 4 cps geclickt werden"
            txt6 = "- (2) On&Off --  - beim Tippen de/aktivieren des Autoclickers, linke/rechte Maustaste muss mit 4 cps geclickt werden"
            txt7 = "Autoclicker:"
            txt8 = "- (3) Hold&Press - beim halten der Aktivierungstaste ist der AC aktiviert [LINKSKLICK]"
            txt9 = "- (4) On&Off --  - beim Tippen de/aktivieren des Autoclickers [LINKSKLICK]"
            txt10 = "Auswahl (1|2|3|4): "
            err1 = "Es muss '1','2','3' oder '4' angegeben werden."
            txt11 = "Wenn gedrückt, welche Maustaste sollte unterstützt werden? (l|r|lr): "
            err2 = "Du kannst nur 'l', 'r' or 'lr' schreiben."
            txt12 = "Drücke ENTER um zu starten."
    class en:
        class ModuleNotFoundError:
            txt1 = "Python-library 'pynput' is not installed."
            txt2 = "Do you want to install 'pynput' (y/n): "
            y1  =  "Ok. You have to install the missing library 'pynput'."
            y2  =  "Type this below in the promt."
            y3  =  "$ sudo pip3 install pynput"
            y4  =  "If you have sudo-rights, enter your password."
            y5  =  "After that you can reopen the app."
            n1  =  "Without this library the app will be stopped."
        class ThreadError:
            txt = "Error: Couldn't start thread."
        class ValueError:
            txt = "Error: You have to input a number."
        class ButtonSelected:
            txt = "] was chosen."
        class Autoclicker:
            on  = "autoclicker -aktivated-"
            off = "autoclicker deaktivated"
        class ProgramEnd:
            txt = "Ended app."
        class Start:
            txt1 = "Please press the activation key once to continue."
            txt2 = "How many clicks per second (cps) would you like to have? : "
            txt3 = "Which mode do you choose?"
            txt4 = "Clickassist:"
            txt5 = "- (1) Hold&Press - by pressing the activation key the autoclicker is enabled, left/right mouse button has to be clicked with 4 cps"
            txt6 = "- (2) On&Off --  - tap the activation key to en/disable the autoclicker, left/right mouse button has to be clicked with 4 cps"
            txt7 = "Autoclicker:"
            txt8 = "- (3) Hold&Press - by pressing the activation key the autoclicker is enabled [LEFTCLICK]"
            txt9 = "- (4) On&Off --  - tap the activation key to en/disable the autoclicker [LEFTCLICK]"
            txt10 = "Choice (1|2|3|4): "
            err1 = "You can only choose '1','2','3' or '4'."
            txt11 = "Which mouse key should be assisted when clicked? (l|r|lr): "
            err2 = "You can only type 'l', 'r' or 'lr'."
            txt12 = "Press ENTER to start."

default_lang = getdefaultlocale()
default_lang = default_lang[0].split("_")
default_lang = default_lang[0]
if default_lang == "de":
    d_lang = lang.de
elif default_lang == "en":
    d_lang = lang.en
else:
    d_lang = lang.en

try:
    from pynput.mouse import Listener
    from pynput.mouse import Button, Controller
except ModuleNotFoundError:
    print(d_lang.ModuleNotFoundError.txt1)
    string = input(d_lang.ModuleNotFoundError.txt2)
    if string == "y" or string == "Y" or string == "yes" or string == "YES" or string == "j" or string == "ja":
        print(d_lang.ModuleNotFoundError.y1)
        print()
        print(d_lang.ModuleNotFoundError.y2)
        print(d_lang.ModuleNotFoundError.y3)
        print(d_lang.ModuleNotFoundError.y4)
        print(d_lang.ModuleNotFoundError.y5)
        sys.exit()

    else:
        print(d_lang.ModuleNotFoundError.n1)

print(cyan)
print("   _____ _ _      _                 _     _   ")
print("  / ____| (_)    | |               (_)   | |  ")
print(" | |    | |_  ___| | ____ _ ___ ___ _ ___| |_ ")
print(" | |    | | |/ __| |/ / _` / __/ __| / __| __|")
print(" | |____| | | (__|   < (_| \__ \__ \ \__ \ |_ ")
print("  \_____|_|_|\___|_|\_\__,_|___/___/_|___/\__|")
print(rst)

mouse = Controller()
activate_button = ""
activate = False
pressed_left = False
pressed_right = False
running = False
counter_l = 20
counter_r = 20

def on_activate(x, y, button, pressed):
    global activate_button
    if pressed:
        activate_button = button
        print("["+str(button)+d_lang.ButtonSelected.txt)
    if not pressed:
        return False

def on_click(x, y, button, pressed):
    break_def = 0
    global activate_button, activate, pressed_left, pressed_right, running
    global counter_l, counter_r
    if button == activate_button:
        if pressed:
            if mode == "2" or mode == "4":
                if activate == True:
                    activate = False
                    sys.stdout.write(u"\u001b[1000D"+gelb+d_lang.Autoclicker.off+rst)
                    break_def = 1
                if break_def == 0:
                    if activate == False:
                        activate = True
                        sys.stdout.write(u"\u001b[1000D"+gruen+d_lang.Autoclicker.on+rst)
            if mode == "1" or mode == "3":
                activate = True
                sys.stdout.write(u"\u001b[1000D"+gruen+d_lang.Autoclicker.on+rst)
        else:
            if mode == "1" or mode == "3":
                activate = False
                sys.stdout.write(u"\u001b[1000D"+gelb+d_lang.Autoclicker.off+rst)
        sys.stdout.flush()
    if running == False:
        if button == Button.left:
            if pressed:
                #print("l pressed")
                pressed_left = True
                counter_l = 0
            else:
                pressed_left = False
        if button == Button.right:
            if pressed:
                #print("r pressed")
                pressed_right = True
                counter_r = 0
            else:
                pressed_right = False

def threadLISTENER():
  with Listener(on_click=on_click) as listener:
    try:
      listener.join()
    except (KeyboardInterrupt, SystemExit):
      raise
    except:
      print(d_lang.ProgramEnd.txt)

def threadCLICKERl():
  global activate, running
  global delay, counter_l, max_count
  global pressed_left, pressed_right
  while True:
    while activate == True:
      if mode == "1" or mode == "2":
        while counter_l <= max_count:
          running = True
          mouse.press(Button.left)
          mouse.release(Button.left)
          running = False
          sleep(delay)
          counter_l = counter_l+1
      if mode == "3" or mode == "4":
          running = True
          mouse.press(Button.left)
          mouse.release(Button.left)
          running = False
          sleep(delay)

def threadCLICKERr():
  global activate, running
  global delay, counter_r, max_count
  global pressed_right
  while True:
    while activate == True:
      if mode == "1" or mode == "2":
        while counter_r <= max_count:
          running = True
          mouse.press(Button.right)
          mouse.release(Button.right)
          running = False
          sleep(delay)
          counter_r = counter_r+1
# -----
print(d_lang.Start.txt1)

with Listener(on_click=on_activate) as listener: listener.join()

try:
  cps = float(input(d_lang.Start.txt2))
except ValueError:
  print(d_lang.ValueError.txt)
  sys.exit()
print()
print(d_lang.Start.txt3)
print(d_lang.Start.txt4)
print(d_lang.Start.txt5)
print(d_lang.Start.txt6)
print(d_lang.Start.txt7)
print(d_lang.Start.txt8)
print(d_lang.Start.txt9)

mode = input(d_lang.Start.txt10)
if mode != "1":
    if mode != "2":
        if mode != "3":
            if mode != "4":
                print(d_lang.Start.err1)
                sys.exit()
if mode == "3" or mode == "4":
    delay = (1/float(cps*2))-0.005
if mode == "1" or mode == "2":
    delay = (1/float(cps*3))-0.005
max_count = int(cps/4)
keys = input(d_lang.Start.txt11)
if keys != "l":
    if keys != "r":
        if keys != "lr":
            print(d_lang.Start.err2)
            sys.exit()
input(d_lang.Start.txt12)
try:
  t1 = threading.Thread(target=threadLISTENER, args=())
  t1.daemon=True
  t1.start()
  if keys == "l" or keys == "lr":
      t2 = threading.Thread(target=threadCLICKERl, args=())
      t2.daemon=True
      t2.start()
  if keys == "r" or keys == "lr":
      t3 = threading.Thread(target=threadCLICKERr, args=())
      t3.daemon=True
      t3.start()

  while True:
      sleep(100)

except (KeyboardInterrupt, SystemExit):
  print()
  print(d_lang.ProgramEnd.txt)

except:
  print(d_lang.ThreadError.txt)
