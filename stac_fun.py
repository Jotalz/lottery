import random
import requests
from bs4 import BeautifulSoup
from constant import *
from tkinter import messagebox
import time


def analyze(url):
    global source
    try:
        if get_value('proxies'):
            #print(get_value('proxies'), '开启代理')
            source = requests.get(url=url, proxies=get_ip(), headers=headers)  # 爬取网页
        else:
            #print(get_value('proxies'), '关闭代理')
            source = requests.get(url=url, headers=headers)  # 爬取网页
            messagebox.showinfo('重要提示', '当前为本地IP模式，请勿频繁刷新或开关软件！否则会被网站监测为爬虫导致IP封锁！（暂时性的）')
        source.encoding = 'utf-8'
        soup = BeautifulSoup(source.text, 'html.parser')

        code_line_red = soup.find('div', class_="ssqRed-dom").text.strip()[1:-1]  # 红球信息所在行，并提取字符
        code_line_blue = soup.find('div', class_="ssqBlue-dom").text.strip()[1:-1]  # 蓝球信息所在行
        code = code_line_red.split(',') + code_line_blue.split(',')  # 完整号码制成列表
        set_value('code', code)

        xq_line = soup.find('div', class_="ssqXqLink-dom")
        detailed_url = url_dic['中国福彩'] + xq_line.text.strip()  # 抓取详情网址

        qh_line = soup.find('div', class_="ssqQh-dom")  # 期号所在行
        period = int(qh_line.text.strip())
        set_value('period', period)

        source2 = requests.get(url=detailed_url, headers=headers)  # 爬取详情页
        source2.encoding = 'utf-8'
        soup2 = BeautifulSoup(source2.text, 'html.parser')

        data_line = soup2.find('p', class_="lotteryDate")  # 开奖日期所在行
        set_value('draw_data', data_line.text.strip())
        #draw_data = get_value('draw_data')

        zj_page = soup2.find('table')  # 中奖信息字段
        zj_line = zj_page.find_all('td')[0:6]
        ssq_bonus.update({'一等奖': str(zj_line[2])[4:-5], '二等奖': str(zj_line[5])[4:-5]})
        #print(code, period,"\n", draw_data,"\n", zj_line)
    except KeyError:
        messagebox.showinfo('可恶', '可能被反爬了！请打开或关闭代理并刷新重试')


def get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def ssq_czj(buy_code, zj_code):
    red_hit_num = 0
    blue_hit_num = 0
    blue_code = buy_code[6]
    for red_code in buy_code[0:6]:
        if red_code in zj_code[0:6]:
            red_hit_num += 1
    if blue_code == zj_code[6]:
        blue_hit_num = 1
    return red_hit_num, blue_hit_num


def get_ip():
    ip_pool = eval(get_value('ip_pool'))
    ip = random.choice(ip_pool)
    proxies = {'http': 'http://' + str(ip)}
    return proxies


def add_money():
    choose = messagebox.askokcancel('技巧', '通过一种可行的方式获取金币')
    try:
        if choose:
            if not os.path.exists('%s/money.txt' % get_value('dp_path')):
                return messagebox.showinfo('啊这', '获取失败！')
            elif os.path.exists('%s/money.txt' % get_value('dp_path')):
                messagebox.showinfo('润了', '金币+100！')
                os.remove('%s/money.txt' % get_value('dp_path'))
                set_value('current_coin', int(get_value('current_coin')) + 100)
                cf.set('金币', 'coin', str(get_value('current_coin')))
                with open('config.ini', 'w') as cff:
                    cf.write(cff)
                from lottery import coin
                coin.set(get_value('current_coin'))
    except OSError:
        messagebox.showerror('ERROR', '未知的错误！')
