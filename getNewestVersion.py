import msvcrt
import zipfile
import threading
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor,wait, FIRST_COMPLETED, ALL_COMPLETED

resultList = []
unfoundList = []
alltask = []


def main():
    file = 'C:\\Users\\niu\Desktop\\上传\CartoonCustomSticker.aab'

    dependenciesDict = {}


    threadList = []
    if zipfile.is_zipfile(file):
        print()
        z = zipfile.ZipFile(file, 'r')
        namelist = z.namelist()
        pool = ThreadPoolExecutor(len(namelist))
        for zFile in namelist:
            if zFile.endswith('.version'):
                # print('"' + zFile.split('/').pop()[:-8] + '":"' + str(z.read(zFile), encoding='utf-8').strip() + '",')
                # print(zFile.split('/').pop()[:-8])
                pair = zFile.split('/').pop()[:-8].split('_')
                # pool.submit(getLatestVersion,pair[0],pair[1])
                # alltask.append(task)
                t = threading.Thread(target=getLatestVersion,args=(pair[0],pair[1]))
                t.start()
                # threadList.append(t)
                # getLatestVersion(pair[0],pair[1])
                # dependenciesDict[pair[0]] = pair[1]

    print('查询中...')
    # t.start()
    # t.join()
    # wait(alltask,return_when=ALL_COMPLETED)

    # for group, artifact in dependenciesDict.items():
        # thread = threading.Thread(target=getLatestVersion, args=(group, artifact))
        # getLatestVersion(group, artifact)
        # threadList.append(thread)

    # for thread in threadList:
    #     thread.start()

    # for thread in threadList:
    #     thread.join()

    print('结果如下:')
    for item in resultList:
        print(item)

    print('\n未查询到的依赖如下:')
    print(unfoundList)

    msvcrt.getch()


def getLatestVersion(group_id, artifact_id):
    global resultList
    global unfoundList
    url = f'https://mvnrepository.com/artifact/{group_id}/{artifact_id}'
    # url = 'https://mvnrepository.com/artifact/androidx.appcompat/appcompat'  # 这里是Spring Boot库的URL
    options = Options()
    options.use_chromium = True
    options.add_argument("headless")
    options.add_argument("disable-gpu")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    driver = webdriver.Edge(options=options)  # 这里使用Edge浏览器
    driver.get(url)
    html = driver.page_source

    # print(f'groupId:{group_id}, artifact:{artifact_id}')

    # print(html)
    soup = BeautifulSoup(html, 'html.parser')
    version_element = soup.find('a', {'class': 'vbtn release'})
    if not version_element is None:
        latest_version = version_element.text.strip()
        print(f'"{group_id}:{artifact_id}":"{latest_version}",')

        resultList.append(f'"{group_id}:{artifact_id}":"{latest_version}",')
    else:
        print(f'{group_id}_{artifact_id}')
        unfoundList.append(f'{group_id}:{artifact_id}')

    driver.quit()


main()

