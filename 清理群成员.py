#!usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 0:35
# @Author  : Fandes
# @FileName: 清理群成员.py
# @Software: PyCharm
import threading
import time
from pynput import keyboard
from selenium import webdriver

tips = "手动登录后,(设置其他筛选条件)按alt+s可以自动下滑加载全部成员页面(也可以自己划下去)," \
       "加载完页面后,按alt+z筛选(没有加载的页面将不会处理),会先筛选出所有符合条件的人," \
       "然后以20/批量选中并弹出删除按钮(qq只允许同一批量删除最多20人)" \
       "手动确认后按F4键继续选中下一批...一一确认即可" \
       "然后手动确认删除"
print(tips)
browser = webdriver.Edge(executable_path="msedgedriver.exe")  # 需要下载浏览器驱动!现在是微软Edge浏览器的驱动!!!
browser.get('https://qun.qq.com/member.html#gid=480429115')
num = 0
n = 8  # 32个线程,根据电脑性能来..
obj = []


class Checkthread(threading.Thread):
    # """ 线程类,人数太多时不开多线程选中会很慢,可以到下面改线程数为1对比一下就知道了"""
    def __init__(self, cids):
        super().__init__()
        self.cids = cids

    def run(self):
        global obj
        global num
        for e in self.cids:
            tds = e.find_elements_by_tag_name("td")
            if tds[-2].text == tds[-4].text:  # 入群时间和最后发言时间相同
                name = e.find_element_by_class_name("group-card").text
                print("入群时间{}和最后发言时间{}相同,{}/{}".format(tds[-2].text, tds[-4].text, name, tds[-7].text))
                # if "21" in name or "20" in name or "19" in name or "18" in name or "17" in name or "16" in name or "15" in name:#筛选名片
                #     continue
                obj.append(e)
                num += 1

        return


def checked(obj):
    browser.execute_script("arguments[0].setAttribute(arguments[1],arguments[2])",
                           obj.find_element_by_class_name("check-input"), "checked", 1)


def listen():
    print("listen")

    def on_search():
        print('<alt>+z pressed')
        global num
        num = 0
        els = browser.find_elements_by_class_name("mb")
        l = len(els)
        threads = []
        for i in range(n):  # 平均分配检测量
            thread = Checkthread(els[(i * l) // n:((i + 1) * l) // n])
            thread.start()
            print("{}->{}线程启动".format((i * l) // n, ((i + 1) * l) // n))
            threads.append(thread)
        for thread in threads:
            thread.join()  # 线程等待
        print("共有{}人符合条件,开始以20/批量选中".format(num))
        i = 0
        for e in obj:
            if i == 0:
                e.find_element_by_class_name("check-input").click()
            else:
                checked(e)
            i += 1
            print("{}.选中{}".format(i, e.find_element_by_class_name("group-card").text))

            def on_press(k):
                if k == keyboard.Key.f4:
                    kbl.stop()  # 按键监听停止
                    print("继续")

            if i == 20 or e == obj[-1]:
                print("手动确认后按F4键继续")  # 手动确认删除比较安全
                browser.find_element_by_class_name("del-member").click()
                kbl = keyboard.Listener(on_press=on_press)
                kbl.start()
                kbl.join()
                i = 0

    def on_end():
        print("scroll to end")
        i = 1
        while True:
            check_height = browser.execute_script("return document.body.scrollHeight;")
            for r in range(5):
                time.sleep(0.1)
                browser.execute_script("window.scrollBy(0,1000)")
                print("滚动中...")
            time.sleep(0.3)
            check_height1 = browser.execute_script("return document.body.scrollHeight;")
            print(str(check_height) + '**************' + str(check_height1))
            if check_height == check_height1:
                break

    hotkey = keyboard.GlobalHotKeys({
        '<alt>+z': on_search,
        '<alt>+s': on_end,
    })

    hotkey.start()
    hotkey.wait()
    hotkey.join()
    print("end")


listen()
