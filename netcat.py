#!/usr/bin/python

# IO 多路复用的非阻塞版本的学习
import os
import select
# This module provides access to the select() and poll() functions available in most operating systems,
# devpoll() available on Solaris and derivatives, epoll() available on Linux 2.5+ and kqueue() available on most BSD. 
# Note that on Windows, it only works for sockets; on other operating systems, it also works for other file types (in particular, 
# on Unix, it works on pipes). 
# It cannot be used on regular files to determine whether a file has grown since it was last read.
import socket
import sys

def relay(sock):
    # Returns a polling object, which supports registering and unregistering file descriptors, and then polling them for I/O events;
    poll = select.poll()
    # 注册量触发Polling 的方式，Available for read 
    poll.register(sock, select.POLLIN) 
    poll.register(sys.stdin, select.POLLIN)

    done = False
    
    while not done:
        events = poll.poll(10000)  # 10 seconds ,等待10 s 返回
        for fileno, event in events:   # 遍历是否为空
            if event & select.POLLIN:  # read 数据
                if fileno == sock.fileno():  # 从socket 读取
                    data = sock.recv(8192)
                    if data:
                        sys.stdout.write(data)   # 打印到标准输出
                    else:
                        done = True
                else:
                    assert fileno == sys.stdin.fileno() # 从标准输入中读取
                    data = os.read(fileno, 8192)
                    if data:
                        sock.sendall(data)      # 发送给对面的socket  
                    else: 
                        sock.shutdown(socket.SHUT_WR)       
                        poll.unregister(sys.stdin)
                        
# python 有引用计数，不需要我们自己关闭。

def main(argv):
    if len(argv) < 3:
        binary = argv[0]
        print "Usage:\n  %s -l port\n  %s host port" % (argv[0], argv[0])
        return
    port = int(argv[2])

    # 建立Socket fd 两者之间都是直接调用relay 函数
    if argv[1] == "-l":
        # server 
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('', port))
        server_socket.listen(5)
        (client_socket, client_address) = server_socket.accept()
        server_socket.close()
        relay(client_socket)
    else:
        # client
        sock = socket.create_connection((argv[1], port))
        relay(sock)


if __name__ == "__main__":
    main(sys.argv)
