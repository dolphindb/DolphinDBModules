# Technical Analysis Indicator Library

[TA-Lib](https://github.com/mrjbq7/ta-lib) is a Python library implemented in C language that encapsulates numerous indicators commonly used in technical analysis of financial market data. To help users calculate these technical indicators in DolphinDB, TA-Lib functions are implemented with DolphinDB script in DolphinDB ta module (ta.dos).

The ta module requires DolphinDB Database Server 1.10.3 or above.

## 1. Naming conventions of functions and parameters

* In TA-Lib, all function names appear in uppercase and all parameters in lowercase. In comparison, in ta module, all function names and parameters use camelCase.

For example, the syntax of function DEMA in TA-Lib is ``DEMA(close, timeperiod = 30)``. The corresponding function in ta module is ``dema(close, timePeriod)``.

* Some TA-Lib functions have optional parameters. In ta module, all parameters are required.

* In order to produce meaningful results, the parameter 'timePeriod' of ta module functions is required to be at least 2.


## 2. Examples

### 2.1 Apply functions directly

Calculate a vector directly with the ta module function `wma`:

```
use ta
close = 7.2 6.97 7.08 6.74 6.49 5.9 6.26 5.9 5.35 5.63
x = wma(close, 5);
```

### 2.2 Apply functions in groups in SQL statements

In the following example, we first construct a table with data of 2 stocks, then conduct a calculation within each group:
```
close = 7.2 6.97 7.08 6.74 6.49 5.9 6.26 5.9 5.35 5.63 3.81 3.935 4.04 3.74 3.7 3.33 3.64 3.31 2.69 2.72
date = (2020.03.02 + 0..4 join 7..11).take(20)
symbol = take(`F,10) join take(`GPRO,10)
t = table(symbol, date, close)
```

Apply ta module function `wma` for each of these two stocks:
```
update t set wma = wma(close, 5) context by symbol
```

### 2.3 Results with multiple columns

Some ta module functions return results with multiple columns, such as function `bBands`.

Example 1:

```
close = 7.2 6.97 7.08 6.74 6.49 5.9 6.26 5.9 5.35 5.63
low, mid, high = bBands(close, 5, 2, 2, 2);
```

Example 2:
```
close = 7.2 6.97 7.08 6.74 6.49 5.9 6.26 5.9 5.35 5.63 3.81 3.935 4.04 3.74 3.7 3.33 3.64 3.31 2.69 2.72
date = (2020.03.02 + 0..4 join 7..11).take(20)
symbol = take(`F,10) join take(`GPRO,10)
t = table(symbol, date, close) 
select *, bBands(close, 5, 2, 2, 2) as `high`mid`low from t context by symbol;

symbol date       close high     mid      low
------ ---------- ----- -------- -------- --------
F      2020.03.02 7.2
F      2020.03.03 6.97
F      2020.03.04 7.08
F      2020.03.05 6.74
F      2020.03.06 6.49  7.292691 6.786    6.279309
F      2020.03.09 5.9   7.294248 6.454    5.613752
F      2020.03.10 6.26  7.134406 6.328667 5.522927
F      2020.03.11 5.9   6.789441 6.130667 5.471892
F      2020.03.12 5.35  6.601667 5.828    5.054333
F      2020.03.13 5.63  6.319728 5.711333 5.102939
GPRO   2020.03.02 3.81
GPRO   2020.03.03 3.935
GPRO   2020.03.04 4.04
GPRO   2020.03.05 3.74
GPRO   2020.03.06 3.7   4.069365 3.817333 3.565302
GPRO   2020.03.09 3.33  4.133371 3.645667 3.157962
GPRO   2020.03.10 3.64  4.062941 3.609333 3.155726
GPRO   2020.03.11 3.31  3.854172 3.482667 3.111162
GPRO   2020.03.12 2.69  3.915172 3.198    2.480828
GPRO   2020.03.13 2.72  3.738386 2.993333 2.24828
```

## 3. Performance comparison

Compared with the corresponding TA-Lib functions, ta module functions have similar performance on average when used directly but far superior performance when calculation is conducted in groups. In the examples of this section, we use function `wma`.

### 3.1 Apply functions directly

In DolphinDB:
```
use ta
close = 7.2 6.97 7.08 6.74 6.49 5.9 6.26 5.9 5.35 5.63
close = take(close, 1000000)
timer x = wma(close, 5);
```

The ta module function `wma` takes 3 milliseconds to calculate for a vector with 1,000,000 elements.

The corresponding Python script is as follows:

```python
close = np.array([7.2,6.97,7.08,6.74,6.49,5.9,6.26,5.9,5.35,5.63,5.01,5.01,4.5,4.47,4.33])
close = np.tile(close,100000)

import time
start_time = time.time()
x = talib.WMA(close, 5)
print("--- %s seconds ---" % (time.time() - start_time))
```

The TA-Lib function WMA takes 11 milliseconds, which is 3.7 times as long as ta module function `wma`.

### 3.2 Apply functions in groups in SQL statements

```
n=1000000
close = rand(1.0, n)
date = take(2017.01.01 + 1..1000, n)
symbol = take(1..1000, n).sort!()
t = table(symbol, date, close)
timer update t set wma = wma(close, 5) context by symbol;
```
The ta module function `wma` takes 17 milliseconds to calculate for all groups. 

The corresponding Python script is as follows:
```python
close = np.random.uniform(size=1000000)
symbol = np.sort(np.tile(np.arange(1,1001),1000))
date = np.tile(pd.date_range('2017-01-02', '2019-09-28'),1000)
df = pd.DataFrame(data={'symbol': symbol, 'date': date, 'close': close})

import time
start_time = time.time()
df["wma"] = df.groupby("symbol").apply(lambda df: talib.WMA(df.close, 5)).to_numpy()
print("--- %s seconds ---" % (time.time() - start_time))
```

The TA-Lib function WMA takes 535 milliseconds to calculate for all groups, which is 31.5 times as long as ta module function `wma`.


## 4. Vectorization

Similar to TA-Lib, all ta module functions are vectorized functions in that both the input and the output are vectors of equal length. The bottom layer of TA-Lib is implemented in C language, which is very efficient. Although the ta module is implemented in DolphinDB scripting language, it makes full use of the built-in vectorized functions and higher-order functions to avoid loops. As a result, it is extremely efficient.

The implementation ta module functions is also extremely concise. The file ta.dos has 765 lines of code in total. For each function, the core code is about 4 lines on average. Users can learn how to write DolphinDB script for efficient vector programming by checking out ta module function definitions.

### 4.1. Handling of null values

If the input vector of TA-Lib functions starts with null values, the calculation starts from the first non-null position. The ta module uses the same strategy. 

In both TA-Lib and ta module, for a rolling or cumulative window function with window length k, the first (k-1) elements of each group in the output vector are null values. If there is a null value after the first non-null element in a group, the result for this null position and all subsequent positions in the group may be null in TA-Lib. In comparison, the results are not null values for these positions in ta module unless the amount of non-null data in the window is not enough for calculation (e.g., when there is only one non-null value in a window to calculate the variance). 

DolphinDB script and result:
```
close = [99.9, NULL, 84.69, 31.38, 60.9, 83.3, 97.26, 98.67]
ta::var(close, 5, 1);

[,,,,670.417819,467.420569,539.753584,644.748976]
```

Python script and result:
```python
close = np.array([99.9, np.nan, 84.69, 31.38, 60.9, 83.3, 97.26, 98.67])
talib.VAR(close, 5, 1)

array([nan, nan, nan, nan, nan, nan, nan, nan])
```

As the first element of the vector 'close' is not null and the second element is null, the result is null on all positions. In short, only when all null values, if any, concentrate on the starting positions are the results of TA-Lib and ta module functions identical on all positions.

### 4.2 Iteration

Many TA-Lib functions use iterations where the current position value is a linear function of the previous position value and the current input: r[n] = coeff * r[n-1] + input[n]. For this type of calculation, DolphinDB introduces function `iterate` for vectorized iteration to avoid the use of loops.

```
def ema(close, timePeriod) {
1 	n = close.size()
2	b = ifirstNot(close)
3	start = b + timePeriod
4	if(b < 0 || start > n) return array(DOUBLE, n, n, NULL)
5	init = close.subarray(:start).avg()
6	coeff = 1 - 2.0/(timePeriod+1)
7	ret = iterate(init, coeff, close.subarray(start:)*(1 - coeff))
8	return array(DOUBLE, start - 1, n, NULL).append!(init).append!(ret)
}
```
The script above is the definition of ta module function `ema`. Line 5 calculates the mean of the first window as the initial value of the iterative sequence. Line 6 defines the iteration coefficient. Line 7 uses the highly-efficient DolphinDB built-in function `iterate` to calculate the ema sequence. To calculate the ema sequence with window length of 10 for a vector with 1,000,000 elements, TA-Lib takes 7.4 milliseconds while ta module takes only 5.0 milliseconds.

### 4.3 Moving window functions

DolphinDB offers various built-in moving window functions including `mcount`, `mavg`, `msum`, `mmax`, `mmin`, `mimax`, `mimin`, `mmed`, `mpercentile`, `mrank`, `mmad`, `mbeta`, `mcorr`, `mcovar`, `mstd` and `mvar`. These moving window functions have been fully optimized. The complexity of most of them is O(n) which means performance is independent of window length. 

Some TA-Lib functions can be implemented with DolphinDB moving window functions. For example, TA-Lib function VAR is population variance, whereas DolphinDB function `mvar` is sample variance. The ta module function `var` is implemented in the following script:
```
def var(close, timePeriod, nddev){
1	n = close.size()
2	b = close.ifirstNot()
3	if(b < 0 || b + timePeriod > n) return array(DOUBLE, n, n, NULL)
4	mobs =  mcount(close, timePeriod)
5	return (mvar(close, timePeriod) * (mobs - 1) \ mobs).fill!(timePeriod - 1 + 0:b, NULL)
}
```

### 4.4 Tips for reducing data replication

When conducting operations such as slicing, joining or appending on a vector, a large amount of data may be replicated. Data replication is usually more time consuming than many simple calculations. Here are some examples about how to reduce data replication.

#### 4.4.1 Use subarrays

When a subset of the elements of a vector are needed in calculation, if we use script such as `close[10:].avg()`, a new vector 'close[10:]' is generated with replicated data from the original vector 'close' before the calculation is conducted. This not only consumes more memory but also takes time. DolphinDB function `subarray` generates a subarray of the original vector. It only records the pointer to the original vector together with the starting and ending positions of the subarray. As the system does not allocate a large block of memory to store the subarray, data replication does not occur. All read-only operations on vectors can be applied directly to a subarray. The implementation of many ta module functions use subarrays. 

#### 4.4.2 Specify capacity for vectors

In DolphinDB, each vector is allocated with a memory capacity. When new data is appended to a vector, if the capacity is insufficient, a larger memory space is allocated to the vector. Data is copied to the new memory space and then the the old memory space is released. With a large vector, this operation may be time-consuming. If the largest possible length of a vector is known, then we can set it as the capacity of the vector in advance to avoid expanding capacity. We can set a vector's capacity in parameter 'capacity' of DolphinDB's built-in function `array` when we create the vector. For example, in the 8th line of the defintion of function `ema` (in section 4.3), we first create a vector with capacity n, and then append the result from the calculation to the vector.

## 5. DolphinDB ta module functions list

### Overlap Studies

**Function**|**Syntax**|**Description**
---|---|---
bBands|bBands(close, timePeriod, nbDevUp, nbDevDn, maType)|Bollinger Bands
dema|dema(close, timePeriod)|Double Exponential Moving Average
ema|ema(close, timePeriod)|Exponential Moving Average
kama|kama(close, timePeriod)|Kaufman Adaptive Moving Average
ma|ma(close, timePeriod, maType)|Moving average
mavp|mavp(inReal, periods, minPeriod, maxPeriod, maType)|Moving average with variable period
midPoint|midPoint(close, timePeriod)|MidPoint over period
midPrice|midPrice(low, high, timePeriod)|Midpoint Price over period
sma|sma(close, timePeriod)|Simple Moving Average
t3|t3(close, timePeriod, vfactor)|Triple Exponential Moving Average (T3)
tema|tema(close, timePeriod)|Triple Exponential Moving Average
trima|trima(close, timePeriod)|Triangular Moving Average
wma|wma(close, timePeriod)|Weighted Moving Average

### Momentum Indicators

**Function**|**Syntax**|**Description**
---|---|---
adx|adx(high, low, close, timePeriod)|Average Directional Movement Index
adxr|adxr(high, low, close, timePeriod)|Average Directional Movement Index Rating
apo|apo(close,fastPeriod,slowPeriod,maType)|Absolute Price Oscillator
aroon|aroon(high,low,timePeriod)|Aroon
aroonOsc|aroonOsc(high, low, timePeriod)|Aroon Oscillator
bop|bop(open, high, low, close)|Balance Of Power
cci|cci(high, low, close, timePeriod)|Commodity Channel Index
cmo|cmo(close, timePeriod)|Chande Momentum Oscillator
dx|dx(high, low, close, timePeriod)|Directional Movement Index
macd|macd(close, fastPeriod, slowPeriod, signalPeriod)|Moving Average Convergence/Divergence
macdExt|macdExt(close, fastPeriod, fastMaType, slowPeriod, slowMaType, signalPeriod, signalMaType)|MACD with controllable MA type
macdFix|macdFix(close, signalPeriod)|Moving Average Convergence/Divergence Fix 12/26
mfi|mfi(high, low, close, volume, timePeriod)|Money Flow Index
minus_di|minus_di(high, low, close, timePeriod)|Minus Directional Indicator
minus_dm|minus_dm(high, low, timePeriod)|Minus Directional Movement
mom|mom(close, timePeriod)|Momentum
plus_di|plus_di(high, low, close, timePeriod)|Plus Directional Indicator
plus_dm|plus_dm(high, low, timePeriod)|Plus Directional Movement
ppo|ppo(close, fastPeriod, slowPeriod, maType)|Percentage Price Oscillator
roc|roc(close, timePeriod)|Rate of change : ((price/prevPrice)-1)*100
rocp|rocp(close, timePeriod)|Rate of change Percentage: (price-prevPrice)/prevPrice
rocr|rocr(close, timePeriod)|Rate of change ratio: (price/prevPrice)
rocr100|rocr100(close, timeperiod)|Rate of change ratio 100 scale: (price/prevPrice)*100
rsi|rsi(close, timePeriod)|Relative Strength Index
stoch|stoch(high, low, close, fastkPeriod, slowkPeriod, slowkMatype, slowdPeriod, slowdMatype)|Stochastic
stochf|stochf(high, low, close, fastkPeriod, fastdPeriod, fastdMatype)|Stochastic Fast
stochRsi|stochRsi(real, timePeriod, fastkPeriod, fastdPeriod, fastdMatype)|Stochastic Relative Strength Index
trix|trix(close, timePeriod)|1-day Rate-Of-Change (ROC) of a Triple Smooth EMA
ultOsc|ultOsc(high, low, close, timePeriod1, timePeriod2, timePeriod3)|Ultimate Oscillator
willr|willr(high, low, close, timePeriod)|Williams' %R

### Volume Indicators

**Function**|**Syntax**|**Description**
---|---|---
ad|ad(high, low, close, volume)|Chaikin A/D Line
obv|obv(close, volume)|On Balance Volume

### Volatility Indicators

**Function**|**Syntax**|**Description**
---|---|---
atr|atr(high, low, close, timePeriod)|Average True Range
natr|natr(high, low, close, timePeriod)|Normalized Average True Range
trange|trange(high, low, close)|True Range

### Price Transform

**Function**|**Syntax**|**Description**
---|---|---
avgPrice|avgPrice(open, high, low, close)|Average Price
medPrice|medPrice(high, low)|Median Price
typPrice|typPrice(high, low, close)|Typical Price
wclPrice|wclPrice(high, low, close)|Weighted Close Price

### Statistic Functions

**Function**|**Syntax**|**Description**
---|---|---
beta|beta(high, low, timePeriod)|Beta
correl|correl(high, low, timePeriod)|Pearson's Correlation Coefficient (r)
linearreg|linearreg(close, timePeriod)|Linear Regression
linearreg_angle|linearreg_angle(close, timePeriod)|Linear Regression Angle
linearreg_intercept|linearreg_intercept(close, timePeriod)|Linear Regression Intercept
linearreg_slope|linearreg_slope(close, timePeriod)|Linear Regression Slope
stdDev|stdDev(close, timePeriod, nbdev)|Standard Deviation
tsf|tsf(close, timePeriod)|Time Series Forecast
var|var(close, timePeriod, nbdev)|Variance

### Other Functions

* For Math Transform and Math Operators functions in TA-Lib, you can use the corresponding DolphinDB built-in functions. For examples, functions SQRT, LN and SUM in TA-Lib correspond to DolphinDB functions `sqrt`,` log` and `msum`, respectively.
* The following TA-Lib functions have not been implemented in the ta module: all Pattern Recognition and Cycle Indicators functions, as well as HT_TRENDLINE (Hilbert Transform-Instantaneous Trendline), ADOSC (Chaikin A / D Oscillator), MAMA (MESA Adaptive Moving Average), SAR (Parabolic SAR) and SAREXT (Parabolic SAR-Extended).

## 6. Future work

* The TA-Lib functions that have not yet been implemented will be implemented in the next version.
* Unlike TA-Lib, DolphinDB's user-defined functions do not support optional arguments or keyword arguments. They will be implemented in DolphinDB Server 1.20.0.
* Now we must use "use ta" to load ta module before using ta module functions. DolphinDB Server will allow pre-loading of modules during system initialization in version 1.20. The functions defined in modules and DolphinDB built-in functions will have the same status, and modules will no longer need to be loaded.



