from selenium import webdriver
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup


# group_id = 'androidx.appcompat'  # 修改为您的组ID
# artifact_id = 'appcompat'  # 修改为您的库ID

def getLatestVersion(group_id, artifact_id):
    url = f'https://mvnrepository.com/artifact/{group_id}/{artifact_id}'
    # url = 'https://mvnrepository.com/artifact/androidx.appcompat/appcompat'  # 这里是Spring Boot库的URL
    options = Options()
    options.use_chromium = True
    options.add_argument("headless")
    options.add_argument("disable-gpu")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    driver = webdriver.Edge(options=options)  # 这里使用Edge浏览器
    # for i in range(10):
    driver.get(url)
    html = driver.page_source

    print(html)
    soup = BeautifulSoup(html, 'html.parser')
    version_element = soup.find('a', {'class': 'vbtn release'})
    latest_version = version_element.text.strip()
    print(f'{group_id}_{artifact_id}:{latest_version}')


    driver.quit()

if __name__ == '__main__':
    for i in range(10):
         getLatestVersion('org.jetbrains.kotlinx', 'kotlinx-coroutines-android')
