# Unified Stream and Batch Processing of WorldQuant 101 Alphas in DolphinDB <!-- omit in toc -->

In 2015, the formulas of 101 quantitative trading alphas used by WorldQuant were presented in the paper [*101 Formulaic Alphas*](https://arxiv.org/pdf/1601.00991.pdf). To conveniently calculate these 101 alphas in DolphinDB, you can use the functions encapsulated in the module **wq101alpha** ([wq101alpha.dos](src/wq101alpha.dos)).
  
This module has the following advantages over Python:

* Better Performance: DolphinDB outperforms Python by a median of 15.5x. For 27.5% of the alphas, DolphinDB is more than 100 times faster than Python. 
* Unified Stream and Batch Processing: Functions defined in this module can be used for both stream and batch processing.
* Simplicity: Most of the 101 alphas can be written with DolphinDB built-in functions. No need to develop new functions.

> All scripts in this tutorial are compatible with DolphinDB V2.00.8, 1.30.20 or higher.


- [1. Naming Conventions](#1-naming-conventions)
- [2. Examples](#2-examples)
  - [2.1 Environment Setup](#21-environment-setup)
  - [2.2 Data Preparation](#22-data-preparation)
  - [2.3 Calculating Alphas Without Industry Information](#23-calculating-alphas-without-industry-information)
  - [2.4 Calculating Alphas with Industry Information](#24-calculating-alphas-with-industry-information)
- [3. Performance Comparison](#3-performance-comparison)
  - [3.1 DolphinDB vs. Python Pandas](#31-dolphindb-vs-python-pandas)
  - [3.2 DolphinDB vs. NumPy](#32-dolphindb-vs-numpy)
- [4. Stream Processing](#4-stream-processing)
- [5. Conclusion](#5-conclusion)
- [Appendix: Required Parameters for Each Alpha](#appendix-required-parameters-for-each-alpha)


## 1. Naming Conventions

- All function names in module **wq101alpha** start with “WQAlpha” followed by a number from 1 to 101. For examples, WQAlpha1，WQAlpha2, etc.

- The following is a list of parameters for alphas defined in the `wq101alpha` module. Each alpha may use a different set of parameters (see [Appendix](#Appendix:-Required-Parameters-for-Each-Alpha)).


| Parameters              | Meaning                       | Contains industry information |
| ----------------------- | ----------------------------- | ----------------------------- |
| tradetime               | trading hours                 | ×                             |
| securityid              | security code                 | ×                             |
| open                    | open price                    | ×                             |
| close                   | close price                   | ×                             |
| high                    | high price                    | ×                             |
| low                     | low price                     | ×                             |
| vol                     | trading volume                | ×                             |
| vwap                    | volume-weighted average price | ×                             |
| cap                     | market capitalization         | √                             |
| indclass                | industry classification       | √                             |

- Two types of alphas are defined in the `wq101alpha` module: alphas with and without industry information.

| Alpha type                   | Input        | Output       | Alpha#                                                                  |
| ---------------------------- | ------------ | ------------ | ----------------------------------------------------------------------- |
| with industry information    | table        | table        | 48，56，58，59，63，67，69，70，76，79，80，82，87，89，90，91，93，97，100|
| without industry information | matrix       | matrix       | all other alphas                                                        |



## 2. Examples

This chapter expounds how to calculate alphas with specific examples.

### 2.1 Environment Setup

Add the module file [wq101alpha.dos](src/wq101alpha.dos) to [home]/modules.

The [home] directory is specified by the configuration parameter *home*. (To check the value of home, use `getHomeDir()`)

### 2.2 Data Preparation

You can simulate daily data with [DataSimulation](https://github.com/dolphindb/Tutorials_EN/blob/master/script/factorPractice/DataSimulation.txt) and industry information with [IndustryInfo](helper/infoDataScript.dos) 。

Alternatively, if you already have tables of daily data and industry information, you need to perform an equal join to combine these two tables, and make sure that the column names are consistent with the parameters defined in the module. 

If you need to change the column names, you can use function `prepareData` in module `prepare101` (add [prepare101.dos](helper/prepare101.dos) to [home]/modules). It converts the column names to the defined parameters. 

* rawData is a table containing non-industry information.
* infoData is a table containing industry information.
* startTime and endTime determine the start time and end time of data. 
* Other parameters are column names to be converted.

Import the `wq101alpha` module and load the data you prepared:

```c++
use wq101alpha
use prepare101
login('admin', '123456')
rawData = loadTable("dfs://k_day_level", "k_day")
infoData = select * from loadTable("dfs://info", "info_data")
startTime = timestamp(2010.01.01)
endTime = timestamp(2010.01.31)
data = prepareData(rawData=rawData, startTime=startTime, endTime=endTime, securityidName="securityid", tradetimeName="tradetime", openName="open", closeName="close", highName="high", lowName="low", volumeName="vol", vwapName="vwap", infoSecurityidName="securityid", capName="cap", indclassName="indclass", infoData=infoData)
```

### 2.3 Calculating Alphas Without Industry Information

In the wq101alpha module, the calculation of alphas without industry information is generally conducted on two dimensions: time-series and cross-section. For these factors, you need to prepare a matrix as the input, and then call function `WQAlpha#`. Check [Appendix](#Appendix:-Required-Parameters-for-Each-Alpha) for specific parameters.

For example, you can calculate alpha 1 and alpha 2 as follows:

```c++
use wq101alpha
input1 = exec close from data where tradetime between startTime : endTime pivot by tradetime, securityid
res1 = WQAlpha1(input1)

input2 = dict(`vol`close`open, panel(data.tradetime, data.securityid, [data.vol, data.close, data.open]))
res2 = WQAlpha2(input2.vol, input2.close, input2.open)
```

We provide function `prepare#` and `calAlpha#` in the [prepare101](helper/prepare101.dos) module to save your time spent on specifying parameters.

Function `prepare#` prepares the parameters required for each alpha and function calAlpha# encapsulates function `prepare#` and `wqAlpha#`.

Take alpha 1 as an example:

```c++
def prepare1(data, startTime, endTime){
    p = exec close from data where tradetime between startTime : endTime pivot by tradetime, securityid
    return p
}

def calAlpha1(data, startTime, endTime){
    input = prepare1(data, startTime, endTime)
    return WQAlpha1(input)
}
//call the module
use prepare101

res = calAlpha1(data, startTime, endTime)
```

> In addition to matrices, parameters of function WQAlpha41, WQAlpha54, and WQAlpha101 can also be vectors. For example, you can calculate alpha 101 using a SQL statement as follows:
>
> ```
> use wq101alpha 
> res = select tradetime, securityid, `alpha101 as factorname, WQAlpha101(close, open, high, low) as val from data where tradetime between startTime : endTime
> ```
>

### 2.4 Calculating Alphas with Industry Information

To calculate alphas with industry information, you need to specify a table as the input.

Take alpha 48 as an example:

```c++
use wq101alpha

res = WQAlpha48(data)
```

You can also use function `calAlpha#` in prepare101 module.

```c++
def calAlpha48(data, startTime, endTime){
    input = select * from data where tradetime between startTime : endTime
    return WQAlpha48(input)
}
//call the module
use prepare101

res = calAlpha48(data, startTime, endTime)
```

> The alpha calculation in the paper 101 Formulatic Alphas adopts several industry classifications, such as ``IndClass``, ``subindustry``, ``IndClass.industry``, ``IndClass.sector``. For the sake of convenience, only ``IndClass`` is used in this module.

Functions in the `wq101alpha` module return a matrix or a table. You can save your results to database if needed. Please refer to [wq101alphaStorage](helper/wq101alphaScript.dos).

## 3. Performance Comparison

Our testings show that the wq101alpha module of DolphinDB outperforms Python pandas and Numpy.

**Hardware**

CPU: Intel(R) Xeon(R) Silver 4216 CPU @ 2.10GHz
OS: 64-bit CentOS Linux 7 (Core)

**Data**

We use the simulated daily data in a year to conduct performance testing (see [TestData](test/dataPerformance.zip)).

### 3.1 DolphinDB vs. Python Pandas

We compare the performance of alpha calculation implemented by DolphinDB module `wq101alpha` and Python pandas

The following is the main script for performance testing of the `wq101alpha` module (see full script in [wq101alphaDDBTime](test/wq101alphaDDBTime.dos)):

```c++
times = array(INT, 0)
defs()
for (i in 1:102){
    if (i in passList) times.append!(NULL)
    else{
        print(i)
        alphaName = exec name from defs() where name = "wq101alpha::WQAlpha"+string(i)
        alphaSyntax = exec syntax from defs() where name = "wq101alpha::WQAlpha"+string(i)
        function = alphaName + alphaSyntax
        t1 = time(now())
        res = parseExpr(function[0]).eval()
        t2 = time(now())
        times.append!(t2 - t1)
    }
}
```

The following is the main script for performance testing of Python pandas (see full script in [wq101alphaPyTime](test/wq101alphaPyTime.py)):

```python
times = []

nofunc = [48, 56, 58, 59, 63, 67, 69, 70, 76, 79, 80, 82, 87, 89, 90, 91, 93, 97, 100]

for i in range(1, 102):
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

``` 



The execution time of all 101 alphas can be found in [PerformanceComparison](test/PerformanceCompare.csv). Alphas that have not yet been implemented in Python pandas or whose results are questionable are excluded. 69 alphas are available for comparison (in millisecond):

| Alpha#     | DolphinDB   | Pandas           | Pandas/DDB| Alpha#     | DolphinDB   | Pandas      | Pandas/DDB| 
| ---------- | ----------- | ---------------- | -------- | ----------- | ----------- | ----------- | ----------| 
| 1          | 86          | 68,837           | 800.43   |  38         | 91          | 89,487      | 983.38   |
| 2          | 229         | 2,117            | 9.24     |  40         | 73          | 2,379       | 32.59    |
| 3          | 140         | 2,018            | 14.41    |  41         | 84          | 11          | 0.13     |
| 4          | 75          | 89,440           | 1,192.53 |  42         | 97          | 218         | 2.25     | 
| 5          | 120         | 600              | 5.       |  43         | 91          | 165,954     | 1,823.67 | 
| 6          | 21          | 1,765            | 84.05    |  44         | 82          | 1,918       | 23.39    | 
| 7          | 148         | 72,001           | 486.49   |  45         | 170         | 4,853       | 28.55    | 
| 8          | 112         | 1,513            | 13.51    |  46         | 35          | 57          | 1.62     | 
| 9          | 50          | 714              | 14.27    |  47         | 252         | 1,156       | 4.59     | 
| 10         | 128         | 808              | 6.31     |  49         | 33          | 37          | 1.13     | 
| 11         | 145         | 898              | 6.2      |  50         | 235         | 2,475       | 10.53    | 
| 12         | 15          | 10               | 0.69     |  51         | 36          | 38          | 1.05     | 
| 13         | 213         | 1,784            | 8.38     |  52         | 131         | 91,360      | 697.4    | 
| 14         | 113         | 1,987            | 17.59    |  53         | 29          | 28          | 0.97     | 
| 15         | 147         | 2,572            | 17.49    |  54         | 175         | 178         | 1.02     | 
| 16         | 208         | 1,776            | 8.54     |  55         | 216         | 2,997       | 13.88    | 
| 17         | 177         | 174,055          | 983.36   |  60         | 154         | 72,081      | 468.06   | 
| 18         | 104         | 2,417            | 23.24    |  61         | 147         | 2,614       | 17.78    | 
| 19         | 72          | 440              | 6.11     |  62         | 354         | 3,204       | 9.05     | 
| 20         | 262         | 439              | 1.68     |  64         | 191         | 2,956       | 15.48    | 
| 21         | 78          | 2,296            | 29.43    |  65         | 181         | 2,968       | 16.4     | 
| 22         | 97          | 2,358            | 24.31    |  68         | 247         | 81,582      | 330.29   |
| 24         | 64          | 686              | 10.72    |  74         | 380         | 4,761       | 12.53    | 
| 25         | 96          | 500              | 5.21     |  75         | 279         | 4,461       | 15.99    |
| 26         | 61          | 182,340          | 2,989.18 |  78         | 384         | 5,204       | 13.55    |
| 27         | 226         | 2,573            | 11.38    |  81         | 519         | 61,954      | 119.37   | 
| 28         | 45          | 2,155            | 47.9     |  83         | 209         | 1,107       | 5.3      |
| 29         | 406         | 89,515           | 220.48   |  84         | 152         | 80,908      | 532.29   |
| 30         | 82          | 832              | 10.15    |  85         | 303         | 184,645     | 609.39   | 
| 32         | 53          | 2,146            | 40.5     |  86         | 123         | 75,681      | 615.3    | 
| 33         | 88          | 148              | 1.68     |  94         | 169         | 221,036     | 1,307.91 |
| 34         | 254         | 1,382            | 5.44     |  95         | 287         | 67,899      | 236.58   | 
| 35         | 131         | 249,748          | 1,906.47 |  99         | 203         | 4,758       | 23.44    |
| 36         | 388         | 92,303           | 237.89   |  101        | 9           | 20          | 2.2      |
| 37         | 148         | 1,953            | 13.2     |             |             |             |          |

The result shows that `wq101alpha` in DolphinDB outperforms python pandas. DolphinDB is faster than Python by a median of 15.5x. For 27.5% of the alphas, DolphinDB is more than 100 times faster than python. 

### 3.2 DolphinDB vs. NumPy

Considering NumPy may have better performance than pandas, we choose 11 alphas that are time-consuming in pandas and implement them with NumPy. See [partialAlphaNumpyTime](test/partialAlpha_npPerformance.py) for test results of NumPy.

Performance comparison of DolphinDB and NumPy:

| Alpha#  | DDB  | pandas  | NumPy  | pandas/DDB         | NumPy/DDB         |
| ------- | ---- | ------- | ------ | ------------------ | ----------------- |
| 1       | 86   | 68,837  | 418    | 800.4              | 4.9               |
| 4       | 75   | 89,440  | 54,417 | 1,192.5            | 725.6             |
| 5       | 120  | 600     | 218    | 5.0                | 1.8               |
| 7       | 148  | 72,001  | 39,472 | 486.5              | 266.7             |
| 8       | 112  | 1,513   | 265    | 13.5               | 2.4               |
| 9       | 50   | 714     | 152    | 14.3               | 3.0               |
| 17      | 177  | 174,055 | 93,704 | 983.4              | 529.4             |
| 29      | 406  | 89,515  | 47,100 | 220.5              | 116.0             |
| 38      | 91   | 89,487  | 46,257 | 983.4              | 508.3             |
| 52      | 131  | 91,360  | 46,715 | 697.4              | 356.6             |
| 83      | 209  | 1,107   | 464    | 5.3                | 2.2               |

We can see that while NumPy is faster than pandas, DolphinDB outperforms both. DolphinDB has optimized the implementation of its window functions. In comparison,  NumPy is not optimized for window calculations implemented by `numpy.lib.stride_tricks.sliding_window_view`. 

## 4. Stream Processing

It is complex to implement most alphas in real time, which requires more than one stream engine. DolphinDB provides the [`streamEngineParser`](https://www.dolphindb.cn/cn/help/200/FunctionsandCommands/FunctionReferences/s/streamEngineParser.html) function to automatically form a pipeline of stream engines to carry out the specified metrics calculation. In `streamEngineParser`, you can directly call functions in module `wq101alpha`. 

See full script in [wq101alphaStreamTest](helper/wq101alphaStreamTest.dos) for the implementation of real-time alpha calculations.

Take alpha 1 for example:

Define the schemata of input and output tables.

```c++
inputSchemaT = table(1:0, ["SecurityID","TradeTime","close"], [SYMBOL,TIMESTAMP,DOUBLE])
resultStream = table(10000:0, ["SecurityID","TradeTime", "factor"], [SYMBOL,TIMESTAMP, DOUBLE])
```

Call the `wq101alpha` module and use `WQAlpha1` as the *metrics* for the `streamEngineParser` function.

```c++
use wq101alpha
metrics = <[WQAlpha1(close)]>
streamEngine = streamEngineParser(name="WQAlpha1Parser", metrics=metrics, dummyTable=inputSchemaT, outputTable=resultStream, keyColumn="SecurityID", timeColumn=`tradetime, triggeringPattern='perBatch', triggeringInterval=4000)
```

Check the status of the stream engines with function [`getStreamEngineStat()`](https://www.dolphindb.cn/cn/help/200/FunctionsandCommands/FunctionReferences/g/getStreamEngineStat.html).

```c++
getStreamEngineStat()

#output
ReactiveStreamEngine->
name            user        status lastErrMsg numGroups ...
-------------   ----------- ------ ---------- --------- ...
WQAlpha1Parser0 admin OK                0         0       
WQAlpha1Parser2 admin OK                0         0       

CrossSectionalEngine->
name            user  status lastErrMsg numRows ...
--------------- ----- ------ ---------- ------- ...
WQAlpha1Parser1 admin OK                0       2          
```

Append data to stream engines and check the output table ``resultStream``.

```c++
streamEngine.append!(data)
//check the result
res = exec factor from resultStream pivot by TradeTime, SecurityID
```


## 5. Conclusion

This tutorial introduces how to calculate 101 alphas with DolphinDB built-in functions in the `wq101alpha` module. This module features efficiency, speed, and simplicity, and achieves unified batch and stream processing.

## Appendix: Required Parameters for Each Alpha

**Alphas without industry information**


| Alpha#                               | Parameters             | Alpha#                 | Parameters                 | Alpha#     | Parameters                  |
| ------------------------------------ | ---------------------- | ---------------------- | -------------------------- | ---------- | --------------------------- |
| 1, 9, 10, 19, 24, 29, 34, 46, 49, 51 | close                  | 23                     | high                       | 71         | vwap, vol, open, close, low |
| 2, 14                                | vol, open, close       | 25, 47, 74             | vwap, vol, close, high     | 72, 77     | vwap, vol, high, low        |
| 3, 6                                 | vol, open              | 27, 50, 61, 81         | vwap, vol                  | 73         | vwap, open, low             |
| 4                                    | low                    | 28, 35, 55, 60, 68, 85 | vol, high, low, close      | 75, 78     | vwap, vol, low              |
| 5                                    | vwap, open, close      | 31, 52                 | vol, close, low            | 83         | vwap, vol, close, high, low |
| 7, 12, 13, 17, 21, 30, 39, 43, 45    | vol, close             | 32, 42, 57, 84         | vwap, close                | 88, 92, 94 | vol, open, close, high, low |
| 8, 18, 33, 37, 38                    | open, close            | 36, 86                 | vwap, vol, open, close     | 95         | vol, open, high, low        |
| 11, 96                               | vwap, vol, close       | 41                     | vwap, high, low            | 65, 98     | vwap, vol, open             |
| 15, 16, 26, 40, 44                   | vol, high              | 53                     | close, high, low           | 99         | vol, high, low              |
| 20, 54, 101                          | open, close, high, low | 62, 64                 | vwap, vol, open, high, low |            |                             |
| 22                                   | vol, high, close       | 66                     | vwap, open, high, low      |            |                             |

**Alphas with industry information**

| Alpha#             | Parameters                       | Alpha#       | Parameters                      |
| ------------------ | -------------------------------- | ------------ | ------------------------------- |
| 48                 | close, indclass                  | 76, 89       | vwap, vol, low, indclass        |
| 56                 | close, cap                       | 80           | vol, open, high, indclass       |
| 58, 59             | vwap, vol, indclass              | 82           | vol, open, indclass             |
| 63, 79             | vwap, vol, open, close, indclass | 90           | vol, close, indclass            |
| 67                 | vwap, vol, high, indclass        | 97           | vwap, vol, low, indclass        |
| 69, 70, 87, 91, 93 | vwap, vol, close, indclass       | 100          | vol, close, high, low, indclass |

**See Also**

- [Module: wqalpha101 module](src/wq101alpha.dos)
- [101 Formulaic Alphas](https://arxiv.org/pdf/1601.00991.pdf)
<!----- [DolphinDB 教程：模块](https://gitee.com/dolphindb/Tutorials_CN/blob/master/module_tutorial.md)--->
- [DataSimulation](https://github.com/dolphindb/Tutorials_EN/blob/master/script/factorPractice/DataSimulation.txt)
- [IndustryInfo](helper/infoDataScript.dos) for industry information simulation
- [wq101alphaStorage](helper/wq101alphaScript.dos) for the storage of results of alpha calculations
- [prepare101.dos](helper/prepare101.dos) for the helper module
<!----- [因子最佳实践中的因子存储章节](https://gitee.com/dolphindb/Tutorials_CN/blob/master/best_practice_for_factor_calculation.md#5-%E5%9B%A0%E5%AD%90%E7%9A%84%E5%AD%98%E5%82%A8%E5%92%8C%E6%9F%A5%E8%AF%A2)--->
- [WorldQuant_alpha101_code](https://github.com/yli188/WorldQuant_alpha101_code) for the implementation of Python pandas
- [TestData](test/dataPerformance.zip) for daily data used in performance comparison
- [wq101alphaDDBTime](test/wq101alphaDDBTime.dos) for test results of wq101alpha module
- [wq101alphaPyTime](test/wq101alphaPyTime.py) for test results of Python pandas
- [PerformanceComparison](test/PerformanceCompare.csv)
- [partialAlphaNumpy](test/partialAlpha_npPerformance.py) for test results of NumPy
- [wq101alphaStreamTest](helper/wq101alphaStreamTest.dos) for the implementation of real-time alpha calculations



