from MyTT import *
import pandas as pd
import time
import dolphindb as ddb

# DolphinDB load data
dataPath = "D:/jiahao/workwpace/dolphindb-mytt/autoTest/testData.csv"
s = ddb.session()
s.connect("localhost", 8848, "admin", "123456")
s.run(f'''
use mytt;
schema = table(`tradedate`symbol`high`low`open`close`vol`bs as `name, `DATE`SYMBOL`DOUBLE`DOUBLE`DOUBLE`DOUBLE`DOUBLE`BOOL as type);
data=loadText("{dataPath}" ,schema=schema);''')

# Python load data
data = pd.read_csv(dataPath)

pythonTestParam = {
    'RD': 'RD(np.array(x.close), D=3)', 'RET': 'RET(np.array(x.close), N=1)', 'ABS': 'ABS(np.array(x.close))',
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
    'ASI': 'ASI(np.array(x.open), np.array(x.close), np.array(x.high), np.array(x.low), M1=26, M2=10)'
}

ddbTestParam = {
    'RD': 'select mytt::RD(close, D=3) as `RD from data context by symbol',
    'RET': 'select RET from (select mytt::RET(close, N=1) as `RET from data group by symbol)',
    'ABS': 'select mytt::ABS(close) as `ABS from data context by symbol',
    'LN': 'select mytt::LN(close) as `LN from data context by symbol',
    'POW': 'select mytt::POW(close, N=2) as `POW from data context by symbol',
    'SQRT': 'select mytt::SQRT(close) as `SQRT from data context by symbol',
    'MAX': 'select mytt::MAX(close, open) as `MAX from data context by symbol',
    'MIN': 'select mytt::MIN(close, open) as `MIN from data context by symbol',
    'IF': 'select mytt::IF(bs, A=2, B=4) as `IF from data context by symbol',
    'REF': 'select mytt::REF(close, N=1) as `REF from data context by symbol',
    'DIFF': 'select mytt::DIFF(close, N=1) as `DIFF from data context by symbol',
    'STD': 'select mytt::STD(close, N=5) as `STD from data context by symbol',
    'SUM': 'select mytt::SUM(vol, N=5) as `SUM from data context by symbol',
    'CONST': 'select mytt::CONST(vol) as `CONST from data context by symbol',
    'HHV': 'select mytt::HHV(close, N=10) as `HHV from data context by symbol',
    'LLV': 'select mytt::LLV(close, N=10) as `LLV from data context by symbol',
    'HHVBARS': 'select mytt::HHVBARS(close, N=10) as `HHVBARS from data context by symbol',
    'LLVBARS': 'select mytt::LLVBARS(close, N=10) as `LLVBARS from data context by symbol',
    'MA': 'select mytt::MA(close, N=10) as `MA from data context by symbol',
    'EMA': 'select mytt::EMA(close, N=10) as `EMA from data context by symbol',
    'SMA': 'select mytt::SMA(close, N=10, M=1) as `SMA from data context by symbol',
    'WMA': 'select mytt::WMA(close, N=10) as `WMA from data context by symbol',
    'DMA': 'select mytt::DMA(close, A=0.5) as `DMA from data context by symbol',
    'AVEDEV': 'select mytt::AVEDEV(close, N=10) as `AVEDEV from data context by symbol',
    'SLOPE': 'select mytt::SLOPE(close, N=11) as `SLOPE from data context by symbol',
    'FORCAST': 'select mytt::FORCAST(close, N=12) as `FORCAST from data context by symbol',
    'LAST': 'select mytt::LAST_(bs, A=10, B=5) as `LAST from data context by symbol',
    'COUNT': 'select mytt::COUNT(bs, N=10) as `COUNT from data context by symbol',
    'EVERY': 'select mytt::EVERY(bs, N=10) as `EVERY from data context by symbol',
    'EXIST': 'select mytt::EXIST(bs, N=10) as `EXIST from data context by symbol',
    'BARSLAST': 'select mytt::BARSLAST(bs) as `BARSLAST from data context by symbol',
    'BARSLASTCOUNT': 'select mytt::BARSLASTCOUNT(bs) as `BARSLASTCOUNT from data context by symbol',
    'CROSS': 'select mytt::CROSS(MA(close,5),MA(close,10)) as `CROSS from data context by symbol',
    'LONGCROSS': 'select mytt::LONGCROSS(MA(close,5),MA(close,10), N=10) as `LONGCROSS from data context by symbol',
    'VALUEWHEN': 'select mytt::VALUEWHEN(bs, close) as `VALUEWHEN from data context by symbol',
    'BETWEEN': 'select mytt::BETWEEN(close, open, high) as `BETWEEN from data context by symbol',
    'MACD': 'select mytt::MACD(close, SHORT_=12, LONG_=26, M=9) as `DIF`DEA`MACD from data context by symbol',
    'KDJ': 'select mytt::KDJ(close, high, low, N=9, M1=3, M2=3) as `K`D`J from data context by symbol',
    'RSI': 'select mytt::RSI(close, N=24) as `RSI from data context by symbol',
    'WR': 'select mytt::WR(close, high, low, N=10, N1=6) as `WR`WR1 from data context by symbol',
    'BIAS': 'select mytt::BIAS(close, L1=6, L2=12, L3=24) as `BIAS1`BIAS2`BIAS3 from data context by symbol',
    'BOLL': 'select mytt::BOLL(close, N=20, P=2) as `UPPER`MID`LOWER from data context by symbol',
    'PSY': 'select mytt::PSY(close, N=12, M=6) as `PSY`PSYMA from data context by symbol',
    'CCI': 'select mytt::CCI(close, high, low, N=14) as `CCI from data context by symbol',
    'ATR': 'select mytt::ATR(close, high, low, N=20) as `ATR from data context by symbol',
    'BBI': 'select mytt::BBI(close, M1=3, M2=6, M3=12, M4=20) as `BBI from data context by symbol',
    'DMI': 'select mytt::DMI(close, high, low, M1=14, M2=6) as `PDI`MDI`ADX`ADXR from data context by symbol',
    'TAQ': 'select mytt::TAQ(high, low, N=10) as `UP`MID`DOWN from data context by symbol',
    'KTN': 'select mytt::KTN(close, high, low, N=20, M=10) as `UPPER`MID`LOWER from data context by symbol',
    'TRIX': 'select mytt::TRIX(close, M1=12, M2=20) as `TRIX`TRMA from data context by symbol',
    'VR': 'select mytt::VR(close, vol, M1=26) as `VR from data context by symbol',
    'EMV': 'select mytt::EMV(high, low, vol, N=14, M=9) as `EMV`MAEMV from data context by symbol',
    'DPO': 'select mytt::DPO(close, M1=20, M2=10, M3=6) as `DPO`MADPO from data context by symbol',
    'BRAR': 'select mytt::BRAR(open, close, high, low, M1=26) as `AR`BR from data context by symbol',
    'DFMA': 'select mytt::DFMA(close, N1=10, N2=50, M=10) as `DIF`DIFMA from data context by symbol',
    'MTM': 'select mytt::MTM(close, N=12, M=6) as `MTM`MTMMA from data context by symbol',
    'MASS': 'select mytt::MASS(high, low, N1=9, N2=25, M=6) as `MASS`MAMASS from data context by symbol',
    'ROC': 'select mytt::ROC(close, N=12, M=6) as `ROC`MAROC from data context by symbol',
    'EXPMA': 'select mytt::EXPMA(close, N1=12, N2=50) as `EXMPAN1`EXMPAN2 from data context by symbol',
    'OBV': 'select mytt::OBV(close, vol) as `OBV from data context by symbol',
    'MFI': 'select mytt::MFI(close, high, low, vol, N=14) as `MFI from data context by symbol',
    'ASI': 'select mytt::ASI(open, close, high, low, M1=26, M2=10) as `ASI`ASIT from data context by symbol'
}

