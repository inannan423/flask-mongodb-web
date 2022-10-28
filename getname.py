# 本地运行版本
from flask import Flask, request
import json
from flask_cors import CORS
import pymongo
from bson import json_util

app = Flask(__name__)
CORS(app, resources=r'/*')  # 注册 CORS, "/*" 允许访问所有api

# 数据库名称
myDataBase = "mydb"
# 集合名称
myCollection = "db1"
# 数据库通信证,换成你自己的
tooken = "mongodb+srv://xxxxx"


# 只接受get方法访问
@app.route("/getname", methods=["GET"])
def check():
    # 默认返回内容
    return_dict = {'return_code': '200', 'return_info': '处理成功', 'result': False}
    # 判断入参是否为空
    if request.args is None:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    # 获取传入的params参数
    get_data = request.args.to_dict()
    ID = get_data.get('ID')
    # 对参数进行操作
    return_dict['result'] = getMongo(ID)

    return json.dumps(return_dict, ensure_ascii=False)


def getMongo(ID):
    # 链接 MongoDB atlas
    myclient = pymongo.MongoClient(tooken)
    mydb = myclient[myDataBase]  # 数据库名称
    mycol = mydb[myCollection]  # 集合名称
    myquery = {"id": ID}  # 查询条件
    mydoc = mycol.find(myquery)  # 查询结果
    # 取出其中的数据格式为json
    for x in mydoc:
        # 将x转换为对象
        x = json.loads(json_util.dumps(x))
        print(x)
        return x


# 示例：如果有第二个接口，可以在这里继续写
# @app.route("/getclass", methods=["GET"])
# def check1():
#     # 默认返回内容
#     return_dict = {'return_code': '200', 'return_info': '处理成功', 'result': False}
#     # 判断入参是否为空
#     if request.args is None:
#         return_dict['return_code'] = '5004'
#         return_dict['return_info'] = '请求参数为空'
#         return json.dumps(return_dict, ensure_ascii=False)
#     # 获取传入的params参数
#     get_data = request.args.to_dict()
#     ID = get_data.get('ID')
#     # 对参数进行操作
#     return_dict['result'] = getMongo1(ID)
#
#     return json.dumps(return_dict, ensure_ascii=False)
#
# def getMongo1(ID):
#     # 链接 MongoDB atlas
#     myclient = pymongo.MongoClient(tooken)
#     mydb = myclient[myDataBase]  # 数据库名称
#     mycol = mydb[myCollection]  # 集合名称
#     myquery = {"id": ID}    # 查询条件
#     mydoc = mycol.find(myquery)     # 查询结果
#     # 取出其中的数据格式为json
#     for x in mydoc:
#         # 将x转换为对象
#         x = json.loads(json_util.dumps(x))
#         print(x)
#         return x

if __name__ == "__main__":
    app.run(debug=True)
