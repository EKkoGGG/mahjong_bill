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
    player1 = Player(name=names['name1'], amount=info['player1']*unit_price*1.0)
    player2 = Player(name=names['name2'], amount=info['player2']*unit_price*1.0)
    player3 = Player(name=names['name3'], amount=info['player3']*unit_price*1.0)
    player4 = Player(name=names['name4'], amount=info['player4']*unit_price*1.0)
    water = info['water']*unit_price*1.0
    room_pay = info['room_pay']
    room_payer = info['room_payer']
    # 计算房费
    player_list = []
    player_list.append(player1)
    player_list.append(player2)
    player_list.append(player3)
    player_list.append(player4)
    real_room_pay = water - room_pay
    unit_room_pay = real_room_pay/4
    for item in player_list:
        item.real_amount = item.amount
        item.amount += unit_room_pay
    if room_payer == '一号':
        player1.amount += room_pay
        player1.isPayRoom = True
    elif room_payer == '二号':
        player2.amount += room_pay
        player2.isPayRoom = True
    elif room_payer == '三号':
        player3.amount += room_pay
        player3.isPayRoom = True
    elif room_payer == '四号':
        player4.amount += room_pay
        player4.isPayRoom = True
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
        if i + 1 == 4:
            break
        if i < minIndex:
            index = minIndex
            if item.amount == 0:
                continue
            for j,item2 in enumerate(player_list[minIndex:]):
                if item2.amount == abs(item.amount) and item2.repay != abs(item.amount):
                    index = j+minIndex
                    break
            player_list[index].repay += abs(item.amount)
            log = '%s 给 %s %s 元' % (
                item.name, player_list[index].name, abs(item.amount))
            log_list.append(log)
        else:
            if item.repay - item.amount == 0:
                continue
            player_list[i+1].repay += (item.repay - item.amount)
            log = '%s 给 %s %s 元' % (
                item.name, player_list[i+1].name, item.repay - item.amount)
            log_list.append(log)      
    put_text('\n')
    for log_item in log_list:
        put_markdown('> '+log_item)

    out_bill_info(player_list, room_pay, unit_room_pay,water)


def out_header():
    set_env(title='麻将分账')
    put_markdown("""# 麻将分账
    `Good Luck !`
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
    if info['water'] <= 0:
        return ('water', '不能为负数！')
    amount = info['player1'] + info['player2'] + \
        info['player3'] + info['player4'] + info['water']
    if amount != 0:
        return ('room_payer', '数据有误，收支不相等，请检查！')


def out_bill_info(player_list, room_pay, unit_room_pay,water):
    put_text('\n')
    for item in player_list:
        if item.isPayRoom == True:
            item.amount -= room_pay
            if water <= room_pay:
                put_markdown('`%s 支付房费 %s 元，扣除水钱 %s 元后，人均房费 %s 元`'
                % (item.name,room_pay,water,abs(unit_room_pay)))
            else:
                put_markdown('`%s 支付房费 %s 元，水钱 %s 元，人均收入剩余水钱 %s 元`'
                % (item.name,room_pay,water,abs(unit_room_pay)))                
            player_list.sort(key=lambda e: e.amount)
            break
    put_table([
        [player_list[3].name, player_list[3].real_amount,
            unit_room_pay, player_list[3].amount],
        [player_list[2].name, player_list[2].real_amount,
            unit_room_pay, player_list[2].amount],
        [player_list[1].name, player_list[1].real_amount,
            unit_room_pay, player_list[1].amount],
        [player_list[0].name, player_list[0].real_amount,
            unit_room_pay, player_list[0].amount]
    ], header=['玩家昵称', '胜负（元）', '房费（元）', '净收入（元）'])


class Player(object):
    def __init__(self, name, amount, real_amount=0, repay=0, isPayRoom=False):
        self.name = name
        self.amount = amount
        self.real_amount = real_amount
        self.repay = repay
        self.isPayRoom = isPayRoom


if __name__ == '__main__':
    start_server(main, port=9003)
