#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Time : 2021/1/28 17:22
# @Author: 王者风范
# @File : sliding.py

'''最大滑动窗口'''
def maxSlidingWindow1(self, nums,k):
    if not nums: return []
    window,res = [], []
    for i,x in enumerate(nums):
        if i>=k and window[0] <=i-k:
            window.pop(0)
        while window and nums[window[-1]]<=x:
            window.pop()
        window.append(i)
        if i>=k-1:
            res.append(nums[window[0]])
    return res


'''Valid Anagram'''
def isAnagram1(self, s, t):
    dic1, dic2 = {}, {}
    for item in s:
        dic1[item] = dic1.get(item,0) +1
    for item in t:
        dic2[item] = dic2.get(item,0) +1
    return dic1 == dic2

def isAnagram2(self,s,t):
    dic1,dic2 = [0]*26, [0]*26
    for item in s:
        dic1[ord(item)-ord('a')] += 1
    for item in t:
        dic2[ord(item)-ord('a')] += 1
    return dic1 == dic2