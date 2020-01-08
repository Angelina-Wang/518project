#!/bin/bash

rm c1_bw$1
rm c2_bw$1

for i in {10..1}
do
    sudo mn -c
    sudo pkill -9 python
    sudo python main.py --bw $(echo $1)
done

python analyze_results.py -f "c1_bw$1"
python analyze_results.py -f "c2_bw$1"
