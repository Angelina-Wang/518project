#!/bin/bash

for j in {5..1}
do
    sudo mn -c
    sudo pkill -9 python
    sudo python main.py --version 3
done

python analyze_results.py -f sendLots
