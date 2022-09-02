# !/usr/bin/env python3
# DolphinDB Inc.
# @Author: DolphinDB
# @Last modification time: 2022.09.01
# @FileName: verifyResult.py

# This script is to compare the WorldQuant 101 alpha results from DolphinDB and Python.
# Remember to get the verify result from DolphinDB and python first.
# Don't forget to change your directory.


import pandas as pd
from pandas.testing import assert_series_equal

ddb = pd.read_csv('/YOUR_DIR/ddbVerifyRes.csv')
py = pd.read_csv('/YOUR_DIR/pyVerifyRes.csv')

for i in range(len(ddb.columns)):
    try:
        assert_series_equal(ddb.iloc[200:, i], py.iloc[200:, i],check_names=False, check_dtype=False)
        print(f"columns[{i}] passed")
    except AssertionError as e:
        print(f"columns[{i}] failed")
        print(e)