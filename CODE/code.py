import time
import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

# Initialize the USB keyboard and US layout
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

# T9 character mappings for multi-tap typing
t9_map = {
    "1": ["a", "b", "c"],
    "2": ["d", "e", "f"],
    "3": ["g", "h", "i"],
    "4": ["j", "k", "l"],
    "5": ["m", "n", "o"],
    "6": ["p", "q", "r", "s"],
    "7": ["t", "u", "v"],
    "8": ["w", "x", "y", "z"],
    "9": ["", "BACKSPACE", "."],  # 1st tap = pending, 2nd tap = backspace, 3rd tap = period
}

# Layer 2 mappings (triggered when key '9' is held down)
layer2_map = {
    "1": "!",
    "2": "@",
    "3": "?",
    "4": "$",
    "5": "%",
    "6": "ENTER",
    "7": "CMD_L",
    "8": "-",
    "9": "CMD_L",
}

# Pins configuration mapping your physical pins to numpad values
pins_config = [
    (board.D0, "1"),
    (board.D1, "4"),
    (board.D6, "7"),
    (board.D10, "2"),
    (board.D7, "5"),
    (board.D8, "8"),
    (board.D4, "6"),
    (board.D2, "9"),
    (board.D5, "3"),
]

buttons = []
for pin, text in pins_config:
    io = digitalio.DigitalInOut(pin)
    io.direction = digitalio.Direction.INPUT
    io.pull = digitalio.Pull.UP
    buttons.append({"io": io, "text": text, "pressed": False})

# T9 cycle state variables
active_key = None
char_index = 0
last_press_time = 0
T9_TIMEOUT = 0.6  # Time window to wait before finalizing the letter

# Layer 9 tracking variables
key_9_down_time = 0
LAYER_HOLD_THRESHOLD = 0.15  # Fast response threshold for holding key 9

def commit_current_character():
    global active_key, char_index
    if active_key is not None:
        chars = t9_map[active_key]
        val = chars[char_index]
        if val != "":
            if val == "BACKSPACE":
                keyboard.send(Keycode.BACKSPACE)
            else:
                layout.write(val)
        active_key = None
        char_index = 0

while True:
    current_time = time.monotonic()
    
    # Check physical state of key 9
    key_9_btn = next(btn for btn in buttons if btn["text"] == "9")
    key_9_is_low = not key_9_btn["io"].value

    # If timeout expired for pending T9 text, commit it
    if active_key and (current_time - last_press_time > T9_TIMEOUT):
        commit_current_character()

    for btn in buttons:
        is_low = not btn["io"].value
        key_val = btn["text"]

        if is_low and not btn["pressed"]:
            btn["pressed"] = True
            
            if key_val == "9":
                key_9_down_time = current_time
            else:
                # Check if key 9 is currently being held down to trigger Layer 2
                if key_9_is_low and (current_time - key_9_down_time > LAYER_HOLD_THRESHOLD):
                    commit_current_character()
                    action = layer2_map.get(key_val)
                    if action == "ENTER":
                        keyboard.send(Keycode.ENTER)
                    elif action == "CAPS_LOCK":
                        keyboard.send(Keycode.CAPS_LOCK)
                    elif action == "CMD_L":
                        keyboard.send(Keycode.COMMAND, Keycode.L)
                    elif action:
                        layout.write(action)
                else:
                    # Standard T9 Typing Layer
                    if key_val in t9_map:
                        if active_key == key_val:
                            chars = t9_map[active_key]
                            char_index = (char_index + 1) % len(chars)
                        else:
                            commit_current_character()
                            active_key = key_val
                            char_index = 0
                        last_press_time = time.monotonic()

            time.sleep(0.04)

        elif not is_low and btn["pressed"]:
            btn["pressed"] = False
            
            # Handle tapping key 9 on release if it wasn't held as a layer modifier
            if key_val == "9":
                hold_duration = current_time - key_9_down_time
                if hold_duration <= LAYER_HOLD_THRESHOLD:
                    if active_key == "9":
                        chars = t9_map["9"]
                        char_index = (char_index + 1) % len(chars)
                    else:
                        commit_current_character()
                        active_key = "9"
                        char_index = 0
                    last_press_time = time.monotonic()

            time.sleep(0.02)

    time.sleep(0.01)
