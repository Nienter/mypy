import requests
from bs4 import BeautifulSoup

group_id = 'androidx.appcompat'  # 修改为您的组ID
artifact_id = 'appcompat'  # 修改为您的库ID
url = f'https://mvnrepository.com/artifact/{group_id}/{artifact_id}'

# response = requests.get(url, headers={
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
# })
#
# soup = BeautifulSoup(response.text, 'html.parser')
#
# # 找到最新版本号所在的元素
# version_element = soup.find('a', {'class': 'vbtn release'})
#
# # 提取版本号
# latest_version = version_element.text.strip()
#
# print(f'Latest version of {group_id}:{artifact_id} is {latest_version}')
url = "https://mvnrepository.com/artifact/androidx.appcompat/appcompat"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.68"}





response = requests.get(url, headers=headers)

print(response.content)