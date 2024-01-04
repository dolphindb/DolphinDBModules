# ops 运维函数库

进行数据库运维时，存在一些常见需求，例如取消集群中未完成的作业、查看数据库磁盘占用情况、关闭不活跃会话等。V1.30.19/V2.00.7 之前版本的 server，用户需要自己开发脚本，来实现这些需求，这增加了维护的难度。为降低用户的开发成本，提升数据库易用性，DolphinDB 自 V1.30.19/V2.00.7 版本开始，增加了数据库运维模块 ops，其覆盖了部分常用的运维脚本，可以满足用户较频繁的运维需求。

> ops 模块兼容 DolpinDB server V1.30.19/V2.00.7 及以上版本。

本教程包含内容：

- [ops 运维函数库](#ops-运维函数库)
  - [1. 环境配置](#1-环境配置)
  - [2. 使用说明](#2-使用说明)
  - [3. 函数说明](#3-函数说明)

## 1. 环境配置

自 1.30.19 和 2.00.7 版本开始，DolphinDB 安装包的 server/modules 目录下已预装 ops.dos，无需用户下载。若在 server/modules 下没找到 ops.dos，通过此处获得 [ops.dos](./src/ops.dos) 文件，并放至节点的 [home]/modules 目录下。其中 [home] 目录由系统配置参数 home 决定，可以通过 `getHomeDir()` 函数查看。

> 更多 DolphinDB 模块的说明，请参阅 [DolphinDB 教程：模块](https://gitee.com/dolphindb/Tutorials_CN/blob/master/module_tutorial.md)。

## 2. 使用说明

通过 use 关键字导入模块。导入模块后，可以通过以下两种方式来使用模块内的自定义函数：

(1) 直接调用模块中的函数：

```
use ops
getAllLicenses()
```

(2) 通过模块中的函数的完整路径来调用：

```
use ops
ops::getAllLicenses()
```

若导入的不同模块中含有相同名称的函数，则必须通过第二种方式调用。

## 3. 函数说明

### 3.1 cancelJobEx <!-- omit in toc -->

**语法**

```Python
cancelJobEx(id=NULL)
```

**参数**

- id: 字符串，表示后台作业的ID，可通过 `getRecentJobs()` 获取。

**详情**

取消集群节点上的后台作业。若指定了参数 id，取消此 id 对应的后台作业，若未指定 id，则取消集群各节点上的所有后台作业。

**例子**

创建 3 个后台作业：

```Python
def testJob(n,id){
   for(i in 0:n){
        writeLog("demo"+id+"is working")
        sleep(1000)
   }
}
submitJob("demo1","just a test",testJob,300,1);
submitJob("demo2","just a test",testJob,300,2);
submitJob("demo3","just a test",testJob,300,3);
```

取消第 1 个作业后，查询作业情况, 发现第 1 个作业的 errorMsg 显示 The task was cancelled：

```Python
 cancelJobEx("demo1")
 pnodeRun(getRecentJobs)
```
| node     | userID | jobId | rootJobId                            | jobDesc     | priority | parallelism | receivedTime            | startTime               | endTime                 | errorMsg                                        |
| -------- | ------ | ----- | ------------------------------------ | ----------- | -------- | ----------- | ----------------------- | ----------------------- | ----------------------- | ----------------------------------------------- |
| comnode1 | admin  | demo1 | 45c4eb71-6812-2b83-814e-ed6b22a99964 | just a test | 4        | 2           | 2022.08.29T17:20:47.061 | 2022.08.29T17:20:47.061 | 2022.08.29T17:22:15.081 | testJob: sleep(1000) => The task was cancelled. |
| comnode1 | admin  | demo2 | 1c16dfec-7c5a-92b3-414d-0cfbdc83b451 | just a test | 4        | 2           | 2022.08.29T17:20:47.061 | 2022.08.29T17:20:47.062 |
| comnode1 | admin  | demo3 | e9dffcc1-3194-9181-8d47-30a325774697 | just a test | 4        | 2           | 2022.08.29T17:20:47.061 | 2022.08.29T17:20:47.062 |                         |

取消所有作业，查看作业情况，发现第 2、3 个作业的 errorMsg 也显示 The task was cancelled：
```
cancelJobEx()
pnodeRun(getRecentJobs)
```
| node     | userID | jobId | rootJobId                            | jobDesc     | priority | parallelism | receivedTime            | startTime               | endTime                 | errorMsg                                        |
| -------- | ------ | ----- | ------------------------------------ | ----------- | -------- | ----------- | ----------------------- | ----------------------- | ----------------------- | ----------------------------------------------- |
| comnode1 | admin  | demo1 | 45c4eb71-6812-2b83-814e-ed6b22a99964 | just a test | 4        | 2           | 2022.08.29T17:20:47.061 | 2022.08.29T17:20:47.061 | 2022.08.29T17:22:15.081 | testJob: sleep(1000) => The task was cancelled. |
| comnode1 | admin  | demo2 | 1c16dfec-7c5a-92b3-414d-0cfbdc83b451 | just a test | 4        | 2           | 2022.08.29T17:20:47.061 | 2022.08.29T17:20:47.062 | 2022.08.29T17:23:15.111 | testJob: sleep(1000) => The task was cancelled. |
| comnode1 | admin  | demo3 | e9dffcc1-3194-9181-8d47-30a325774697 | just a test | 4        | 2           | 2022.08.29T17:20:47.061 | 2022.08.29T17:20:47.062 | 2022.08.29T17:23:15.111 | testJob: sleep(1000) => The task was cancelled. |

### 3.2 closeInactiveSessions <!-- omit in toc -->

**语法**

```Python
closeInactiveSessions(hours=12)
```

**参数**

- hours: 一个数值，用于判断 session 是否过期的时长。单位为小时，默认值为 12。

**返回值**

返回一个表，包含所有节点仍活跃 sessions 的信息。其表结构与 `getSessionMemoryStat` 返回的表结构一致。

**详情**

若 session 最后一次活跃时间与当前时间的差值大于 hours 指定值，则认为该 session 过期了。调用 `closeInactiveSessions` 会将所有过期会话关闭。通过 `getSessionMemoryStat` 方法查看 session 最后一次活跃时间。

**例子**

```Python
getSessionMemoryStat()
```
| userId | sessionId  | memSize | remoteIP        | remotePort | createTime              | lastActiveTime          |
| ------ | ---------- | ------- | --------------- | ---------- | ----------------------- | ----------------------- |
| admin  | 1195587396 | 16      | 125.119.128.134 | 20252      | 2022.09.01T08:42:16.980 | 2022.09.01T08:45:23.808 |
| guest  | 2333906441 | 16      | 115.239.209.122 | 37284      | 2022.09.01T06:39:05.530 | 2022.09.01T08:42:17.127 |
```Python
closeInactiveSessions(0.05)
```
| userId | sessionId  | memSize | remoteIP        | remotePort | createTime              | lastActiveTime          | node      |
| ------ | ---------- | ------- | --------------- | ---------- | ----------------------- | ----------------------- | --------- |
| admin  | 1195587396 | 16      | 125.119.128.134 | 20252      | 2022.09.01T08:42:16.980 | 2022.09.01T08:45:23.808 | DFS_NODE1 |

### 3.3 getDDL <!-- omit in toc -->

**语法**

```Python
getDDL(database, tableName)
```

**参数**

- database: 字符串，表示数据库的路径，如 "dfs://demodb"。
- tableName: 字符串，表示分布式表名。

**返回值**

返回数据库创建语句、分布式表中各字段名称及类型、以及创建分布式表的语句。

**详情**

输出指定分布式表的建表语句。

**例子**

```Python
n=1000000
ID=rand(10, n)
x=rand(1.0, n)
t=table(ID, x)
db=database("dfs://rangedb", RANGE,  0 5 10)
pt=db.createPartitionedTable(t, `pt, `ID)
getDDL("dfs://rangedb", "pt")
#output

db = database("dfs://rangedb")
colName = `ID`x
colType = [INT,DOUBLE]
tbSchema = table(1:0, colName, colType)
db.createPartitionedTable(table=tbSchema,tableName=`pt,partitionColumns=`ID)

```

### 3.4 getTableDiskUsage <!-- omit in toc -->

**语法**

```Python
getTableDiskUsage(database, tableName, byNode=false)
```

**参数**

- database: 字符串，表示数据库的路径，如 "dfs://demodb"。
- tableName: 字符串，表示分布式表名。
- byNode: 布尔值，表示是否按节点显示磁盘使用量。默认值是 false，表示显示所有节点的磁盘使用总量。

**返回值**

返回一张记录磁盘占用信息的表，包含字段：
- node: 字符串，表示节点别名。仅在 byNode = true 时显示。
- diskGB: DOUBLE 浮点数，表示指定分布式表占用的磁盘空间。

**详情**

获取指定分布式表占用的磁盘空间大小。

**例子**

```Python
getTableDiskUsage("dfs://rangedb", "pt", true)
```
| node      | diskGB   |
| --------- | -------- |
| DFS_NODE1 | 0.008498 |

### 3.5 dropRecoveringPartitions <!-- omit in toc -->

**语法**

```Python
dropRecoveringPartitions(dbPath , tableName="")
```

**参数**

- dbPath: 字符串，表示数据库的路径，如 "dfs://demodb"。
- tableName: 字符串，表示分布式表名，仅当指定分区粒度 chunkGranularity 为 TABLE 时指定。关于 chunkGranularity 的说明参见：[database](https://www.dolphindb.cn/cn/help/FunctionsandCommands/FunctionReferences/d/database.html)。

**详情**

强制删除指定数据库的正在恢复的分区。当表的分区粒度 chunkGranularity 为 TABLE 时必须指定 tableName 参数。

**例子**

首先，查看集群中所有 chunk 的元数据信息。
```Python
rpc(getControllerAlias(), getClusterChunksStatus)
```

| chunkId                              | file                         | size | version | vcLength | versionChain                                          | state      | replicas                             | replicaCount | lastUpdated             | permission |
| ------------------------------------ | ---------------------------- | ---- | ------- | -------- | ----------------------------------------------------- | ---------- | ------------------------------------ | ------------ | ----------------------- | ---------- |
| 5c3bd88f-8a13-a382-2848-cb7c6e75d0fa | /olapDemo/20200905/61_71/53R | 0    | 2       | 3        | 19752:0:2:7460 -> 19506:0:1:7214 -> 19506:0:0:7214 -> | RECOVERING | DFS_NODE1:2:0:false:7494976728710525 | 1            | 2022.08.23T04:20:03.100 | READ_WRITE |
| 620526c7-6cf1-3c89-5444-de04f46aaa93 | /olapDemo/20200904/51_61/53R | 0    | 2       | 3        | 19746:0:2:7454 -> 19495:0:1:7203 -> 19495:0:0:7203 -> | RECOVERING | DFS_NODE1:2:0:false:7494976704543705 | 1            | 2022.08.23T04:20:02.564 | READ_WRITE |

由结果表看出，此时数据库 olapDemo 的 2 个分区 /olapDemo/20200904/ 和 /olapDemo/20200905/ 均处于 RECOVERING 状态。  
调用 dropRecoveringPartitions 强制删除所有正在恢复的分区：

```Python
dropRecoveringPartitions(database("dfs://olapDemo"));
```

### 3.6 getAllLicenses <!-- omit in toc -->

**语法**

```Python
getAllLicenses()
```

**参数**

无

**返回值**

返回一张表，显示各个节点的 license 过期时间，包含字段：
- nodeAlias: 字符串，表示节点别名。
- endDate: 日期值，表示节点 license 过期时间。

**详情**

获取集群中各个节点的 license 过期时间。

**例子**

```Python
getAllLicenses()
```
| nodeAlias | endDate    |
| --------- | ---------- |
| DFS_NODE1 | 2042.01.01 |
| ctl18920  | 2042.01.01 |
| agent     | 2042.01.01 |

### 3.7 updateAllLicenses <!-- omit in toc -->

**语法**

```Python
updateAllLicenses()
```

**参数**

无

**返回值**

同 `getAllLicenses()` 的返回值

**详情**

在线更新集群中各个节点的 license，并返回 license 过期信息。  
注意，调用此函数前，需要先替换 license 文件。

**例子**

```Python
updateAllLicenses()
```
| nodeAlias | endDate    |
| --------- | ---------- |
| DFS_NODE1 | 2042.01.01 |
| ctl18920  | 2042.01.01 |
| agent     | 2042.01.01 |

### 3.8 unsubscribeAll <!-- omit in toc -->

**语法**

```Python
unsubscribeAll(tbName=NULL)
```

**参数**

- tbName: 字符串标量，表示要取消订阅的表名。默认值NULL，即如若不填参数，表示取消所有表的订阅。


**详情**

取消某个表的订阅，参数为NULL，即如若不填参数时可以取消所有表的订阅。

**例子**

```Python
share streamTable(10:0, `id`val, [INT, INT]) as st
t = table(10:0, `id`val, [INT, INT])
subscribeTable(tableName=`st, actionName=`sub_st, handler=append!{t})
undef(st, SHARED)
#error
All subscriptions to the shared stream table [st] must be cancelled before it can be undefined.

unsubscribeAll()
undef(st, SHARED)
```


取消某个表的订阅：
```python
share streamTable(10:0, `id`val, [INT, DOUBLE]) as test_1
res = table(10:0, `id`val, [INT, DOUBLE])
subscribeTable(tableName=`test_1,handler=append!{res},actionName="sub_test_1")
unsubscribeAll("test_1")
```

### 3.9 gatherClusterPerf <!-- omit in toc -->

**语法**

```Python
gatherClusterPerf(monitoringPeriod=60, scrapeInterval=15, dir="/tmp")
```

**参数**

- monitoringPeriod: 整数值，表示监控时间，单位为秒，默认为 60。
- scrapeInterval: 整数值，表示抓取间隔，单位为秒，默认为 15。
- dir: 字符串，表示保存路径，默认为 "/tmp"。

**详情**

根据指定的监控时间和抓取间隔获取集群中各个节点的性能监控信息，并将结果保存至指定目录的 statis.csv 文件。输出内容说明见 [getClusterPerf](https://dolphindb.cn/cn/help/200/FunctionsandCommands/FunctionReferences/g/getClusterPerf.html)。

**例子**

```Python
gatherClusterPerf(30, 3, "/tmp")
// 30s 后查看 /tmp/statis.csv 里的结果
```

### 3.10 gatherStreamingStat <!-- omit in toc -->

**语法**

```Python
gatherStreamingStat(subNode, monitoringPeriod=60, scrapeInterval=15, dir="/tmp")
```

**参数**

- subNode: 字符串，表示订阅节点的别名。
- monitoringPeriod: 整数值，表示监控时间，单位为秒，默认为 60。
- scrapeInterval: 整数值，表示抓取间隔，单位为秒，默认为 15。
- dir: 字符串，表示保存路径，默认为 "/tmp"。

**详情**

根据指定的监控时间和抓取间隔获取指定订阅节点的工作线程的状态信息，并将结果保存至指定目录的 sub_worker_statis.csv 文件。输出内容说明见 [getStreamingStat](https://dolphindb.cn/cn/help/200/FunctionsandCommands/FunctionReferences/g/getStreamingStat.html?highlight=subWorkers)。

**例子**

```Python
gatherStreamingStat(30, 3, "/tmp")
// 30s 后查看 /tmp/sub_worker_statis.csv 里的结果
```

### 3.11 getDifferentData <!-- omit in toc -->

**语法**

```Python
getDifferentData(t1, t2)
```

**参数**

- t1: 内存表句柄。
- t2: 内存表句柄。

**返回值**

若存在不同行，返回不同的行；否则打印 "Both tables are identical"。

**详情**

使用 [eqObj](https://dolphindb.cn/cn/help/200/FunctionsandCommands/FunctionReferences/e/eqObj.html) 比较两张内存表的每一行是否相同。比较的两张表的长度必须相同。

**例子**

```Python
t1=table(1 2 3 as id, 4 5 6 as val)
t2=table(1 8 9 as id, 4 8 9 as val)
t3=table(1 2 3 as id, 4 5 6 as val)
for (row in getDifferentData(t1, t2))
  print row
#output
id val
-- ---
2  5
3  6
id val
-- ---
8  8
9  9

getDifferentData(t1, t3)
#output
Both tables are identical
```

### 3.12 checkChunkReplicas <!-- omit in toc -->

**语法**

```Python
checkChunkReplicas(dbName, tableName, targetChunkId)
```

**参数**

- dbName: 字符串，表示数据库的路径，如 "dfs://demodb"。
- tableName: 字符串，表示分布式表名。
- targetChunkId: 字符串，表示要检查的 chunk 的 ID，可通过 [getTabletsMeta()](https://dolphindb.cn/cn/help/FunctionsandCommands/FunctionReferences/g/getTabletsMeta.html) 查看。

**返回值**

布尔值，表示指定分区的副本数据是否一致。

**详情**

检查数据库表指定分区的两个副本的数据是否一致。仅当控制节点配置 dfsReplicationFactor 值为 2 时有效。

**例子**

```Python
n=1000000
ID=rand(10, n)
x=rand(1.0, n)
t=table(ID, x)
db=database("dfs://rangedb", RANGE,  0 5 10)
pt=db.createPartitionedTable(t, `pt, `ID)
pt.append!(t)
checkChunkReplicas("dfs://rangedb", "pt", "af8268f0-151e-c18b-a84c-a77560b721e6") // chunk ID 可通过 getTabletsMeta() 查看
#output
true
```

使用 `kill -9 PID` 杀死其中一个数据节点，执行如下脚本：

```Python
pt.append!(t)
checkChunkReplicas("dfs://rangedb", "pt", "af8268f0-151e-c18b-a84c-a77560b721e6") // chunk ID 可通过 getTabletsMeta() 查看
#output
checkChunkReplicas: throw "colFiles on two replicas are not same" => colFiles on two replicas are not same
```

重新启动杀死的数据节点，待副本数据同步后，再次执行 checkChunkReplicas()：

```Python
checkChunkReplicas("dfs://rangedb", "pt", "af8268f0-151e-c18b-a84c-a77560b721e6") // chunk ID 可通过 getTabletsMeta() 查看
#output
true
```

### 3.13 clearAllSubscriptions <!-- omit in toc -->

**语法**

```Python
clearAllSubscriptions()
```

**参数**

- 该函数无参数

**返回值**

返回取消订阅的流数据表名称和句柄名称，并打印"All subscriptions have been cleared !"。

**详情**

取消当前节点所有的流数据表订阅。

**例子**

```Python
clearAllSubscriptions()
```
unsub: st, sub1  
All subscriptions have been cleared !

### 3.14 dropAllEngines <!-- omit in toc -->

**语法**

```Python
dropAllEngines()
```

**参数**

- 该函数无参数

**返回值**

返回"All engines have been dropped !"。

**详情**

释放当前节点所有的流数据引擎的定义。

**例子**

```Python
dropAllEngines()
```
All engines have been dropped !

### 3.15 existsShareVariable <!-- omit in toc -->

**语法**

```Python
existsShareVariable(names)
```

**参数**

- names: 可以是字符串标量或向量，表示对象名。

**返回值**

返回一个标量/向量，表示names中的每个元素是否为共享变量。

**详情**

判断一个字符串标量或向量中的每个元素是否为共享变量。

**例子**

```Python
share streamTable(10000:0, `timestamp`sym`val, [TIMESTAMP, SYMBOL, INT]) as variable1
existsShareVariable("variable1")
```
true

### 3.16 clearAllSharedTables <!-- omit in toc -->

**语法**

```Python
clearAllSharedTables()
```

**参数**

- 该函数无参数

**返回值**

返回删除的共享表的表名，并打印"All shared table have been cleared !"。

**详情**

删除当前节点所有的共享表。

**例子**

```Python
clearAllSharedTables()
```
Drop Shared Table: st  
All shared table have been cleared !

### 3.17 clearAllStreamEnv <!-- omit in toc -->

**语法**

```Python
clearAllStreamEnv()
```

**参数**

- 该函数无参数

**返回值**

同clearAllSubscriptions()、dropAllEngines()、sclearAllSharedTables()三个函数的返回值汇总。

**详情**

清除当前节点所有的流数据环境，包括流数据表订阅、流数据引擎和共享表。

**例子**

```Python
clearAllStreamEnv()
```
unsub: st, sub1  
All subscriptions have been cleared !  
All engines have been dropped !  
Drop Stream Table: dummyTable1  
All stream table have been cleared !  

### 3.18 getPersistenceTableNames <!-- omit in toc -->

**语法**

```Python
getPersistenceTableNames()
```

**参数**

- 该函数无参数

**返回值**

所有共享持久化流表的表名。

**详情**

获得所有共享持久化流表的表名。

**例子**

```Python
getPersistenceTableNames()
```
[st1,st2]

### 3.19 getNonPersistenceTableNames <!-- omit in toc -->

**语法**

```Python
getNonPersistenceTableNames()
```

**参数**

- 该函数无参数

**返回值**

所有非持久化共享流表名。

**详情**

获取所有非持久化共享流表名。

**例子**

```Python
getNonPersistenceTableNames()
```
[st1,st2]

### 3.20 getPersistenceStat <!-- omit in toc -->

**语法**

```Python
getPersistenceStat()
```

**参数**

- 该函数无参数

**返回值**

返回所有启用了持久化的共享流数据表的元数据。

**详情**

获取所有持久化共享流表的状态。

**例子**

```Python
getPersistenceStat()
```
| lastLogSeqNum | sizeInMemory | asynWrite | compress | retentionMinutes | sizeOnDisk | persistenceDir        | hashValue | diskOffset | totalSize | raftGroup | memoryOffset | tablename |
| ------------- | ------------ | --------- | -------- | ---------------- | ---------- | --------------------- | --------- | ---------- | --------- | --------- | ------------ | --------- |
| -1            | 0            | TRUE      | TRUE     | 1440             | 0          | C:/DolphinDB/Data/st2 | 1         | 0          | 0         | -1        | 0            | st2       |

### 3.21 getNonPersistenceTableStat <!-- omit in toc -->

**语法**

```Python
getNonPersistenceTableStat()
```

**参数**

- 该函数无参数

**返回值**

返回所有非持久化的共享流数据表的元数据。

**详情**

获取所有非持久化共享流表状态。

**例子**

```Python
getNonPersistenceTableStat()
```
| TableName | rows | columns | bytes |
| --------- | ---- | ------- | ----- |
| st3       | 0    | 3       | 20    |

### 3.22 clearAllPersistenceTables <!-- omit in toc -->

**语法**

```Python
clearAllPersistenceTables()
```

**参数**

- 该函数无参数

**返回值**

该函数无返回值。

**详情**

删除所有持久化流表。

**例子**

```Python
clearAllPersistenceTables()
```


### 3.23 getDatabaseDDL <!-- omit in toc -->

**语法**

```Python
getDatabaseDDL(dbName)
```

**参数**

- dbName : 库名（字符串标量）

**返回值**

建库语句（字符串标量）

**详情**

获得目标库的建库语句。


**例子**

```Python
dbName = "dfs://testDatabaseRANGE"
db1 = database(dbName, RANGE, 1985.01.01 1990.01.01 1995.01.01 2000.01.01 2005.01.01 2010.01.01)
getDatabaseDDL(dbName)

#output
database(directory = 'dfs://testDatabaseRANGE', partitionType = RANGE, partitionScheme =[1985.01.01,1990.01.01,1995.01.01,2000.01.01,2005.01.01,2010.01.01], engine= `OLAP, atomic = `TRANS)
```


### 3.24 getDBTableDDL <!-- omit in toc -->

**语法**

```Python
getDBTableDDL(dbName,tbName)
```

**参数**

- dbName : 库名（字符串标量）
- tbName : 表名（字符串标量）

**返回值**

数据库中的建表语句（字符串标量）

**详情**

获得目标库内的表的建表语句。

**例子**

```Python
dbName = "dfs://test_OLAP_RANGE"
tbName1 = "partition1"
tbName2= "dimension1"
db1 = database(dbName, RANGE, 1985.01.01 1990.01.01 1995.01.01 2000.01.01 2005.01.01 2010.01.01)
tbSchema = table(1:0, `SecurityID`DateTime`Open`High`Low`Close, [SYMBOL, DATETIME, DOUBLE, DOUBLE, DOUBLE, DOUBLE])
db = database(dbName)
tb1 = createPartitionedTable(db, tbSchema, tbName1, ["DateTime"])
tb2 = createTable(db, tbSchema, tbName2)
getDBTableDDL(dbName,tbName1)
getDBTableDDL(dbName,tbName2)

#output
createPartitionedTable(dbHandle = database('dfs://test_OLAP_RANGE'),table = table(1:0, ["SecurityID","DateTime","Open","High","Low","Close"],["SYMBOL","DATETIME","DOUBLE","DOUBLE","DOUBLE","DOUBLE"]),tableName = 'partition1',partitionColumns =["DateTime"],compressMethods = dict(["SecurityID","DateTime","Open","High","Low","Close"],["lz4","lz4","lz4","lz4","lz4","lz4"]))

createTable(dbHandle = database('dfs://test_OLAP_RANGE'),table = table(1:0, ["SecurityID","DateTime","Open","High","Low","Close"],["SYMBOL","DATETIME","DOUBLE","DOUBLE","DOUBLE","DOUBLE"]),tableName = 'dimension1',compressMethods = dict(["SecurityID","DateTime","Open","High","Low","Close"],["lz4","lz4","lz4","lz4","lz4","lz4"]))
```

### 3.25 getChunkUsageByNode <!-- omit in toc -->

**语法**

```Python
getChunkUsageByNode(dbName, tbName)
```

**参数**

- dbName : 库名（字符串标量）
- tbName : 表名（字符串标量）

**返回值**

返回一张表，里面包含了要检查的库表在各个节点分别有多少个 chunk，这些 chunk 的磁盘用量（单位：字节），以及每个节点 chunk 的磁盘用量占总 chunk 磁盘用量的比率。

**详情**

获取某个分布式表在各个节点的chunk分布情况、磁盘用量及占比。

**例子**

```Python
getChunkUsageByNode("dfs://TL_level2", "trade")
```

| node        | count | diskUsage | percent    |
| ----------- | ----- | --------- | ---------- |
| dnode1      | 33    | 4897619   | 0.34497003 |
| dnode2      | 35    | 4827365   | 0.34002160 |
| dnode3      | 32    | 4472246   | 0.31500835 |

### 3.26 getChunkUsageByVolume <!-- omit in toc -->

**语法**

```Python
getChunkUsageByVolume(dbName, tbName, node=NULL)
```

**参数**

- dbName : 库名（字符串标量）
- tbName : 表名（字符串标量）
- node : 节点名（字符串标量或向量，默认为 NULL）

**返回值**

返回一张表，里面包含了要检查的库表在各个节点的各个 volume 上分别有多少个 chunk，这些 chunk 的磁盘用量（单位：字节），以及各节点每个 volume 的 chunk 的磁盘用量占每个节点上 chunk 磁盘用量的比率。

**详情**

获取某个分布式表在各个节点的各个 volume 上的 chunk 分布情况和磁盘用量占比。

**例子**

```Python
getChunkUsageByVolume("dfs://TL_level2", "trade")
```

| node     | path          | count | diskUsage | percent    |
| -------- | ------------- | ----- | --------- | ---------- |
| P1-node1 | /hdd0/volumes | 3     | 638678    | 0.40908590 |
| P1-node1 | /hdd1/volumes | 5     | 922554    | 0.59091409 |
| P2-node1 | /hdd0/volumes | 7     | 709995    | 0.43487914 |
| P2-node1 | /hdd1/volumes | 5     | 922631    | 0.56512085 |
| P3-node1 | /hdd0/volumes | 4     | 426067    | 0.54544744 |
| P3-node1 | /hdd1/volumes | 2     | 355066    | 0.45455255 |