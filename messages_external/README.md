# DolphinDB外部消息通信模块
使用httpClient插件的`httpGet`以及`httpPost`可以进行企业微信发送群聊消息以及应用消息、钉钉发送群聊消息，在[利用httpClient插件整合外部消息](https://github.com/dolphindb/Tutorials_CN/blob/master/send_messages_external_systems.md)教程文档中有完整的在企业微信、钉钉管理页面的操作和DolphinDB脚本。
本messages_external模块提供三个模块方法，在创建一个应用或者创建一个群聊后，发送消息。

## 1. 加载

### 1.1 加载httpClient插件
本模块需要使用httpClient插件中的`httpGet`和`httpPost`两个插件方法，需要先加载httpClient插件。

需要有libPluginHttpClient.so和PluginHttpClient.txt两个插件程序文件。

> 可以在[DolphinDB插件项目](https://github.com/dolphindb/DolphinDBPlugin)的/httpClient/bin/linux64/目录下找到这两个文件，但需要注意分支版本号需要与所用的DolphinDB server版本相同。

确认PluginHttpClient.txt和libPluginHttpClient.so在同一个目录下，执行以下脚本来加载插件：
```
loadPlugin("<PluginDir>/httpClient/bin/linux64/PluginHttpClient.txt");
```
### 1.2 加载模块
```
use messages_external;
```

##  2. 用户接口

### 2.1 messages_external::weChat_group_chat

#### 语法

messages_external::weChat_group_chat(corp_id, corp_secret, chatId, message)

#### 详情

发送一条消息到指定的企业微信群。

#### 参数

* corp_id：公司id。类型为字符串。通过登录企业微信的企业账号来查看。
* corp_secret：应用密钥。类型为字符串。通过登录企业微信的企业账号来查看，如果没有则需要创建。
* chatId：群聊id。类型为字符串。只能通过调用企业微信的创建群聊的http协议的api获得。在[利用httpClient插件整合外部消息](https://github.com/dolphindb/Tutorials_CN/blob/master/send_messages_external_systems.md)的2.1.4.1章节为创建企业微信群聊的步骤。
* message：文本消息内容。类型为字符串。
#### 返回值

如果发送消息成功，返回一个bool真值。
如果发送失败，返回一个字典，由企业微信返回的json格式的http应答正文转换得来，有如下键值：
* errcode：错误码。因为此时调用企业微信的api失败，会是一个非零的值。
* errmsg：对返回码的文本描述内容。

#### 例子

```
corp_id="xxx";
corp_secret="xxx";
chatId="xxx";
message="This is a test message";
ret=messages_external::weChat_group_chat(corp_id, corp_secret, chatId, message);
assert 1,typestr(ret)==BOOL;
```

### 2.2 messages_external::weChat_application

>需要注意指定的应用的可见范围，应用的可见范围即推送消息的人群范围。在使用企业微信的企业账号登录后，点击对应的应用，在这个应用的详情页面可以设置可见范围。

#### 语法

messages_external::weChat_application(corp_id, corp_secret, agentId, message)

#### 详情

发送企业微信的应用消息。

#### 参数

* corp_id：公司id。类型为字符串。通过登录企业微信的企业账号来查看。
* corp_secret：应用密钥。类型为字符串。通过登录企业微信的企业账号来查看，如果没有应用则需要创建一个自建应用。
* agentId：应用id。类型为字符串。通过登录企业微信的企业账号来查看，如果没有则需要创建一个自建应用。
* message：文本消息内容。类型为字符串。

#### 返回值

如果发送消息成功，返回一个bool真值。
如果发送失败，返回一个字典，由企业微信返回的json格式的http应答正文转换得来，有如下键值：
* errcode：错误码。因为此时调用企业微信的api失败，会是一个非零的值。
* errmsg：对返回码的文本描述内容。

#### 例子

```
corp_id="xxx";
corp_secret="xxx";
agentId="xxx";
message="This is a test message";
ret=messages_external::weChat_application(corp_id, corp_secret, agentId, message);
assert 1,typestr(ret)==BOOL;
```

### 2.3 messages_external::dingding_group_chat

#### 语法

messages_external::dingding_group_chat(corp_id, corp_secret, chatId, message)

#### 详情

发送一条消息到指定的企业微信群。

#### 参数

* app_key：企业应用id。类型为字符串。通过登录钉钉的企业账号查看应用详情可以获得，如果没有则需要创建应用。
* corp_secret：应用密钥。类型为字符串。通过登录钉钉的企业账号查看应用详情可以获得，如果没有则需要创建应用。
* chatId：群聊id。类型为字符串。只能通过调用钉钉的创建群聊的http协议的api获得。在[利用httpClient插件整合外部消息](https://github.com/dolphindb/Tutorials_CN/blob/master/send_messages_external_systems.md)的2.2.3章节有创建钉钉群聊的具体步骤。
* message：文本消息内容。类型为字符串。

#### 返回值

如果发送消息成功，返回一个bool真值。
如果发送失败，返回一个字典，由钉钉返回的json格式的http应答正文转换得来，有如下键值：
* errcode：错误码。因为此时调用钉钉的api失败，会是一个非零的值。
* errmsg：对返回码的文本描述内容。如果文本内容为访问ip不在白名单之中，则需要到钉钉网页管理端找到对应的应用，然后添加DolphinDB server公网出口ip到ip白名单即可。

#### 例子

```
app_key="xxx";
app_secret="xxx";
DchatId="xxx";
message="xxx";
ret=messages_external::dingding_group_chat(app_key, app_secret, DchatId, message);
assert 1,typestr(ret)==BOOL;
```
