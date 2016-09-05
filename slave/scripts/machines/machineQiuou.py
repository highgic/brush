#! -*- coding=utf-8 -*-
import os
import time
# import logging
import random
import re
from machines.StateMachine import Machine
from appium4droid import webdriver
from appium4droid.common.exceptions import *
from appium4droid.support.ui import WebDriverWait
from random import choice

from jiema.jiumaSDK import Jiuma
from jiema.feimaSDK import Feima
from jiema.yamaSDK import Yama
from jiema.ailezanSDK import Ailezan
from jiema.jimaSDK import Jima
from jiema.shenhuaSDK import Shenhua
from jiema.yimaSDK import Yima

try:
    from util import screenshot, run_qpy2_script
except ImportError:
    screenshot = lambda: 1
    run_qpy2_script = lambda x: None


class Machinex(Machine):
    def __init__(self, driver, code_platform, fm_uname, fm_pwd):
        super(Machinex, self).__init__(self.initdata)
        self.driver = driver
        self.code_platform = code_platform      #接码平台
        self.code_user = fm_uname       #接码平台帐号
        self.code_pwd = fm_pwd      #接码平台密码
        self.appname = "求偶"       #app名字
        self.appname_en = "qiuou"     #记录文件用缩写英文名
        self.imei = None
        self.runnum = None        #记录运行次数

    def initdata(self):
        self.phone = None
        self.pwd = None
        self.begintime = None
        self.endstime = None
        self.try_count = 0      #初始化出错尝试次数
        self.readnum = random.randint(2, 2)     #初始化阅读次数
        #初始化阅读菜单
        self.ismenu1 = True
        self.ismenu2 = True
        self.ismenu3 = True
        self.ismenu4 = True
        self.ismenu5 = True
        #选择初始化接码平台
        if self.code_platform == "feima":
            self.code = Feima(self.code_user, self.code_pwd, None)
        elif self.code_platform == "yama":
            self.code = Yama(self.code_user, self.code_pwd, None)
        elif self.code_platform == "yima":
            self.code = Yima(self.code_user, self.code_pwd, None)
        elif self.code_platform == "ailezan":
            self.code = Ailezan(self.code_user, self.code_pwd, None)
        elif self.code_platform == "jima":
            self.code = Jima(self.code_user, self.code_pwd, None)
        elif self.code_platform == "jiuma":
            self.code = Jiuma(self.code_user, self.code_pwd, None)
        elif self.code_platform == "shenhua":
            self.code = Shenhua(self.code_user, self.code_pwd, None)

        return self.begin

    def begin(self):
        dr = self.driver
        dr.press_keycode(3)
        time.sleep(1)
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name(self.appname)).click()
        time.sleep(10)
        #检测已进入app
        WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("cn.partygo.qiuou:id/wv_age"))
        self.begintime = "开始:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        time.sleep(5)
        #新开软件翻页
        # self.swipes(600, 500, 300, choice([440, 560, 560]), random.randint(0, 10), 2, 2)
        # WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("")).click()
        return self.sign

    def sign(self):
        dr = self.driver
        #选择年龄
        self.swipes(600, 500, 300, choice([440, 560, 560]), random.randint(0, 10), 2, 2)
        #选择性别
        WebDriverWait(dr, 20).until(lambda d: d.find_element_by_id(choice(["cn.partygo.qiuou:id/btn_male", "cn.partygo.qiuou:id/btn_female"]))).click()
        time.sleep(1)
        #你来这干什么
        self.select_one_by_id("cn.partygo.qiuou:id/tv_value")
        time.sleep(1)
        #身高
        self.select_one_by_id("cn.partygo.qiuou:id/tv_value")
        time.sleep(1)
        #标签
        self.select_one_by_id("cn.partygo.qiuou:id/tv_value")
        time.sleep(1)
        #收入
        self.select_one_by_id("cn.partygo.qiuou:id/tv_value")
        time.sleep(1)
        #学历
        self.select_one_by_id("cn.partygo.qiuou:id/tv_value")
        time.sleep(1)
        if random.randint(0, 1):
            #选择头像
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("cn.partygo.qiuou:id/btn_gallery")).click()
            time.sleep(1)
            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("1touxiang")).click()
            time.sleep(1)
            self.swipes(300, random.randint(800, 1000), 300, random.randint(300, 500), random.randint(0, 80))
            time.sleep(5)
            self.select_one_by_id("cn.partygo.qiuou:id/checkBox1")
            time.sleep(1)
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("cn.partygo.qiuou:id/tv_header_menu")).click()
            time.sleep(1)
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.miui.gallery:id/wallpaper_apply")).click()
            time.sleep(5)
        else:
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("cn.partygo.qiuou:id/tv_header_menu")).click()
            time.sleep(1)
        #推荐
        if random.randint(0, 1):
            for x in range(5):
                try:
                    WebDriverWait(dr, 20).until(lambda d: d.find_element_by_id(choice(["cn.partygo.qiuou:id/btn_consider_1", "cn.partygo.qiuou:id/btn_consider_2"]))).click()
                    time.sleep(1)
                except TimeoutException:
                    break
        else:
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("cn.partygo.qiuou:id/tv_header_menu")).click()
            time.sleep(1)
        return self.do

    def do(self):
        dr = self.driver
        try:
            while self.readnum:
                print("剩下阅读次数:%s" % self.readnum)
                random_read = random.randint(0, 4)
                if random_read == 0:
                    if self.ismenu1:
                        print("goto menu1")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("cn.partygo.qiuou:id/fl_home")).click()
                        time.sleep(5)
                        return self.menu1
                    return self.do
                elif random_read == 1:
                    if self.ismenu2:
                        print("goto menu2")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("cn.partygo.qiuou:id/fl_message")).click()
                        time.sleep(5)
                        return self.menu2
                    return self.do
                elif random_read == 2:
                    if self.ismenu3:
                        print("goto menu3")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("cn.partygo.qiuou:id/ll_discover")).click()
                        time.sleep(5)
                        return self.menu3
                    return self.do
                elif random_read == 3:
                    if self.ismenu4:
                        print("goto menu4")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("cn.partygo.qiuou:id/fl_dynamic")).click()
                        time.sleep(5)
                        return self.menu4
                    return self.do
                else:
                    if self.ismenu5:
                        print("goto menu5")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("cn.partygo.qiuou:id/ll_myspace")).click()
                        time.sleep(5)
                        return self.menu5
                    return self.do
        except TimeoutException:
            print("查找菜单出错")
            return self.exception_returnapp()
        print("阅览完毕")
        return self.ends

    def menu1(self):
        dr = self.driver
        try:
            self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(1, 5), 2, 10)
            self.select_one_by_id("cn.partygo.qiuou:id/iv_video_cut")
            time.sleep(random.randint(5, 15))
            self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(3, 5), 5, 10)
            dr.press_keycode(4)
            time.sleep(5)
            self.readnum -= 1
            self.ismenu1 = False
        except Exception as e:
            print("error in menu1")
            return self.exception_returnapp()
        return self.do

    def menu2(self):
        dr = self.driver
        try:
            self.select_one_by_id("cn.partygo.qiuou:id/msg_item_title")
            time.sleep(random.randint(5, 15))
            dr.press_keycode(4)
            time.sleep(1)
            self.readnum -= 1
            self.ismenu2 = False
        except Exception as e:
            print("error in menu2")
            return self.exception_returnapp()
        return self.do

    def menu3(self):
        dr = self.driver
        try:
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("cn.partygo.qiuou:id/btn_yes")).click()
            time.sleep(1)
            self.ismenu3 = False
        except Exception as e:
            print("error in menu3")
            return self.exception_returnapp()
        return self.do

    def menu4(self):
        dr = self.driver
        try:
            self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(1, 5), 2, 10)
            dr.press_keycode(4)
            time.sleep(5)
            self.ismenu4 = False
        except Exception as e:
            print("error in menu4")
            return self.exception_returnapp()
        return self.do

    def menu5(self):
        dr = self.driver
        try:
            self.ismenu5 = False
        except Exception as e:
            print("error in menu5")
            return self.exception_returnapp()
        return self.do

    def ends(self):
        #记录时间
        self.endstime = "结束:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        print(self.begintime)
        print(self.endstime)
        time.sleep(2)
        try:
            with open('/sdcard/1/time%s.log' % self.appname_en, 'a') as f:
                f.write('\n激活 %s.%s, %s, %s, count:%s' % (time.localtime().tm_mon, time.localtime().tm_mday, self.begintime, self.endstime, self.runnum))
        except:
            pass
        time.sleep(3)
        #效率控制
        # st = [1200, 1200, 1200, 1200, 1200, 1200, 180, 120, 40, 20, 10, 10,
        #       10, 20, 20, 20, 10, 10, 5, 0, 0, 0, 0, 0]
        #
        # print("现在时间是%s:%s,脚本将在%s秒后继续执行" % (time.localtime().tm_hour, time.localtime().tm_min, st[time.localtime().tm_hour-1]))
        # time.sleep(st[time.localtime().tm_hour-1])

        return self.exit

    def uuwise(self):
        dr = self.driver
        dr.press_keycode(3)
        time.sleep(1)
        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("UUWiseDemo")).click()
        time.sleep(1)
        try:
            btlogin = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.example.uuwisedemo:id/btn_login"))
        except TimeoutException:
            self.try_count += 1
            if self.try_count > 5:
                return self.exit
            dr.press_keycode(4)
            time.sleep(1)
            return self.uuwise
        edtsuser = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.example.uuwisedemo:id/et_loginname"))
        edtspwd = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.example.uuwisedemo:id/et_loginpwd"))
        uuuser = 'xiaoxiaozhuan'
        uupwd = 'meiriq2014'
        if edtsuser.text == uuuser and edtspwd.text == uupwd:
            pass
        else:
            edtsuser.send_keys(uuuser)
            time.sleep(1)
            edtspwd.send_keys(uupwd)
            time.sleep(1)
        btlogin.click()
        screenshotpath = dr.find_element_by_id("com.example.uuwisedemo:id/et_path")
        for x in range(10):
            screenshotpath.click()
            time.sleep(0.5)
            dr.press_keycode(123)
            time.sleep(0.5)
            for i in range(40):
                dr.press_keycode(67)
            if screenshotpath.text == "路径":
                break
        screenshotpath.send_keys('/sdcard/captcha.png')
        time.sleep(1)
        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.example.uuwisedemo:id/btn_recognize")).click()
        time.sleep(1)
        captcha = None
        try:
            msg = WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.example.uuwisedemo:id/txt_code"))
            match = re.search(r'验证码：\d+\|([0-9a-zA-Z]+)', msg.text)
            if match:
                captcha = match.group(1)
            else:
                captcha = None
        except:
            pass
        dr.press_keycode(4)
        time.sleep(1)
        dr.press_keycode(82)
        time.sleep(2)
        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name(self.appname)).click()
        return captcha

    def get_filemessage(self, filename):
        if os.path.exists("D:/brush/slave/scripts/doc/%s" % filename):
            with open("D:/brush/slave/scripts/doc/%s" % filename, 'r', encoding='utf-8') as f:
                 strname = f.readlines()
        elif os.path.exists("/sdcard/1/%s" % filename):
            with open("/sdcard/1/%s" % filename, 'r', encoding='utf-8') as f:
                 strname = f.readlines()
        else:
            strname = ""
        time.sleep(1)
        return strname[random.randint(0, strname.__len__()-1)].strip()

    def swipes(self, x1, y1, x2, y2, swipe_num=1, swipe_time_a=1, swipe_time_b=1):
        dr = self.driver
        print("swipenum:%s" % swipe_num)
        for x in range(swipe_num):
            dr.swipe(x1, y1, x2, y2)
            time.sleep(random.randint(swipe_time_a, swipe_time_b))

    def select_one_by_id(self, find_id, find_time=30, find_min=0, find_max=0):
        selectone = WebDriverWait(self.driver, find_time).until(lambda d: d.find_elements_by_id(find_id))
        if find_max == 0:
            selectone[random.randint(find_min, selectone.__len__()-1)].click()
        else:
            selectone[random.randint(find_min, find_max)].click()

    def exception_returnapp(self):
        dr = self.driver
        print("try_count:%s" % self.try_count)
        self.try_count += 1
        if self.try_count > 5:
            return self.exit
        dr.press_keycode(4)
        time.sleep(1)
        dr.press_keycode(4)
        time.sleep(1)
        dr.press_keycode(82)
        time.sleep(2)
        try:
            WebDriverWait(dr, 2).until(lambda d: d.find_element_by_name(self.appname)).click()
        except TimeoutException:
            dr.press_keycode(4)
        time.sleep(5)
        return self.do


