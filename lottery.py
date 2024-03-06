import random
import re
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from constant import *
from stac_fun import analyze, get_time, ssq_czj,add_money
from ip_catch import FreeIP
import threading

if cf.get('路径配置', 'save_path') == '':
    def_path = os.getcwd()
else:
    def_path = cf.get('路径配置', 'save_path')


class Window:
    def __init__(self, name):
        global coin
        self.init_name = name
        self.init_name.title("双色球随机选号V1.0")
        self.init_name.iconbitmap(icon_path)
        self.screenWidth = self.init_name.winfo_screenwidth()  # 屏幕宽度
        self.screenHeight = self.init_name.winfo_screenheight()
        self.init_name.geometry("600x320+%d+%d" % (self.screenWidth / 2, self.screenHeight / 3))
        self.init_name.resizable(False, False)  # 禁止改变窗口大小x,y
        self.init_name.configure(background='#ffffff')  # 设置背景颜色

        self.style = ttk.Style()

        coin = tk.StringVar()
        self.time = tk.StringVar()
        self.check_var1 = tk.IntVar()
        self.check_var2 = tk.IntVar()
        self.check_var3 = tk.IntVar()
        self.check_var4 = tk.IntVar()
        self.check_var5 = tk.IntVar()
        self.check_var6 = tk.IntVar()
        self.check_var7 = tk.IntVar()
        self.number = tk.StringVar()

        self.first_num = ''
        self.second_num = ''
        self.third_num = ''
        self.fourth_num = ''
        self.fifth_num = ''
        self.sixth_num = ''
        self.seventh_num = ''

        self.data = tk.Label(self.init_name, textvariable=self.time, font=("微软雅黑", 15), background="white")
        self.money = tk.Label(self.init_name, textvariable=coin, fg='gold', font=("微软雅黑", 15), background="white")
        self.first = tk.Label(self.init_name, text='01', font=("微软雅黑", 35), background="white", foreground='red')
        self.second = tk.Label(self.init_name, text='02', background="white", font=("微软雅黑", 35), fg='red')
        self.third = tk.Label(self.init_name, text='03', background="white", font=("微软雅黑", 35), fg='red')
        self.fourth = tk.Label(self.init_name, text='04', background="white", font=("微软雅黑", 35), fg='red')
        self.fifth = tk.Label(self.init_name, text='05', background="white", font=("微软雅黑", 35), fg='red')
        self.sixth = tk.Label(self.init_name, text='06', background="white", font=("微软雅黑", 35), fg='red')
        self.seventh = tk.Label(self.init_name, text='07', background="white", font=("微软雅黑", 35), fg='blue')
        self.buffer = tk.Label(self.init_name, text='', background="white", font=("微软雅黑", 1), fg='green')
        self.value_list = [self.first, self.second, self.third, self.fourth, self.fifth, self.sixth, self.seventh]
        self.get_time()
        coin.set(cf.get('金币', 'coin'))
        self.book()

    def book(self):
        self.data.place(x=70, y=8)
        self.money.place(x=370, y=8)
        self.first.place(x=30, y=40)
        self.second.place(x=110, y=40)
        self.third.place(x=190, y=40)
        self.fourth.place(x=270, y=40)
        self.fifth.place(x=350, y=40)
        self.sixth.place(x=430, y=40)
        self.seventh.place(x=510, y=40)
        self.style.configure('my.TCheckbutton', background='white')
        tk.Label(self.init_name, text='时间:', font=("微软雅黑", 15), background="white").place(x=20, y=7)
        tk.Label(self.init_name, text='金币:', font=("微软雅黑", 15), fg='gold', background="white").place(x=320, y=7)
        ttk.Checkbutton(self.init_name, variable=self.check_var1, command=self.lock1, style='my.TCheckbutton').place(
            x=54, y=120)
        ttk.Checkbutton(self.init_name, variable=self.check_var2, command=self.lock2, style='my.TCheckbutton').place(
            x=134, y=120)
        ttk.Checkbutton(self.init_name, variable=self.check_var3, command=self.lock3, style='my.TCheckbutton').place(
            x=214, y=120)
        ttk.Checkbutton(self.init_name, variable=self.check_var4, command=self.lock4, style='my.TCheckbutton').place(
            x=294, y=120)
        ttk.Checkbutton(self.init_name, variable=self.check_var5, command=self.lock5, style='my.TCheckbutton').place(
            x=374, y=120)
        ttk.Checkbutton(self.init_name, variable=self.check_var6, command=self.lock6, style='my.TCheckbutton').place(
            x=454, y=120)
        ttk.Checkbutton(self.init_name, variable=self.check_var7, command=self.lock7, style='my.TCheckbutton').place(
            x=534, y=120)
        tk.Label(self.init_name, text='结果：', bg='white').place(x=170, y=180)

        ttk.Entry(self.init_name, textvariable=self.number, width=30, style='my.TEntry').place(x=210, y=180)
        self.style.configure('my.TButton', font=("微软雅黑", 20), background='white')
        ttk.Button(self.init_name, text='开始生成选号', style='my.TButton', command=self.create).place(x=220, y=230)
        self.style.configure('u.TButton', font=("微软雅黑", 10), background='white')
        ttk.Button(self.init_name, text='保存选号', style='u.TButton', command=self.save_win).place(x=440, y=177)
        ttk.Button(self.init_name, text='查中奖', style='u.TButton', command=check).place(x=40, y=170)
        ttk.Button(self.init_name, text='刷新', style='u.TButton', command=thread_update).place(x=40, y=210)
        ttk.Button(self.init_name, text='兑奖', style='u.TButton', command=redeem).place(x=40, y=250)
        set_value('ip_pool', cf.get('代理', 'ip_pool'))  # 从配置文件读取IP池记录在软件内存中
        set_value('current_coin', cf.get('金币', 'coin'))  # 从配置文件读取金币数量记录在软件内存中
        analyze(url_dic['双色球'])

    def get_time(self):
        self.time.set(get_time())
        self.init_name.after(1000, self.get_time)

    def lock1(self):
        if self.check_var1.get() == 1:
            self.value_list[0] = self.buffer
        else:
            self.value_list[0] = self.first

    def lock2(self):
        if self.check_var2.get() == 1:
            self.value_list[1] = self.buffer
        else:
            self.value_list[1] = self.second

    def lock3(self):
        if self.check_var3.get() == 1:
            self.value_list[2] = self.buffer
        else:
            self.value_list[2] = self.third

    def lock4(self):
        if self.check_var4.get() == 1:
            self.value_list[3] = self.buffer
        else:
            self.value_list[3] = self.fourth

    def lock5(self):
        if self.check_var5.get() == 1:
            self.value_list[4] = self.buffer
        else:
            self.value_list[4] = self.fifth

    def lock6(self):
        if self.check_var6.get() == 1:
            self.value_list[5] = self.buffer
        else:
            self.value_list[5] = self.sixth

    def lock7(self):
        if self.check_var7.get() == 1:
            self.value_list[6] = self.buffer
        else:
            self.value_list[6] = self.seventh

    def create(self):
        for i in range(6):
            n = str(random.randint(1, 33))
            self.value_list[i]['text'] = n if len(n) == 2 else n.zfill(2)
        self.value_list[6]['text'] = str(random.randint(1, 16)).zfill(2)
        self.first_num = self.first.cget('text')
        self.second_num = self.second.cget('text')
        self.third_num = self.third.cget('text')
        self.fourth_num = self.fourth.cget('text')
        self.fifth_num = self.fifth.cget('text')
        self.sixth_num = self.sixth.cget('text')
        self.seventh_num = self.seventh.cget('text')

        result = repr(self.first_num + ',' + self.second_num + ',' + self.third_num + ',' + self.fourth_num + ',' +
                      self.fifth_num + ',' + self.sixth_num + ',' + self.seventh_num).strip("'")
        self.number.set(result)
        set_value('result', result)

    def save_win(self):
        if self.number.get() != '':
            inferior = tk.Tk()
            save = SaveBoard(inferior)
            save.windows_init()
            # result = self.number.get()
        else:
            messagebox.showinfo(title='别急', message='需要先生成选号')


