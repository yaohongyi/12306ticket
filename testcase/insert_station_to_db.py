#!/usr/bin/env python
# -*- coding: utf-8 -*-

from public.station import Station
import pymysql

station = Station()
response = station.query_station_from_12306()
connection_info = {'host':'127.0.0.1', 'port':3306, 'user':'root',
                     'passwd':'123456', 'db':'12306ticket', 'charset':'utf8'}
conn = pymysql.connect(**connection_info)
cur = conn.cursor()
insert_sql = "insert into station(station_name,code) VALUES(%s,%s)"
for i in response:
    cur.execute(insert_sql, (i, response[i]))
conn.commit()
query_data = cur.execute('select * from station')

print cur.fetchall()
conn.close()