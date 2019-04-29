# smote unbalance dataset
from __future__ import division
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
import sys
import pickle


"""
    Parameters
    ----------
    data : 原始数据
    tag_index : 因变量所在的列数，以0开始
    max_amount : 少类别类想要达到的数据量
    std_rate : 多类:少类想要达到的比例
    #如果max_amount和std_rate同时定义优先考虑max_amount的定义
    kneighbor : 生成数据依赖kneighbor个附近的同类点，建议不超过5个
    kdistinctvalue : 认为每列不同元素大于kdistinctvalue及为连续变量，否则为class变量
    method ： 生成方法
"""


# smote unbalance dataset
def smote(data, tag_index, max_amount,std_rate, kneighbor, kdistinctvalue, method,num):
    try:
        data = pd.DataFrame(data)
        #print(data)
    except:
        raise ValueError
    case_state = data.iloc[:, tag_index].groupby(data.iloc[:, tag_index]).count()
    #print(case_state)
    #print(min(case_state))    #只是输出最小数字38
    #aimed_date = data[data["Chance of Admit"] == 6]
    #print(aimed_date)
    case_rate = max(case_state) / min(case_state)
    location = []
    if case_rate < 0.5:
        print('不需要smote过程')
        return data
    else:
        # 拆分不同大小的数据集合
        less_data = np.array(
            data[data.iloc[:, tag_index] == np.array(case_state[case_state == num].index)[0]])
        # print(less_data)
        #more_data = np.array(
         #   data[data.iloc[:, tag_index] == np.array(case_state[case_state == max(case_state)].index)[0]])
        #print(more_data)

        # 找出每个少量数据中每条数据k个邻居
        neighbors = NearestNeighbors(n_neighbors=kneighbor,algorithm='auto').fit(less_data)

        for i in range(len(less_data)):
            point = less_data[i, :]
            location_set = neighbors.kneighbors([less_data[i]], return_distance=False)[0]
            location.append(location_set)
        # 确定需要将少量数据补充到上限额度
        # 判断有没有设定生成数据个数，如果没有按照std_rate(预期正负样本比)比例生成
        if max_amount > 0:
            amount = max_amount
        else:
            amount = int(max(case_state) / std_rate)
        # 初始化，判断连续还是分类变量采取不同的生成逻辑
        times = 0
        continue_index = []  # 连续变量
        class_index = []  # 分类变量
        for i in range(less_data.shape[1]):
            if len(pd.DataFrame(less_data[:, i]).drop_duplicates()) > kdistinctvalue:
                continue_index.append(i)
            else:
                class_index.append(i)
        case_update = list()
        location_transform = np.array(location)
        while times < amount:
            # 连续变量取附近k个点的重心，认为少数样本的附近也是少数样本
            new_case = []
            pool = np.random.permutation(len(location))[1]
            neighbor_group = location_transform[pool]
            if method == 'mean':
                new_case1 = less_data[list(neighbor_group), :][:, continue_index].mean(axis=0)

                # 解决小数点问题
                # new_case1[len(new_case1) - 1] = float(int(new_case1[len(new_case1) - 1])
                # 解决小数点问题
                # new_case1[len(new_case1)-1] = float(int(new_case1[len(new_case1)-1]))
                new_case1[len(new_case1) - 1] = round(new_case1[len(new_case1) - 1], 2)  # round有时会五进有时不进
                new_case1[0] = int(new_case1[0] + 0.5)  # 第一列
                new_case1[1] = int(new_case1[1] + 0.5)  # 第二列
            # 连续样本的附近点向量上的点也是异常点
            if method == 'random':
                away_index = np.random.permutation(len(neighbor_group) - 1)[1]
                neighbor_group_removeorigin = neighbor_group[1:][away_index]
                new_case1 = less_data[pool][continue_index] + np.random.rand() * (
                    less_data[pool][continue_index] - less_data[neighbor_group_removeorigin][continue_index])
            # 分类变量取mode
            new_case2 = np.array(pd.DataFrame(less_data[neighbor_group, :][:, class_index]).mode().iloc[0, :])
            # new_case = list(new_case1) + list(new_case2)
            # 解决列数混乱的问题
            for i in range(len(new_case1) + len(new_case2)):
                new_case.append('');
            for i in range(len(new_case1)):
                new_case[continue_index[i]] = new_case1[i]
            for j in range(len(new_case2)):
                new_case[class_index[j]] = new_case2[j]
            # new_case = list(new_case1) + list(new_case2)
            new_case = list(new_case)

            if times == 0:
                case_update = new_case
            else:
                case_update = np.c_[case_update, new_case]
            #print('已经生成了%s条新数据，完成百分之%.2f' % (times, times * 100 / amount))
            times = times + 1
        less_origin_data = np.hstack((less_data[:, continue_index], less_data[:, class_index]))
#        more_origin_data = np.hstack((more_data[:, continue_index], more_data[:, class_index]))
        data_res = np.vstack((data,  np.array(case_update.T)))  #将新增的数据追加
        #data_res = np.vstack((more_origin_data, less_origin_data, np.array(case_update.T)))

        label_columns = [1] * (
                less_origin_data.shape[0] + np.array(case_update.T).shape[0])
        #label_columns = [0] * more_origin_data.shape[0] + [1] * (
        #less_origin_data.shape[0] + np.array(case_update.T).shape[0])
        data_res = pd.DataFrame(data_res)
        # print(data_res)
    return data_res