"""
麻将分账
"""
from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import set_env


def main():
    put_markdown("""# 麻将分账
    Good Luck !
    """, strip_indent=4)
    info = input_group('分账信息：', [
        input('一张牌多少钱（元）', name='unit_price', type=NUMBER, value='2'),
        input('一号胜负（个）', name='win1', type=NUMBER),
        input('二号胜负（个）', name='win2', type=NUMBER),
        input('三号胜负（个）', name='win3', type=NUMBER),
        input('四号胜负（个）', name='win4', type=NUMBER),
        input('水钱（个）', name='water', type=NUMBER),
        input('房费（元）', name='room_pay', type=FLOAT),
        select('付房费者', name='room_payer', options=['一号', '二号', '三号', '四号'])
    ])

    unit_price = info['unit_price']
    win1 = Player('一号', info['win1']*unit_price)
    win2 = Player('二号', info['win2']*unit_price)
    win3 = Player('三号', info['win3']*unit_price)
    win4 = Player('四号', info['win4']*unit_price)

    win1.amount = info['win1']*unit_price
    win2.amount = info['win2']*unit_price
    win3.amount = info['win3']*unit_price
    win4.amount = info['win4']*unit_price
    water = info['water']*unit_price
    room_pay = info['room_pay']
    room_payer = info['room_payer']
    real_room_pay = 0
    if water < room_pay:
        real_room_pay = room_pay - water
    unit_room_pay = real_room_pay/4
    win1.amount -= unit_room_pay
    win2.amount -= unit_room_pay
    win3.amount -= unit_room_pay
    win4.amount -= unit_room_pay
    if room_payer == '一号':
        win1.amount += room_pay
    elif room_payer == '二号':
        win2.amount += room_pay
    elif room_payer == '三号':
        win3.amount += room_pay
    elif room_payer == '四号':
        win4.amount += room_pay


    win_list = []
    win_list.append(win1)
    win_list.append(win2)
    win_list.append(win3)
    win_list.append(win4)

    win_list.sort(key=lambda e: e.amount)

    minIndex = 0
    log_list = []
    log = ''
    for item in win_list:
        if item.amount > 0:
            break
        minIndex += 1
    if minIndex == win_list.count:
        log = '此账单不用分账，每位参与人都收支平衡'

    for i, item in enumerate(win_list):
        if i + 1 == win_list.count:
            break
        if i < minIndex:
            if item.amount == 0:
                continue
            win_list[minIndex].repay += abs(item.amount)
            log = '%s 给 %s %s 元' % (
                item.name, win_list[minIndex].name, abs(item.amount))
            log_list.append(log)
        else:
            if item.repay - item.amount == 0:
                continue
            win_list[i+1].repay += (item.repay - item.amount)
            log = '%s 给 %s %s 元' % (
                item.name, win_list[i+1].name, item.repay - item.amount)
            log_list.append(log)
    for log_item in log_list:
        put_markdown(log_item)


class Player(object):
    def __init__(self, name, amount, repay=0):
        self.name = name
        self.amount = amount
        self.repay = repay

if __name__ == '__main__':
    start_server(main, port=9003)