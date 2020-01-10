#!/bin/bash

rm -f dynamic*

for i in {10..1}
do
    sudo mn -c
    sudo pkill -9 python
    sudo python main.py --num_clients 8 --version 5
done

python analyze_results.py -f dynamic
