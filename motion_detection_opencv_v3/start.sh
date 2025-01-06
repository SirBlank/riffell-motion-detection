#!/bin/bash
python3 curr-animation-socket.py &
python3 main_code_socket_no_led.py &
python3 alicat_control.py &
wait