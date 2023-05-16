import datetime
import json
import time
import requests
import pymysql
from datetime import date, timedelta

url = "https://webapi.sporttery.cn/gateway/jc/football/getMatchCalculatorV1.qry?poolCode=hhad,had&channel=c"

headers = {
    "Content-Type": " application/json"
}


def getdata():
    responese = requests.get(url, headers).text
    responese = json.loads(responese)
    all = len(responese['value']['matchInfoList'])
    for j in range(0, all):
        day1 = responese['value']['matchInfoList'][j]['businessDate']
        print(day1)
        dslen = len(responese['value']['matchInfoList'][j]['subMatchList'])
        for i in range(0, dslen):
            num = responese['value']['matchInfoList'][j]['subMatchList'][i]['matchNum']
            addname = responese['value']['matchInfoList'][j]['subMatchList'][i]['leagueAbbName']
            zhuname = responese['value']['matchInfoList'][j]['subMatchList'][i]['homeTeamAllName']
            kename = responese['value']['matchInfoList'][j]['subMatchList'][i]['awayTeamAbbName']
            lens = len(responese['value']['matchInfoList'][j]['subMatchList'][i]['oddsList'])
            for z in range(0, lens):
                hh = responese['value']['matchInfoList'][j]['subMatchList'][i]['oddsList'][z]['poolCode']
                if z == 0 and hh == "HHAD":
                    rasheng = responese['value']['matchInfoList'][j]['subMatchList'][i]['oddsList'][0]['a']
                    rhsheng = responese['value']['matchInfoList'][j]['subMatchList'][i]['oddsList'][0]['h']
                    rd = responese['value']['matchInfoList'][j]['subMatchList'][i]['oddsList'][0]['d']
                    rang1 = responese['value']['matchInfoList'][j]['subMatchList'][i]['oddsList'][0]['goalLine']
                elif z == 1 and hh == "HAD":
                    asheng = responese['value']['matchInfoList'][j]['subMatchList'][i]['oddsList'][1]['a']
                    hsheng = responese['value']['matchInfoList'][j]['subMatchList'][i]['oddsList'][1]['h']
                    d = responese['value']['matchInfoList'][j]['subMatchList'][i]['oddsList'][1]['d']
                    rang = responese['value']['matchInfoList'][j]['subMatchList'][i]['oddsList'][1]['goalLine']
                elif z == 0 and hh == "HAD":
                    asheng = responese['value']['matchInfoList'][j]['subMatchList'][i]['oddsList'][0]['a']
                    hsheng = responese['value']['matchInfoList'][j]['subMatchList'][i]['oddsList'][0]['h']
                    d = responese['value']['matchInfoList'][j]['subMatchList'][i]['oddsList'][0]['d']
                    rang1 = responese['value']['matchInfoList'][j]['subMatchList'][i]['oddsList'][0]['goalLine']
                elif z == 1 and hh == "HHAD":
                    rasheng = responese['value']['matchInfoList'][j]['subMatchList'][i]['oddsList'][1]['a']
                    rhsheng = responese['value']['matchInfoList'][j]['subMatchList'][i]['oddsList'][1]['h']
                    rd = responese['value']['matchInfoList'][j]['subMatchList'][i]['oddsList'][1]['d']
                    rang = responese['value']['matchInfoList'][j]['subMatchList'][i]['oddsList'][1]['goalLine']
                else:
                    break
            print("-------------" + addname + "-------------")
            print(num)
            print(zhuname + "-" + kename + "[0]   胜 " + hsheng + "--平 " + d + "--负 " + asheng)
            print(zhuname + "-" + kename + "[" + rang + rang1 + "]   胜 " + rhsheng + "--平 " + rd + "--负 " + rasheng)


def amidithion():
    starttime = date.today() + timedelta(days=-1)
    endtime = time.strftime("%Y-%m-%d", time.localtime())
    url = "https://webapi.sporttery.cn/gateway/jc/football/getMatchResultV1.qry?matchPage=1&pcOrWap=0&leagueId=&matchBeginDate=" + str(
        starttime) + "&matchEndDate=" + str(endtime)
    response = requests.get(url).text
    print(url)
    response = json.loads(response)
    lenght = len(response['value']['matchResult'])
    for i in range(0, lenght):
        day = str(starttime).replace("-", "")
        num = str(response['value']['matchResult'][i]['matchNum'])
        score = response['value']['matchResult'][i]['sectionsNo999']
        win = response['value']['matchResult'][i]['winFlag']
        goalLine = response['value']['matchResult'][i]['goalLine']
        if score == "取消":
            continue
        if win == "A":
            win = "负"
        elif win == "H":
            win = "胜"
        else:
            win = "平"
        a = int(score[2])
        if goalLine[0] == "+":
            h = int(score[0]) + int(goalLine[1])
        else:
            h = int(score[0]) - int(goalLine[1])
        if a > h:
            rwin = "让负"
        elif a < h:
            rwin = "让胜"
        else:
            rwin = "让平"
        id = str(day + num)
        print(num + "，比分：" + score + "比赛结果：" + win + "，让球结果：" + rwin)
if __name__ == '__main__':
    getdata()
    amidithion()