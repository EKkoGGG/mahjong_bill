"""
麻将分账
"""
from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import set_env


def main():
    # 输出头部内容
    out_header()
    # 输入分账信息
    info = input_bill_info()
    # 输入玩家昵称
    names = input_names()
    # 获取分账信息
    unit_price = info['unit_price']
    player1 = Player(names['name1'], info['player1']*unit_price)
    player2 = Player(names['name2'], info['player2']*unit_price)
    player3 = Player(names['name3'], info['player3']*unit_price)
    player4 = Player(names['name4'], info['player4']*unit_price)
    water = info['water']*unit_price
    room_pay = info['room_pay']
    room_payer = info['room_payer']
    # 计算房费
    player_list = []
    player_list.append(player1)
    player_list.append(player2)
    player_list.append(player3)
    player_list.append(player4)
    real_room_pay = room_pay - water
    if water < room_pay:
        real_room_pay = -real_room_pay
    unit_room_pay = real_room_pay/4
    for item in player_list:
        item.amount += unit_room_pay
    if room_payer == '一号':
        player1.amount += room_pay
    elif room_payer == '二号':
        player2.amount += room_pay
    elif room_payer == '三号':
        player3.amount += room_pay
    elif room_payer == '四号':
        player4.amount += room_pay
    player_list.sort(key=lambda e: e.amount)
    # 分账计算
    minIndex = 0
    log_list = []
    log = ''
    for item in player_list:
        if item.amount > 0:
            break
        minIndex += 1

    for i, item in enumerate(player_list):
        if i + 1 == player_list.count:
            break
        if i < minIndex:
            if item.amount == 0:
                continue
            player_list[minIndex].repay += abs(item.amount)
            log = '%s 给 %s %s 元' % (
                item.name, player_list[minIndex].name, abs(item.amount))
            log_list.append(log)
        else:
            if item.repay - item.amount == 0:
                continue
            player_list[i+1].repay += (item.repay - item.amount)
            log = '%s 给 %s %s 元' % (
                item.name, player_list[i+1].name, item.repay - item.amount)
            log_list.append(log)
    for log_item in log_list:
        put_markdown(log_item)


def out_header():
    set_env(title='麻将分账')
    put_markdown("""# 麻将分账
    Good Luck !
    """, strip_indent=4)


def input_bill_info():
    return input_group('分账信息：', [
        input('一张牌多少钱（元）', name='unit_price', type=NUMBER, value='2'),
        input('一号胜负（个）', name='player1', type=NUMBER),
        input('二号胜负（个）', name='player2', type=NUMBER),
        input('三号胜负（个）', name='player3', type=NUMBER),
        input('四号胜负（个）', name='player4', type=NUMBER),
        input('水钱（个）', name='water', type=NUMBER),
        input('房费（元）', name='room_pay', type=FLOAT),
        select('付房费者', name='room_payer', options=['一号', '二号', '三号', '四号'])
    ], validate=check_form)


def input_names():
    return input_group('玩家昵称：', [
        input('一号昵称', name='name1', type=TEXT, value='一号'),
        input('二号昵称', name='name2', type=TEXT, value='二号'),
        input('三号昵称', name='name3', type=TEXT, value='三号'),
        input('四号昵称', name='name4', type=TEXT, value='四号'),
    ])


def check_form(info):
    if info['unit_price'] <= 0:
        return ('unit_price', '不能为负数！')
    amount = info['player1'] + info['player2'] + \
        info['player3'] + info['player4'] + info['water']
    if amount != 0:
        return ('room_payer', '数据有误，收支不相等，请检查！')


class Player(object):
    def __init__(self, name, amount, repay=0):
        self.name = name
        self.amount = amount
        self.repay = repay


if __name__ == '__main__':
    start_server(main, port=9003)
