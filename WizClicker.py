#Wiz 101 autoclicker

#Imports for catching inputs, as well as starting a thread
from pynput.keyboard import KeyCode, Controller, Listener, Key
import time, os, sys, threading

#Set the dir to correctly grab script.txt
scriptdir = os.path.abspath(os.path.dirname(sys.argv[0]))

#Create lines to pull from
lines = []
try:
    with open(os.path.join(scriptdir, 'script.txt')) as f:
        lines = [line.strip() for line in f if line.strip()]
except:
    print("There is no script.txt file in the .exe folder. There will be no chatting. Timing will be 0.5 shorter on looping\n\n")

#Setup controllers for inputting mouse and keyboard, as well as start and stop buttons
keyboard = Controller()
from pynput.mouse import Button, Controller 
mouse = Controller()
start_stop_key = Key.f1
stop_key = Key.f2

#Thread for the autoclicker (Named walk, but does both walking and clicking. Possibly change in future if adding Bazaar support)
class Walk(threading.Thread):

    def __init__(self):
        super(Walk, self).__init__()
        self.running = False
        self.program_running = True
        self.m_button = Button.left
        self.f_button = KeyCode(char='w')
        self.b_button = KeyCode(char='s')
        self.maybe = True
    
    def start_walking(self):
        self.running = True
        print("Starting!")
  
    def stop_walking(self): 
        self.running = False
        print("Pausing!")
  
    def exit(self): 
        self.stop_walking() 
        print("Stopping!")
        self.program_running = False


    def run(self):
        while self.program_running:
            while self.running:
                #Walk back and forth in a way that (hopefully) won't move you out of the battle range, but enough to remove the after battle ghost thing
                keyboard.press(self.b_button)
                time.sleep(1)
                keyboard.release(self.b_button)
                keyboard.press(self.f_button)
                time.sleep(2.3)
                keyboard.release(self.f_button)
                keyboard.press(self.b_button)
                time.sleep(1)
                keyboard.release(self.b_button)
                #Attempt to click on a card in the center of the screen
                mouse.position = (965, 518)
                time.sleep(0.1)
                mouse.click(self.m_button)
                time.sleep(0.1)
                mouse.position = (735, 645)
                time.sleep(1)
                #Only click pass every other loop, to prevent desyncing causing multiple WizClicker users from actually casting spells
                if(self.maybe):
                    mouse.click(self.m_button)
                self.maybe = not self.maybe
                time.sleep(0.1)

                #optional script posting. Is included in walk script to prevent it from accidently eating walking controls.
                if lines:
                    keyboard.press(Key.enter)
                    time.sleep(0.1)
                    keyboard.release(Key.enter)
                    time.sleep(0.1)
                    keyboard.type(lines[0])
                    keyboard.press(Key.enter)
                    time.sleep(0.1)
                    keyboard.release(Key.enter)
                    time.sleep(0.1)
                    lines.pop(0)
                    time.sleep(0.2)
            time.sleep(0.1)
            
            
#Startup Text
print("Hello! Thank you for using WizClicker 1.0\nControls:\n     F1: Start and stop the program.\n     F2: Exit the program\nPlease excuse the slight delay between pressing pause and pressing exit, it must finish its loop first.")
print("\nThis program will:\n  * Walk back and forth\n  * Attempt to click a card in the center of the screen\n  * Select Pass if it cannot\n  * Type the next line in script.txt (If you would prefer this not to happen, delete script.txt)")

#Start the walk thread
walk_thread = Walk()
walk_thread.start()

#Define input
def on_press(key): 
    if key == start_stop_key: 
        if walk_thread.running: 
            walk_thread.stop_walking() 
        else: 
            walk_thread.start_walking() 
              
    elif key == stop_key: 
        walk_thread.exit() 
        listener.stop() 

#Start input capture
with Listener(on_press=on_press) as listener: 
    listener.join() 