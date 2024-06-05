#!/bin/bash

# Start process.py in the background
python process.py &
FILE2_PID=$!

python main_server.py &
FILE3_PID=$!


python app.py &
FILE1_PID=$!



python pull-service.py

cleanup() {
    echo "Stopping services..."
    kill $FILE2_PID $FILE3_PID $FILE1_PID  # Kill both processes
    exit
}


# Trap termination signals
trap cleanup INT TERM


while true; do
    if ! kill -0 $FILE2_PID >/dev/null 2>&1; then
        echo "process.py has exited."
        exit 1
    fi
    sleep 1
done
