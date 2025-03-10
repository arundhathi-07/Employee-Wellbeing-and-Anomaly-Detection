import time
from pynput import mouse, keyboard

def track_activity():
    last_activity_time = time.time()
    timeout = 15

    def on_press(key):
        nonlocal last_activity_time
        print(f"Key {key} pressed")
        last_activity_time = time.time()

    def on_click(x, y, button, pressed):
        nonlocal last_activity_time
        if pressed:
            print(f"Mouse clicked at ({x}, {y})")
            last_activity_time = time.time()

    with keyboard.Listener(on_press=on_press) as keyboard_listener, mouse.Listener(on_click=on_click) as mouse_listener:
        while True:
            if time.time() - last_activity_time > timeout:
                print("User is disengaged.")
                last_activity_time = time.time()

            time.sleep(1)
