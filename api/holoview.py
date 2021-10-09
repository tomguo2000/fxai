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
from flask import request, Response
import requests,json,base64,random,logging,time,asn1tools


holoview = Blueprint("holoview", __name__)


@holoview.route('/', methods=['GET'])
def holoview_index():
    # forword all params to upstreamURL
    params = request.args.to_dict()
    upstreamURL = 'http://192.168.0.237:8678/api/ibsreveal/'
    return requests.get(upstreamURL, params=params).content


@holoview.route('/checkSignal', methods=['GET'])
def holoview_checkSignal():
    # forword all params to upstreamURL
    params = request.args.to_dict()
    upstreamURL = 'http://192.168.0.237:8678/api/holoview/checkSignal'
    return requests.get(upstreamURL, params=params).content

