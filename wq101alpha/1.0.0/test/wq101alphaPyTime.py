# !/usr/bin/env python3
# DolphinDB Inc.
# @Author: DolphinDB
# @Last modification time: 2022.09.01
# @FileName: wq101alphaPyTime.py

# This script is to test the performance of the implementation of WorldQuant 101 alpha in python.
# You will need to put alpha101_adjusted.py and this wq101alphaPyTime.py in the same folder.
# You will need to use dataPerformance.csv. Don't forget to change your directory.
# The overall time cost is about 42 minutes.

import time
import pandas as pd
from tqdm import tqdm
from alpha101_adjusted import Alphas

data = pd.read_csv('/YOUR_DIR/dataPerformance.csv')
df = data.pivot(index='tradetime', columns='securityid') 


stock = Alphas(df)

a1 = getattr(Alphas, 'alpha00' + str(1))
times = []

nofunc = [48, 56, 58, 59, 63, 67, 69, 70, 76, 79, 80, 82, 87, 89, 90, 91, 93, 97, 100]

for i in tqdm(range(1, 102)):
    if i in nofunc:
        times.append('no function')
        continue
    else:
        factor = getattr(Alphas, "alpha{:03d}".format(i))
    try:
        t1 = time.time()
        res = factor(stock)
        t2 = time.time()
        times.append(t2 - t1)
    except Exception:
        times.append('error')

timeRes = pd.DataFrame({"alphaName":list(range(1,102)),"timeCost":times})
timeRes.to_csv('/YOUR_DIR/pyPerformance.txt',index=False)
