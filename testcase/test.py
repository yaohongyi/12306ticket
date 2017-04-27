#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, re

url = "https://kyfw.12306.cn/otn/leftTicket/query?" \
      "leftTicketDTO.train_date=2017-05-26&leftTicketDTO.from_station=SZQ&" \
      "leftTicketDTO.to_station=NCG&purpose_codes=ADULT"
response = requests.get(url, verify=False).json()
for i in response['data']['result']:
      print i
