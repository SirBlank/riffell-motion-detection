import usbrelay_py
import time 
import threading

# OS Version: Ubuntu 22.04.4
# Python: 3.10.12
# Time: Python version
# Threading: Python version

# Note that a call to count() is required to enumerate the attached relays
# before attempting to operate the relays

# This function checks if relay is connected or not 
def board_check():
    count = usbrelay_py.board_count()
    print("Count: ",count)

# This function gives the detials to the board
def board_details():
    boards = usbrelay_py.board_details()
    print("Boards: ",boards)
    return boards

# Initializes the board to find the relay
def init ():
    global boards, board
    boards = board_details()
    board = boards[0]
    
# Turn on relay based on the number 
def on_relay(number):
    usbrelay_py.board_control(board[0],number,1)

# Turn off the relay based on the number 
def off_relay(number):
    usbrelay_py.board_control(board[0],number,0)


# Global stop event
stop_event = threading.Event()

# This function starts the relay based on the pause, duration, start
# Pause: how the system will wait until after turning on and off both relays
# Duration: how the relay will be on for 
# Start: indicates if it should start or not  
def Start(pause, duration, start):
    # Ensure the stop_event is cleared at the start
    stop_event.clear()

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

            # Stops when the main program closes
            if stop_event.is_set():
                break
    finally:
        Stop()  # Ensure relays are turned off in any case
        print("Relays turned off")

# Functions turn offs all of the relays
def Stop():
    off_relay(1)
    off_relay(2)
    print("Relays turned off")

# Requests the relays to be turned off 
def request_stop():
    stop_event.set()

