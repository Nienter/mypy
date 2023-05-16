import os

import requests
from lxml import etree
from requests.exceptions import RequestException


def get_page(url):
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/99.0.4844.84 Safari/537.36',
            'accept-language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
            'cache-control': 'max-age=0',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                      '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9 '
        }
        response = requests.get(url=url, headers=headers)
        # 更改编码方式，否则会出现乱码的情况
        response.encoding = "utf-8"
        # print(response.status_code)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_page(html):
    try:
        global count
        count += 1
        res = etree.HTML(html)

        red = res.xpath('//*[@class="ball_red"]//text()')
        blue = res.xpath('//*[@class="ball_blue"]//text()')

        # print(red + blue)
        dd = list(red)
        # dd.append(num)
        source.writelines(str(dd) + "\n")

        # sums(red+blue)
    except Exception as e:
        pass


def main(my_num):
    ssq_url = 'https://kaijiang.500.com/shtml/ssq/{}.shtml'.format(str(my_num))
    dlt_url = 'https://kaijiang.500.com/shtml/dlt/{}.shtml'.format(str(my_num))
    html = get_page(dlt_url)
    # print(html)
    parse_page(html)


def findStr(text):
    t = open("b.txt", "a")
    with open("a.txt", 'r') as f:
        counts = 0
        for line in f.readlines():
            time = line.count(text)
            # if time != 0:
            # print(line)
            counts += time
        print("%s出现的次数：%d" % (text, counts))
        if counts <= 5:
            t.write("%s %d\n" % (text, counts))
            # t.close()

    t.close()


class ndder:
    count = 0
    name = ''

    def __init__(self, name, count):
        self.count = count
        self.name = name


def filterNum():
    er = open("b.txt", "r")
    er.read()


# def get_last_line(inputfile):
#     global lo
#     filesize = os.path.getsize(inputfile)
#     blocksize = 1024
#     dat_file = open(inputfile, 'r')
#     last_line = ""
#
#     lines = dat_file.readlines()
#     count = len(lines)
#     if count > 60:
#         num = 60
#     else:
#         num = count
#     i = 1
#     lastre = []
#     for i in range(1, 2):
#         if lines:
#             n = -i
#             last_line = lines[n].strip()
#             # print "last line : ", last_line
#             dat_file.close()
#             # print i
#             # lastre.append(last_line)
#             print(last_line)
#
#             last_line = last_line.replace('[', '').replace(']', '').replace('\'', '')
#             # print(last_line.split(',')[0])
#             lo = []
#             for num in range(0, len(last_line.split(','))):
#                 s = last_line.split(',')[num]
#                 lo.append(int(s))
#             print(lo)
#     return lo


def alter(file, old_str, new_str):
    """
    替换文件中的字符串
    :param file:文件名
    :param old_str:就字符串
    :param new_str:新字符串
    :return:
    """
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if old_str in line:
                line = line.replace(old_str, new_str)
            file_data += line
    with open(file, "w", encoding="utf-8") as f:
        f.write(file_data)


if __name__ == '__main__':
    start = 22000

    source = open("a.txt", "w")
    for num in range(start, 22038):
        main(num)
    source.close()

    count = 0
    text = '0'
    for u in range(36):
        if u < 10:
            if u != 0:
                u = str("0" + str(u))
        result = open("a.txt", "r")
        text = str(u)

    findStr(text)

    # print(get_last_line("a.txt"))
    # li = list(get_last_line('a.txt'))
    # t = len(li)
    # for num in range(0, t):
    #     a = li[num]
    #     fl = open('b.txt', 'r')
    #     alter('b.txt', str(a), "kkkk")
    # text = '18'

    # print("爬取的数目为："+str(count))
