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
from config import env, returncode
import requests,json,base64,random,logging,time,asn1tools
from common.setlog2 import logger
from service.profileService import ProfileService
import pymongo
from pymongo.errors import AutoReconnect
from retrying import retry
from dbconfig import db


profiles = Blueprint("profiles", __name__)

@profiles.route('/getProfiles', methods=["GET"])
def profiles_getProfiles():
    _profiles = ProfileService.getProfiles()
    return {
               "code": 200,
               "message": "getProfiles成功",
               "businessObj": _profiles
           }, 200

@profiles.route('/downloadProfile', methods=["GET"])
def profiles_downloadProfile():
    profileName = request.args.get('profileName')
    p=ProfileService.getProfile(profileName)
    if p:
        return {
                   "code": 200,
                   "message": "downloadProfile成功",
                   "businessObj": p
               }, 200
    else:
        return {
                   "code": 188010,
                   "message": "下载了个寂寞，啥也没有",
                   "businessObj": p
               }, 200



@profiles.route('/uploadProfile', methods=["POST"])
def profiles_uploadProfile():
    reqdata = request.data

    try:
        # 检查入参
        reqdata = reqdata.decode()
        try:
            # 转为json
            postdata_json = json.loads(reqdata)
            profileName = postdata_json['profileName']
            author = postdata_json['author']
            description = postdata_json['description']
            content = postdata_json['content']
            overwrite = postdata_json.get('overwrite')

        except Exception as ex:
            raise Exception("188000")

        # 检查冲突
        p = ProfileService(profileName,author,description,content)
        if ProfileService.checkConflict(p) == "188004":
            raise Exception("188004")

        # 执行入库
        if ProfileService.save2db(p, overwrite):
            return {
                       "code": 200,
                       "message": f"uploadProfile成功",
                       "businessObj": None
                   }, 200
        else:
            return {
                       "code": 188005,
                       "message": f"uploadProfile失败",
                       "businessObj": None
                   }, 200


    except Exception as ex:
        logger.warning(ex)
        logger.warning(returncode[ex.args[0]])
        return {
                   "code": ex.args[0],
                   "message": returncode[ex.args[0]],
                   "businessObj": None
               }, 200


@profiles.route('/checkConflict', methods=["POST"])
def profiles_checkConflict():
    reqdata = request.data

    try:
        # 检查入参
        reqdata = reqdata.decode()
        try:
            # 转为json
            postdata_json = json.loads(reqdata)
            profileName = postdata_json['profileName']
            author = postdata_json['author']

        except Exception as ex:
            raise Exception("188001")

        # 检查冲突
        p = ProfileService(profileName,author)

        return {
                   "code": 200,
                   "message": f"checkConflict成功",
                   "businessObj": ProfileService.checkConflict(p)
               }, 200

    except Exception as ex:
        logger.warning(ex)
        logger.error(returncode[ex.args[0]])
        return {
                   "code": ex.args[0],
                   "message": returncode[ex.args[0]],
                   "businessObj": None
               }, 400



@profiles.route('/deleteProfile', methods=["DELETE"])
def profiles_deleteProfile():

    return {
               "code": 200,
               "message": "deleteProfile成功",
               "businessObj": None
           }, 200
