import csv
import matplotlib.pyplot as plt

Zb = [[], []]
# with open('F:/zhengwangwork/test csv/4.csv','rb')as f:
#     reader=csv.reader(f)
#     for row in reader:
#         print(row[0])
file = open('gold.csv','r', encoding='UTF-8')  # 打开csv文件
reader = csv.reader(file)  # 读取csv文件
data = list(reader)  # 将csv数据转化为列表
length_h = len(data)  # 得到数据行数
lenght_l = len(data[0])  # 得到每行长度

x = list()
y = list()

for i in range(0, length_h):  # 从第一行开始读取
    x.append(data[i][0])  # 将第一列数据从第一行读取到最后一行付给列表x
    y.append(data[i][2])  # 将第三列数据从第一行读取到最后一行付给列表y
plt.plot(x, y)  # 绘制折线图
plt.show()  # 显示折线图