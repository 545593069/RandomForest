import matplotlib.pyplot as plt
# 算法正确率见'算法改进前后正确率对比-运行结果.txt'文件
# 树个数
treeNum_list = [20,30,40,50,60,70,80]
# 改进前算法模型正确率（%）
original_acc=[90.60402684563759 ,91.94630872483222 ,92.61744966442953 ,93.28859060402685 ,92.61744966442953 ,
              92.61744966442953 ,93.28859060402685]
# 改进后算法模型正确率（%）
improved_acc=[94.56066945606695,93.30543933054393,94.56066945606695 ,94.97907949790795 ,94.14225941422593 ,
              94.14225941422593 ,95.81589958158996]

# plt.ylim(top=100.0, bottom=0.0)
plt.plot(treeNum_list,original_acc,marker='o', mec='r', mfc='w',label='Original Algorithm')
plt.plot(treeNum_list, improved_acc, marker='*', ms=10,label=u'Improved Algorithm')
plt.legend()
plt.grid()
plt.xlabel('number of tree') #X轴标签
plt.ylabel("accuracy rate") #Y轴标签
plt.title("Comparision of Accuracy Rate on DataSet of Admission_Predict") #标题
plt.show()