def check():
    buy_count = 0  # 本期购买数
    hit_count = 0  # 本期中奖数
    hit_mark_list = []  # 中奖备注列表
    hit_mx_list = []  # 中奖明细信息列表
    text = ''  # 展示中奖信息
    if not os.path.exists('%s/双色球.txt' % def_path):
        return messagebox.showinfo('啊这', '尚无保存记录！')
    with open('%s/双色球.txt' % def_path, 'r+') as recording:
        for line in recording.readlines():
            buy_period = re.search(r'(?<=\u7b2c).*?(?=\u671f)', line, re.U).group()  # 读取购买期号
            if buy_period == str(get_value('period')):  # 如果是开奖的这一期
                buy_count += 1
                buy_code = re.search(r'(?<=<).*?(?=>)', line).group().split(',')  # 读取购买号码
                r, b = ssq_czj(buy_code, get_value('code'))  # 计算出红球和蓝球的对应个数
                ssq_key = str(r) + '+' + str(b)  # 生成规则key
                if r > 3 or b > 0:  # 筛选中奖号
                    hit_count += 1
                    hit_mark = re.search(r'\S*', line).group()
                    bet_num = re.search(r'\d+(?=注)', line).group()  # 读取购买了几注
                    jx = '%s' % ssq_regdic[ssq_key]  # 查找几等奖
                    jj = '%s*%s' % (ssq_bonus[jx], bet_num)  # 查找奖额
                    jx_jj = jx + jj + '元'  # 拼接文本
                    hit_mx_list.append(jx_jj)
                    if len(hit_mark) < 5:  # 优化备注显示
                        hit_mark_list.append(hit_mark)
                    else:
                        hit_mark = hit_mark[0:3] + '...' + hit_mark[-1:-3]
                        hit_mark_list.append(hit_mark)
        # 将中奖信息以文本形式罗列在对话框
        for i in range(len(hit_mark_list)):
            add = '{}:    {}'.format(hit_mark_list[i], hit_mx_list[i])
            text += add + '\n'
        if hit_count == 0:  # 返回查询结果
            messagebox.showinfo(title='查询结果',
                                message='期号：{}    出奖号：{}\n本期您共购买了{}组号码，都未中奖'.format(get_value('period'),
                                                                                    get_value('code'), buy_count))
        else:
            messagebox.showinfo(title='查询结果',
                                message='期号：{}    出奖号：{}\n本期您共购买了{}组号码，中奖{}组\n{}'.format(get_value('period'),
                                                                                         get_value('code'),
                                                                                         buy_count, hit_count, text))


