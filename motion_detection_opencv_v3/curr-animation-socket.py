import pyglet
from pyglet.gl import *
import time
import socket
import threading
import IR_LED
import board
import digitalio
import csv
import random
import os
import pandas as pd
from datetime import datetime


"""
current working script
"""

# Window dimensions
window_width, window_height = 1920, 1080

# Get available displays
display = pyglet.canvas.get_display()
screens = display.get_screens()

# Select primary and secondary screens
primary_screen = screens[0]
secondary_screen = screens[1] if len(screens) > 1 else primary_screen 

# Create a fullscreen window on the secondary screen
window = pyglet.window.Window(
    fullscreen=True,
    screen=secondary_screen,
    vsync=True,
    width=window_width,
    height=window_height
)

# PARAMS TO ADJUST:
# Bar properties
bar_width = 70
bar_height = 700
bar_color = (0, 0, 0, 1)
background_white = True
max_extent_dist = 400 # Maximum extent distance from the center
bar_speed = 300  # Speed in pixels per second
animation_duration = max_extent_dist*4/bar_speed  # Duration of the animation in seconds

# Initial states
animation_active = False
bar_x = (window_width - bar_width) / 2  # Start at middle position

# Define pins and patterns for LEDs
pins = [
    board.C3, board.C2, board.C1, board.C0,
    board.C7, board.C6, board.C5, board.C4,
    board.D7, board.D6, board.D5, board.D4
]

pattern = {
    "Left": pins[8],
    "Right": pins[4],
    "MD": [pins[10], pins[11]]
}

# Set up the LED
LED_PIN = board.C6
led = digitalio.DigitalInOut(LED_PIN)
led.direction = digitalio.Direction.OUTPUT
led.value = False
led_state = False

led_dataset = []
last_led_on_time = None


def setup_projection():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, window_width, 0, window_height)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def draw_background(background_white, window_width, window_height):
    if background_white:
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
    else:
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        glBegin(GL_QUADS)
        glColor4f(133.0 / 255.0, 132.0 / 255.0, 131.0 / 255.0, 1.0)
        glVertex2f(0, window_height // 2)
        glVertex2f(window_width, window_height // 2)
        glVertex2f(window_width, window_height)
        glVertex2f(0, window_height)
        glEnd()

        glBegin(GL_QUADS)
        glColor4f(1.0, 1.0, 1.0, 1.0)
        glVertex2f(0, 0)
        glVertex2f(window_width, 0)
        glVertex2f(window_width, window_height // 2)
        glVertex2f(0, window_height // 2)
        glEnd()

def draw_vertical_bar(x, bar_width, bar_height, window_height, bar_color):
    glColor4f(*bar_color)
    glBegin(GL_QUADS)
    glVertex2f(x, (window_height - bar_height) / 2)
    glVertex2f(x + bar_width, (window_height - bar_height) / 2)
    glVertex2f(x + bar_width, (window_height - bar_height) / 2 + bar_height)
    glVertex2f(x, (window_height - bar_height) / 2 + bar_height)
    glEnd()

@window.event
def on_draw():
    window.clear()
    setup_projection()
    draw_background(background_white, window_width, window_height)
    draw_vertical_bar(bar_x, bar_width, bar_height, window_height, bar_color)

def update_bar_position(dt):
    global bar_x, direction, animation_active, start_time

    if not animation_active:
        return

    elapsed_time = time.time() - start_time

    # Calculate distance to move based on speed and time
    move_distance = speed_pixels_per_sec * dt
    bar_x += direction * move_distance
    center = False

    # Check if the bar has reached max extent and needs to bounce
    middle_pos = (window_width - bar_width) / 2
    farthest_left = middle_pos - max_extent_dist
    farthest_right = middle_pos + max_extent_dist

    if bar_x <= farthest_left or bar_x >= farthest_right:
        direction *= -1  # Reverse direction

    # Reset position to center after animation duration
    if elapsed_time >= animation_duration:
        animation_active = False
        time.sleep(1)
        bar_x = middle_pos
        IR_LED.LED_off(pattern["Left"])
        IR_LED.LED_off(pattern["Right"])
        data = [['bar_width', bar_width], ['bar_height', bar_height], ['bar_color', bar_color],
                ['background_white', background_white], ['max_extent_dist', max_extent_dist], ['bar_speed', bar_speed],
                ['animation_duration', animation_duration], ['direction', direction]]
        df = pd.DataFrame(data, columns=['variable_names', 'values'])
        base_folder = '/mnt/data/DATA'
        df.to_csv(os.path.join(base_folder, f'{log_time}_viz_params.csv'), index=False)


    # LED Blinking Logic
    handle_led_logic(direction)

def handle_led_logic(direction):
    if direction == 1: # if right
        IR_LED.LED_off(pattern["Left"])
        IR_LED.LED_on(pattern["Right"])
    else: # if left
        IR_LED.LED_off(pattern["Right"])
        IR_LED.LED_on(pattern["Left"])

@window.event
def on_close():
    pyglet.app.exit()

def blink_led(dt):
    global led_state, led_dataset, last_led_on_time
    led_state = not led_state
    led.value = led_state
    current_time = time.time()
    if led_state:
        # LED turned on
        last_led_on_time = current_time
    else:
        # LED turned off
        if last_led_on_time is not None:
            diff = current_time - last_led_on_time
            led_dataset.append({'on': last_led_on_time, 'off': current_time, 'diff': diff})
            last_led_on_time = None

def start_animation(speed, duration, color, background_white_input, max_extent_distance):
    global start_time, animation_active, log_time
    global background_white, speed_pixels_per_sec, animation_duration, bar_color, direction

    # Assign the parameter values to the global variables
    background_white = background_white_input
    speed_pixels_per_sec = speed
    animation_duration = duration
    bar_color = tuple(c / 255.0 for c in color[:3]) + (color[3],)
    start_time = time.time()
    animation_active = True
    direction = random.choice([-1, 1])  # 1 for right, -1 for left
    log_time = datetime.now().strftime("%Y-%-m-%d_%H-%M-%S.%f")[:-3]
    print(log_time)
    print(direction)

    # Initialize the LEDs
    IR_LED.init(pins)

    # Start LED blinking
    pyglet.clock.schedule_interval(blink_led, 0.0714)

def socket_server():
    host = 'localhost'
    port = 5000
    s = None

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))
            s.listen()
            print('Listening for connections on {}:{}...'.format(host, port))
            while True:
                conn, addr = s.accept()
                with conn:
                    print('Connected by', addr)
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        start_animation(
                            speed=bar_speed,
                            duration=animation_duration,
                            color=bar_color,
                            background_white_input=background_white,
                            max_extent_distance=max_extent_dist
                        )
    except Exception as e:
        print("Socket server error:", e)
    finally:
        print("Socket server shutting down.")
        if s:
            s.close()

if __name__ == "__main__":
    # Start the socket server in a separate thread
    server_thread = threading.Thread(target=socket_server, daemon=True)
    server_thread.start()

    pyglet.clock.schedule_interval(update_bar_position, 1 / 240.0)
    try:
        pyglet.app.run()
    except KeyboardInterrupt:
        print("Stopping animation...")
    finally:
        print("Closing...")
        for pin in pins:
            IR_LED.LED_off(pin)
