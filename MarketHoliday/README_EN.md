# Trading Calendar 

Trading calendar is a frequently used tool for data analysis, which helps to quickly obtain exchange calendars and perform calculations based on trading calendars. Starting from version 2.00.9/1.30.21, DolphinDB provides built-in trading calendars of more than fifty exchanges.

This tutorial describes how to use and customize trading calendars in DolphinDB. Specifically: check trading days; perform calculations based on trading calendars; create your own trading calendars; update trading calendars.

- [Trading Calendar](#trading-calendar)
  - [1. Use Trading Calendars](#1-use-trading-calendars)
    - [1.1 Check Trading Days](#11-check-trading-days)
    - [1.2 Create the DateOffset of Trading Days](#12-create-the-dateoffset-of-trading-days)
    - [1.3 Obtain the Closest Trading Day](#13-obtain-the-closest-trading-day)
    - [1.4 Data Sampling Based on Trading Days](#14-data-sampling-based-on-trading-days)
  - [2. Customize Trading Calendars](#2-customize-trading-calendars)
    - [2.1 Add a New Trading Calendar](#21-add-a-new-trading-calendar)
    - [2.2 Update the Trading Calendar](#22-update-the-trading-calendar)
  - [3. Calendar Support](#3-calendar-support)

## 1. Use Trading Calendars

The built-in trading calendars can be used for various scenarios.

### 1.1 Check Trading Days

You can use function [`getMarketCalendar(marketName, [startDate], [endDate])`](https://www.dolphindb.com/help200/FunctionsandCommands/FunctionReferences/g/getMarketCalendar.html) to get trading days of the corresponding exchange in the date range determined by *startDate* and *endDate*.

To check the trading days of New York Stock Exchange (XNYS) between 2022.1.1 and 2022.1.10:

```c++
getMarketCalendar("XNYS",2022.01.01, 2022.01.10)

#output
[2022.01.03,2022.01.04,2022.01.05,2022.01.06,2022.01.07,2022.01.10]
```

### 1.2 Create the DateOffset of Trading Days

To shift a trading day forward or backward, you can use function [`temporalAdd(date, duration, exchangeId)`](https://www.dolphindb.com/help200/FunctionsandCommands/FunctionReferences/t/temporalAdd.html).

Take XNYS for example, we add two trading days to the dates between 2023.1.1 and 2023.1.6:

```c++
dates=[2023.01.01, 2023.01.02, 2023.01.03, 2023.01.04, 2023.01.05, 2023.01.06]
temporalAdd(dates,2,"XNYS")

#output
[2023.01.04,2023.01.04,2023.01.05,2023.01.06,2023.01.09,2023.01.10]
```


### 1.3 Obtain the Closest Trading Day

You can get the closest trading day of a certain day with function [`transFreq(X,rule)`](https://www.dolphindb.com/help200/FunctionsandCommands/FunctionReferences/t/transFreq.html).

For example, specify parameter *rule* as XNYS. We can get the closest trading days of each date between 2023.1.1 and 2023.1.6:

```c++
dates=[2023.01.01, 2023.01.02, 2023.01.03, 2023.01.04, 2023.01.05, 2023.01.06]
dates.transFreq("XNYS")

#output
[2022.12.30,2022.12.30,2023.01.03,2023.01.04,2023.01.05,2023.01.06]
```

### 1.4 Data Sampling Based on Trading Days

You can choose functions [`asFreq(X,rule)`](https://www.dolphindb.com/help200/FunctionsandCommands/FunctionReferences/a/asFreq.html) or [`resample(X,rule,func)`](https://www.dolphindb.com/help200/FunctionsandCommands/FunctionReferences/r/resample.html) to sample data on trading days. The only difference of the two lies in whether data can be aggregated.

Function `asFreq(X,rule)` will return the result by trading days. If there are multiple records in the same trading day, only the first value will be taken. If there is no data in a trading day, it will be filled with NULL.

The following example obtains the stock prices of XNYS in trading days from 2022.12.30 to 2023.1.6:

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


Function `resample(X,rule,func)` will return the aggregated result of data sampled by trading days. 

In the following example, we obtain the closing prices of XNYS stocks in trading days from 2022.12.30 to 2023.1.6:

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


## 2. Customize Trading Calendars

DolphinDB also allows administrators to customize trading calendars with built-in functions.

### 2.1 Add a New Trading Calendar

Suppose there is an exchange named “DDB“, function [`addMarketHoliday(marketName, holiday)`](https://www.dolphindb.com/help200/FunctionsandCommands/CommandsReferences/a/addMarketHoliday.html) can be used to add a new DDB calendar. A *DDB.csv* file will be added to the */marketHoliday/* directory. Weekends are recognized as holidays in DolphinDB by default, therefore, only weekday holidays need to be filled in the file.

Once a new trading calendar has been generated, functions such as getMarketCalendar can be used directly based on the new calendar:

```c++
//set 2023.01.03 (Tue.) and 2023.01.04 (Wed.) as holidays
holiday = 2023.01.03 2023.01.04  
//user login
login(`admin,`123456)
//generate a trading calendar
addMarketHoliday("DDB",holiday)

//get the trading days of the new calendar in a date range
getMarketCalendar("DDB",2023.01.01, 2023.01.10)
#output
[2023.01.02,2023.01.05,2023.01.06,2023.01.09,2023.01.10]

temporalAdd(2023.01.01,2,"DDB")
#output
2023.01.05
```

> The newly added trading calendar is only valid on the current node. Execute function `addMarketHoliday` on other nodes for it to take effect on those nodes. 

### 2.2 Update the Trading Calendar

If you want to update the existing calendar of DDB exchange, function [`updateMarketHoliday(marketName, holiday)`](https://www.dolphindb.com/help200/FunctionsandCommands/CommandsReferences/u/updateMarketHoliday.html) can be used to reset the holidays.

> **Note**: The file will be overwritten. The original holidays will be replaced with the holidays specified by this function. 

The following example resets the dates 2023.03.07 and 2023.03.08 as holidays for the DDB calendar. Check the next trading day after 2022.01.01 with function `temporalAdd`:

```c++
//set 2023.03.07 (Tue.) and 2023.03.08 (Wed.) as holiday
updateMarketHoliday("DDB",2023.03.07 2023.03.08)

//the original holidays 2023.01.03 and 2023.01.04 are no longer holidays
getMarketCalendar("DDB",2023.01.01, 2023.01.10)
#output
[2023.01.02,2023.01.03,2023.01.04,2023.01.05,2023.01.06,2023.01.09,2023.01.10]

//As holidays, 2023.03.07 and 2023.03.08 are not included in the trading calendar
getMarketCalendar("DDB",2023.03.01, 2023.03.10)
#output
[2023.03.01,2023.03.02,2023.03.03,2023.03.06,2023.03.09,2023.03.10]
```


## 3. Calendar Support

All exchange calendars supported are listed below. 

Note that calendars are updated according to the holidays announced on the official website of each exchange and the local governments.


- **Major Stock Exchanges**

| ISO Code | Exchange | Country | Exchange Website | CSV File Path | Starting from |
|:---:|---|---|---|---|---|
| AIXK | Astana International Exchange | Kazakhstan | https://aix.kz/trading/trading-calendar/ | marketHoliday/AIXK.csv | 2017 |
| ASEX | Athens Stock Exchange | Greece | https://www.athexgroup.gr/market-alternative-holidays | marketHoliday/ASEX.csv | 2004 |
| BVMF | BMF Bovespa | Brazil | https://www.b3.com.br/en_us/solutions/platforms/puma-trading-system/for-members-and-traders/trading-calendar/holidays/ | marketHoliday/BVMF.csv | 2004 |
| CMES | Chicago Mercantile Exchange | USA | https://www.cmegroup.com/tools-information/holiday-calendar.html#cmeGlobex | marketHoliday/CMES.csv | 2004 |
| IEPA | ICE US | US | https://www.theice.com/holiday-hours?utm_source=website&utm_medium=search&utm_campaign=spotlight | marketHoliday/IEPA.csv | 2004 |
| XAMS | Euronext Amsterdam | Netherlands | https://www.euronext.com/en/trade/trading-hours-holidays | marketHoliday/XAMS.csv | 2004 |
| XASX | Austrialian Securities Exchange | Australia | https://www2.asx.com.au/markets/market-resources/asx-24-trading-calendar | marketHoliday/XASX.csv | 2004 |
| XBKK | Stock Exchange of Thailand | Thailand | https://www.set.or.th/en/about/event-calendar/holiday?year=2023 | marketHoliday/XBKK.csv | 2004 |
| XBOG | Colombia Securities Exchange | Colombia | https://www.bvc.com.co/non-business-market-days | marketHoliday/XBOG.csv | 2004 |
| XBOM | Bombay Stock Exchange | India | https://www.bseindia.com/static/markets/marketinfo/listholi.aspx | marketHoliday/XBOM.csv | 2004 |
| XBRU | Euronext Brussels | Belgium | https://www.euronext.com/en/trade/trading-hours-holidays#:~:text=Calendar%20of%20business%20days%202023%20%20%20Euronext:%20%20Closed%20%2012%20more%20rows%20 | marketHoliday/XBRU.csv | 2004 |
| XBSE | Bucharest Stock Exchange | Romania | https://www.bvb.ro/TradingAndStatistics/TradingSessionSchedule | marketHoliday/XBSE.csv | 2004 |
| XBUD | Budapest Stock Exchange | Hungary | https://www.bse.hu/Products-and-Services/Trading-information/trading-calendar-2023 | marketHoliday/XBUD.csv | 2004 |
| XBUE | Buenos Aires Stock Exchange | Argentina | marketHoliday/XBUE.csv | 2004 |
| XCBF | CBOE Futures | USA | https://www.cboe.com/about/hours/us-futures/ | marketHoliday/XCBF.csv | 2004 |
| XCSE | Copenhagen Stock Exchange | Denmark | https://www.nasdaqomxnordic.com/tradinghours/ | marketHoliday/XCSE.csv | 2004 |
| XDUB | Irish Stock Exchange | Ireland | https://www.euronext.com/en/trade/trading-hours-holidays | marketHoliday/XDUB.csv | 2004 |
| XETR | Xetra | Germany | https://www.xetra.com/xetra-en/newsroom/trading-calendar | marketHoliday/XETR.csv | 2004 |
| XFRA | Frankfurt Stock Exchange | Germany | https://www.boerse-frankfurt.de/en/know-how/trading-calendar | marketHoliday/XFRA.csv | 2004 |
| XHEL | Helsinki Stock Exchange | Finland | https://www.nasdaqomxnordic.com/tradinghours/XHEL | marketHoliday/XHEL.csv | 2004 |
| XHKG | Hong Kong Exchanges | Hong Kong, China | https://www.hkex.com.hk/News/HKEX-Calendar?sc_lang=zh-HK&defaultdate=2023-02-01 | marketHoliday/XHKG.csv | 2004 |
| XICE | Iceland Stock Exchange | Iceland | https://www.nasdaqomxnordic.com/tradinghours/ | marketHoliday/XICE.csv | 2004 |
| XIDX | Indonesia Stock Exchange | Indonesia | https://idx.co.id/en/about-idx/trading-holiday/ | marketHoliday/XIDX.csv | 2004 |
| XIST | Istanbul Stock Exchange | Türkiye | https://borsaistanbul.com/en/sayfa/3631/official-holidays | marketHoliday/XIST.csv | 2004 |
| XJSE | Johannesburg Stock Exchange | South Africa | https://www.jse.co.za/ | marketHoliday/XJSE.csv | 2004 |
| XKAR | Pakistan Stock Exchange | Pakistan | https://www.psx.com.pk/psx/exchange/general/calendar-holidays | marketHoliday/XKAR.csv | 2004 |
| XKLS | Malaysia Stock Exchange | Malaysia | https://www.bursamalaysia.com/about_bursa/about_us/calendar | marketHoliday/XKLS.csv | 2004 |
| XKRX | Korea Exchange | Republic of Korea | http://global.krx.co.kr/contents/GLB/05/0501/0501110000/GLB0501110000.jsp | marketHoliday/XKRX.csv | 2004 |
| XLIM | Lima Stock Exchange | Peru |  | marketHoliday/XLIM.csv | 2004 |
| XLIS | Euronext Lisbon | Portugal | https://www.euronext.com/en/trade/trading-hours-holidays | marketHoliday/XLIS.csv | 2004 |
| XLON | London Stock Exchange | England | https://www.londonstockexchange.com/securities-trading/trading-access/business-days | marketHoliday/XLON.csv | 2004 |
| XMAD | Euronext Lisbon | Portugal | https://www.euronext.com/en/trade/trading-hours-holidays | marketHoliday/XMAD.csv | 2004 |
| XMEX | Mexican Stock Exchange | Mexico | https://www.bmv.com.mx/en/bmv-group/holiday-schedule | marketHoliday/XMEX.csv | 2004 |
| XMIL | Borsa Italiana | Italy | https://www.borsaitaliana.it/borsaitaliana/calendario-e-orari-di-negoziazione/calendario-borsa-orari-di-negoziazione.en.htm | marketHoliday/XMIL.csv | 2004 |
| XMOS | Moscow Exchange | Russia | https://www.moex.com/en/tradingcalendar/ | marketHoliday/XMOS.csv | 2004 |
| XNYS | New York Stock Exchange | USA | https://www.nyse.com/markets/hours-calendars | marketHoliday/XNYS.csv | 2004 |
| XNZE | New Zealand Exchangen | New Zealand | https://www.nzx.com/services/nzx-trading/hours-boards | marketHoliday/XNZE.csv | 2004 |
| XOSL | Oslo Stock Exchange | Norway | https://www.euronext.com/en/trade/trading-hours-holidays | marketHoliday/XOSL.csv | 2004 |
| XPAR | Euronext Paris | France | https://www.euronext.com/en/trade/trading-hours-holidays | marketHoliday/XPAR.csv | 2004 |
| XPHS | Philippine Stock Exchange | Philippines | https://www.pse.com.ph/investing-at-pse/#investing2 | marketHoliday/XPHS.csv | 2004 |
| XPRA | Prague Stock Exchange | Czech Republic | https://www.pse.cz/en/trading/trading-information/trading-calendar | marketHoliday/XPRA.csv | 2004 |
| XSES | Singapore Exchange | Singapore | https://www.mom.gov.sg/employment-practices/public-holidays | marketHoliday/XSES.csv | 2004 |
| XSGO | Santiago Stock Exchange | Chile | https://www.euronext.com/en/trade/trading-hours-holidays | marketHoliday/XSGO.csv | 2004 |
| XSHE | Shenzhen Stocak Exchange | China | http://www.szse.cn/disclosure/index.html | marketHoliday/XSHE.csv | 1992 |
| XSHG | Shanghai Stock Exchange | China | http://www.sse.com.cn/market/view/ | marketHoliday/XSHG.csv | 1991 |
| XSTO | Stockholm Stock Exchange | Sweden | https://www.nasdaqomxnordic.com/tradinghours/ | marketHoliday/XSTO.csv | 2004 |
| XSWX | SIX Swiss Exchange | Switzerland | https://www.six-group.com/en/products-services/the-swiss-stock-exchange/market-data/news-tools/trading-currency-holiday-calendar.html#/ | marketHoliday/XSWX.csv | 2004 |
| XTAI | Taiwan Stock Exchange Corp | Taiwan, China | https://www.twse.com.tw/en/holidaySchedule/holidaySchedule | marketHoliday/XTAI.csv | 2004 |
| XTKS | Tokyo Stock Exchange | Japan | https://www.jpx.co.jp/english/corporate/about-jpx/calendar/ | marketHoliday/XTKS.csv | 2004 |
| XTSE | Toronto Stock Exchange | Canada | https://www.tsx.com/trading/calendars-and-trading-hours/calendar | marketHoliday/XTSE.csv | 2004 |
| XWAR | Poland Stock Exchange | Poland |  | marketHoliday/XWAR.csv | 2004 |
| XWBO | Wiener Borse | Austria | https://www.wienerborse.at/en/trading/trading-information/trading-calendar/ | marketHoliday/XWBO.csv | 2004 |

- **Exchanges in Mainland, China**

| ISO Code| Exchange | Country | Exchange Website | CSV File Path | Starting from |
|:---:|:---:|:---:|:---:|:---:|:---:|
| SSE | Shanghai Stock Exchange | China | http://www.sse.com.cn/market/view/ | marketHoliday/SSE.csv | 1991 |
| SZSE | Shenzhen Stocak Exchange | China | http://www.szse.cn/disclosure/index.html | marketHoliday/SZSE.csv | 1991 |
| CFFEX | China Finacial Futures Exchange | China | http://www.cffex.com.cn/jyrl/ | marketHoliday/CFFEX.csv | 2007 |
| SHFE | Shanghai Futures Exchange | China | https://www.shfe.com.cn/bourseService/businessdata/calendar/ | marketHoliday/SHFE.csv | 1992 |
| CZCE | Zhengzhou Commodity Exchange | China | http://www.czce.com.cn/cn/jysj/jyyl/H770313index_1.htm | marketHoliday/CZCE.csv | 1991 |
| DCE | Dalian Commodity Exchange | China | http://big5.dce.com.cn:1980/SuniT/www.dce.com.cn/DCE/TradingClearing/Exchange%20Notice/1516085/index.html | marketHoliday/DCE.csv | 1994 |
| INE | Shanghai International Energey Exchange | China | https://www.ine.cn/en/news/notice/6598.html | marketHoliday/INE.csv | 2017 |