# threading work
def update():
    if cf.get('代理', 'proxies_mode') == 'True':
        set_value('proxies', True)
    else:
        set_value('proxies', False)
    analyze(url_dic['双色球'])


def thread_update():
    new_gx = threading.Thread(target=update)
    new_gx.start()


def redeem():
    total_jj = 0
    if not os.path.exists('%s/双色球.txt' % def_path):
        return messagebox.showinfo('啊这', '尚无保存记录！')
    if str(get_value('period')) == cf.get('金币','history'):
        messagebox.showinfo(title='兑奖失败', message='本期已经兑过奖啦！')
    else:
        with open('%s/双色球.txt' % def_path, 'r+') as recording:
            for line in recording.readlines():
                buy_period = re.search(r'(?<=\u7b2c).*?(?=\u671f)', line, re.U).group()  # 读取购买期号
                if buy_period == str(get_value('period')):
                    buy_code = re.search(r'(?<=<).*?(?=>)', line).group().split(',')  # 读取购买号码
                    r, b = ssq_czj(buy_code, get_value('code'))  # 计算出红球和蓝球的对应个数
                    ssq_key = str(r) + '+' + str(b)  # 生成规则key
                    if r > 3 or b > 0:  # 筛选中奖号
                        bet_num = re.search(r'\d+(?=注)', line).group()  # 读取购买了几注
                        jx = '%s' % ssq_regdic[ssq_key]  # 查找几等奖
                        jj = int(ssq_bonus[jx]) * int(bet_num)  # 计算奖额
                        total_jj += jj
        cf.set('金币', 'history', str(get_value('period')))
        #cf.set('金币', 'redeemed', 'True')
        with open('config.ini', 'w') as cff:
            cf.write(cff)
        if total_jj == 0:
            messagebox.showinfo(title='poor', message='很遗憾，你根本没有中奖，这边给您加个air')
        else:
            set_value('current_coin', int(get_value('current_coin')) + total_jj)
            cf.set('金币', 'coin', str(get_value('current_coin')))
            with open('config.ini', 'w') as cff:
                cf.write(cff)
            coin.set(get_value('current_coin'))
            messagebox.showinfo(title='兑奖成功', message='已将近期全部中奖号码兑出，共获得%s元' % total_jj)


class Menu(Window):
    def __init__(self, name):
        super().__init__(name)
        self.menu_bar = tk.Menu(self.init_name)
        self.setting_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="设置", menu=self.setting_menu)
        self.setting_menu.add_command(label="自定义保存路径", command=path_set)
        self.switch = tk.IntVar()
        if cf.get('代理', 'proxies_mode') == 'True':
            self.switch.set(1)
        self.setting_menu.add_checkbutton(label="启用代理", command=self.proxies_switch, selectcolor='coral',
                                          variable=self.switch)
        self.setting_menu.add_command(label="更新IP池", command=update_ip)
        self.menu_bar.add_command(label="打钱",command=add_money)
        self.menu_init()

    def menu_init(self):
        self.init_name.config(menu=self.menu_bar)

    def proxies_switch(self):
        if self.switch.get() == 1:
            cf.set('代理', 'proxies_mode', 'True')
            messagebox.showinfo('生效提醒', '已开启代理模式！请刷新以应用代理')
        else:
            cf.set('代理', 'proxies_mode', 'False')
        with open('config.ini', 'w') as cff:
            cf.write(cff)


