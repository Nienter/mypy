import json
import os
import random
import sys
import threading

import pyperclip
import requests
from jsonsearch import JsonSearch

# 接口请求地址

baseUrlCD = "https://static.vtsys.xyz/"
baseUrlSH = "https://www.mosys.xyz/"
baseUrl = ""
urlKeyCD = "vtsys"
urlKeySH = "mosys"
urlKey = ""

# 请求头
headers = {
    "content-type": "application/json",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImp0aSI6InN4cy00ZjFnMjNhMTJhYSJ9.eyJpc3MiOiJkZXZpbnplbmciLCJqdGkiOiJzeHMtNGYxZzIzYTEyYWEiLCJpYXQiOjE2ODQxMTk2NjUsImV4cCI6MTY4NDIwNjA2NSwiZW1haWwiOiJuaXVAdmljdHVyYm8uY29tIiwidWlkIjoiNjMiLCJ1c2VybmFtZSI6Im5wayJ9.q5N3v1Fn1bc_iz2NFQzKZTXOSLjCc4gbxcQ-sNQESwM",
    "authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImp0aSI6InN4cy00ZjFnMjNhMTJhYSJ9.eyJpc3MiOiJkZXZpbnplbmciLCJqdGkiOiJzeHMtNGYxZzIzYTEyYWEiLCJpYXQiOjE2ODQxMTk2NjUsImV4cCI6MTY4NDIwNjA2NSwiZW1haWwiOiJuaXVAdmljdHVyYm8uY29tIiwidWlkIjoiNjMiLCJ1c2VybmFtZSI6Im5wayJ9.q5N3v1Fn1bc_iz2NFQzKZTXOSLjCc4gbxcQ-sNQESwM"
}

# 键值队
payload = {

}
payloadCD = {
    "email": "niu@victurbo.com",
    "passcode": "otnkvb0sl8"
}
payloadSH = {
    "email": "niu@victurbo.com",
    "passcode": "5l4ghv74ewq"
}


def login():
    # login
    loginresponse = requests.get(url=loginUrl, data=getJson)
    print(loginresponse.json())
    headers.update(
        {"token": loginresponse.json()["data"]["token"], "authorization": loginresponse.json()["data"]["token"]})
    print(headers)
    with open("header.json", 'w') as f:
        json.dump(headers, f)
    loginresponse.close()


