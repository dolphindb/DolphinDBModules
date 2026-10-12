# !/usr/bin/env python3
# DolphinDB Inc.
# @Author: DolphinDB
# @Last modification time: 2022.09.09
# @FileName: partialAlpha_npPerformance.py

# This script is to test the performance of the implementation of WorldQuant 101 alpha in python numpy.
# You will need to use dataPerformance.csv. Don't forget to change your directory.
# The overall time cost is about 6 minutes.

import numpy as np
import pandas as pd
import time

def rankdata(a, method='average', *, axis=None):
    # this rankdata refer to scipy.stats.rankdata (https://github.com/scipy/scipy/blob/v1.9.1/scipy/stats/_stats_py.py#L9047-L9153)
    if method not in ('average', 'min', 'max', 'dense', 'ordinal'):
        raise ValueError('unknown method "{0}"'.format(method))

    if axis is not None:
        a = np.asarray(a)
        if a.size == 0:
            np.core.multiarray.normalize_axis_index(axis, a.ndim)
            dt = np.float64 if method == 'average' else np.int_
            return np.empty(a.shape, dtype=dt)
        return np.apply_along_axis(rankdata, axis, a, method)

    arr = np.ravel(np.asarray(a))
    algo = 'mergesort' if method == 'ordinal' else 'quicksort'
    sorter = np.argsort(arr, kind=algo)

    inv = np.empty(sorter.size, dtype=np.intp)
    inv[sorter] = np.arange(sorter.size, dtype=np.intp)

    if method == 'ordinal':
        return inv + 1

    arr = arr[sorter]
    obs = np.r_[True, arr[1:] != arr[:-1]]
    dense = obs.cumsum()[inv]

    if method == 'dense':
        return dense

    # cumulative counts of each unique value
    count = np.r_[np.nonzero(obs)[0], len(obs)]

    if method == 'max':
        return count[dense]

    if method == 'min':
        return count[dense - 1] + 1

    # average method
    return .5 * (count[dense] + count[dense - 1] + 1)



def rolling_rank(na):
    return rankdata(na.transpose(),method='min',axis=0)[-1].transpose()

def ts_rank(x, window=10):
    a_rolled = np.lib.stride_tricks.sliding_window_view(x, window,axis = 0)
    return np.append(np.full([window-1,np.size(x, 1)],np.nan),rolling_rank(a_rolled),axis = 0)

def returns(x):
    a = (np.diff(x, axis = 0, append=np.nan)/x)
    return np.append([a[-1]],a[:-1],axis = 0)

def stddev(x, window=10):
    a_rolled = np.lib.stride_tricks.sliding_window_view(x, window,axis = 0)
    return np.append(np.full([window-1,np.size(x, 1)],np.nan),np.std(a_rolled, axis=-1, ddof=1),axis = 0)
    # return np.std(a_rolled, axis=-1)

def rank(x):
    return rankdata(x,method='min',axis=1)/np.size(x, 1)

def ts_argmax(x, window=10):
    a_rolled = np.lib.stride_tricks.sliding_window_view(x, window,axis = 0)
    return np.append(np.full([window-1,np.size(x, 1)],np.nan),np.argmax(a_rolled, axis=-1) + 1,axis = 0)

def sma(x, window=10):
    a_rolled = np.lib.stride_tricks.sliding_window_view(x, window,axis = 0)
    return np.append(np.full([window-1,np.size(x, 1)],np.nan),np.mean(a_rolled, axis=-1),axis = 0)

def delta(x, period=1):
    return x - delay(x,period)

def delay(x, period=1):
    e = np.empty_like(x)
    e[:period] = np.nan
    e[period:] = x[:-period]
    return e

def sign(x):
    return np.sign(x)

def log(x):
    return np.log(x)

def ts_sum(x, window=10): 
    a_rolled = np.lib.stride_tricks.sliding_window_view(x, window,axis = 0)
    return np.append(np.full([window-1,np.size(x, 1)],np.nan),np.sum(a_rolled, axis=-1),axis = 0)

