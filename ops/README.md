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

### 3.4 dropRecoveringPartitions <!-- omit in toc -->

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

### 3.5 getAllLicenses <!-- omit in toc -->

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

### 3.6 updateAllLicenses <!-- omit in toc -->

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

### 3.7 unsubscribeAll <!-- omit in toc -->

**语法**

```Python
unsubscribeAll()
```

**参数**

无

**详情**

取消当前节点上的所有订阅。

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

### 3.8 gatherClusterPerf <!-- omit in toc -->

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

### 3.8 gatherStreamingStat <!-- omit in toc -->

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

### 3.9 getDifferentData <!-- omit in toc -->

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

### 3.10 checkChunkReplicas <!-- omit in toc -->

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