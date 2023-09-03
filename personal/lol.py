from lcu_driver import Connector
import datetime

connector = Connector()

name = '蓝火大魔王'  # 在这里修改名字，要登录一个同区的账号


@connector.ready
async def connect(connection):
    summoner = await connection.request('post',
                                        '/lol-summoner/v2/summoners/names',
                                        data=[name])
    summoner = await summoner.json()
    summoner = summoner[0]['puuid']
    match = await connection.request('get',
                                     '/lol-match-history/v1/products/lol/'
                                     + summoner + '/matches')
    history = await match.json()
    for i in history['games']['games']:
        start_time = datetime.datetime.strptime(i['gameCreationDate'][:19],
                                                '%Y-%m-%dT%H:%M:%S')
        start_time = start_time + datetime.timedelta(hours=8)
        start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
        champion_name = await connection.request('get',
                                                 '/lol-champ-select/v1/grid-champions/'
                                                 + str(i['participants'][0]['championId']))
        champion_name = await champion_name.json()
        champion_name = champion_name['name']
        print(start_time, ('\033[31m败\033[0m', '\033[34m胜\033[0m')[i['participants'][0]['stats']['win']],
              '[' + champion_name + ']', str(i['participants'][0]['stats']['kills'])
              + '-' + str(i['participants'][0]['stats']['deaths'])
              + '-' + str(i['participants'][0]['stats']['assists']), i['gameMode'])


connector.start()



