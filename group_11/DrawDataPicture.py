import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data_all = pd.read_csv('DataSet.csv', encoding='gbk')
# GRE Score成绩分布图
fig = sns.distplot(data_all['GRE Score'], kde=False)
plt.title("Distribution of GRE Scores")
plt.show()

# University Rating分布图
fig = sns.distplot(data_all['University Rating'], kde=False)
plt.title("Distribution of University Rating")
plt.show()

# CGPA成绩分布图
fig = sns.distplot(data_all['CGPA'], kde=False)
plt.title("Distribution of CGPA")
plt.show()

# GRE Score vs CGPA成绩分布图
fig = sns.regplot(x="GRE Score", y="CGPA", data=data_all)
plt.title("GRE Score vs CGPA")
plt.show()

# CGPA vs University Rating分布图
sns.lineplot(y="CGPA", x="University Rating",hue="Research",data=data_all)
plt.show()