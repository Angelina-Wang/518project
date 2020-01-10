#!/bin/bash

do
    for j in {10..1}
    do
        sudo mn -c
        sudo pkill -9 python
        sudo python main.py --version 3
    done
done

python analyze_results.py -f sendLots
