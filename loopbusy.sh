#!/bin/bash

rm -f busy_c*

for i in {10..1}
do

    sudo mn -c
    sudo pkill -9 python
    sudo python main.py --cpu_frac $(echo $1) --version 2
done

python analyze_results.py -f busy_c1
python analyze_results.py -f busy_c2
