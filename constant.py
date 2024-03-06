import os
import sys
import configparser

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/103.0.0.0 Safari/537.36",
           "cookie": "HMF_CI=f2b6c357fe46de3914bf6ded24af4662c75606aa142c47b192265da5a28e1dbb68; 21_vq=13"}
url_dic = {'中国福彩': 'http://www.cwl.gov.cn', '双色球': 'http://www.cwl.gov.cn/fcpz/yxjs/ssq/', '待扩展': None}

ssq_regdic = {'6+1': '一等奖', '6+0': '二等奖', '5+1': '三等奖', '5+0': '四等奖', '4+1': '四等奖', '4+0': '五等奖', '3+1': '五等奖',
              '1+1': '六等奖', '2+1': '六等奖', '0+1': '六等奖', '3+0': '未中奖', '2+0': '未中奖', '0+0': '未中奖', '1+0': '未中奖'}
ssq_bonus = {'一等奖': 0, '二等奖': 0, '三等奖': 3000, '四等奖': 200, '五等奖': 10, '六等奖': 5}

_global_dict = {}


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


config_path = resource_path("config.ini")
icon_path = resource_path('icon.ico')
cf = configparser.ConfigParser()
cf.read(config_path)


def _init():  # 初始化
    global _global_dict
    _global_dict = {}
    set_value('result', '')
    set_value('code', [])
    set_value('period', 0)
    set_value('draw_data', '')
    set_value('proxies', True if cf.get('代理', 'proxies_mode') == 'True' else False)
    # set_value('redeemed',True if cf.get('金币', 'redeemed') == 'True' else False)
    set_value('history', cf.get('金币', 'history'))
    set_value('dp_path', os.path.join(os.path.expanduser("~"), 'Desktop'))


def set_value(key, value):
    # 定义一个全局变量
    _global_dict[key] = value


def get_value(key):
    # 获得一个全局变量，不存在则提示读取对应变量失败
    try:
        return _global_dict[key]
    except KeyError:
        print('读取' + key + '失败\r\n')