class Machinex2(Machine):
    def __init__(self, driver):
        super(Machinex2, self).__init__(self.initdata)
        self.driver = driver
        self.appname = ""       #app名字
        self.appname_en = ""     #记录文件用缩写英文名
        self.imei = None        #imei
        self.remain_day = None      #留存天数

    def initdata(self):
        self.begintime = None
        self.endstime = None
        self.try_count = 0      #初始化出错尝试次数
        self.readnum = random.randint(1, 1)     #初始化阅读次数
        #初始化阅读菜单
        self.ismenu1 = True
        self.ismenu2 = True
        self.ismenu3 = True
        self.ismenu4 = True
        self.ismenu5 = True

        return self.begin

    def begin(self):

        return self.login

    def login(self):
        dr = self.driver
        try:
            with open('/sdcard/1/user%s.log' % self.appname_en, 'r') as f:
                selectuser = f.read()
        except:
            with open('D:/brush/slave/scripts/doc/user%s.log' % self.appname_en, 'r') as f:
                selectuser = f.read()
        user = re.search(r'imei:%s,(\d+)' % self.imei, selectuser)
        pwd = re.search(r'imei:%s,\d+,([0-9a-z]+)' % self.imei, selectuser)
        if user and pwd:
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("")).click()
            time.sleep(1)
            edit = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_class_name("android.widget.EditText"))
            edit[0].send_keys(str(user.group(1)))
            time.sleep(1)
            edit[1].send_keys(str(pwd.group(1)))
            time.sleep(1)
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("")).click()
            time.sleep(5)
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id(""))
        time.sleep(5)
        return self.do



    def ends(self):
        #记录时间
        self.endstime = "结束:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        print(self.begintime)
        print(self.endstime)
        time.sleep(2)
        try:
            with open('/sdcard/1/time%s2.log' % self.appname_en, 'a') as f:
                f.write('\n留存%s  %s.%s, %s, %s' % (self.remain_day, time.localtime().tm_mon, time.localtime().tm_mday, self.begintime, self.endstime))
        except:
            pass
        time.sleep(3)
        return self.exit

    def get_filemessage(self, filename):
        if os.path.exists("D:/brush/slave/scripts/doc/%s" % filename):
            with open("D:/brush/slave/scripts/doc/%s" % filename, 'r', encoding='utf-8') as f:
                 strname = f.readlines()
        elif os.path.exists("/sdcard/1/%s" % filename):
            with open("/sdcard/1/%s" % filename, 'r', encoding='utf-8') as f:
                 strname = f.readlines()
        else:
            strname = ""
        time.sleep(1)
        return strname[random.randint(0, strname.__len__()-1)].strip()

    def swipes(self, x1, y1, x2, y2, swipe_num=1, swipe_time_a=1, swipe_time_b=1):
        dr = self.driver
        print("swipenum:%s" % swipe_num)
        for x in range(swipe_num):
            dr.swipe(x1, y1, x2, y2)
            time.sleep(random.randint(swipe_time_a, swipe_time_b))

    def select_one_by_id(self, find_id, find_time=30, find_min=0, find_max=0):
        selectone = WebDriverWait(self.driver, find_time).until(lambda d: d.find_elements_by_id(find_id))
        if find_max == 0:
            selectone[random.randint(find_min, selectone.__len__()-1)].click()
        else:
            selectone[random.randint(find_min, find_max)].click()

    def exception_returnapp(self):
        dr = self.driver
        print("try_count:%s" % self.try_count)
        self.try_count += 1
        if self.try_count > 5:
            return self.exit
        dr.press_keycode(4)
        time.sleep(1)
        dr.press_keycode(4)
        time.sleep(1)
        dr.press_keycode(82)
        time.sleep(2)
        try:
            WebDriverWait(dr, 2).until(lambda d: d.find_element_by_name(self.appname)).click()
        except TimeoutException:
            dr.press_keycode(4)
        time.sleep(5)
        return self.do



if __name__ == "__main__":
    wd = webdriver.Remote()
    time.sleep(2)
