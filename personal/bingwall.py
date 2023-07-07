import json
import urllib.request
from datetime import date

import requests
import os.path
import ctypes
import sys

print(sys.path)


# 请求网页，跳转到最终 img 地址
def get_img_url(raw_img_url="https://bing.biturl.top/?resolution=3840"):
    sys.path.append("E:\\pywork\\venv\\Lib\\site-packages\\requests")
    r = requests.get(raw_img_url)
    img_url = r.text  # 得到图片文件的网址
    data = json.loads(img_url)['url']
    print('img_url:', data)

    return data


def save_img(img_url, dirname):
    # 保存图片到磁盘文件夹dirname中
    try:
        if not os.path.exists(dirname):
            print('文件夹', dirname, '不存在，重新建立')
            # os.mkdir(dirname)
            os.makedirs(dirname)
        today = str(date.today())
        # 获得图片文件名，包括后缀
        basename = today+".jpg"
        # 拼接目录与文件名，得到图片路径
        filepath = os.path.join(dirname, basename)
        # 下载图片，并保存到文件夹中
        urllib.request.urlretrieve(img_url, filepath)
    except IOError as e:
        print('文件操作失败', e)
    except Exception as e:
        print('错误 ：', e)
    print("Save", filepath, "successfully!")

    return filepath


def set_img_as_wallpaper(filepath):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, filepath, 0)


if __name__ == '__main__':
    dirname = "E:\\bingImg"  # 图片要被保存在的位置
    img_url = get_img_url()
    filepath = save_img(img_url, dirname)  # 图片文件的路径
    set_img_as_wallpaper(filepath)
