import usbrelay_py
import time 
import threading
# Note that a call to count() is required to enumerate the attached relays
# before attempting to operate the relays


def board_check():
    count = usbrelay_py.board_count()
    print("Count: ",count)

def board_details():
    boards = usbrelay_py.board_details()
    print("Boards: ",boards)
    return boards

def init ():
    global boards, board
    boards = board_details()
    board = boards[0]
    
def on_relay(number):
    usbrelay_py.board_control(board[0],number,1)

def off_relay(number):
    usbrelay_py.board_control(board[0],number,0)

# relay_control.py

# relay_control.py

import time
import threading

# Global stop event
stop_event = threading.Event()

def Start(pause, duration, start):
    # Ensure the stop_event is cleared at the start
    stop_event.clear()

    # Assuming board_check and init are defined elsewhere
    board_check()
    print("Found device")
    init()
    print("Opened device")

    try:
        while start and not stop_event.is_set():
            # Wait for a certain time
            time.sleep(pause)

            # Turn on the first relay & wait duration
            on_relay(1)
            print("TURN ON 1")
            time.sleep(duration)

            # Turn off the first relay & wait before turning second on
            off_relay(1)
            print("TURN OFF 1")
            time.sleep(5)

            # Turn on the second relay & wait duration
            on_relay(2)
            print("TURN ON 2")
            time.sleep(duration)

            # Turn off the second relay
            off_relay(2)
            print("TURN OFF 2")

            if stop_event.is_set():
                break
    finally:
        Stop()  # Ensure relays are turned off in any case
        print("Relays turned off")

def Stop():
    off_relay(1)
    off_relay(2)
    print("Relays turned off")

def request_stop():
    stop_event.set()

