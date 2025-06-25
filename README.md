### 使用指南
1. 将 ```ryu_project``` 放在 ```ryu/ryu/app/```目录下
2. 将 ```traffic_monitor.py```放在```ryu/ryu/app```

运行以下命令：
```sh 
ysx@ubuntu:~/ryu/ryu/app$ ryu-manager --verbose ofctl_rest.py rest_topology.py traffic_monitor.py --observe-links
ysx@ubuntu:~/ryu/ryu/app/ryu_project$ sudo python3 topo.py
```
---
#### 拓扑测试
启动```topo.py```后，可以在```mininet```运行以下命令测试服务器情况：

1. 测试 FTP 端口是否开放
```sh
h2 nc -zv ftp 21
```
预期输出：Connection to 10.0.0.4 21 port [tcp/ftp] succeeded!

2. 测试 Web 服务器
使用 curl 测试 HTTP 连接
```sh
h1 curl http://10.0.0.3
```
或者在 h1 上手动添加 web 的主机名解析
```sh
mininet> h1 bash
echo "10.0.0.3 web" >> /etc/hosts
exit
```
然后再次测试：
```sh
h1 curl http://web
```
预期输出：返回 Web 服务器的文件列表。

3. 测试 Mail 服务器
```sh
h2 nc -zv mail 25
```
预期输出：```Connection to 10.0.0.5 25 port [tcp/smtp] succeeded!```<br/><br/>
手动发送邮件测试
```sh
h2 telnet mail 25
```
然后输入：
```sh
EHLO example.com
MAIL FROM: <user@example.com>
RCPT TO: <recipient@example.com>
DATA
Subject: Test Email
This is a test email.
.
QUIT
```
预期输出：
250 OK（表示命令成功）。
在 mail 主机的终端或 /tmp/mail.log 中可以看到邮件内容。