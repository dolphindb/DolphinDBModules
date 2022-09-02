# !/usr/bin/env python3
# DolphinDB Inc.
# @Author: DolphinDB
# @Last modification time: 2022.09.01
# @FileName: wq1AlphaPyRes.py

# This script is to verify the correctness of the implementation of WorldQuant 101 alpha in python.
# You will need to put alpha101_adjusted.py and this wq1AlphaPyRes.py in the same folder.
# You will need to use dataPerformance.csv. Don't forget to change your directory.

import pandas as pd
from alpha101_adjusted import Alphas


data = pd.read_csv('/YOUR_DIR/dataPerformance.csv')
selected = ['sz000001', 'sz000002', 'sz000003', 'sz000004', 'sz000005', 'sz000006', 'sz000007', 'sz000008', 'sz000009', 'sz000010']
data_selected = data[data['securityid'].isin(selected)]
df = data_selected.pivot(index='tradetime', columns='securityid')

def get_Allalpha(data):
        stock=Alphas(data)
        df = pd.DataFrame()
        errorList = [23,31,39,48,56,57,58,59,63,64,66,67,68,69,70,71,72,73,76,77,79,80,82,87,88,89,90,91,92,93,96,97,98,100]
        for i in range(1, 102):
            if i in errorList: 
                continue
            else: 
                funcNo = "alpha{:03d}".format(i)
                print("start Alpha"+str(i))
                alphaName = 'alpha' + str(i)
                df[alphaName]=eval("stock."+funcNo+"()").iloc[0:,0]
        return df
 

res = get_Allalpha(df)
res.to_csv('/YOUR_DIR/pyVerifyRes.csv')


