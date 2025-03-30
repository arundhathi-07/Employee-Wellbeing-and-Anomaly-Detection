import time
from pynput import mouse, keyboard
import threading

class DisengagementTracker:
    def __init__(self, timeout=15):
        self.last_activity_time = time.time()
        self.timeout = timeout
        self.disengaged = False
        self.running = True
        self.last_print_time = time.time()

    def on_press(self, key):
        self.last_activity_time = time.time()
        if self.disengaged:
            self.disengaged = False
            print("[ENGAGEMENT] User re-engaged")

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.last_activity_time = time.time()
            if self.disengaged:
                self.disengaged = False
                print("[ENGAGEMENT] User re-engaged")

    def check_activity(self):
        with keyboard.Listener(on_press=self.on_press) as keyboard_listener, \
             mouse.Listener(on_click=self.on_click) as mouse_listener:
            while self.running:
                current_time = time.time()
                if current_time - self.last_activity_time > self.timeout:
                    if not self.disengaged:
                        self.disengaged = True
                        print("[ENGAGEMENT] User disengaged")
                
                # Print status every 5 seconds
                if current_time - self.last_print_time > 5:
                    status = "disengaged" if self.disengaged else "engaged"
                    print(f"[ENGAGEMENT] Current status: {status}")
                    self.last_print_time = current_time
                
                time.sleep(1)
    
    def start(self):
        self.thread = threading.Thread(target=self.check_activity)
        self.thread.daemon = True
        self.thread.start()
    
    def stop(self):
        self.running = False
        self.thread.join()