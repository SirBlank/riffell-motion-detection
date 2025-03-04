#!/bin/bash

python animation.py &
pid1=$!
python main.py
pid2=$!

cleanup() {
    echo "Stopping all Python processes..."
    kill $pid1 $pid2 $pid3
}

trap cleanup SIGINT

wait