import csv

import pandas as pd
from group_11.group_11 import SMOTE
import matplotlib.pyplot as plt
groupArray = []
success = 0
fail = 0
with open("DataSet2.csv") as csvFile:
    for line in csvFile:
        groupArray.append(line.split(","))

    with open("DataSet2.csv", 'w+', newline='') as f1:
        writer = csv.writer(f1)
        header = ['GRE Score', 'TOEFL Score', 'University Rating', 'SOP', 'LOR', 'CGPA', 'Research', 'Level']
        writer.writerow(header)
        for row in range(len(groupArray)):
            if row != 0:
                tempArray = []
                for j in range(8):
                    tempArray.append(str(groupArray[row][j]))  #行数据
                print(tempArray)
            if row != 0:
                num = float(groupArray[row][7])
                if num <= 0.60:
                    groupArray[row][7] = "0"
                    tempArray[len(tempArray)-1]='0'
                    writer.writerow(tempArray)
                    fail = fail + 1
                elif num > 0.60:
                    success = success + 1
                    groupArray[row][7] = "1"
                    tempArray[len(tempArray) - 1] = '1'
                    writer.writerow(tempArray)
        print(tempArray)

print("Admit的个数:", success, "  Fail的个数:", fail)


def plotDistribution(success, fail):
    # 画图
    plt.xticks((0, 1), (u"Admit(1)", u"Not Admit(0)"))
    # rects = plt.bar(left=(0, 1), height=(success, fail), width=0.4, align="center",color='rgby')    # 钟惠原来的
    rects = plt.bar([0, 1], (success, fail), width=0.4, align="center", color='rgby')               # 玉敏改过的
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2., 1.03 * height, "%s" % float(height))
    plt.show()
plotDistribution(success, fail)

# 调用SMOTE处理少数类样本操作函数
data = pd.read_csv('DataSet2.csv', low_memory=False)
data=SMOTE.smote(data, 7, 300, 5, 5, 10, 'mean', 97)

#  #保存到新数据文件DataSet3
def writeList2CSV(myList,filePath):
    try:
        file=open(filePath,'w')
        for items in myList:
            for item in items:
                file.write(str(item))
                file.write(",")
            file.write("\n")
    except Exception :
        print("数据写入失败，请检查文件路径及文件编码是否正确")
    finally:
        file.close();# 操作完成一定要关闭
dataset = data.values
List = [['GRE Score', 'TOEFL Score', 'University Rating', 'SOP', 'LOR', 'CGPA', 'Research', 'Level']]

for k in dataset:
    i=0
    temp=[]
    for j in k:
        temp.append(j)
        i=i+1
    List.append(temp)

writeList2CSV(List,'DataSet3.csv')

# 统计新数据集DataSet3的样本个数
groupArray2 = []
success2 = 0
fail2 = 0
with open("DataSet3.csv") as csvFile:
    for line in csvFile:
        groupArray2.append(line.split(","))
    for row in range(len(groupArray2)):
         if row != 0:
                num = float(groupArray2[row][7])
                if num == 1.0:
                    success2 = success2 + 1
                elif num == 0.0:
                    fail2 = fail2 + 1

    print("Admit的个数:", success2, "  Fail的个数:", fail2)
    plotDistribution(success2, fail2)