def path_set():
    global def_path
    choose = filedialog.askdirectory(title="选择保存路径")
    if choose != '':  # 防止点了修改保存位置直接返回导致返回值为空，造成无效修改和报错
        def_path = choose
        if cf.get('路径配置', 'save_path') == '':
            if os.path.exists('%s/双色球.txt' % os.getcwd()):  # 防止所在目录无对应文件而造成报错
                shutil.move('%s/双色球.txt' % os.getcwd(), def_path)
        elif cf.get('路径配置', 'save_path') == def_path:  # 选择路径未发生变更不响应
            messagebox.showinfo('多此一举', '本来就是保存在这里哒！')
        else:
            try:
                if os.path.exists('%s/双色球.txt' % def_path):
                    messagebox.showinfo('重复文件', '%s存在同名文件，已将其合并' % def_path)
                    with open('%s/双色球.txt' % cf.get('路径配置', 'save_path'), 'r', ) as source:
                        with open('%s/双色球.txt' % def_path, 'a+') as target:
                            for line in source.readlines():
                                target.write('%s' % line)
                    os.remove('%s/双色球.txt' % cf.get('路径配置', 'save_path'))
                shutil.move('%s/双色球.txt' % cf.get('路径配置', 'save_path'), def_path)
                messagebox.showinfo('设置成功', '保存路径已变更为%s，即时生效！' % def_path)
            except OSError:
                pass
                # print('重复路径，无指定文件，无法移动文件到目标目录')
        cf.set('路径配置', 'save_path', def_path)  # 无论文件是否移动，保存路径会被更改
        with open('config.ini', 'w') as cff:
            cf.write(cff)


# 更新代理池需要一定的时间，单线程会使程序在更新时卡住，使用多线程解决这个问题
def update_ip():
    ip_get = FreeIP()
    new_ip = threading.Thread(target=ip_get.run)
    new_ip.start()


class SaveBoard:
    def __init__(self, name):
        self.save_gui = name
        self.save_gui.title("保存设置")
        self.screenWidth = self.save_gui.winfo_screenwidth()
        self.screenHeight = self.save_gui.winfo_screenheight()
        self.save_gui.geometry("300x120+%d+%d" % (self.screenWidth * 2 / 3, self.screenHeight * 1 / 3))
        self.save_gui.resizable(False, False)

        self.bets_var = 1
        self.content = tk.StringVar()
        self.remark_box = tk.Entry(self.save_gui, textvariable=self.content, width=25)
        self.save_path = def_path + '\\双色球.txt'

    def windows_init(self):
        adjust = tk.Scale(self.save_gui, orient='horizontal', from_=1, to=10, command=self.select_value, resolution=1,
                          length=100, sliderlength=20, activebackground='Gold')
        tk.Label(self.save_gui, text='请输入选号备注:').pack()
        self.remark_box.pack(pady=10)
        tk.Button(self.save_gui, text='确定', width=6, height=1, command=self.sure).pack(side='left', padx=20)

        tk.Button(self.save_gui, text='取消', width=6, height=1, command=self.back).pack(side='right', padx=20)
        adjust.pack(anchor='center')

    def select_value(self, value):
        self.bets_var = int(value)

    def sure(self):
        global coin
        if self.remark_box.get() != '':
            remark = self.remark_box.get()
            try:
                if os.path.exists(self.save_path):
                    with open(self.save_path, 'a+') as f:
                        f.write(
                            "{:15}{:20}{}{:>30}{:>10}\n".format(remark, '第' + str(get_value('period') + 1) + '期', '<' +
                                                                get_value('result') + '>', get_time(),
                                                                str(self.bets_var) + '注'))
                        self.back()
                        messagebox.showinfo('保存成功', '已成功保存选号至%s' % self.save_path)
                        set_value('current_coin', int(get_value('current_coin')) - 2 * self.bets_var)
                        cf.set('金币', 'coin', str(get_value('current_coin')))
                        with open('config.ini', 'w') as cff:
                            cf.write(cff)
                        coin.set(get_value('current_coin'))
                else:
                    with open(self.save_path, 'a+') as f:
                        f.write(
                            "{:15}{:20}{}{:>30}{:>10}\n".format(remark, '第' + str(get_value('period') + 1) + '期', '<' +
                                                                get_value('result') + '>', get_time(),
                                                                str(self.bets_var) + '注'))
                        self.back()
                        messagebox.showinfo('保存成功', '已成功保存选号至%s' % self.save_path)
                        set_value('current_coin', int(get_value('current_coin')) - 2 * self.bets_var)
                        cf.set('金币', 'coin', str(get_value('current_coin')))
                        with open('config.ini', 'w') as cff:
                            cf.write(cff)
                        coin.set(get_value('current_coin'))
            except OSError:
                messagebox.showerror(title='无效路径', message='无法找到保存路径（可能的原因：更换了使用设备；重命名过存储文件夹；\n解决方案：重新设置保存路径')
        else:
            messagebox.showinfo(title='无有效输入', message='选号备注不能为空')

    def back(self):
        self.save_gui.destroy()


class Inquire:
    def __init__(self):
        pass
