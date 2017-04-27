# coding:utf-8

import requests
from prettytable import PrettyTable
from public.station import Station

class Ticket(object):
    def __init__(self, purpose_codes='ADULT'):
        '''
        车次查询条件关键字
        :param train_date: 乘车日期
        :param from_station: 始发站
        :param to_station: 到达站
        :param purpose_codes: 乘客类型
        '''
        station = Station()
        # 提示用户输入始发站，然后到数据库中查询是否存在对应的车站代号，不存在则提示重新输入
        from_station = station.db_operate(raw_input('请输入始发站：'))
        while from_station == None:
            from_station = station.db_operate(raw_input('起点站不存在，请重新输入始发站：'))
        # 提示用户输入到达站，然后到数据库中查询是否存在对应的车站代号，不存在则提示重新输入
        to_station = station.db_operate(raw_input('请输入到达站：'))
        while to_station == None:
            to_station = station.db_operate(raw_input('到达站不存在，请输入到达站：'))
        train_date = raw_input('请输入乘车日期：')
        self.kwargs = {}
        self.kwargs['train_date'] = train_date
        self.kwargs['from_station'] = from_station
        self.kwargs['to_station'] = to_station
        self.kwargs['purpose_codes'] = purpose_codes

    def query_ticket(self):
        '''
        根据“始发站”“到达站”“乘车日期”“乘客类型”查询车次信息
        :return: 返回原始接口车次信息
        '''
        # 拼接带请求参数的查询车次url
        url = "https://kyfw.12306.cn/otn/leftTicket/query?" \
              "leftTicketDTO.train_date=%(train_date)s" \
              "&leftTicketDTO.from_station=%(from_station)s" \
              "&leftTicketDTO.to_station=%(to_station)s" \
              "&purpose_codes=%(purpose_codes)s" % self.kwargs
        print url
        response = requests.get(url, verify=False).json()
        train_total = len(response['data'])
        print '根据您提供的乘车信息共查询到%d趟车次，车次信息如下：' % train_total
        table = PrettyTable(['车次', '出发站', '到达站', '历时', '商务座','一等座', '二等座', '软卧', '硬卧', '硬座', '无座'])
        for i in range(train_total):
            station_train_code = response['data'][i]['queryLeftNewDTO']['station_train_code']
            from_station_name = response['data'][i]['queryLeftNewDTO']['from_station_name']
            to_station_name = response['data'][i]['queryLeftNewDTO']['to_station_name']
            take_time = response['data'][i]['queryLeftNewDTO']['lishi']
            swz_num = response['data'][i]['queryLeftNewDTO']['swz_num']
            zy_num = response['data'][i]['queryLeftNewDTO']['zy_num']
            ze_num = response['data'][i]['queryLeftNewDTO']['ze_num']
            rw_num = response['data'][i]['queryLeftNewDTO']['rw_num']
            yw_num = response['data'][i]['queryLeftNewDTO']['yw_num']
            yz_num = response['data'][i]['queryLeftNewDTO']['yz_num']
            wz_num = response['data'][i]['queryLeftNewDTO']['wz_num']
            # 给table表格插入数据
            table.add_row([station_train_code, from_station_name, to_station_name, take_time, swz_num,
                           zy_num, ze_num, rw_num, yw_num, yz_num, wz_num])
        print table
        return response
