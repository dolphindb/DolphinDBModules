# The ops Module

Starting from DolphinDB 1.30.19/2.00.7, you can use the "ops" module to perform database maintenance tasks such as canceling running jobs in a cluster, viewing disk usage and closing inactive sessions without having to write your own maintenance script.

- [The ops Module](#the-ops-module)
  - [1. Environment](#1-environment)
  - [2. Calling Module Functions](#2-calling-module-functions)
  - [3. Function Reference](#3-function-reference)
    - [3.1 cancelJobEx](#31-canceljobex)
    - [3.2 closeInactiveSessions](#32-closeinactivesessions)
    - [3.3 getDDL](#33-getddl)
    - [3.4 getTableDiskUsage](#34-gettablediskusage)
    - [3.5 dropRecoveringPartitions](#35-droprecoveringpartitions)
    - [3.6 getAllLicenses](#36-getalllicenses)
    - [3.7 updateAllLicenses](#37-updatealllicenses)
    - [3.8 unsubscribeAll](#38-unsubscribeall)
    - [3.9 gatherClusterPerf](#39-gatherclusterperf)
    - [3.10 gatherStreamingStat](#310-gatherstreamingstat)
    - [3.12 checkChunkReplicas](#312-checkchunkreplicas)


## 1. Environment

The ops module is delivered with DolphinDB server 1.30.19/2.00.7 or higher. The module file *ops.dos* is under the directory `server/modules`. 

You can also download the ops module [here](https://github.com/dolphindb/DolphinDBModules/blob/master/ops/src/ops.dos).  Place the module file under the directory `[home]/modules` on the controller and data nodes in your cluster. The `[home]` directory is specified by the configuration parameter *home*, which you can check with the function `getHomeDir()`.

For more information about DolphinDB modules, see [tutorial: Modules](https://github.com/dolphindb/Tutorials_EN/blob/master/module_tutorial_EN.md).

## 2. Calling Module Functions

Import the ops module with the `use` keyword. There are 2 ways to call the module functions:

- Refer to the module function directly

```
use ops 
getAllLicenses()
```

- Specify the full namespace of the function

Use this option if other imported modules in the current session contain functions that have the same name.

```
use ops 
ops::getAllLicenses()
```

## 3. Function Reference

### 3.1 cancelJobEx

**Syntax**

```
cancelJobEx(id=NULL)
```

**Arguments**

- id: a string indicating a background job ID, which you can get with the server function `getRecentJobs()`.

**Details**

Cancels running background jobs in the cluster. If *id* is specified, cancel the specified job; otherwise, cancel all the background jobs in the cluster.

**Example**

Create 3 background jobs:

```
def testJob(n,id){
   for(i in 0:n){
        writeLog("demo"+id+"is working")
        sleep(1000)
   }
}
submitJob("demo1","test background job1",testJob,300,1);
submitJob("demo2","test background job2",testJob,300,2);
submitJob("demo3","test background job3",testJob,300,3);
```

Cancel the job “demo1“ and get the status of all background jobs on the data nodes and compute nodes:

```
 cancelJobEx("demo1") 
 pnodeRun(getRecentJobs)
```

The result shows that “demo1“ is marked as “The task was cancelled.“

| node     | userID | jobId | rootJobId                            | jobDesc              | priority | parallelism | receivedTime            | startTime               | endTime                 | errorMsg                                        |
| :------- | :----- | :---- | :----------------------------------- | :------------------- | :------- | :---------- | :---------------------- | :---------------------- | :---------------------- | :---------------------------------------------- |
| comnode1 | admin  | demo1 | 45c4eb71-6812-2b83-814e-ed6b22a99964 | test background job1 | 4        | 2           | 2022.08.29T17:20:47.061 | 2022.08.29T17:20:47.061 | 2022.08.29T17:22:15.081 | testJob: sleep(1000) => The task was cancelled. |
| comnode1 | admin  | demo2 | 1c16dfec-7c5a-92b3-414d-0cfbdc83b451 | test background job2 | 4        | 2           | 2022.08.29T17:20:47.061 | 2022.08.29T17:20:47.062 |                         |                                                 |
| comnode1 | admin  | demo3 | e9dffcc1-3194-9181-8d47-30a325774697 | test background job3 | 4        | 2           | 2022.08.29T17:20:47.061 | 2022.08.29T17:20:47.062 |                         |                                                 |

To cancel all jobs, run the following script:

```cancelJobEx()
pnodeRun(getRecentJobs)
```

### 3.2 closeInactiveSessions

**Syntax**

```
closeInactiveSessions(hours=12)
```

**Arguments**

- hours: a numeric value indicating the session timeout period (in hours). The default value is 12.

**Return**

Returns a table containing information on all active sessions in the cluster. The table has the same schema as the table returned by the server function [getSessionMemoryStat](https://dolphindb.com/help/FunctionsandCommands/FunctionReferences/g/getSessionMemoryStat.html).

**Details**

If a session has been inactive for a time period longer than the specified *hours*, it is considered as timed out. Call this function to close all inactive sessions. 

Note: To check the last active time of a session, call server function [getSessionMemoryStat](https://dolphindb.com/help/FunctionsandCommands/FunctionReferences/g/getSessionMemoryStat.html).

**Examples**

```
getSessionMemoryStat()
```

| userId | sessionId  | memSize | remoteIP        | remotePort | createTime              | lastActiveTime          |
| :----- | :--------- | :------ | :-------------- | :--------- | :---------------------- | :---------------------- |
| admin  | 1195587396 | 16      | 125.119.128.134 | 20252      | 2022.09.01T08:42:16.980 | 2022.09.01T08:45:23.808 |
| guest  | 2333906441 | 16      | 115.239.209.122 | 37284      | 2022.09.01T06:39:05.530 | 2022.09.01T08:42:17.127 |

```
closeInactiveSessions(0.05)
```

| userId | sessionId  | memSize | remoteIP        | remotePort | createTime              | lastActiveTime          | node      |
| :----- | :--------- | :------ | :-------------- | :--------- | :---------------------- | :---------------------- | :-------- |
| admin  | 1195587396 | 16      | 125.119.128.134 | 20252      | 2022.09.01T08:42:16.980 | 2022.09.01T08:45:23.808 | DFS_NODE1 |

### 3.3 getDDL

**Syntax**

```
getDDL(database, tableName)
```

**Arguments**

- database: a string indicating the path to a distributed database, e.g., “dfs://demodb“.
- tableName: a string indicating the name of a DFS table

**Details**

Returns the DDL statements that can be used to recreate the specified database and the DFS table, as well as the column names and column types of the DFS table.

**Examples**

```n=1000000
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

### 3.4 getTableDiskUsage

**Syntax**

```
getTableDiskUsage(database, tableName, byNode=false)
```

**Arguments**

- database: a string indicating the path to a distributed database, e.g., “dfs://demodb“.
- tableName: a string indicating the name of a DFS table.
- byNode: is a Boolean indicating whether to display disk usage by node. The default value is false, i.e., to display the total disk usage of all nodes.

**Details**

Returns a table displaying the disk usage of the specified DFS table. It has the following columns:

- node: a string indicating a node alias. It is returned only when *byNode = true*.
- diskGB: a DOUBLE value indicating the disk usage of the specified DFS table.

**Examples**

```
getTableDiskUsage("dfs://rangedb", "pt", true)
```

| node      | diskGB   |
| :-------- | :------- |
| DFS_NODE1 | 0.008498 |

### 3.5 dropRecoveringPartitions 

**Syntax**

```
dropRecoveringPartitions(dbPath , tableName="")
```

**Arguments**

- dbPath:a string indicating the path to a distributed database, e.g., “dfs://demodb“.
- tableName: a string indicating the name of a DFS table. Specify it only when the database chunk granularity is at TABLE level (i.e.,[database](https://dolphindb.com/help/FunctionsandCommands/FunctionReferences/d/database.html): chunkGranularity = 'TABLE'). 

**Details**

Deletes the partitions in RECOVERING status from the specified database. *tableName* is a required parameter when the database chunk granularity is at TABLE level.

**Example**

First, get the metadata of all chunks in the cluster with the following server functions:

```
rpc(getControllerAlias(), getClusterChunksStatus)
```

| chunkId                              | file                         | size | version | vcLength | versionChain                                          | state      | replicas                             | replicaCount | lastUpdated             | permission |
| :----------------------------------- | :--------------------------- | :--- | :------ | :------- | :---------------------------------------------------- | :--------- | :----------------------------------- | :----------- | :---------------------- | :--------- |
| 5c3bd88f-8a13-a382-2848-cb7c6e75d0fa | /olapDemo/20200905/61_71/53R | 0    | 2       | 3        | 19752:0:2:7460 -> 19506:0:1:7214 -> 19506:0:0:7214 -> | RECOVERING | DFS_NODE1:2:0:false:7494976728710525 | 1            | 2022.08.23T04:20:03.100 | READ_WRITE |
| 620526c7-6cf1-3c89-5444-de04f46aaa93 | /olapDemo/20200904/51_61/53R | 0    | 2       | 3        | 19746:0:2:7454 -> 19495:0:1:7203 -> 19495:0:0:7203 -> | RECOVERING | DFS_NODE1:2:0:false:7494976704543705 | 1            | 2022.08.23T04:20:02.564 | READ_WRITE |

The result suggests that both chunk files of the “olapDemo“ database are in RECOVERING status.

Execute `dropRecoveringPartitions` to force delete these two partitions:

```
dropRecoveringPartitions(database("dfs://olapDemo"));
```

### 3.6 getAllLicenses 

**Syntax**

```
getAllLicenses()
```

**Arguments**

None

**Details**

Returns a table displaying the license expiration date of all nodes in the cluster. It has the following columns:

- nodeAlias: a string indicating a node alias.
- endDate: a date indicating the expiration date.

 

**Examples**

```
getAllLicenses()
```

| nodeAlias | endDate    |
| :-------- | :--------- |
| DFS_NODE1 | 2042.01.01 |
| ctl18920  | 2042.01.01 |
| agent     | 2042.01.01 |

### 3.7 updateAllLicenses 

**Syntax**

```
updateAllLicenses()
```

**Arguments**

None

**Return**

Returns a table displaying the license expiration date of all nodes in the cluster. It has the following columns:

- nodeAlias: a string indicating a node alias.
- endDate: a date indicating the expiration date.

**Details**

Note: Execute this function after you have replaced the license files on the nodes.

Updates the license on all nodes in a cluster without a reboot. Return license expiration information.

**Example**

```
updateAllLicenses()
```

| nodeAlias | endDate    |
| :-------- | :--------- |
| DFS_NODE1 | 2042.01.01 |
| ctl18920  | 2042.01.01 |
| agent     | 2042.01.01 |

### 3.8 unsubscribeAll 

**Syntax**

```
unsubscribeAll()
```

**Arguments**

None

**Details**

Cancels all subscriptions on the current node.

**Examples**

```
share streamTable(10:0, `id`val, [INT, INT]) as st
t = table(10:0, `id`val, [INT, INT])
subscribeTable(tableName=`st, actionName=`sub_st, handler=append!{t})
undef(st, SHARED)
#error
All subscriptions to the shared stream table [st] must be cancelled before it can be undefined.

unsubscribeAll()
undef(st, SHARED)
```

### 3.9 gatherClusterPerf 

**Syntax**

```
gatherClusterPerf(monitoringPeriod=60, scrapeInterval=15, dir="/tmp")
```

**Arguments**

- monitoringPeriod: an integer indicating the time frame (in seconds) of monitoring. The default value is 60.
- scrapeInterval: the interval (in seconds) at which the monitoring metrics are scraped. The default value is 15. 
- dir: a string indicating an existing directory to save the monitoring result. The default value is “/tmp“. 

Note: For a Windows system, use absolute-path and forward slashes (“**/**”) or double backslashes (\\) to separate the directories. 

**Details**

Gets cluster performance monitoring metrics based on the specified monitoring period and scrape interval. Exports the result to the specified directory in a *statis.csv* file. For more information about the monitoring metrics, see server function [getClusterPerf](https://dolphindb.com/help/FunctionsandCommands/FunctionReferences/g/getClusterPerf.html).

**Examples**

```
gatherClusterPerf(30, 3, "/tmp") 
// check the result in /tmp/statis.csv after 30 seconds
```

### 3.10 gatherStreamingStat

**Syntax**

```
gatherStreamingStat(subNode, monitoringPeriod=60, scrapeInterval=15, dir="/tmp")
```

**Arguments**

- subNode: a string indicating the alias of a subscriber node.
- monitoringPeriod: an integer indicating the timeframe (in seconds) of the monitoring. The default value is 60.
- scrapeInterval: the interval (in seconds) at which the monitoring metrics are scraped. The default value is 15. 
- dir: a string indicating an existing directory to save the monitoring result. The default value is “/tmp“.

Note: For a Windows system, use absolute-path and forward slashes (“**/**”) or double backslashes (\\) to separate the directories. 

**Details**

Gets the status of workers on the a subscriber node based on the specified monitoring period and scrape interval. Export the result to the specified directory in a *sub_worker_statis.csv* file. For more information about the monitoring metrics, see server function [getStreamingStat](https://dolphindb.com/help/FunctionsandCommands/FunctionReferences/g/getStreamingStat.html).

**Examples**

```
gatherStreamingStat("subNode",30, 3, "/tmp") 
// check the result in /tmp/sub_worker_statis.csv after 30 seconds
```

 3.11 getDifferentData 

**Syntax**

```
getDifferentData(t1, t2)
```

**Arguments**

- t1 / t2: a handle to an in-memory table. 

**Details**

Checks if the values of *t1* and *t2* are identical by calling server function [eqObj](https://dolphindb.com/help/FunctionsandCommands/FunctionReferences/e/eqObj.html).  *t1* and *t2* must be of the same size.

**Return**

Returns the rows that are different in the two specified tables; otherwise, print “Both tables are identical“.

**Examples**

```
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

### 3.12 checkChunkReplicas

**Syntax**

```
checkChunkReplicas(dbName, tableName, targetChunkId)
```

**Arguments**

- dbName: a string indicating the path to a distributed database, e.g., “dfs://demodb“.
- tableName: a string indicating the name of a DFS table.
- targetChunkId: a string indicating a chunk ID which you can get with server function [getTabletsMeta](https://dolphindb.com/help/FunctionsandCommands/FunctionReferences/g/getTabletsMeta.html). 

**Details**

Checks if the two replicas of the specified chunk are identical. This function is available only when the configuration parameter *dfsReplicationFactor* is set to 2 on the controller.

**Return**

A Boolean indicating whether the data of two chunk replicas are identical.

**Examples**

```
n=1000000
ID=rand(10, n)
x=rand(1.0, n)
t=table(ID, x)
db=database("dfs://rangedb", RANGE,  0 5 10)
pt=db.createPartitionedTable(t, `pt, `ID)
pt.append!(t)
checkChunkReplicas("dfs://rangedb", "pt", "af8268f0-151e-c18b-a84c-a77560b721e6")
#output
true
```

 Stop a data node with the `kill -9 PID` command:

```
pt.append!(t)
checkChunkReplicas("dfs://rangedb", "pt", "af8268f0-151e-c18b-a84c-a77560b721e6")// get the chunk ID with getTabletsMeta()
#output
checkChunkReplicas: throw "colFiles on two replicas are not same" => colFiles on two replicas are not same
```

Reboot the data node. When the chunk recovery is complete, execute `checkChunkReplicas()` again:

```
checkChunkReplicas("dfs://rangedb", "pt", "af8268f0-151e-c18b-a84c-a77560b721e6") // chunk ID can be checked with getTabletsMeta() 
#output
true
```

### 3.13 clearAllSubscriptions 

**Syntax**

```
clearAllSubscriptions()
```

**Arguments**

None

**Return**

Returns the unsubscribed stream table name and handle name, and prints "All subscriptions have been cleared !".

**Details**

Clears all subscriptions of the current node.

**Example**

```
clearAllSubscriptions()
```
unsub: st, sub1  
All subscriptions have been cleared !

### 3.14 dropAllEngines 

**Syntax**

```
dropAllEngines()
```

**Arguments**

None

**Return**

Returns "All engines have been dropped !".

**Details**

Clears all engines of the current node.

**Example**

```
dropAllEngines()
```
All engines have been dropped !

### 3.15 existsShareVariable 

**Syntax**

```
existsShareVariable(names)
```

**Arguments**

- names: a string scalar/vector indicating object name(s).

**Return**

Returns a scalar/vector indicating whether each element of names is a shared variable.

**Details**

Determines whether each element of a string scalar or vector is a shared variable.

**Example**

```
share streamTable(10000:0, `timestamp`sym`val, [TIMESTAMP, SYMBOL, INT]) as variable1
existsShareVariable("variable1")
```
true

### 3.16 clearAllSharedTables 

**Syntax**

```
clearAllSharedTables()
```

**Arguments**

None

**Return**

Returns the name of the deleted shared table and prints "All shared table have been cleared !".

**Details**

Deletes all shared tables of the current node.

**Example**

```
clearAllSharedTables()
```
Drop Shared Table: st  
All shared table have been cleared !

### 3.17 clearAllStreamEnv 

**Syntax**

```
clearAllStreamEnv()
```

**Arguments**

None

**Return**

Same as the returns conbination of the clearAllSubscriptions, dropAllEngines, and clearAllSharedTables.

**Details**

Clears all streaming environments of the current node, including subscriptions, engines and shared tables.

**Example**

```
clearAllStreamEnv()
```
unsub: st, sub1  
All subscriptions have been cleared !  
All engines have been dropped !  
Drop Stream Table: dummyTable1  
All stream table have been cleared !

### 3.18 getPersistenceTableNames 

**Syntax**

```
getPersistenceTableNames()
```

**Arguments**

None

**Return**

Prints the table names of all shared stream tables with persistence enabled.

**Details**

Gets the table names of all shared stream tables with persistence enabled.

**Example**

```
getPersistenceTableNames()
```
[st1,st2]

### 3.19 getNonPersistenceTableNames 

**Syntax**

```
getNonPersistenceTableNames()
```

**Arguments**

None

**Return**

Prints the table names of all shared stream tables with persistence unenabled.

**Details**

Gets the table names of all shared stream tables with persistence unenabled.

**Example**

```
getNonPersistenceTableNames()
```
[st1,st2]

### 3.20 getPersistenceStat 

**Syntax**

```
getPersistenceStat()
```

**Arguments**

None

**Return**

Returns metadata of all shared stream tables with persistence enabled.

**Details**

Gets the status of all shared stream tables with persistence enabled.

**Example**

```
getPersistenceStat()
```
| lastLogSeqNum | sizeInMemory | asynWrite | compress | retentionMinutes | sizeOnDisk | persistenceDir        | hashValue | diskOffset | totalSize | raftGroup | memoryOffset | tablename |
| ------------- | ------------ | --------- | -------- | ---------------- | ---------- | --------------------- | --------- | ---------- | --------- | --------- | ------------ | --------- |
| -1            | 0            | TRUE      | TRUE     | 1440             | 0          | C:/DolphinDB/Data/st2 | 1         | 0          | 0         | -1        | 0            | st2       |

### 3.21 getNonPersistenceTableStat 

**Syntax**

```
getNonPersistenceTableStat()
```

**Arguments**

None

**Return**

Returns metadata of all shared stream tables with persistence unenabled.

**Details**

Gets the status of all shared stream tables with persistence unenabled.

**Example**

```
getNonPersistenceTableStat()
```
| TableName | rows | columns | bytes |
| --------- | ---- | ------- | ----- |
| st3       | 0    | 3       | 20    |

### 3.22 clearAllPersistenceTables 

**Syntax**

```
clearAllPersistenceTables()
```

**Arguments**

None

**Return**

None

**Details**

Deletes all stream tables with persistence enabled.

**Example**

```
clearAllPersistenceTables()
```

 
