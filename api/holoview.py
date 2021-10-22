"""
index_blue = Blueprint("admin",__name__)
两个必要参数'admin'蓝图名字;'__name__'蓝图所在的模块或者包，一般为'__name__'变量

index_blue = Blueprint('admin', __name__, url_prefix='/admin')
#为url添加前缀，url为/admin/edit才能访问edit（）函数

index_blue = Blueprint("admin",__name__,static_folder='static_admin')
#访问静态文件。使用/static_admin/*** 访问static_admin目录下的静态文件

index_blue = Blueprint("admin",__name__,static_folder='static_admin',static_url_path='/lib')
#使用 static_url_path 来改变静态目录的路由。 访问路径为/lib/***

index_blue = Blueprint('admin',__name__,template_folder='my_templates')
#设置模板目录
"""

from flask import Blueprint,render_template,make_response,jsonify
from flask import request
from config import env
import requests
import base64
import os


holoview = Blueprint("holoview", __name__)


@holoview.route('/', methods=['GET'])
def holoview_index():
    # forword all params to upstreamURL
    params = request.args.to_dict()
    # Add env(online / test / local) into query params
    if not params.get('env'):
        params['env'] = env

    upstreamURL = 'http://192.168.0.237:8678/api/holoview/'
    return requests.get(upstreamURL, params=params).content, [('Content-Type', 'application/json')]


@holoview.route('/checkSignal', methods=['GET'])
def holoview_checkSignal():
    # forword all params to upstreamURL
    params = request.args.to_dict()
    # Add env(online / test / local) into query params
    if not params.get('env'):
        params['env'] = env

    upstreamURL = 'http://192.168.0.237:8678/api/holoview/checkSignal'

    return requests.get(upstreamURL, params=params).content, [('Content-Type', 'application/json')]


@holoview.route('/findSignal', methods=['GET'])
def holoview_findSignal():
    # forword all params to upstreamURL
    params = request.args.to_dict()
    # Add env(online / test / local) into query params
    if not params.get('env'):
        params['env'] = env

    upstreamURL = 'http://192.168.0.237:8678/api/holoview/findSignal'

    return requests.get(upstreamURL, params=params).content, [('Content-Type', 'application/json')]


@holoview.route('/overall', methods=["GET"])
def holoview_getOverall():
    overall = {
        "event_ConnStatusList": "Tbox到平台连接事件",
        "event_VehicleLoginList": "车辆登录Vehicle服务事件",
        "event_RemoteCmdList": "远程控车指令事件",
        "message_tj32960Login": "国标登录报文",
        "message_tj32960Live": "国标实发报文",
        "message_tj32960Resent": "国标补发报文",
        "message_MSLive": "企标实发报文",
        "message_MSResent": "企标补发报文",
        "message_MSWarning": "企标告警报文",
        "message_MiscList": "Misc报文",
        "message_HeartbeatList": "心跳报文"
    }
    return {
               "code": 200,
               "message": "获取整体指标成功",
               "businessObj": overall
           }, 200



@holoview.route('/help', methods=["GET"])
def holoview_getHelp():
    # 这是本项目提供help内容的demo
    # with open('static/imgs/max16.png', 'rb') as f:
    #     img_base64data = base64.b64encode(f.read())
    #     imgData = img_base64data.decode()
    #     imgData = "data:image/png;base64," + imgData
    # return render_template('holoview_help.html', img1data=imgData)

    params = request.args.to_dict()
    upstreamURL = 'http://192.168.0.237:8678/api/holoview/help'

    return requests.get(upstreamURL, params=params).content