#!/usr/bin/python3
# (c) Snocember 2020, github.com/snocember

import threading
from time import sleep
import sys
try:
    from pynput.mouse import Listener
    from pynput.mouse import Button, Controller
except ModuleNotFoundError:
    print("Die erforderliche Python-Bibliothek 'pynput' ist nicht installiert.")
    string = input("Möchten sie die Bibliothek installieren? (y/n): ")
    if string == "y" or string == "Y" or string == "yes" or string == "YES":
        print("Ok. Die fehlende Bibliothek 'requests' wird nachinstalliert.")
        print()
        print("Geben sie diese Zeile in die Kommandozeile ein.")
        print("$ sudo pip3 install pynput")
        print("Sie müssen ihr Passwort eingeben, wenn sie Sudo-Berechtigungen haben.")
        sys.exit()

    else:
        print("Dann nicht.")

gelb = '\033[30;103m'
gruen = "\033[42m"
rst = "\033[0m"

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
        print("["+str(button)+"] wurde ausgewählt.")
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
                    sys.stdout.write(u"\u001b[1000D"+gelb+"Autoclicker deaktiviert"+rst)
                    break_def = 1
                if break_def == 0:
                    if activate == False:
                        activate = True
                        sys.stdout.write(u"\u001b[1000D"+gruen+"Autoclicker -aktiviert-"+rst)
            if mode == "1" or mode == "3":
                activate = True
                sys.stdout.write(u"\u001b[1000D"+gruen+"Autoclicker -aktiviert-"+rst)
        else:
            if mode == "1" or mode == "3":
                activate = False
                sys.stdout.write(u"\u001b[1000D"+gelb+"Autoclicker deaktiviert"+rst)
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
    except KeyboardInterrupt:
      raise
    except:
      print("Programm beendet.")

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

print("Drücke bitte die Aktivierungstaste einmal um sie festzulegen.")
with Listener(on_click=on_activate) as listener:
        listener.join()
try:
  cps = float(input("Wie viele Clicks pro Sekunde (cps) möchstest du haben? : "))
except ValueError:
  print("Error: Du musst eine Zahl eintragen.")
  sys.exit()
print()
print("Welchen Modus möchtest du haben?")
print("Clickassist:")
print("- (1) Hold&Press - beim halten der Aktivierungstaste ist der AC aktiviert, linke/rechte Maustaste muss mit 4 cps geclickt werden")
print("- (2) On&Off --  - beim Tippen de/aktivieren des Autoclickers, linke/rechte Maustaste muss mit 4 cps geclickt werden")
print("Autoclicker:")
print("- (3) Hold&Press - beim halten der Aktivierungstaste ist der AC aktiviert [LINKSKLICK]")
print("- (4) On&Off --  - beim Tippen de/aktivieren des Autoclickers [LINKSKLICK]")

mode = input("Auswahl (1|2|3|4): ")
if mode != "1":
    if mode != "2":
        if mode != "3":
            if mode != "4":
                print("Es muss '1','2','3' oder '4' angegeben werden.")
                sys.exit()
if mode == "3" or mode == "4":
    delay = (1/float(cps*2))-0.005
if mode == "1" or mode == "2":
    delay = (1/float(cps*3))-0.005
max_count = int(cps/4)
input("Drücke ENTER um zu starten.")
try:
  t1 = threading.Thread(target=threadLISTENER, args=())
  t2 = threading.Thread(target=threadCLICKERl, args=())
  t3 = threading.Thread(target=threadCLICKERr, args=())
  t1.daemon=True
  t2.daemon=True
  t3.daemon=True
  t1.start()
  t2.start()
  t3.start()
  while True:
      sleep(100)

except (KeyboardInterrupt, SystemExit):
  print()
  print("Programm wird beendet.")

except:
  print("Error: Konnte Thread nicht starten.")
