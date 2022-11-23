# 国泰君安 191 Alpha 因子库 <!-- omit in toc -->

[国泰君安 191 Alpha 因子](src/gtja191Alpha.dos) 来源于国泰君安 2017 年 6 月份公布的研报《基于短周期价量特征的多因子选股体系——数量化专题之九十三》，属于短周期价量因子。为了使用户更方便地计算因子，本模块使用 DolphinDB 脚本实现了所有 191 个因子的函数，并封装在 DolphinDB 模块  **gtja191Alpha** ([gtja191Alpha.dos](src/gtja191Alpha.dos)) 中。

本文将为大家介绍该因子库的基本规范，并以其中几个因子为例，展示因子库在批计算、流计算中的应用。
  
> 本教程包含的所有代码兼容 DolphinDB 2.00.9，1.30.21 及以上版本。

本教程包含内容：

- [1. 函数命名规则与入参规范](#1-函数命名规则与入参规范)
- [2. 批计算使用范例](#2-批计算使用范例)
  - [2.1 环境准备](#21-环境准备)
  - [2.2 数据准备](#22-数据准备)
  - [2.3 使用范例](#23-使用范例)
  - [2.4 注意事项](#24-注意事项)
- [3. 实时流计算使用范例](#3-实时流计算使用范例)
- [4. 小结](#4-小结)
- [5. 附录](#5-附录)
  - [5.1 附录1-因子入参一览表](#51-附录1-因子入参一览表)
  - [5.2 附录2](#52-附录2)

## 1. 函数命名规则与入参规范

- gtja191Alpha 模块中的所有函数命名规则为 gtjaAlpha + 因子序号， 如 gtjaAlpha1 ，gtjaAlpha29 ，gtjaAlpha166 。

- 每一个因子的入参字段有所不同，具体参考 [附录1-因子入参一览表](#51-附录1-因子入参一览表) 。本教程涉及到的所有字段如下：

  | 参数名称 / 标准字段名称 | 参数含义           |
  | ----------------------- | ------------------ |
  | tradetime               | 交易时间           |
  | securityid              | 股票代码           |
  | open                    | 开盘价             |
  | close                   | 收盘价             |
  | high                    | 最高价             |
  | low                     | 最低价             |
  | vol                     | 交易量             |
  | vwap                    | 成交量加权平均价格 |
  | index_open              | 指数开盘价         |
  | index_close             | 指数收盘价         |

- gtja191Alpha 模块中的所有因子均为矩阵入参。



## 2. 批计算使用范例

本章节将从环境配置、数据准备、计算调用方法等方面具体介绍 gtja191Alpha.dos 模块的用法。

### 2.1 环境准备

把附件的 gtja191Alpha.dos 放在 [home]/modules 目录下，[home] 目录由系统配置参数 home 决定，可以通过 getHomeDir() 函数查看。

有关模块使用的更多细节，请参见：[DolphinDB 教程：模块](https://gitee.com/dolphindb/Tutorials_CN/blob/master/module_tutorial.md) 。


### 2.2 数据准备

本文提供了因子测试用的 [日频数据文件 (datatest.csv)](/gtja191Alpha/helper/datatest.zip) ，该数据包含了国泰君安 191 因子 [所需的字段](#1-函数命名规则与入参规范) 。如使用其他数据，请对照 [所需的字段](#1-函数命名规则与入参规范) 自行添加缺少字段。

对于数据，需要保证当前数据的表字段名与模块字段名一致。为方便使用，本教程准备了一个辅助模块 [gtja191Prepare.dos](helper/gtja191Prepare.dos) 来帮助统一字段名。调用前辅助模块前，需将该辅助模块放置在 gtja191Alpha 同级目录下。

辅助模块中有三类函数：
1. prepareData 函数，可将数据与标准字段的名称对齐。函数的参数中，rawData 为使用的数据源，startTime 与 endTime 为需要的数据的起始时间和结束时间，其余参数为现有字段名与标准字段的对应名称。
2. gtjaPrepare 函数，将表中字段提取成计算所需的矩阵并用字典存储。
3. gtjaCalAlpha# 函数，最终计算函数，会调用 gtjaPrepare 函数及 gtja191Alpha 模块中的计算函数。

辅助模块具体用法将在本节及 2.3 节中介绍。

一般来说，数据准备阶段，用户需调用辅助模块中的 prepareData 函数将数据与标准字段名称对齐。

> 如若用户采用的数据字段名与 [输入字段](#1-函数的命名与入参规范) 中的标准字段名一致，无需调用准备函数 prepareData 。

载入模块和数据方法如下，data 为准备好的数据：

```c++
use gtja191Alpha
use gtja191Prepare
login('admin', '123456')
rawData = loadText("/YOUR_DIR/datatest.csv")
startTime = timestamp(2010.01.01)
endTime = timestamp(2010.01.31)
data = prepareData(rawData=rawData, startTime=startTime, endTime=endTime, securityidName="securityid", tradetimeName="tradetime", openName="open", closeName="close", highName="high", lowName="low", volumeName="vol", vwapName="vwap", indexCloseName="index_close", indexOpenName="index_open")
```

### 2.3 使用范例

gtja191Alpha 模块中的所有因子均为矩阵入参，故用户需先准备矩阵，再调用对应的 gtjaAlpha# 函数，返回的结果亦为矩阵。由于不同因子计算时用到的参数不同，用户需通过查询 [附录1-因子入参一览表](#81-附录1-因子入参一览表) 来确定所需的参数。

以国泰君安 Alpha 第1号因子为例，计算方法如下：

```c++
use gtja191Alpha
open, close, vol = panel(data.tradetime, data.securityid, [data.open, data.close, data.vol])
res = gtjaAlpha1(open, close, vol)

//or you can use dictionary
input = dict(`open`close`vol, panel(data.tradetime, data.securityid, [data.open, data.close, data.vol]))
res = gtjaAlpha1(input.open, input.close, input.vol)
```

为了更加便于用户计算，省去查询参数这一步骤，因子计算 [辅助函数模块 gtja191Prepare.dos](helper/gtja191Prepare.dos) 提供了所需的矩阵准备函数 gtjaPrepare 和计算函数 gtjaCalAlpha#，用户可将其作为模块导入。

以 gtjaAlpha 第 1 号因子为例，辅助模块内的函数如下：

```c++
def gtjaPrepare(data, startTime, endTime){
    t = select securityid, tradetime, vol, low, high, close, open, vwap, index_close, index_open from data where tradetime between startTime : endTime
    return dict(`vol`low`high`close`open`vwap`index_close`index_open, panel(t.tradetime, t.securityid, [t.vol, t.low, t.high, t.close, t.open, t.vwap, t.index_close, t.index_open]))
}

def gtjaCalAlpha1(data, startTime, endTime){
    input = gtjaPrepare(data, startTime, endTime)
    return gtja191Alpha::gtjaAlpha1(input.open,input.close,input.vol)
}
//调用方法如下：
use gtja191Prepare

res = gtjaCalAlpha1(data, startTime, endTime)
```


### 2.4 注意事项

gtja191Alpha 模块中部分因子的原公式定义并不明确，gtja191Alpha 模块对这些做了一定的调整：

- 因子内做 RANK(A) 或 TSRANK(A, n) 计算时，默认用百分比的形式返回排名。
  
- 计算 SMA(A, n, m) 值时，取用数据A过去n天的加权平均值，其中平滑系数参数alpha=n/m。
  
- 原论文中定义 SUMAC(A, n) 为计算 A 的前 n 项的累加，实际计算时与计算 SUM(A, n) 无异。

## 3. 实时流计算使用范例

国泰君安 191 Alpha 因子中大多数因子的实现方式都较为复杂，在流计算中，需要创建多个引擎级联完成。DolphinDB 提供了一个解析引擎 [`streamEngineParser`](https://www.dolphindb.cn/cn/help/200/FunctionsandCommands/FunctionReferences/s/streamEngineParser.html) 来代替人工创建并串联多个引擎，大大提高效率。除此之外，gtja191Alpha 模块也实现了批流一体，即做流计算时无需修改计算代码，直接在流引擎 `streamEngineParser` 中调用即可。

`streamEngineParser` 解析本模块因子计算的大致逻辑如下，用户如自行写因子函数时可以做参考：
1. 涉及到 [row 系列函数](https://www.dolphindb.cn/cn/help/200/FunctionsandCommands/SeriesOfFunctions/rowFunctions.html) 的计算，会解析为横截面引擎([`CrossSectionalEngine`](https://www.dolphindb.cn/cn/help/200/FunctionsandCommands/FunctionReferences/c/createCrossSectionalEngine.html))。
2. 如若计算中用到了 [rolling](https://www.dolphindb.cn/cn/help/200/Functionalprogramming/TemplateFunctions/rolling.html) 函数，会解析为时间序列聚合引擎([`TimeSeriesEngine`](https://www.dolphindb.cn/cn/help/200/FunctionsandCommands/FunctionReferences/c/createTimeSeriesEngine))。
3. 其余计算会解析为响应式状态引擎([`ReactiveStreamEngine`](https://www.dolphindb.cn/cn/help/200/FunctionsandCommands/FunctionReferences/c/createReactiveStateEngine.html))。

本小节以国泰君安 Alpha 第 1 号因子为例，演示如何调用 gtja191Alpha 模块，实现流计算：

1. 首先定义输入输出的表结构：

```c++
inputSchema = table(1:0, ["SecurityID","TradeTime","open","close","vol"], [SYMBOL,TIMESTAMP,DOUBLE,DOUBLE,DOUBLE])
resultStream = table(10000:0, ["SecurityID","TradeTime","factor"], [SYMBOL,TIMESTAMP,DOUBLE])
```

2. 调用 gtja191Alpha 模块，并在 `streamEngineParser` 中使用 gtjaAlpha1 函数：

```c++
use gtja191Alpha
metrics = <[SecurityID,gtjaAlpha1(open,close,vol)]>
streamEngine = streamEngineParser(name="gtjaAlpha1Parser", metrics=metrics, dummyTable=inputSchema, outputTable=resultStream, keyColumn="SecurityID", timeColumn=`tradetime, triggeringPattern='keyCount', triggeringInterval=4000)
```

部分因子可能会创建多个引擎，可以调用 [`getStreamEngineStat()`](https://www.dolphindb.cn/cn/help/200/FunctionsandCommands/FunctionReferences/g/getStreamEngineStat.html) 查看总共串联了哪些引擎：

```c++
getStreamEngineStat()

#output
ReactiveStreamEngine->
name          user  status lastErrMsg numGroups numRows numMetrics memoryInUsed snapshotDir ...
------------- ----------- ------ ---------- --------- ------- ---------- ------------ ----------- 
gtjaAlpha1P...guest OK                4000      84000   5          800928                   ...
gtjaAlpha1P...guest OK                4000      84000   2          1264872                  ...

CrossSectionalEngine->
name         user  status lastErrMsg   numRows numMetrics metrics      triggering...triggering......
------------ -------- ------ ------------ ---------- ---------- ------------ ------------------ --------------- ---
gtjaAlpha1...guest OK                  4000    3          SecurityID...keyCount     4000         ...      
```

3. 将数据注入引擎，即可在 resultStream 输出表中查看结果：

```c++
streamEngine.append!((select SecurityID, TradeTime, close, high, low from data order by TradeTime))
//check the result
res = exec factor from resultStream pivot by TradeTime, SecurityID
```

> 完整 国泰君安 191 Alpha 流计算流程代码可查看 [国泰君安191Alpha流计算完整过程](helper/gtja191StreamTest.dos) 。

## 4. 小结

本文介绍了 `gtja191Alpha` 模块的用法。该模块用 DolphinDB 内置函数实现了 国泰君安 191 Alpha 因子，具有简单便捷、批流一体的特点。

## 5. 附录

### 5.1 附录1-因子入参一览表

| 因子序号 | 所需参数 | 因子序号| 所需参数 | 因子序号 | 所需参数 |
| :------------------------------------: | :-------------------------------------: | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :-------------------------------------: | :-------------------------------------: | :-------------------------------------- |
| 15, 37,  54, 184, 185                  | open, close                             | 119                                                                                                                                                                                                                                | open,vol,vwap                           | 9, 68, 123                              | high,low,vol                            |
| 55, 107, 137, 171                      | open,close,high,low                     | 10,  14, 18, 19, 20, 21, 22, 23, 24, 27, 31, 34, 46, 53, 58, 63, 65, 66, 67, 71,  79, 86, 88, 89, 98, 106, 112, 116, 122, 127, 129, 135, 143, 146, 147, 151,  152, 153, 157, 160, 162, 165, 166, 167, 169, 173, 174, 183, 189, 190 | close                                   | 77,  130                                | high,low,vol,vwap                       |
| 140                                    | open,close,high,low,vol                 | 2,  3, 28, 47, 57, 59, 72, 78, 82, 96, 110, 126, 158, 159, 161, 164, 172, 175,  186                                                                                                                                                | close,high,low                          | 8,  13                                  | high,low,vwap                           |
| 1, 136                                 | open,close,vol                          | 11,  52, 60, 111, 115, 117, 128, 150, 176, 191                                                                                                                                                                                     | close,high,low,vol                      | 5,  32, 42, 62, 83, 141                 | high,vol                                |
| 39, 45                                 | open,close,vol,vwap                     | 114                                                                                                                                                                                                                                | close,high,low,vol,vwap                 | 108                                     | high,vol,vwap                           |
| 12                                     | open,close,vwap                         | 104                                                                                                                                                                                                                                | close,high,vol                          | 103                                     | low                                     |
| 6, 187                                 | open,high                               | 101,  163, 170                                                                                                                                                                                                                     | close,high,vol,vwap                     | 44,  61, 74, 138, 179                   | low,vol,vwap                            |
| 118                                    | open,high,low                           | 33,  91                                                                                                                                                                                                                            | close,low,vol                           | 80,  81, 97, 100, 102, 145, 155, 168    | vol                                     |
| 56, 69                                 | open,high,low,vol                       | 4,  25, 29, 40, 43, 48, 76, 84, 85, 94, 99, 113, 134, 142, 178, 180                                                                                                                                                                | close,vol                               | 16,  36, 70, 90, 95, 121, 132, 154      | vol,vwap                                |
| 87                                     | open,high,low,vwap                      | 7,  64, 73, 92, 125, 131, 144                                                                                                                                                                                                      | close,vol,vwap                          | 41                                      | vwap                                    |
| 93                                     | open,low                                | 17,  26, 120, 124                                                                                                                                                                                                                  | close,vwap                              | 30, 149, 181                            | close,index_close                       |
| 156                                    | open,low,vwap                           | 38,  177                                                                                                                                                                                                                           | high                                    | 75,  182                                | close,open,index_close,index_open       |
| 35, 105, 139, 148 &emsp;&emsp;&emsp;   | open,vol                                | 49,  50, 51, 109, 133, 188                                                                                                                                                                                                         | high,low                                |                                         |                                         |



### 5.2 附录2

- [国泰君安 191 Alpha 因子模块](src/gtja191Alpha.dos)
- [日频数据文件](/gtja191Alpha/helper/datatest.zip)
- [国泰君安191 Alpha 辅助模块](helper/gtja191Prepare.dos)
- [国泰君安191Alpha流计算完整过程](helper/gtja191StreamTest.dos)
