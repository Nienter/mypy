import re
import time

import pymongo
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/80.0.3987.149 Safari/537.36 '
}
myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient["test"]
mycol = mydb["ten" + time.strftime('%Y-%m-%d', time.localtime())]


def main(end):
    date = time.strftime('%Y-%m-%d', time.localtime())
    for page in range(1, end):
        url = 'https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery1123006312403289455082_1689321984215&fid=f109' \
              f'&po=0&pz=50&pn={page}&np=1&fitt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=m:0+t:6+f:!2,m:0+t:13+f:!2,' \
              'm:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2,m:0+t:7+f:!2,m:1+t:3+f:!2&fields=f12,f14,f2,f109,f164,f165,' \
              'f166,f167,f168,f169,f170,f171,f172,f173,f257,f258,f124,f1,f13&_={int(time.time() * 1000)}'
        content = get_page(url=url)
        # print(content)
        result = jquery_list(content, data_mode='{')
        for i in result['data']['diff']:
            f12, f14, f109 = i['f12'], i['f14'], i['f109']
            data = {"date": date, "stock_code": f12, "name": f14, 'percent': f109}
            mycol.insert_one(data)
            # if data.get("stock_code") == "600163":
            #     print(data)


def delete_data():
    # myquery = {"name": {"$regex": ".*"}}
    # myquery = {"stock_code": {"$regex": "^((688|30))"},
    #            "name": {"$regex": "^((?!(ST|\\*ST|\u9000)).)*$"}}  # 去掉科创板,去掉ST,去掉带退字的

    myquery1 = {"stock_code": {"$regex": "^((688|30))"}}
    mycol.delete_many(myquery1)
    myquery2 = {"name": {"$regex": "^(ST|\\*ST)(.)*$"}}
    mycol.delete_many(myquery2)
    myquery3 = {"name": {"$regex": "^(.)*(\u9000)$"}}
    mycol.delete_many(myquery3)
    # mydoc = mycol.delete_many(myquery)
    myquery = {"name": {"$regex": ".*"}}
    mydoc = mycol.find(myquery)
    for x in mydoc:
        print(x.get("name") + ":" + str(x.get("percent") / 100))


def jquery_list(jquery, data_mode='[') -> dict:
    reverse_mode = {'[': ']', '{': '}', '(': ')'}
    tail_str = jquery[-5:][::-1]
    # return json.loads(jquery[jquery.index(data_mode): -tail_str.index(reverse_mode[data_mode])])
    return eval(jquery[jquery.index(data_mode): -tail_str.index(reverse_mode[data_mode])])


def get_page(url, json=False):
    """
    获取源码
    """
    if json:
        return requests.get(url=url, headers=headers).json()
    return requests.get(url=url, headers=headers).text


if __name__ == '__main__':
    main(10)
    delete_data()


