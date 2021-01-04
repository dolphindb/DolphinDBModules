# DolphinDB Modules

This project encapsulates the implementation of functions commonly used in the fields of quantitative finance and IoT in modules. We encourage DolphinDB developers to contribute modules.

## Introduction

In DolphinDB, a module is a code package that contains only function definitions.

- Module files are stored under directory [home]/modules on a DolphinDB node.
- The suffix of all module fileUse is .dos, which is an abbreviation of "dolphindb script".
- The first line of a module file can only be the keyword "module" followed by the module name. For example: ```module fileLog```.
- Other than the first line, a module file contains only function definitions.

## Directory Structure

The first-level directory under directory 'modules' is named after the module name. For example, the first-level directory of the 'ta' module is 'ta', which contains the implementation of the [TA-Lib package](https://mrjbq7.github.io/ta-lib/index.html).

Under the first-level directory of each module, there are 'src' and 'test' directories. 
* Function definitions are saved in the 'src' directory.
* The 'test' directory contains test cases, which are named after module name and function name (e.g., 'test_ta_function_ma.txt').

## Quick Start

We use the ta module in this project as an example to demonstrate the deployment and use of modules.

### 1. How to deploy module

#### Download module

Download the entire project and unzip it:

```
unzip dolphindbmodules-master.zip
```

#### Deploy module

Create the 'modules' directory under the directory "/DolphinDB/server/":
```
mkdir modules
```

Copy the .dos files to the 'modules' directory:
```
cp /dolphindbmodules-master/ta/src/ta.dos /DolphinDB/server/modules/
```


### 2. How to import modules into your project

DolphinDB uses keyword 'use' to import the module 'ta'. Note that the module imported by keyword 'use' only applies for the current session. After importing a module, we can use the functions in the module in two ways:

#### Use functions directly
```
use ta

close=1..40
ma(close, 30, 0)
```
#### Call functions with the full path
```
use ta

close=1..40
ta::ma(close, 30, 0)
```
