import getopt, sys, os

ApplicationVersion = "0.0.13"

online = {
    # DB参数
    # "dbserver": "mongodb://rwuser:9WWoq3x1fpQ!@192.168.0.233:8635,192.168.0.54:8635/tjkeys?authSource=admin&replicaSet=replica",
    "dbserver": "mongodb://rwuser:9WWoq3x1fpQ!@192.168.0.133:8635,192.168.0.158:8635/tjkeys?authSource=admin&replicaSet=replica",
    "db_connect": True,

    # eureka服务参数
    "eureka_server": "http://fuxi-service-registry-0.fuxi-service-registry-service:8090/eureka/, http://fuxi-service-registry-2.fuxi-service-registry-service:8090/eureka/, http://fuxi-service-registry-1.fuxi-service-registry-service:8090/eureka/",
    "app_name": "FUXI-SERVICE-AI",
    "renewal_interval_in_secs": 5,
    "duration_in_secs": 15,
    "instance_port": 9200,

    # pushV2的url
    "push_v2_url": 'http://fuxi-basic-push-api-service:80/push/api/v2/push',

    # 日志的存储路径和名称
    "LOG_path": "/data/log/",
    "LOG_basename": "fuxi-service-ai.log"
}

test = {
    # 以下是Mongo4的库
    "dbserver": "mongodb://rwuser:3BHoq3xxf5b!@192.168.0.160:8635,192.168.0.100:8635/tjkeys?authSource=admin&replicaSet=replica",
    "db_connect": True,

    # eureka服务参数
    "eureka_server": "http://fuxi-service-registry-0.fuxi-service-registry-service:8090/eureka/, http://fuxi-service-registry-2.fuxi-service-registry-service:8090/eureka/, http://fuxi-service-registry-1.fuxi-service-registry-service:8090/eureka/",
    "app_name": "FUXI-SERVICE-AI",
    "renewal_interval_in_secs": 5,
    "duration_in_secs": 15,
    "instance_port": 9200,

    # pushV2的url
    "push_v2_url": 'http://localgw.test.cloud.enovatemotors.com/push/api/v2/push',

    # 日志的存储路径和名称
    "LOG_path": "/data/log/",
    "LOG_basename": "fuxi-service-ai.log"
}

local = {
    # DB参数
    "dbserver": "mongodb://rwuser:3BHoq3xxf5b!@192.168.0.160:8635,192.168.0.100:8635/tjkeys?authSource=admin&replicaSet=replica",
    "db_connect": True,

    # eureka服务参数
    "eureka_server": "http://192.168.100.7:8091/eureka/",
    "app_name": "FUXI-SERVICE-AI",
    "renewal_interval_in_secs": 5,
    "duration_in_secs": 15,
    "instance_port": 9200,

    # pushV2的url
    "push_v2_url": 'http://localgw.test.cloud.enovatemotors.com/push/api/v2/push',

    # 日志的存储路径和名称
    "LOG_path": "/tmp/data/log/",
    "LOG_basename": "fuxi-service-ai-local.log"
}



returncode = {
    "188000": "参数错误，需要 profileName, author, description, content, public, overwrite(可选)",
    "188001": "参数错误，需要 profileName, author",
    "188002": "没有这个profileName存在，敞开了来上传",
    "188003": "小天发现这个配置文件的名称已经存在，是否覆盖？",
    "188004": "小天在库里找到一样名字和作者的profile，不让你上传",
    "188005": "写库失败",
    "188010": "下载了个寂寞",
    "188011": "小天删除不了这个profile，因为压根不是你上传的",
    "188012": "小天删除不了这个profile，因为根本找不到这个名字，你骗我",


    "189000": "其他未知错误，小天也搞不定了"
}


# 判断命令行参数
cmd_env = None
try:
    opts, args = getopt.getopt(sys.argv[1:], "h:")
    if opts:
        for op, value in opts:
            if op == "-h":
                # if value in ['online', 'test', 'local']:
                cmd_env = value
    else:
        pass
except:
    pass

# 判断环境变量参数
env_env = None
try:
    env_dist = os.environ
    for key in env_dist:
        if key == 'env':
            env_env = env_dist[key]
except:
    pass

# 确认最后使用的env参数
if cmd_env:
    env = cmd_env
elif env_env:
    env = env_env
else:
    # 默认值
    env = 'local'

if env == 'local':
    CONFIG = local
elif env == 'test':
    CONFIG = test
else:
    CONFIG = online
