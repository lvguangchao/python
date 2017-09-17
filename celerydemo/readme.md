=====================基于tornado 整合 celery 搭建分布式非阻塞异步框架================
#author lvguangchao 
#email  582128198@qq.com


install
   
    1. celery
	2. tornado-celery
	3. tornado
	4. rabbmit

tutorial 

   celery 本身不u包含消息服务，使用第三方消息服务（rabbmit or redis）
   celery 在其中一台机器上运行之后，就会在存储在rabbmit上
   我们通过方法名.delay() 并不是在本机器上执行这个方法，而是调用rabbitmq上到远程方法
   
   关于 celery 到启动问题，网上到教程都是通过命令行执行celery -A task worker命令启动
   celery.exe 对应着celery.bin.worker 模块，里面有一句execute_from_commandline
   
   正确启动方式：   
   worker.run(broker=broker, concurrency=4,
               traceback=False, loglevel='INFO')
			   
   tcelery 作用：Setup celery to use non blocking producer
   
   
 参考：http://blog.csdn.net/github_25679381/article/details/50574707
    
  
    