def requestKey(str2):
    # 构造发送请求
    response = requests.get(url=getProductUrl, headers=headers, data=getJson)
    print(response.json())

    # 打印响应数据
    if response.json()['status'] == 2:  # 过期了
        print("可能过期,正在重新登录")
        login()
    else:
        with open('header.json', 'r') as f:
            header = json.load(f)
        print(header)
        response = requests.get(url=getProductUrl, headers=header, data=getJson)
        s = response.json()["data"]["data"]
        # print(s)
        # print(len(s))
        for index in s:
            if index["app_name"] == str2:
                if index["flurry_appkey"] is not None:
                    print("flurry_appkey " + index["flurry_appkey"])
                if index["fb_id"] is not None:
                    print("fb_id " + index["fb_id"])
                if index["fb_client_secret"] is not None:
                    print("fb_client_secret " + index["fb_client_secret"])
                if index["metric_appkey"] is not None:
                    print("metric_appkey " + index["metric_appkey"])
                if index["jks_id"] is not None:
                    print("jks_id " + index["jks_id"])
                if index['appsflyer_appkey'] is not None:
                    print("appsflyer_appkey " + index["appsflyer_appkey"])
                if index["jks_id"] != "0":
                    js = {"id": index["jks_id"]}
                    jk = json.dumps(js).encode('utf-8').decode('unicode_escape')
                    print(jk)
                    re = requests.get(downloadKeyUrl, headers=header, data=jk)
                    downurl = baseUrl + re.json()["data"]["download_url"]
                    print(downurl)
                    myfile = requests.get(downurl, headers=header, data=jk)
                    # https: // static.vtsys.xyz // uploads / jks / 645c65cdd1627.jks
                    # https: // www.mosys.xyz // uploads / jks / 642bc3712decd.jks
                    # print(myfile.content.decode("unicode_escape"))
                    filename = os.path.basename(downurl)
                    # print(os.path.join('../file', filename) + "*" + downurl)
                    with open(os.path.join('.\\', filename), "wb") as file:
                        file.write(myfile.content)
                    re.close()
                    myfile.close()
                    response.close()
                break
            for xr in index["children"]:
                # print(xr["app_name"])
                if xr["app_name"] == str2:
                    if xr["flurry_appkey"] is not None:
                        print("flurry_appkey " + xr["flurry_appkey"])
                    if xr["fb_id"] is not None:
                        print("fb_id " + xr["fb_id"])
                    if xr["fb_client_secret"] is not None:
                        print("fb_client_secret " + xr["fb_client_secret"])
                    if xr["metric_appkey"] is not None:
                        print("metric_appkey " + xr["metric_appkey"])
                    if xr["jks_id"] is not None:
                        print("jks_id " + xr["jks_id"])
                    if xr['appsflyer_appkey'] is not None:
                        print("appsflyer_appkey " + xr["appsflyer_appkey"])
                    if xr["jks_id"] != "0":
                        js = {"id": xr["jks_id"]}
                        jk = json.dumps(js).encode('utf-8').decode('unicode_escape')
                        # print(jk)
                        re = requests.get(downloadKeyUrl, headers=header, data=jk)
                        downurl = baseUrl + re.json()["data"]["download_url"]
                        print(downurl)
                        myfile = requests.get(downurl, headers=header, data=jk)
                        # https: // static.vtsys.xyz // uploads / jks / 645c65cdd1627.jks
                        # https: // www.mosys.xyz // uploads / jks / 642bc3712decd.jks
                        # print(myfile.content.decode("unicode_escape"))
                        filename = os.path.basename(downurl)
                        # print(os.path.join('.\\file', filename) + "*" + downurl)
                        with open(os.path.join('.\\', filename), "wb") as file:
                            file.write(myfile.content)
                        re.close()
                        myfile.close()
                        response.close()
                    break
        #     # print(index["app_name"])
        #     # if index["app_name"]==str:
        #     #   print(index["flurry_appkey"])
        #     #   print(index["fb_id"])
        #     #   print(index["fb_client_secret"])
        #     #   print(index["jks_id"])
        #     #   print()
        #     #   break


def clear_input():
    """清除输入缓冲区"""
    if os.name == 'nt':  # Windows系统
        os.system('cls')
        print("\033[2J")
    else:  # Unix/Linux系统和Mac OS X系统
        os.system('clear')

    try:
        # 在Python 3.x中使用input函数时，输入缓冲区已被清除
        input()
    except:
        # 在Python 2.x或在IDE环境下使用input函数时，
        # 需要手动清除输入缓冲区，否则会造成多次输入的问题
        import sys
        sys.stdin.flush()
        sys.stdin.readline()


def start(str2):
    requestKey(str2)


if __name__ == '__main__':
    while True:
        str = input("c or s\n")
        str3 = input('l or r\n')

        if str.lower() == "c".lower():
            baseUrl = baseUrlCD
            urlKey = urlKeyCD
            payload = payloadCD
        else:
            baseUrl = baseUrlSH
            urlKey = urlKeySH
            payload = payloadSH

            # 转换成json
        getProductUrl = f"https://api.{urlKey}.xyz/rest.php/act/apps/person?page=1&pagesize=20&app_name=&dataType=dev" \
                        f"&app_type=&dev_status= "
        loginUrl = f"https://api.{urlKey}.xyz/rest.php/token/get"
        downloadKeyUrl = f"https://api.{urlKey}.xyz/rest.php/acc/jks/download"
        getJson = json.dumps(payload).encode('utf-8').decode('unicode_escape')

        if str3 == 'r':
            str2 = input("name\n")
            try:
                with open('header.json', 'r') as f:
                    headers = json.load(f)
                    # 或者使用 f.readlines() 方法读取每一行

            except FileNotFoundError:
                print('文件不存在,请登录')
                continue
            # # text = pyperclip.paste()  # 从剪贴板中获取文本
            # # text = text.strip()
            # # print(text)
            # thread = threading.Thread(target=start, args=(str2,))
            # thread.start()
            # thread.join()
            start(str2)
        else:
            # thread = threading.Thread(target=login)
            # thread.start()
            # thread.join()
            login()

# os.system("pause")
