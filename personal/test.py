import json
import time

import pymongo as pymongo
import requests

# http://quote.eastmoney.com/center/gridlist.html#hs_a_board
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/80.0.3987.149 Safari/537.36 '
}

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient["gupiao"]
mycol = mydb["gu" + time.strftime('%Y-%m-%d', time.localtime())]
# mycol = mydb["gu" + time.strftime('2023-01-09', time.localtime())]
# mycol = mydb["gu11222"]


def get_page(url, json=False):
    """
    获取源码
    """
    if json:
        return requests.get(url=url, headers=headers).json()
    return requests.get(url=url, headers=headers).text


def jquery_list(jquery, data_mode='[') -> dict:
    reverse_mode = {'[': ']', '{': '}', '(': ')'}
    tail_str = jquery[-5:][::-1]
    # return json.loads(jquery[jquery.index(data_mode): -tail_str.index(reverse_mode[data_mode])])
    return eval(jquery[jquery.index(data_mode): -tail_str.index(reverse_mode[data_mode])])


def main(end):
    date = time.strftime('%Y-%m-%d', time.localtime())
    for page in range(1, end):
        url = 'http://65.push2.eastmoney.com/api/qt/clist/get?cb=jQuery1124020466762984478337' \
              f'_1609556336027&pn={page}&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&' \
              'fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&' \
              'fields=f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,' \
              f'f24,f25,f22,f11,f62,f128,f136,f115,f152,f37,f100,f102&_={int(time.time() * 1000)}'
        content = get_page(url=url)
        result = jquery_list(content, data_mode='{')
        for i in result['data']['diff']:
            f12, f14, f9, f37 = i['f12'], i['f14'], i['f9'], i['f37']
            data = {"date": date, "stock_code": f12, "name": f14, 'PE': f9, 'ROE': f37}
            mycol.insert_one(data)
            if data.get("stock_code") == "600163":
                print(data)


def orderForFinal():
    mydoc = mycol.find()
    print(mycol.count_documents({}))
    x = mycol.count_documents({})
    for i in range(x):
        newvalues = {"$set": {"finalOrder": mydoc.__getitem__(i).get("PEORDER") + mydoc.__getitem__(i).get("ROEORDER")}}
        mycol.update_one({"stock_code": mydoc.__getitem__(i).get("stock_code")}, newvalues)


def orderForPE():
    mydoc = mycol.find().sort([("PE", 1), ("_id", 1)])
    x = mycol.count_documents({})
    for i in range(x):
        newvalues = {"$set": {"PEORDER": i + 1}}
        mycol.update_one({"stock_code": mydoc.__getitem__(i).get("stock_code")}, newvalues)
    for x in mydoc:
        print(x)


def orderForROE():
    mydoc = mycol.find().sort([("ROE", -1), ("_id", 1)])
    x = mycol.count_documents({})
    for i in range(x):
        newvalues = {"$set": {"ROEORDER": i + 1}}
        mycol.update_one({"stock_code": mydoc.__getitem__(i).get("stock_code")}, newvalues)
    for x in mydoc:
        print(x)


# 删除无效数据
def deleteNUllData():
    myquery = {"PE": "-"}
    mycol.delete_many(myquery)
    myquery1 = {"PE":{"$lt":0}}
    mycol.delete_many(myquery1)
    myquery2 = {"ROE": {"$lt": 0}}
    mycol.delete_many(myquery2)
    # mycol.update_many({},{'$unset':{'finalORDER':'1'}},)


# 发现有重复数据，删掉
def deleteNUll2Data():
    myquery = {"PEORDER": {"$exists": False}}
    mycol.delete_many(myquery)


# 最终排名
def rank():
    mydoc = mycol.find().sort([("finalOrder", 1), ("_id", 1)])
    x = mycol.count_documents({})
    for i in range(x):
        newvalues = {"$set": {"Rank": i + 1}}
        mycol.update_one({"stock_code": mydoc.__getitem__(i).get("stock_code")}, newvalues)


def printData():
    #   myquery = {"name": {"$regex": "^((?!\u9000).)*$"}}
    myquery = {"stock_code": {"$regex": "^(?!(688|30))"}, "name": {"$regex": "^((?!(ST|\\*ST|\u9000)).)*$"}}  # 去掉科创板,去掉ST,去掉带退字的
    mydoc = mycol.find(myquery).sort([("Rank", 1)]).limit(200)
    for x in mydoc:
        print(x.get("name"))


if __name__ == '__main__':
    # main(252)
    # deleteNUllData()
    # orderForPE()
    # orderForROE()
    deleteNUll2Data()
    orderForFinal()
    rank()
    printData()
