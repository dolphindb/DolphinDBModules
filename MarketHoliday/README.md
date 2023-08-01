# 交易日历 

交易日历是数据分析经常用到的工具，可以帮助快速获取对应交易所的交易日及进行相应的日期计算。DolphinDB 自 2.00.9/1.30.21 版本开始，提供交易日历功能，并内置世界五十多个交易所的交易日历。用户既可以直接使用内置的交易日历，也可以自定义交易日历，基于场景进行个性化定制。

本教程将会从交易日历的查询和应用、如何自定义交易日历、以及交易日历的来源等三个方面介绍如何使用 DolphinDB 的交易日历。


- [交易日历](#交易日历)
  - [1. 交易日历的查询和应用](#1-交易日历的查询和应用)
    - [1.1 查询交易日历-getMarketCalendar](#11-查询交易日历-getmarketcalendar)
    - [1.2 基于交易日历的日期偏移计算 - temporalAdd](#12-基于交易日历的日期偏移计算---temporaladd)
    - [1.3 基于交易日历取最近的交易日 - transFreq](#13-基于交易日历取最近的交易日---transfreq)
    - [1.4 基于交易日的数据采样 - asFreq/resample](#14-基于交易日的数据采样---asfreqresample)
  - [2. 自定义及更新内置交易日历](#2-自定义及更新内置交易日历)
    - [2.1 新增交易日历](#21-新增交易日历)
    - [2.2 替换交易日历](#22-替换交易日历)
  - [3. 交易日历出处](#3-交易日历出处)
    - [3.1 国际交易所 ISO CODE 列表](#31-国际交易所-iso-code-列表)
    - [3.2 中国大陆交易所简称列表](#32-中国大陆交易所简称列表)

## 1. 交易日历的查询和应用

DolphinDB 内置的交易日历可以支持多个场景的应用：
1. 搭配 `getMarketCalendar` 函数查询指定范围内的交易日；
2. 搭配 `temporalAdd` , `transFreq` , `asFreq` , `resample` 等内置函数，基于交易日进行计算。

### 1.1 查询交易日历-getMarketCalendar

可使用函数 [`getMarketCalendar(marketName, [startDate], [endDate])`](https://www.dolphindb.cn/cn/help/FunctionsandCommands/FunctionReferences/g/getMarketCalendar.html) 获取对应交易所在 startDate 和 endDate 确定的时间范围内的的交易日历。以纽交所（XNYS）为例，获取2022年1月1日至2022年1月10日间的交易日历的脚本如下：

```c++
getMarketCalendar("XNYS",2022.01.01, 2022.01.10)

#output
[2022.01.03,2022.01.04,2022.01.05,2022.01.06,2022.01.07,2022.01.10]
```

### 1.2 基于交易日历的日期偏移计算 - temporalAdd

如需对交易日历做时间偏移，可以使用 [`temporalAdd(date, duration, exchangeId)`](https://www.dolphindb.cn/cn/help/FunctionsandCommands/FunctionReferences/t/temporalAdd.html) 函数，获取给定时间的偏移的交易日。以纽交所（XNYS）为例，获取2023年1月1日至2023年1月6日增加2个交易日的日期的脚本如下：

```c++
dates=[2023.01.01, 2023.01.02, 2023.01.03, 2023.01.04, 2023.01.05, 2023.01.06]
temporalAdd(dates,2,"XNYS")

#output
[2023.01.04,2023.01.04,2023.01.05,2023.01.06,2023.01.09,2023.01.10]
```


### 1.3 基于交易日历取最近的交易日 - transFreq

[`getMarketCalendar`](https://www.dolphindb.cn/cn/help/FunctionsandCommands/FunctionReferences/g/getMarketCalendar.html) 函数可以获取相应时间范围内的交易日。但是如若某天不是交易日，又想获得该日期前最近的一个交易日，可以使用 [`transFreq(X,rule)`](https://www.dolphindb.cn/cn/help/FunctionsandCommands/FunctionReferences/t/transFreq.html?highlight=transfreq)函数。指定 `rule` 参数为对应交易所编码，可获取对应日期的最近的交易日。以纽交所 (XNYS) 为例，获取2023年1月1日至1月6日最近的交易日历的脚本如下：

```c++
dates=[2023.01.01, 2023.01.02, 2023.01.03, 2023.01.04, 2023.01.05, 2023.01.06]
dates.transFreq("XNYS")

#output
[2022.12.30,2022.12.30,2023.01.03,2023.01.04,2023.01.05,2023.01.06]
```

### 1.4 基于交易日的数据采样 - asFreq/resample

基于交易日的数据采样，可使用函数 [`asFreq(X,rule)`](https://www.dolphindb.cn/cn/help/FunctionsandCommands/FunctionReferences/a/asFreq.html?highlight=asfreq) 或者函数 [`resample(X,rule,func)`](https://www.dolphindb.cn/cn/help/FunctionsandCommands/FunctionReferences/r/resample.html?highlight=resample)，两者的区别在于是否对数据做聚合操作，resample 可以配合聚合函数使用，而 asFreq 函数是纯粹的取值。

函数 [`asFreq(X,rule)`] 会将数据按交易日（维度为天）展开，如果某一天的交易日数据有多个，只取第一个值。如若数据中没有交易日序列中的数据，会以 NULL 填充。以纽交所 (XNYS) 某支股票数据为例，获取2022年12月30日至2023年01月06日的交易日数据的脚本如下：

```c++
timestampv = [2022.12.30T23:00:00.000,2023.01.01T00:00:00.000,2023.01.03T00:10:00.000,2023.01.03T00:20:00.000,2023.01.04T00:20:00.000,2023.01.04T00:30:00.000,2023.01.06T00:40:00.000]
close = [100.10, 100.10, 100.10, 78.89, 88.99, 88.67, 78.78]
s=indexedSeries(timestampv, close)
s.asFreq("XNYS")

#output
           #0                 
           ------
2022.12.30|100.10
2023.01.03|100.10
2023.01.04|88.99 
2023.01.05|                   
2023.01.06|78.78
```


函数 [`resample(X,rule,func)`](https://www.dolphindb.cn/cn/help/FunctionsandCommands/FunctionReferences/r/resample.html?highlight=resample) 可以在采样的基础上，搭配聚合函数获取想要的交易日数据。以纽交所 (XNYS) 某支股票收盘价数据为例，查询每日收盘价的脚本如下：

```c++
timestampv = [2022.12.30T23:00:00.000,2023.01.01T00:00:00.000,2023.01.03T00:10:00.000,2023.01.03T00:20:00.000,2023.01.04T00:20:00.000,2023.01.04T00:30:00.000,2023.01.06T00:40:00.000]
close = [100.10, 100.10, 100.10, 78.89, 88.99, 88.67, 78.78]
s=indexedSeries(timestampv, close)
s.resample("XNYS", last)

#output
           #0                 
           ------
2022.12.30|100.10
2023.01.03|78.89
2023.01.04|88.67 
2023.01.05|                   
2023.01.06|78.78
```


## 2. 自定义及更新内置交易日历

DolphinDB 自 1.30.21/2.00.9 版本开始提供交易日历功能。内置的世界上五十多个交易所的节假日的 csv 文件存放于 `marketHolidayDir` 配置项对应的文件夹下（默认为 *marketHoliday* 文件夹），并以交易所的编码命名该文件，例如：“XNYS”（纽交所）。

DolphinDB 启动时会解析 *marketHolidayDir* 下所有的 csv 文件，启动后便可在 `resample`, `asfreq`, `transFreq`, `temporalAdd` 等函数内使用该交易所的编码。

DolphinDB 也支持管理员用户自定义交易日历，或者对现有交易日历修改和更新。管理员用户可通过 DolphinDB 内置函数更新交易日历：

- 使用 `addMarketHoliday` 新建交易日历
- 使用 `updateMarketHoliday` 更新交易日历

本章节余下部分将介绍如何通过上述两个函数自定义及更新内置交易日历。

### 2.1 新增交易日历

假设需要新增交易所 “DDB” 的交易日历，可以通过 [`addMarketHoliday(marketName, holiday)`](https://www.dolphindb.cn/cn/help/FunctionsandCommands/CommandsReferences/a/addMarketHoliday.html?highlight=addmarket) 函数，添加 “DDB” 的交易日历。`addMarketHoliday` 函数会在 */marketHoliday/* 目录下添加新的 *DDB.csv* 文件。

DolphinDB 在处理 holiday 文件时会自动过滤周末（周六、周日），因此在提交 holiday 文件时，不需要添加周末日期，只添加非周末的节假日信息即可。

新增交易日历后，可直接调用 `getMarketCalendar` 等函数对新的交易日历进行操作：

```c++
//将 2023.01.03 2023.01.04(周二, 周三) 设置为节假日
holiday = 2023.01.03 2023.01.04  
//用户登录
login(`admin,`123456)
//添加交易日历
addMarketHoliday("DDB",holiday)

//获取指定日期区间的交易日历
getMarketCalendar("DDB",2023.01.01, 2023.01.10)
#output
[2023.01.02,2023.01.05,2023.01.06,2023.01.09,2023.01.10]

temporalAdd(2023.01.01,2,"DDB")
#output
2023.01.05
```

> 新增的交易所与模块的适用范围一样，目前都是只对当前节点有效。如果需要对其他节点生效，在其他节点进行同样的操作即可。

### 2.2 替换交易日历

假设需要更新已建好的 “DDB” 交易所的交易日历，可以使用函数 [`updateMarketHoliday(marketName, holiday)`](https://www.dolphindb.cn/cn/help/FunctionsandCommands/CommandsReferences/u/updateMarketHoliday.html?highlight=updatemarketholiday) 重新设置该文件的节假日信息，进而更新该交易所的交易日历。

> **注意**：该函数设置的节假日信息将覆盖旧的交易日历文件，不可单独对该文件更新或新增节假日信息。

以下做法可以将已有的 “DDB” 交易所重新指定 2023.03.07、2023.03.08 为交易所节假日，且不保留之前的 holiday 日期。通过 `temporalAdd` 查询 2022.01.01 的下一个交易日的脚本如下：

```c++
//将 2023.03.07 2023.03.08(周二, 周三) 重新设置为节假日
updateMarketHoliday("DDB",2023.03.07 2023.03.08)

//2023.01.03 2023.01.04(周二, 周三) 不再是节假日
getMarketCalendar("DDB",2023.01.01, 2023.01.10)
#output
[2023.01.02,2023.01.03,2023.01.04,2023.01.05,2023.01.06,2023.01.09,2023.01.10]

//2023.03.07, 2023.03.08(周二, 周三) 作为节假日，不会出现在交易日历中
getMarketCalendar("DDB",2023.03.01, 2023.03.10)
#output
[2023.03.01,2023.03.02,2023.03.03,2023.03.06,2023.03.09,2023.03.10]
```


## 3. 交易日历出处

本章里列举了 *marketHoliday* 目录下的所有交易所的信息。为了方便国内用户使用，除了用交易所的 ISO Code 标识交易所名（[交易所 ISO CODE 列表](#31-交易所iso-code)）之外，增加了对国内六大交易所（上交所、深交所、中金所、上期所、郑商所、大商所、上能源）采用国内交易所简称作为标识名（[中国交易所简称列表](#32-中国交易所简称列表)）。


### 3.1 国际交易所 ISO CODE 列表

针对世界各国知名交易所（含上交所和深交所），统一采用 ISO Code 作为交易所的标识码。交易日历数据来源于各交易所官网公布的交易所节假日以及各地政府公布的法定节假日公告。

| 标识码<br>（ISO Code） | 交易所 | 国家 | 交易所节假日的公布网站 | 交易日历备注 | CSV 文件路径 | 开始年份 |
|:---:|---|---|---|---|---|---|
| AIXK | Astana International Exchange | Kazakhstan | https://aix.kz/trading/trading-calendar/ | 剔除 2022.12.01 | marketHoliday/AIXK.csv | 2017 |
| ASEX | Athens Stock Exchange | Greece | https://www.athexgroup.gr/market-alternative-holidays | 新增 2022.06.13、2022.05.02、2022.04.22、2022.03.07、2023.02.27、2023.04.17、2023.04.14、2023.06.05 | marketHoliday/ASEX.csv | 2004 |
| BVMF | BMF Bovespa | Brazil | https://www.b3.com.br/en_us/solutions/platforms/puma-trading-system/for-members-and-traders/trading-calendar/holidays/ | 剔除 2022.12.01 | marketHoliday/BVMF.csv | 2004 |
| CMES | Chicago Mercantile Exchange | USA | https://www.cmegroup.com/tools-information/holiday-calendar.html#cmeGlobex |  | marketHoliday/CMES.csv | 2004 |
| IEPA | ICE US | US | https://www.theice.com/holiday-hours?utm_source=website&utm_medium=search&utm_campaign=spotlight | 剔除 2023.04.07 | marketHoliday/IEPA.csv | 2004 |
| XAMS | Euronext Amsterdam | Netherlands | https://www.euronext.com/en/trade/trading-hours-holidays |  | marketHoliday/XAMS.csv | 2004 |
| XASX | Austrialian Securities Exchange | Australia | https://www2.asx.com.au/markets/market-resources/asx-24-trading-calendar |  | marketHoliday/XASX.csv | 2004 |
| XBKK | Stock Exchange of Thailand | Thailand | https://www.set.or.th/en/about/event-calendar/holiday?year=2023 | 剔除 2023.01.03、2022.01.03、2022.05.02、2022.12.12, 新增 2022.12.11、2022.10.14、2022.07.29、2022.07.13、2022.06.05、2022.05.05、2022.05.01、2022.02.16、2022.01.02、2023.03.06、2023.05.05、2023.08.01 | marketHoliday/XBKK.csv | 2004 |
| XBOG | Colombia Securities Exchange | Colombia | https://www.bvc.com.co/non-business-market-days | 剔除 2023.12.29 | marketHoliday/XBOG.csv | 2004 |
| XBOM | Bombay Stock Exchange | India | https://www.bseindia.com/static/markets/marketinfo/listholi.aspx | 新增 2023holidays | marketHoliday/XBOM.csv | 2004 |
| XBRU | Euronext Brussels | Belgium | https://www.euronext.com/en/trade/trading-hours-holidays#:~:text=Calendar%20of%20business%20days%202023%20%20%20Euronext:%20%20Closed%20%2012%20more%20rows%20 |  | marketHoliday/XBRU.csv | 2004 |
| XBSE | Bucharest Stock Exchange | Romania | https://www.bvb.ro/TradingAndStatistics/TradingSessionSchedule | 新增 2022.04.25、2022.04.22、2022.06.13、2023.04.17、2023.04.14、2023.06.05 | marketHoliday/XBSE.csv | 2004 |
| XBUD | Budapest Stock Exchange | Hungary | https://www.bse.hu/Products-and-Services/Trading-information/trading-calendar-2023 |  | marketHoliday/XBUD.csv | 2004 |
| XBUE | Buenos Aires Stock Exchange | Argentina |  | 新增 2022.12.09、2023.06.19、2023.05.26、2023.10.13、2023.11.08、2023.10.20 | marketHoliday/XBUE.csv | 2004 |
| XCBF | CBOE Futures | USA | https://www.cboe.com/about/hours/us-futures/ |  | marketHoliday/XCBF.csv | 2004 |
| XCSE | Copenhagen Stock Exchange | Denmark | https://www.nasdaqomxnordic.com/tradinghours/ |  | marketHoliday/XCSE.csv | 2004 |
| XDUB | Irish Stock Exchange | Ireland | https://www.euronext.com/en/trade/trading-hours-holidays |  | marketHoliday/XDUB.csv | 2004 |
| XETR | Xetra | Germany | https://www.xetra.com/xetra-en/newsroom/trading-calendar |  | marketHoliday/XETR.csv | 2004 |
| XFRA | Frankfurt Stock Exchange | Germany | https://www.boerse-frankfurt.de/en/know-how/trading-calendar |  | marketHoliday/XFRA.csv | 2004 |
| XHEL | Helsinki Stock Exchange | Finland | https://www.nasdaqomxnordic.com/tradinghours/XHEL |  | marketHoliday/XHEL.csv | 2004 |
| XHKG | Hong Kong Exchanges | Hong Kong, China | https://www.hkex.com.hk/News/HKEX-Calendar?sc_lang=zh-HK&defaultdate=2023-02-01 |  | marketHoliday/XHKG.csv | 2004 |
| XICE | Iceland Stock Exchange | Iceland | https://www.nasdaqomxnordic.com/tradinghours/ |  | marketHoliday/XICE.csv | 2004 |
| XIDX | Indonesia Stock Exchange | Indonesia | https://idx.co.id/en/about-idx/trading-holiday/ | 新增 2023.12.26、2023.09.28、2023.07.19、2023.06.29、2023.06.02、2023.04.26、2023.04.25、2023.04.24、2023.04.21、2023.03.23、2023.03.22、2023.01.23、2022.03.03、2022.02.28、2023.05.02、2023.05.03、2023.05.16 | marketHoliday/XIDX.csv | 2004 |
| XIST | Istanbul Stock Exchange | Turkey | https://borsaistanbul.com/en/sayfa/3631/official-holidays |  | marketHoliday/XIST.csv | 2004 |
| XJSE | Johannesburg Stock Exchange | South Africa | https://www.jse.co.za/ |  | marketHoliday/XJSE.csv | 2004 |
| XKAR | Pakistan Stock Exchange |  | https://www.psx.com.pk/psx/exchange/general/calendar-holidays | 新增 2023.04.21、2023.11.09、2022.12.26 | marketHoliday/XKAR.csv | 2004 |
| XKLS | Malaysia Stock Exchange | Malaysia | https://www.bursamalaysia.com/about_bursa/about_us/calendar | 剔除 2023.04.21、2023.06.28、2023.09.27, 新增 2022.02.06、2023.06.29、2023.09.28、2023.11.13 | marketHoliday/XKLS.csv | 2004 |
| XKRX | Korea Exchange | Republic of Korea | http://global.krx.co.kr/contents/GLB/05/0501/0501110000/GLB0501110000.jsp |  | marketHoliday/XKRX.csv | 2004 |
| XLIM | Lima Stock Exchange | Peru |  |  | marketHoliday/XLIM.csv | 2004 |
| XLIS | Euronext Lisbon | Portugal | https://www.euronext.com/en/trade/trading-hours-holidays |  | marketHoliday/XLIS.csv | 2004 |
| XLON | London Stock Exchange | England | https://www.londonstockexchange.com/securities-trading/trading-access/business-days | 新增 2023.05.08 | marketHoliday/XLON.csv | 2004 |
| XMAD | Euronext Lisbon | Portugal | https://www.euronext.com/en/trade/trading-hours-holidays |  | marketHoliday/XMAD.csv | 2004 |
| XMEX | Mexican Stock Exchange | Mexico | https://www.bmv.com.mx/en/bmv-group/holiday-schedule |  | marketHoliday/XMEX.csv | 2004 |
| XMIL | Borsa Italiana | Italy | https://www.borsaitaliana.it/borsaitaliana/calendario-e-orari-di-negoziazione/calendario-borsa-orari-di-negoziazione.en.htm |  | marketHoliday/XMIL.csv | 2004 |
| XMOS | Moscow Exchange | Russia | https://www.moex.com/en/tradingcalendar/ | 剔除 2023.01.09、2023.11.06、2022.01.03、2022.06.13 | marketHoliday/XMOS.csv | 2004 |
| XNYS | New York Stock Exchange | USA | https://www.nyse.com/markets/hours-calendars |  | marketHoliday/XNYS.csv | 2004 |
| XNZE | New Zealand Exchangen | New Zealand | https://www.nzx.com/services/nzx-trading/hours-boards |  | marketHoliday/XNZE.csv | 2004 |
| XOSL | Oslo Stock Exchange | Norway | https://www.euronext.com/en/trade/trading-hours-holidays |  | marketHoliday/XOSL.csv | 2004 |
| XPAR | Euronext Paris | France | https://www.euronext.com/en/trade/trading-hours-holidays |  | marketHoliday/XPAR.csv | 2004 |
| XPHS | Philippine Stock Exchange | Philippines | https://www.pse.com.ph/investing-at-pse/#investing2 | 新增 2022.12.08、2023.01.02、2023.04.10、2023.11.02、2023.11.27、2023.12.08 | marketHoliday/XPHS.csv | 2004 |
| XPRA | Prague Stock Exchange | Czech Republic | https://www.pse.cz/en/trading/trading-information/trading-calendar |  | marketHoliday/XPRA.csv | 2004 |
| XSES | Singapore Exchange | Singapore | https://www.mom.gov.sg/employment-practices/public-holidays | 新增 2023.12.25、2023.11.13、2023.08.09、2023.06.29、2023.06.02、2023.05.01、2023.04.07、2023.01.24、2023.01.23 | marketHoliday/XSES.csv | 2004 |
| XSGO | Santiago Stock Exchange | Chile | https://www.euronext.com/en/trade/trading-hours-holidays |  | marketHoliday/XSGO.csv | 2004 |
| XSHE | Shenzhen Stocak Exchange | China | http://www.szse.cn/disclosure/index.html | 新增2023.10.06、2023.06.23、2023.05.03、2023.05.02，剔除1991年数据（2023.05.06更新） | marketHoliday/XSHE.csv | 1992 |
| XSHG | Shanghai Stock Exchange | China | http://www.sse.com.cn/market/view/ |  | marketHoliday/XSHG.csv | 1991 |
| XSTO | Stockholm Stock Exchange | Sweden | https://www.nasdaqomxnordic.com/tradinghours/ |  | marketHoliday/XSTO.csv | 2004 |
| XSWX | SIX Swiss Exchange | Switzerland | https://www.six-group.com/en/products-services/the-swiss-stock-exchange/market-data/news-tools/trading-currency-holiday-calendar.html#/ |  | marketHoliday/XSWX.csv | 2004 |
| XTAI | Taiwan Stock Exchange Corp | Taiwan, China | https://www.twse.com.tw/en/holidaySchedule/holidaySchedule |  | marketHoliday/XTAI.csv | 2004 |
| XTKS | Tokyo Stock Exchange | Japan | https://www.jpx.co.jp/english/corporate/about-jpx/calendar/ | 新增 2023.03.21 | marketHoliday/XTKS.csv | 2004 |
| XTSE | Toronto Stock Exchange | Canada | https://www.tsx.com/trading/calendars-and-trading-hours/calendar |  | marketHoliday/XTSE.csv | 2004 |
| XWAR | Poland Stock Exchange | Poland |  |  | marketHoliday/XWAR.csv | 2004 |
| XWBO | Wiener Borse | Austria | https://www.wienerborse.at/en/trading/trading-information/trading-calendar/ | 剔除 2023.05.29 | marketHoliday/XWBO.csv | 2004 |

### 3.2 中国大陆交易所简称列表

为方便中国大陆用户使用，DolphinDB 也提供了中国大陆六大交易所（上交所、深交所、中金所、上期所、郑商所、大商所、上能源）的简称作为标识码。

| 标识码 <br>(ISO Code) | 交易所 | 国家 | 交易所节假日的公布网站 | 交易日历备注 | CSV 文件路径 | 开始年份 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| SSE | Shanghai Stock Exchange | China | http://www.sse.com.cn/market/view/ | 剔除2024.01.01（2023.05.06更新） | marketHoliday/SSE.csv | 1991 |
| SZSE | Shenzhen Stocak Exchange | China | http://www.szse.cn/disclosure/index.html | 剔除2024.01.01（2023.05.06更新） | marketHoliday/SZSE.csv | 1991 |
| CFFEX | China Finacial Futures Exchange | China | http://www.cffex.com.cn/jyrl/ | 剔除2006年数据（2023.05.06更新） | marketHoliday/CFFEX.csv | 2007 |
| SHFE | Shanghai Futures Exchange | China | https://www.shfe.com.cn/bourseService/businessdata/calendar/ |  | marketHoliday/SHFE.csv | 1992 |
| CZCE | Zhengzhou Commodity Exchange | China | http://www.czce.com.cn/cn/jysj/jyyl/H770313index_1.htm |  | marketHoliday/CZCE.csv | 1991 |
| DCE | Dalian Commodity Exchange | China | http://big5.dce.com.cn:1980/SuniT/www.dce.com.cn/DCE/TradingClearing/Exchange%20Notice/1516085/index.html | 新增2022.09.12（2023.05.06更新） | marketHoliday/DCE.csv | 1994 |
| INE | Shanghai International Energey Exchange | China | https://www.ine.cn/en/news/notice/6598.html |  | marketHoliday/INE.csv | 2017 |
