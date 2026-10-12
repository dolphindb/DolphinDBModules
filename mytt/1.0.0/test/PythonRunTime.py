from MyTT import *
import pandas as pd
import time

test_PATH = './'
data = pd.read_csv(test_PATH + "/testData.csv")

def functionRunTime(name, param):
    t1 = time.time()
    # 核心计算逻辑
    data.groupby("symbol").apply(lambda x: eval(param))
    t2 = time.time()
    print(name, str(np.around((t2 - t1) * 1000, 3)) + "ms")
    return (t2 - t1) * 1000

testParam = {'RD': 'RD(np.array(x.close), D=3)', 'RET': 'RET(np.array(x.close), N=1)', 'ABS': 'ABS(np.array(x.close))',
              'LN': 'LN(np.array(x.close))', 'POW': 'POW(np.array(x.close), N=2)', 'SQRT': 'SQRT(np.array(x.close))',
              'MAX': 'MAX(np.array(x.close), np.array(x.open))', 'MIN': 'MIN(np.array(x.close), np.array(x.open))',
              'IF': 'IF(np.array(x.bs), A=2, B=4)', 'REF': 'REF(np.array(x.close), N=1)',
              'DIFF': 'DIFF(np.array(x.close), N=1)', 'STD': 'STD(np.array(x.close), N=5)',
              'SUM': 'SUM(np.array(x.vol), N=5)', 'CONST': 'CONST(np.array(x.vol))',
              'HHV': 'HHV(np.array(x.close), N=10)', 'LLV': 'LLV(np.array(x.close), N=10)',
              'HHVBARS': 'HHVBARS(np.array(x.close), N=10)', 'LLVBARS': 'LLVBARS(np.array(x.close), N=10)',
              'MA': 'MA(np.array(x.close), N=10)', 'EMA': 'EMA(np.array(x.close), N=10)',
              'SMA': 'SMA(np.array(x.close), N=10, M=1)', 'WMA': 'WMA(np.array(x.close), N=10)',
              'DMA': 'DMA(np.array(x.close), A=0.5)', 'AVEDEV': 'AVEDEV(np.array(x.close), N=10)',
              'SLOPE': 'SLOPE(np.array(x.close), N=11)', 'FORCAST': 'FORCAST(np.array(x.close), N=12)',
              'LAST': 'LAST(np.array(x.bs), A=10, B=5)', 'COUNT': 'COUNT(np.array(x.bs), N=10)',
              'EVERY': 'EVERY(np.array(x.bs), N=10)', 'EXIST': 'EXIST(np.array(x.bs), N=10)',
              'BARSLAST': 'BARSLAST(np.array(x.bs))', 'BARSLASTCOUNT': 'BARSLASTCOUNT(np.array(x.bs))',
              'CROSS': 'CROSS(MA(np.array(x.close),5),MA(np.array(x.close),10))',
              'LONGCROSS': 'LONGCROSS(MA(np.array(x.close),5),MA(np.array(x.close),10), N=10)',
              'VALUEWHEN': 'VALUEWHEN(np.array(x.bs), np.array(x.close))',
              'BETWEEN': 'BETWEEN(np.array(x.close), np.array(x.open), np.array(x.high))',
              'MACD': 'MACD(np.array(x.close), SHORT=12, LONG=26, M=9)',
              'KDJ': 'KDJ(np.array(x.close), np.array(x.high), np.array(x.low), N=9, M1=3, M2=3)',
              'RSI': 'RSI(np.array(x.close), N=24)',
              'WR': 'WR(np.array(x.close), np.array(x.high), np.array(x.low), N=10, N1=6)',
              'BIAS': 'BIAS(np.array(x.close), L1=6, L2=12, L3=24)', 'BOLL': 'BOLL(np.array(x.close), N=20, P=2)',
              'PSY': 'PSY(np.array(x.close), N=12, M=6)',
              'CCI': 'CCI(np.array(x.close), np.array(x.high), np.array(x.low), N=14)',
              'ATR': 'ATR(np.array(x.close), np.array(x.high), np.array(x.low), N=20)',
              'BBI': 'BBI(np.array(x.close), M1=3, M2=6, M3=12, M4=20)',
              'DMI': 'DMI(np.array(x.close), np.array(x.high), np.array(x.low), M1=14, M2=6)',
              'TAQ': 'TAQ(np.array(x.high), np.array(x.low), N=10)',
              'KTN': 'KTN(np.array(x.close), np.array(x.high), np.array(x.low), N=20, M=10)',
              'TRIX': 'TRIX(np.array(x.close), M1=12, M2=20)', 'VR': 'VR(np.array(x.close), np.array(x.vol), M1=26)',
              'EMV': 'EMV(np.array(x.high), np.array(x.low), np.array(x.vol), N=14, M=9)',
              'DPO': 'DPO(np.array(x.close), M1=20, M2=10, M3=6)',
              'BRAR': 'BRAR(np.array(x.open), np.array(x.close), np.array(x.high), np.array(x.low), M1=26)',
              'DFMA': 'DFMA(np.array(x.close), N1=10, N2=50, M=10)', 'MTM': 'MTM(np.array(x.close), N=12, M=6)',
              'MASS': 'MASS(np.array(x.high), np.array(x.low), N1=9, N2=25, M=6)',
              'ROC': 'ROC(np.array(x.close), N=12, M=6)', 'EXPMA': 'EXPMA(np.array(x.close), N1=12, N2=50)',
              'OBV': 'OBV(np.array(x.close), np.array(x.vol))',
              'MFI': 'MFI(np.array(x.close), np.array(x.high), np.array(x.low), np.array(x.vol), N=14)',
              'ASI': 'ASI(np.array(x.open), np.array(x.close), np.array(x.high), np.array(x.low), M1=26, M2=10)'}

runTime = {'functionName': [], 'runTime': []}
for name in testParam:
    runTime['functionName'].append(name)
    runTime['runTime'].append(functionRunTime(name, testParam[name]))

pd.DataFrame(runTime).to_csv("Python_RunTime.csv",index=False)
