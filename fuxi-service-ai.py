# -*- coding:utf-8 -*-
from config import CONFIG,env
from flask import Flask, request
from common.setlog2 import set_logger
from config import ApplicationVersion
from api.holoview import holoview
from api.profiles import profiles
from flask_gzip import Gzip

logger = set_logger(CONFIG['LOG_path'], CONFIG['LOG_basename'], env=env)

app = Flask(__name__, static_folder='', static_url_path='')
app.register_blueprint(holoview, url_prefix="/ai/api/holoview")
app.register_blueprint(profiles, url_prefix="/ai/api/holoview/profiles")

gzip = Gzip(app)

@app.before_request
def logger_request_info():
    headers = {'Content-Type': request.headers.get('Content-Type'),
               'Authorization': request.headers.get('Authorization'),
               'Request-id': request.headers.get('request-id')}
    X_Forwarded_For = request.headers.get('X-Forwarded-For')
    Fx_Remote_Addr = request.headers.get('Fx-Remote-Addr')
    logger.info(f"请求URL:{request.url}. 来源IP地址:{Fx_Remote_Addr}. 来源X_Forwarded_For地址:{X_Forwarded_For}"
                f"请求方法:{request.method}. HEADER:{headers}. BODY:{request.data}")


# @app.after_request
def logger_response_info(response):
    X_Forwarded_For = request.headers.get('X-Forwarded-For')
    Fx_Remote_Addr = request.headers.get('Fx-Remote-Addr')
    Request_id = request.headers.get('request-id')
    logger.info(f"请求URL:{request.url}. 来源IP地址:{Fx_Remote_Addr}. 来源X_Forwarded_For地址:{X_Forwarded_For}. Request_id:{Request_id}. Response: {response} ")
    return response


@app.route('/ai/version', methods=["GET"])
def get_version():
    return {
        "code": 200,
        "message": "SUCCESS",
        "businessObj": {
            "buildTime": "",
            "version": ApplicationVersion
        }
    }


if __name__ == '__main__':
    logger.info("main starting....这条日志在用gunicore启动时，会不打印")
    app.run(host='0.0.0.0',port=9200,debug=False,use_reloader=False)

