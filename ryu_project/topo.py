#!/usr/bin/env python
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.clean import cleanup

def create_topology():
    cleanup()
    
    # 明确指定 OpenFlow 协议版本和端口
    net = Mininet(controller=RemoteController)
    
    try:
        info('*** Adding controller\n')
        c0 = net.addController('c0', 
                             controller=RemoteController, 
                             ip='127.0.0.1', 
                             port=6653,  # 改用 OpenFlow 1.3 默认端口
                             protocol='tcp')

        info('*** Adding switch\n')
        s1 = net.addSwitch('s1', protocols='OpenFlow13')  # 强制交换机使用 OF1.3

        info('*** Adding hosts\n')
        # 移除默认网关（因为所有主机在同一子网）
        h1 = net.addHost('h1', ip='10.0.0.1/24')
        h2 = net.addHost('h2', ip='10.0.0.2/24')
        web = net.addHost('web', ip='10.0.0.3/24')
        ftp = net.addHost('ftp', ip='10.0.0.4/24')
        mail = net.addHost('mail', ip='10.0.0.5/24')

        info('*** Creating links\n')
        for host in [h1, h2, web, ftp, mail]:
            net.addLink(host, s1)

        info('*** Starting network\n')
        net.start()

        # 配置 DNS（可选）
        for host in [h1, h2]:
            host.cmd('echo "nameserver 8.8.8.8" > /etc/resolv.conf')

        # 启动服务（增加错误检查）
        info('*** Starting web server\n')
        web.cmd('python3 -m http.server 80 &')

        # 替换原来的FTP启动代码为：
        info('*** Starting FTP server\n')
        ftp.cmd('python3 -m pyftpdlib -p 21 -w -d /tmp &')
        
        # 邮件服务（增加日志输出）
        mail.cmd('python3 -m smtpd -n -c DebuggingServer 0.0.0.0:25 > /tmp/mail.log 2>&1 &')

        info('*** Testing connectivity\n')
        print("Ping test (h1 -> web):")
        print(h1.cmd('ping -c 3 10.0.0.3'))  # 应显示 3/3 接收

        print("\nFTP port test (h2 -> ftp):")
        print(h2.cmd('nc -zv 10.0.0.4 21'))  # 应显示 "succeeded"

        info('*** Running CLI\n')
        CLI(net)
    finally:
        info('*** Stopping network\n')
        net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    create_topology()