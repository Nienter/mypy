import requests
from bs4 import BeautifulSoup

# 获取歌曲页面的 HTML
url = 'https://music.163.com/song?id=1398663417'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}
response = requests.get(url, headers=headers)

# 解析 HTML
soup = BeautifulSoup(response.text, 'html.parser')

# 获取歌曲名
song_name = soup.find('em', class_='f-ff2')
print('歌曲名：', song_name)

# 获取歌手名
singer_name = soup.find('div', class_='cnt').find_all('a')[1].string
print('歌手名：', singer_name)

# 获取歌词（需要进入歌词页面）
song_id = url.split('=')[-1]
lyric_url = f'https://music.163.com/api/song/lyric?id={song_id}&lv=-1&kv=-1&tv=-1'
lyric_response = requests.get(lyric_url, headers=headers)
lyric_json = lyric_response.json()
if 'lrc' in lyric_json.keys():
    lyric = lyric_json['lrc']['lyric']
    print('歌词：', lyric)
else:
    print('未找到歌词')