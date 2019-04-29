import numpy as np
import matplotlib as mpl
from sklearn import metrics
from group_11.group_11 import myRF


def caculateAUC(data,inTree):
    np.random.seed(0)
    labels = list()
    # x_test = list()
    for x_data in data:
        labels.append(float(x_data[-1]))
    n_class = len(labels)

    # 计算属于各个类别的概率，返回值的shape = [n_samples, n_classes]
    y_predict=list()
    for x_data in data:
        predicRes = myRF.predict(inTree, x_data)
        y_predict.append(float(predicRes))
    fpr, tpr, thresholds = metrics.roc_curve(labels, y_predict)
    auc = metrics.auc(fpr, tpr)
    # fpr, tpr, thresholds = roc_curve(labels, y_predict, pos_label=1)
    # rac_auc = auc(fpr, tpr)
    # print('手动计算auc：', auc)
    # 绘图
    mpl.rcParams['font.sans-serif'] = u'SimHei'
    mpl.rcParams['axes.unicode_minus'] = False
    return fpr,tpr,auc

import plotTree
def caculateRFAUC(testdata,trees):
    # 计算森林中每棵树的AUC并画图
    fpr_list = list()
    tpr_list = list()
    auc_list = list()
    for tree in trees:
        fpr, tpr, auc = caculateAUC(testdata, tree)
        # FPR就是横坐标,TPR就是纵坐标
        fpr_list.append(fpr)
        tpr_list.append(tpr)
        auc_list.append(auc)
    # plotTree.plotAUC(fpr_list, tpr_list, auc_list)
    return auc_list

