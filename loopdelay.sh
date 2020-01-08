#!/bin/bash


for i in {10..1}
do
    sudo mn -c
    sudo pkill -9 python
    sudo python main.py --delay $(echo $1)
done

python analyze_results.py -f "c1_d$1"
python analyze_results.py -f "c2_d$1"
