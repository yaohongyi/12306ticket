#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
作者：都君大魔王
描述:
'''
import requests,re,pymysql

class Station(object):
    def __init__(self):
        pass
    def query_station_from_12306(self, station_version='1.9002'):
        '''
        查询12306网站的车站信息，返回的是车站信息字典，中文车站名&车站代号
        :param station_version: 获取车站信息接口地址版本号（12306不断的升级车站信息接口）
        :return: 字典形式的车站信息
        '''
        url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
        # 获取车站接口返回的车站信息
        response = requests.get(url, verify=False, params=station_version).text
        # 利用正则表达式提取车站中文名和代号
        reg = re.compile(u"([\u4e00-\u9fa5]*)\|([A-Z]*)\|")
        station_list = re.findall(reg, response)
        # 因为正则表达式提取出来的是由元组组成的列表，利用dict转换成字典
        station_dict = dict(station_list)
        return station_dict
    def db_operate(self, station_name, operate_type='select', data=None, host='127.0.0.1', port=3306, user='root',
                     passwd='123456', db='12306ticket', charset='utf8'):
        '''
        对数据库station表的相关操作
        :param operation_type: 操作数据库类型。insert更新车站信息，select查询车站信息。
        :param data: 12306车站接口返回的数据
        :param station_name: 车站中文名
        :param host: 数据库IP
        :param port: 数据库端口
        :param user: 数据库访问用户名
        :param passwd: 密码
        :param db: 库名
        :param charset: 数据库编码方式 
        :return: 如果操作类型是查询车站信息，且车站信息存在，则返回车站代码
        '''
        conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
        cur = conn.cursor()
        if operate_type == 'insert':
            cur.execute("delete from station")
            insert_sql = "insert into station(station_name,code) VALUES(%s,%s)"
            for i in data:
                cur.execute(insert_sql, (i, data[i]))
        if operate_type == 'select':
            # 执行查询语句并返回受影响行数
            code = cur.execute("select code from station where station_name=%s", station_name)
            # 如果查询到了数据，则返回车站代号，查询到的数据是由元组组成的列表，
            if code:
                return cur.fetchone()[0]
            else:
                return