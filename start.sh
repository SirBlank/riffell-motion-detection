#!/bin/bash

# Animation script here
python animation_v3.py &
pid1=$!

# Camera script here
python main_code.py
pid2=$!

cleanup() {
    echo "Stopping all Python processes..."
    kill $pid1 $pid2 $pid3
}

trap cleanup SIGINT

wait