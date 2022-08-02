# DolphinDB 模块 (Modules)

本项目将量化金融与物联网领域常用函数用DolphinDB脚本实现并封装在模块中，便于DolphinDB开发者使用。我们也欢迎DolphinDB开发者们贡献模块。

## Module(模块)简介

在DolphinDB中，模块是指只包含函数定义的代码包。它具有以下特点：

* 模块文件保存在[home]/modules目录下。
* 模块文件名的后缀为.dos。dos是"dolphindb script"的缩写。
* 模块文件第一行只能使用 module 后接模块名以声明模块，例如 ```module fileLog``` 。 
* 模块文件除第一行外的内容仅可包含函数定义。

关于模块的更多细节，请参考[DolphinDB模块教程](https://gitee.com/dolphindb/Tutorials_CN/blob/master/module_tutorial.md)。

## 目录结构

一级目录以module的名称命名，例如'ta'模块的一级目录名为'ta'，该目录下包含了[TA-Lib包](https://mrjbq7.github.io/ta-lib/index.html)中一些常用指标的实现。

每个module的一级目录下包含'src'和'test'目录：
* 'src'目录下包含所有函数的DolphinDB实现脚本。
* 'test'目录下包含每个函数的测试用例。测试用例以模块名称和函数名称命名（例如'test_ta_function_ma.txt'）。

## 快速入门

下面以本项目中的金融交易数据技术分析模块(ta module)为例，简单演示模块的部署和使用。

### 1. 如何部署module

#### 下载module

下载整个项目并解压：
```
unzip dolphindbmodules-master.zip
```

#### 部署module

在/DolphinDB/server/目录下创建modules目录：
```
mkdir modules
```

将需要使用的.dos的文件复制到modules目录下：
```
cp /dolphindbmodules-master/ta/src/ta.dos /DolphinDB/server/modules/
```

### 2. 如何在项目中导入module

使用[use](https://www.dolphindb.cn/cn/help/Use.html)关键字来导入模块'ta'。注意，use关键字导入的模块是会话隔离的，仅对当前会话有效。

导入模块后，我们可以通过以下两种方式来使用模块内的函数：

#### 直接使用模块中的函数

```
use ta

close=1..40
ma(close, 30, 0)
```

#### 通过完整路径来调用模块中的函数

```
use ta

close=1..40
ta::ma(close, 30, 0)
```