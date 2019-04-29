import matplotlib.pyplot as plt
decisionNode = dict(boxstyle="sawtooth", fc="0.8")

leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")  # 箭头样式

#  centerPt节点中心坐标  parentPt 起点坐标
def plotNode( Nodename, centerPt, parentPt, nodeType):
    creatPlot.ax1.annotate(Nodename, xy=parentPt, xycoords='axes fraction', xytext=centerPt,
                           textcoords='axes fraction', va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)
 # 1 有多少个叶节点，以便确定x轴的长度
def getNumleafs(mytree): # 获得叶节点数目，输入为我们前面得到的树（字典）
    # dict_keys(['index', 'value', 'left', 'right'])
    Numleafs = 0 # 初始化
    # 左子树
    if type(mytree['left']).__name__ == 'dict':
        Numleafs += getNumleafs(mytree['left'])
    else:
        Numleafs += 1
    # 右子树
    if type(mytree['right']).__name__ == 'dict':
        Numleafs += getNumleafs(mytree['right'])
    else:
        Numleafs += 1
    return Numleafs

# 获取树的高度
def getTreeDepth(mytree):
    maxDepth = 0
    thisDepth=0
    # 左子树
    if type(mytree['left']).__name__ == 'dict':  # 判断如果里面的一个value是否还是dict
        thisDepth = 1 + getTreeDepth(mytree['left'])  # 递归调用
    else:
        thisDepth = 1
    if thisDepth > maxDepth:
        maxDepth = thisDepth
    # 右子树
    if type(mytree['right']).__name__ == 'dict':  # 判断如果里面的一个value是否还是dict
        thisDepth = 1 + getTreeDepth(mytree['right'])  # 递归调用
    else:
        thisDepth = 1
    if thisDepth > maxDepth:
        maxDepth = thisDepth
    return maxDepth

def plotMidText(cntrPt, parentPt, txtString):   #  在两个节点之间的线上写上字
    xMid = (parentPt[0]-cntrPt[0])/2.0 + cntrPt[0]
    yMid = (parentPt[1]-cntrPt[1])/2.0 + cntrPt[1]
    creatPlot.ax1.text(xMid, yMid, txtString)  # text() 的使用

def plotTree(myTree, parentPt, nodeName,features):  # 画树
    numleafs = getNumleafs(myTree)
    depth = getTreeDepth(myTree)
    # print('plotTree: ',numleafs,depth)
    # firstStr = list(myTree.keys())[0]
    feaStr = features[myTree['index']]
    valStr = str(myTree['value'])
    firstStr = feaStr +'='+valStr

    cntrPt = (plotTree.xOff+(0.5/plotTree.totalw+float(numleafs)/2.0/plotTree.totalw), plotTree.yOff)
    plotMidText(cntrPt, parentPt, nodeName)

    # plotNode(firstStr, cntrPt, parentPt, decisionNode)
    plotNode(firstStr, cntrPt, parentPt, decisionNode)

    # 左子树
    # secondDict = myTree[firstStr]
    plotTree.yOff = plotTree.yOff - 1.0 / plotTree.totalD  # 减少y的值，将树的总深度平分，每次减少移动一点(向下，因为树是自顶向下画的）
    keys = ['left','right']
    # leftStr = str(myTree['index']) + '<' + str(myTree['value'])
    # rightStr = str(myTree['index']) + '>' + str(myTree['value'])
    str_leafNode = [feaStr +'<'+valStr, feaStr +'>'+valStr]
    i=0
    for key in keys:
        if type(myTree[key]).__name__ == 'dict':
            plotTree(myTree[key], cntrPt, str_leafNode[i],features)
        else:
            plotTree.xOff = plotTree.xOff + 1.0 / plotTree.totalw
            plotNode(myTree[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str_leafNode[i])
        i = i + 1;
    plotTree.yOff = plotTree.yOff + 1.0 / plotTree.totalD

def creatPlot(inTree,features):  # 使用的主函数
    fig = plt.figure(1, facecolor='white')
    plt.figure(figsize=(20,20), facecolor='#ffffcc', edgecolor='#ffffcc')
    fig.clf()  # 清空绘图区
    axprops = dict(xticks=[], yticks=[]) # 创建字典 存储
    creatPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
    plotTree.totalw = float(getNumleafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))  # 创建两个全局变量存储树的宽度和深度
    plotTree.xOff = -0.5/plotTree.totalw # 追踪已经绘制的节点位置 初始值为 将总宽度平分 在取第一个的一半
    plotTree.yOff = 1.0
    plotTree(inTree, (0.5,1.0), '',features)  # 调用函数，并指出根节点源坐标
    plt.show()

import numpy as np
def plotAUC(fpr_list,tpr_list,auc_list):
    for i in range(len(fpr_list)):
        plt.plot(fpr_list[i], tpr_list[i], c='r', lw=2, alpha=0.7, label=u'AUC=%.3f' % auc_list[i])
        plt.plot((0, 1), (0, 1), c='#808080', lw=1, ls='--', alpha=0.7)
    plt.xlim((-0.01, 1.02))
    plt.ylim((-0.01, 1.02))
    plt.xticks(np.arange(0, 1.1, 0.1))
    plt.yticks(np.arange(0, 1.1, 0.1))
    plt.xlabel('False Positive Rate', fontsize=13)
    plt.ylabel('True Positive Rate', fontsize=13)
    plt.grid(b=True, ls=':')
    plt.legend(loc='lower right', fancybox=True, framealpha=0.8, fontsize=12)
    plt.title(u'决策树分类后的ROC和AUC', fontsize=17)
    plt.show()

def plotAUCbar(trees_num,auc_list):
    name_list = list()
    num_list = list()
    for i in range(trees_num):
        name_list.append('T' + str(i))
        num_list.append(round(auc_list[i] * 100, 1))
    rects = plt.bar(range(len(num_list)), num_list, color='rgby')
    # X轴标题
    # index = [0, 1, 2, 3]
    index = list(range(trees_num))
    index = [float(c) + 0.4 for c in index]
    # plt.ylim(ymax=1.0, bott=0.0)
    plt.ylim(top=100.0, bottom=80.0)
    plt.xticks(index, name_list)
    plt.ylabel("arrucay(%)")  # X轴标签
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height, str(height) + '%', ha='center', va='bottom')
    plt.show()

