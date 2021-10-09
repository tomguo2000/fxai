# gunicorn.conf

# 并行工作进程数
workers = 2
# 指定每个工作者的线程数
threads = 2
# 监听内网端口8080
bind = '127.0.0.1:9200'
# 设置守护进程,将进程交给supervisor管理
daemon = 'false'
# 工作模式协程
worker_class = 'sync'
# 设置最大并发量
worker_connections = 2000
# 设置进程文件目录
pidfile = '/tmp/gunicorn.pid'
# 设置访问日志和错误信息日志路径
accesslog = '../data/log/gunicorn_access.log'
errorlog = '../data/log/gunicorn_error.log'
# 设置日志记录水平
loglevel = 'debug'
# 设置环境变量
# raw_env = ["env=test"]
