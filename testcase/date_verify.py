#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
作者：都君大魔王
描述:

'''
import re
my_date = raw_input('请输入乘车日期：')
result = True
while result:
    reg = re.compile('[0-9]{3}[1-9]-(1[0-2]|0[1-9])-(0[1-9]|[1-2][0-9]|3[0-1])')
    result = re.search(reg, my_date)
    if result == None:
       my_date = raw_input('日期不正确，请重新输入：')
