#usr/bin/python
#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time
import unittest
class YoudanWeb:
    #初始化环境
    def initialize(self):
        chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = chromedriver
        self.driver = webdriver.Chrome(chromedriver)
        #self.driver = webdriver.PhantomJS()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.base_url ="https://m.youdan.me"
    #搜索栏搜索
    def search(self,keywords):
        driver = self.driver
        driver.get(self.base_url +"/")
        time.sleep(2)
        driver.find_element_by_xpath(".//a[@class='sprite search-ico txt-over']").click()
        input = driver.find_element_by_id('filterValue')
        input.send_keys(keywords)
        time.sleep(2)
        input.send_keys(Keys.ENTER)
        return driver.page_source
    #进入有单h5
    def open_homepage(self):
        driver = self.driver
        driver.get(self.base_url +"/")
    #登录账号
    def login(self,user,pwd):
        driver = self.driver
        driver.find_element_by_xpath(".//a[@class='nav-ico']").click()
        time.sleep(1)
        driver.find_element_by_xpath(".//a[@class='blue-btn']").click()
        time.sleep(2)
        driver.find_element_by_id('mobile').send_keys(user)
        driver.find_element_by_id('password').send_keys(pwd)
        time.sleep(1)
        return driver.page_source
    #判断登录按钮状态
    # 返回为1登录按钮灰显
    # 返回为2登录按钮亮显
    def checklogin_button(self):
        driver = self.driver
        classname = driver.find_element_by_id("next").get_attribute("class")
        if classname == 'sure-btn normal':
            return 1
        elif classname == 'sure-btn':
            return 2
        else:
            return 3
    #判断登录结果
    def checklogin(self):
        driver = self.driver
        driver.find_element_by_id("next").click()
        msg = driver.find_element_by_xpath(".//div[@class='msg-box wrong-msg hide']//div[@class='msg-txt']//p").get_attribute()
        print msg.text
        if msg == u'该号码未注册':
            return 1
        elif msg == u'手机号或密码错误':
            return 2
    def clicklogin_button(self):
        driver = self.driver
        driver.find_element_by_id("next").click()
    #退出登录
    def logoff(self):
        self.open_homepage()
        driver = self.driver
        driver.find_element_by_xpath(".//a[@class='nav-ico']").click()
        time.sleep(1)
        driver.find_element_by_xpath(".//a[@class='blue-btn']").click()
    #关闭浏览器
    def quit(self):
        self.driver.quit()
    #截屏
    def save_screenshot(self,name):
        self.driver.save_screenshot('%s.png'%name)
    #进入产品列表
    def get_product_list(self):
        driver = self.driver
        driver.find_element_by_xpath(".//a[@class='nav-ico']").click()
        time.sleep(1)
        driver.find_element_by_xpath(".//nav[@class='main-nav']//ul//li[2]").click()
        time.sleep(2)
    #查看产品详情type表示产品类型，array第几个产品
    def get_product_details(self,type,array):
        self.open_homepage()
        self.get_product_list()
        driver = self.driver
        if type == 1:
            driver.find_element_by_xpath(".//section[@class='search-list pro-list']//div[%s]"%array).click()
            time.sleep(2)
        else:
            driver.find_element_by_xpath(".//section[@class='pro-tab display-box']//div[%s]"%type).click()
            time.sleep(2)
            driver.find_element_by_xpath(".//section[@class='search-list pro-list']//div[%s]"%array).click()
            time.sleep(2)
    #点击上传产品
    def upload_click(self):
        self.open_homepage()
        driver = self.driver
        driver.find_element_by_id("upload").click()
        time.sleep(1)
        if u'《上架说明》' not in driver.page_source:
            driver.find_element_by_id('mobile').send_keys('15914145610')
            driver.find_element_by_id('password').send_keys('123456')
            time.sleep(1)
            driver.find_element_by_id("next").click()
        else:
            pass
        return driver.page_source
    #点击上传产品并填写产品名
    def set_product_name(self,name):
        driver = self.driver
        driver.find_element_by_id('productName').send_keys(name)
        time.sleep(1)
        driver.find_element_by_xpath(".//a[@class='sure-btn']").click()
        time.sleep(1)
        return driver.page_source
    #选择返佣方式
    def set_rake_back(self,type):
        driver = self.driver
        choose = driver.find_element_by_xpath(".//section[@class='check-way']//div[%s]"%type)
        choose.click()
        time.sleep(1)
        return driver.page_source
    #de
    def clean_cooike(self):
        driver = self.driver
        driver.delete_all_cookies()
youdan = YoudanWeb()
youdan.initialize()
youdan.open_homepage()
youdan.login('18507097209','456789')
youdan.checklogin_button()
youdan.checklogin()




