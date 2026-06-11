from machine import Pin
import time

# 1. Pin Definitions
# LEDs set as outputs
green_led = Pin(4, Pin.OUT)
yellow_led = Pin(5, Pin.OUT)
red_led = Pin(2, Pin.OUT)

# Button set as input with internal pull-up resistor
button = Pin(15, Pin.IN, Pin.PULL_UP)

# 2. State Definitions
STARTUP = 0
GREEN = 1
YELLOW = 2
RED = 3
EMERGENCY = 4

current_state = STARTUP

# 3. Time tracking variables
previous_ticks = time.ticks_ms()
current_interval = 2000  # 2 seconds for the initial STARTUP phase

# Helper function to set all LEDs at once
def set_leds(g, y, r):
    green_led.value(g)
    yellow_led.value(y)
    red_led.value(r)

# --- SETUP PHASE ---
# Requirement: Startup pe teenon LEDs band honi chahiye
set_leds(0, 0, 0)
print("STARTUP (All LEDs OFF)")

# --- MAIN LOOP ---
while True:
    current_ticks = time.ticks_ms()
    
    # Read the button (0 means pressed because of PULL_UP)
    button_pressed = (button.value() == 0)

    # Check for Emergency Button Press
    if button_pressed and current_state != EMERGENCY:
        current_state = EMERGENCY
        previous_ticks = current_ticks
        current_interval = 5000 # 5 seconds for Emergency Green
        
        set_leds(1, 0, 0) # Turn GREEN on immediately
        print("EMERGENCY")

    # Handle the Normal Cycle and Transitions
    if current_state == STARTUP:
        if time.ticks_diff(current_ticks, previous_ticks) >= current_interval:
            current_state = GREEN
            previous_ticks = current_ticks
            current_interval = 5000
            set_leds(1, 0, 0)
            print("GREEN")

    elif current_state == GREEN:
        if time.ticks_diff(current_ticks, previous_ticks) >= current_interval:
            current_state = YELLOW
            previous_ticks = current_ticks
            current_interval = 2000
            set_leds(0, 1, 0)
            print("YELLOW")

    elif current_state == YELLOW:
        if time.ticks_diff(current_ticks, previous_ticks) >= current_interval:
            current_state = RED
            previous_ticks = current_ticks
            current_interval = 5000
            set_leds(0, 0, 1)
            print("RED")

    elif current_state == RED:
        if time.ticks_diff(current_ticks, previous_ticks) >= current_interval:
            current_state = GREEN
            previous_ticks = current_ticks
            current_interval = 5000
            set_leds(1, 0, 0)
            print("GREEN")

    elif current_state == EMERGENCY:
        # After 5 seconds of Emergency Green, resume the normal cycle by moving to YELLOW
        if time.ticks_diff(current_ticks, previous_ticks) >= current_interval:
            current_state = YELLOW
            previous_ticks = current_ticks
            current_interval = 2000
            set_leds(0, 1, 0)
            print("YELLOW")
            