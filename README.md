程硕Linux 网络编程课程中

关于IO 复用在使用阻塞IO 的情况下，会发生的问题。即 ：一个SOCKET 发生了阻塞，会导致整个IO 复用的所有连接发生阻塞；

课程

https://www.bilibili.com/video/BV1MX4y1A7uN?p=21

源代码地址：https://github.com/chenshuo/recipes

结论就是：IO 复用 socket 考虑使用的是，非阻塞的方式，而不是阻塞的方式的来，实现的。
