#!/usr/bin/python3

'''括号是否匹配1'''
def isValid(self, s):
    stack = []
    paren_map = {')': '(', ']': '[', '}': '{'}
    for c in s:
        if c not in paren_map:
            stack.append(c)
        elif not stack or paren_map[c] != stack.pop():
            return False
    return not stack


'''括号是否匹配2'''
def isValid2(self, s):
    queue1, queue2 = [], []
    paren_map = {')': '(', ']': '[',  '}': '{'}
    for c in s:
        if c not in paren_map:
            queue1.append(c)
        else:
            queue1.reverse()
            while queue1.__len__() != 0:
                queue2.append(queue1.pop())
            if not queue2 or paren_map[c] != queue2.pop():
                return False
    return not queue2





