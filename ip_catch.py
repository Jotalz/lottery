import requests
import json
from constant import cf


usable_ip = ''


def check_ip(ip_list):
    iip = []
    for got_ip in ip_list:
        if len(iip) > 5:  # 有5个可用ip就停止检测
            break
        ip_port = "{}:{}".format(got_ip["host"], got_ip["port"])
        proxies = {'https': ip_port}
        try:
            response = requests.get('https://icanhazip.com/', proxies=proxies,
                                    timeout=3).text  # 如果请求该网址，返回的IP地址与代理IP一致，则认为代理成功
            # 可以更改timeout时间
            if response.strip() == got_ip["host"]:
                # print("可用的IP地址为：{}".format(ip_port))
                iip.append(ip_port)
        except Exception:
            pass
            # print("不可用的IP地址为：{}".format(ip_port))
    return iip


class FreeIP:
    def __init__(self):
        self.url = "http://proxylist.fatezero.org/proxy.list"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
                                      "like Gecko) Chrome/103.0.0.0 Safari/537.36"}

    def run(self):
        global usable_ip
        response = requests.get(url=self.url).content.decode()

        ip_list = []
        proxies_list = response.split('\n')

        for proxy_str in proxies_list:
            try:
                proxy = {}
                proxy_json = json.loads(proxy_str)
                if proxy_json["anonymity"] == "high_anonymous" and proxy_json["type"] == "https":
                    host = proxy_json['host']
                    port = proxy_json['port']
                    proxy["host"] = host
                    proxy["port"] = port
                    ip_list.append(proxy)
                    # print("{}符合https和高匿条件".format(host))
            except Exception:
                pass
                # print(proxy_str)

        usable_ip = check_ip(ip_list)
        cf.set('代理', 'ip_pool', str(usable_ip))  # 将可用IP写入配置文件,此处需要多线程防卡顿
        with open('config.ini', 'w') as cff:
            cf.write(cff)
        # print("可用的IP地址有{}个".format(len(correct_ip)))


if __name__ == '__main__':
    ip = FreeIP()
    ip.run()
