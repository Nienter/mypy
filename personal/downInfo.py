import json
import os
import sys
import threading

import requests
import random
from jsonsearch import JsonSearch
import pyperclip

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
    "email": "niu@victurbo.com",
    "passcode": "otnkvb0sl8"
}


def login():
    # login
    loginResponse = requests.get(url=loginUrl, data=getJson)
    print(loginResponse.json())
    headers.update(
        {"token": loginResponse.json()["data"]["token"], "authorization": loginResponse.json()["data"]["token"]})
    print(headers)
    start()


def requestKey(str2):
    # 构造发送请求
    response = requests.get(url=getProductUrl, headers=headers, data=getJson)
    # print(response.json())
    # 打印响应数据
    s = response.json()["data"]["data"]
    # print(s)
    # print(len(s))
    for index in s:
        if index["app_name"] == str2:
            print("flurry_appkey " + index["flurry_appkey"])
            print("fb_id " + index["fb_id"])
            print("fb_client_secret " + index["fb_client_secret"])
            print("metric_appkey "+index["metric_appkey"])
            print("jks_id " + index["jks_id"])

            if index["jks_id"] != "0":
                js = {"id": index["jks_id"]}
                jk = json.dumps(js).encode('utf-8').decode('unicode_escape')
                print(jk)
                re = requests.get(downloadKeyUrl, headers=headers, data=jk)
                downurl = baseUrl + re.json()["data"]["download_url"]
                print(downurl)
                myfile = requests.get(downurl, headers=headers, data=jk)
                # https: // static.vtsys.xyz // uploads / jks / 645c65cdd1627.jks
                # https: // www.mosys.xyz // uploads / jks / 642bc3712decd.jks
                # print(myfile.content.decode("unicode_escape"))
                filename = os.path.basename(downurl)
                print(os.path.join('../file', filename) + "*" + downurl)
                with open(os.path.join('../file', filename), "wb") as file:
                    file.write(myfile.content)
            break
        for xr in index["children"]:
            # print(xr["app_name"])
            if xr["app_name"] == str2:
                print("flurry_appkey " + xr["flurry_appkey"])
                print("fb_id " + xr["fb_id"])
                print("fb_client_secret " + xr["fb_client_secret"])
                print("jks_id " + xr["jks_id"])
                if xr["jks_id"] != "0":
                    js = {"id": xr["jks_id"]}
                    jk = json.dumps(js).encode('utf-8').decode('unicode_escape')
                    # print(jk)
                    re = requests.get(downloadKeyUrl, headers=headers, data=jk)
                    downurl = baseUrl + re.json()["data"]["download_url"]
                    # print(downurl)
                    myfile = requests.get(downurl, headers=headers, data=jk)
                    # https: // static.vtsys.xyz // uploads / jks / 645c65cdd1627.jks
                    # https: // www.mosys.xyz // uploads / jks / 642bc3712decd.jks
                    # print(myfile.content.decode("unicode_escape"))
                    filename = os.path.basename(downurl)
                    # print(os.path.join('.\\file', filename) + "*" + downurl)
                    with open(os.path.join('..\\', filename), "wb") as file:
                        file.write(myfile.content)
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
        else:
            baseUrl = baseUrlSH
            urlKey = urlKeySH

            # 转换成json
        getProductUrl = f"https://api.{urlKey}.xyz/rest.php/act/apps/person?page=1&pagesize=20&app_name=&dataType=dev" \
                        f"&app_type=&dev_status= "
        loginUrl = f"https://api.{urlKey}.xyz/rest.php/token/get"
        downloadKeyUrl = f"https://api.{urlKey}.xyz/rest.php/acc/jks/download"
        getJson = json.dumps(payload).encode('utf-8').decode('unicode_escape')

        if str3 == 'r':
            str2 = input("name\n")
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