def ts_min(x, window=10):
    a_rolled = np.lib.stride_tricks.sliding_window_view(x, window,axis = 0)
    return np.append(np.full([window-1,np.size(x, 1)],np.nan),np.min(a_rolled, axis=-1),axis = 0)

def ts_max(x, window=10):
    a_rolled = np.lib.stride_tricks.sliding_window_view(x, window,axis = 0)
    return np.append(np.full([window-1,np.size(x, 1)],np.nan),np.max(a_rolled, axis=-1),axis = 0)


def scale(x):
    return np.divide(x.T,np.abs(x).sum(axis=1)).T


# partial WorldQuant 101 alpha definition.
def alpha001(data):
    inner = data['close'].copy()
    np.putmask(inner, returns(data['close']) < 0, stddev(returns(data['close']), 20))
    return rank(ts_argmax(inner ** 2, 5)) - 0.5

def alpha004(data):
    return -1 * ts_rank(rank(data['low']), 9)

def alpha005(data):
    return  (rank((data['open'] - (ts_sum(data['vwap'], 10) / 10))) * (-1 * abs(rank((data['close'] - data['vwap'])))))

def alpha007(data):
    adv20 = sma(data['volume'], 20)
    alpha = -1 * ts_rank(abs(delta(data['close'], 7)), 60) * sign(delta(data['close'], 7))
    alpha[adv20 >= data['volume']] = -1
    return alpha

def alpha008(data):
    return -1 * (rank(((ts_sum(data['open'], 5) * ts_sum(returns(data['close']), 5)) -
                        delay((ts_sum(data['open'], 5) * ts_sum(returns(data['close']), 5)), 10))))

def alpha009(data):
    delta_close= delta(data['close'], 1)
    cond_1 = ts_min(delta_close, 5) > 0
    cond_2 = ts_max(delta_close, 5) < 0
    alpha = -1 * delta_close
    np.putmask(alpha, cond_1 | cond_2, delta_close)
    return alpha  

def alpha017(data):
    adv20 = sma(data['volume'], 20)
    return -1 * (rank(ts_rank(data['close'], 10)) *
                    rank(delta(delta(data['close'], 1), 1)) *
                    rank(ts_rank((data['volume'] / adv20), 5)))

def alpha029(data):
    return (ts_min(rank(rank(scale(log(ts_sum(rank(rank(-1 * rank(delta((data['close'] - 1), 5)))), 2))))), 5) +
            ts_rank(delay((-1 * returns(data['close'])), 6), 5))

def alpha038(data):
    inner = data['close'] / data['open']
    return -1 * rank(ts_rank(data['open'], 10)) * rank(inner)

def alpha052(data):
    return (((-1 * delta(ts_min(data['low'], 5), 5)) *
                rank(((ts_sum(returns(data['close']), 240) - ts_sum(returns(data['close']), 20)) / 220))) * ts_rank(data['volume'], 5))

def alpha083(data):
    return ((rank(delay(((data['high'] - data['low']) / (ts_sum(data['close'], 5) / 5)), 2)) * rank(rank(data['volume']))) / (((data['high'] -data['low']) / (ts_sum(data['close'], 5) / 5)) / (data['vwap'] - data['close'])))



data = pd.read_csv('/YOUR_DIR/dataPerformance.csv')
df = data.pivot(index='tradetime', columns='securityid')

# here generates an array which is written in FORTRAN-contiguous order (column major)
data = { k: df[k].to_numpy() for k in df.columns }

times = []

funcNo = [1,4,5,7,8,9,17,29,38,52,83]

for i in funcNo:
    factor = "alpha{:03d}".format(i)
    try:
        t1 = time.time()
        res = eval(factor+"(data)")
        t2 = time.time()
        times.append(t2 - t1)
    except Exception:
        times.append('error')

timeRes = pd.DataFrame({"alphaName":funcNo,"timeCost":times})
timeRes.to_csv('/YOUR_DIR/npPerformance.txt',index=False)