# Return type： 1: return single column; 2: return 2 columns; 3: return a scala
functionType = {'RD': 1, 'ABS': 1, 'LN': 1, 'POW': 1, 'SQRT': 1, 'MAX': 1, 'MIN': 1, 'IF': 1, 'REF': 1, 'DIFF': 1,
                'STD': 1,
                'SUM': 1, 'CONST': 1, 'HHV': 1, 'LLV': 1, 'HHVBARS': 1, 'LLVBARS': 1, 'MA': 1, 'EMA': 1, 'SMA': 1,
                'WMA': 1,
                'DMA': 1, 'AVEDEV': 1, 'SLOPE': 1, 'FORCAST': 1, 'LAST': 1, 'COUNT': 1, 'EVERY': 1, 'EXIST': 1,
                'FILTER': 1,
                'BARSLAST': 1, 'BARSLASTCOUNT': 1, 'BARSSINCEN': 1, 'CROSS': 1, 'LONGCROSS': 1, 'VALUEWHEN': 1,
                'BETWEEN': 1,
                'TOPRANGE': 1, 'LOWRANGE': 1, 'RSI': 1, 'CCI': 1, 'ATR': 1, 'BBI': 1, 'VR': 1, 'OBV': 1, 'MFI': 1,
                'DSMA': 1,
                'SUMBARSFAST': 1, 'SAR': 1, 'TDX_SAR': 1, 'MACD': 2, 'KDJ': 2, 'WR': 2, 'BIAS': 2, 'BOLL': 2, 'PSY': 2,
                'DMI': 2,
                'TAQ': 2, 'KTN': 2, 'TRIX': 2, 'EMV': 2, 'DPO': 2, 'BRAR': 2, 'DFMA': 2, 'MTM': 2, 'MASS': 2, 'ROC': 2,
                'EXPMA': 2,
                'ASI': 2, 'XSII': 2, 'RET': 3}


def pythonResultTransformer(functionName, data):
    if functionType[functionName] == 1:
        return pd.DataFrame(np.concatenate(tuple([i for i in data])))
    if functionType[functionName] == 2:
        return pd.DataFrame(np.concatenate(tuple([np.array(i).T for i in data])))
    if functionType[functionName] == 3:
        return pd.DataFrame(data)


def autoTest(functionName, pythonStr, ddbStr):
    pythonResult = pythonResultTransformer(functionName, data.groupby('symbol').apply(lambda x: eval(pythonStr))).fillna(0).values
    where_are_inf = np.isinf(pythonResult)
    pythonResult[where_are_inf] = 0
    ddbResult = s.run(ddbStr).fillna(0).values
    # error = np.mean(np.abs((pythonResult).astype('float') - (ddbResult).astype('float'))/(np.abs((pythonResult).astype('float'))+1))
    error = np.sum(np.abs((pythonResult).astype('float') - (ddbResult).astype('float')))
    if error >= 1e-8 :
        print(f"The gap of {functionName} between Python and DolphinDB : {error}")


# test
for functionName in pythonTestParam.keys():
    autoTest(functionName, pythonTestParam[functionName], ddbTestParam[functionName])
