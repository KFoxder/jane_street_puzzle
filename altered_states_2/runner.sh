#!/bin/bash

# Define the number of processes to spawn based on num cpu
num_processes=$(sysctl -n hw.ncpu)

# Loop to spawn the processes
for ((i=0; i<num_processes; i++))
do
    echo "pypy3 main.py &"
    pypy3 main.py &
done

# Wait for all processes to finish
wait