#coding=utf-8
import urllib
import re
import httplib2
import os
from datetime import datetime
from Tkinter import *
import json
from lxml import etree

'''
Created on May 10, 2016
@author: qianbingbing
@funcation:get information from Taobao or Tmall
parameter:url
return:image
'''
TIMEOUT = 100
#设置Request Headers
DEFAULT_HEADERS1 = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:18.0) Gecko/20100101 Firefox/18.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-us,en;q=0.5',
    'Accept-Encoding': 'gzip',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
    'Keep-Alive': '115',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Host':'dsc.taobaocdn.com'
}
#设置Request Headers
DEFAULT_HEADERS2 = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:18.0) Gecko/20100101 Firefox/18.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-us,en;q=0.5',
    'Accept-Encoding': 'gzip',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
    'Keep-Alive': '115',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Host':'gd3.alicdn.com'
}
#定义全局变量
PICPATH = ''
def http_get1(url):
        conn = httplib2.Http(timeout=TIMEOUT)
        content = conn.request(uri=url, method='GET', body=None, headers=DEFAULT_HEADERS1)
        return content
def http_get2(url):
        conn = httplib2.Http(timeout=TIMEOUT)
        content = conn.request(uri=url, method='GET', body=None, headers=DEFAULT_HEADERS2)
        return content
#创建图片存放目录
def set_fodlerName():
    global PICPATH
    foldername = datetime.now().strftime('%Y-%m-%d-%H-%M')
    PICPATH = 'F:\\taobaoImage\\%s\\' % (foldername) #下载到的本地目录
    if not os.path.exists(PICPATH):   #路径不存在时创建一个
        os.makedirs(PICPATH)
    return PICPATH
#获取详细描述的api
def getRealurl(url):
    html = urllib.urlopen(url).read()
    #天猫店铺
    reg1 = r'"descUrl":"(.*?)"'
    #普通店铺
    reg2 = r'descUrl          : location\.protocol===\'http\:\' \? \'(.*?)\''
    imgre = re.compile(reg1)
    imglist = re.findall(imgre,html)
    if imglist:
        print '天猫店铺:'+ imglist[0]
    else:
        imgre = re.compile(reg2)
        imglist = re.findall(imgre,html)
        print '普通店铺：'+ imglist[0]
    return imglist[0]
#根据详细描述的api得到详细描述图片
def getRealimg(url):
    global PICPATH
    html = http_get1('http:'+url)
    #两条正则规则。反复调试得出的结果，可能还有bug
    reg1 = r'middle" src="(.*?)">'
    reg2 = r'src="(.*?)" align="absmiddle">'
    imgre = re.compile(reg1)
    imglist = re.findall(imgre,html[1])
    '''
	如果通过第一个正则匹配不到内容则尝试使用第二个正则来匹配
	'''
    if imglist:
        print '第一条正则有效'
        for i in imglist:
            print i
    else:
        print '第一条正则无效'
        imgre = re.compile(reg2)
        imglist = re.findall(imgre,html[1])
        for i in imglist:
            print i
    x = 1
    for image in imglist:
        #调试后发现getimg获取图片都会403,所以使用urlretrieve  待确定原因
        #getimg(image,u'详情图%s.jpg'%x)
        urllib.urlretrieve(image,PICPATH+u'/详情图%s.jpg'%x)
        print u'详情图%s'%x
        x += 1
#抓取颜色分类图片
def getColorImg(url):
    html = urllib.urlopen(url).read()
    reg = r'background:url\((.*?\.jpg)'
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    print imglist
    x = 1
    for image in imglist:
        getimg(image,u'颜色图%s.jpg'%x)
        print u'颜色%s'%x
        x += 1
#抓取小图
def getSamilImg(url):
    html = urllib.urlopen(url).read()
    #天猫店铺
    reg1 = r'img src="(.*?\.jpg)'
    #普通店铺
    reg2 = r'img data-src="(.*?\.jpg)'
    imgre = re.compile(reg1)
    imglist = re.findall(imgre,html)
    if imglist:
        print '天猫店铺:'+ imglist[0]
    else:
        imgre = re.compile(reg2)
        imglist = re.findall(imgre,html)
        print '普通店铺：'+ imglist[0]
    x = 1
    for image in imglist:
        getimg(image,u'缩图%s.jpg'%x)
        x += 1
#保存图片
def getimg(imageURL,fileName):
    global PICPATH
    if  'http'in imageURL:
        pass
    else:
        imageURL = 'http:'+imageURL
    image_name =PICPATH + fileName
    content = http_get2(imageURL)
    with open(image_name, 'wb') as f:
        f.write(content[1])
    print u'保存图片%s'%fileName
'''
#获取天猫商城详细描述api
#此接口作废，不再适用，但可借鉴次接口的写法
def getdescrptionApi(url):
     html = urllib.urlopen(url).read()
     reg1 = r'"newProGroup"[\s\S]+"weight":'
     imgre = re.compile(reg1)
     imglist = re.findall(imgre,html.decode('gbk', 'ignore'))
     print imglist
     s = '{'+imglist[0]+'0}'
     jo = json.loads(s,encoding='utf-8')
     for group in jo['newProGroup']:
         print group['groupName']
         for j in group['attrs']:
             print j['name']+':'+j['value']
     reg2 = r'"title":"(.*?)"'
     imgre = re.compile(reg2)
     imglist = re.findall(imgre,html.decode('gbk', 'ignore'))
     print imglist[0].encode('utf-8')
'''
#天猫获取宝贝标题和产品参数信息
def getdescrptionTmall(url):
     html = urllib.urlopen(url).read()
     page = etree.HTML(html.lower().decode('gbk'))
     attrlist = page.xpath("//div[@class='attributes-list']//li")
     for i in attrlist:
         print i.text
     reg1 = r'"title":"(.*?)"'
     imgre = re.compile(reg1)
     imglist = re.findall(imgre,html.decode('gbk', 'ignore'))
     print imglist[0].encode('utf-8')
#店铺获取宝贝标题和产品参数信息
def getdescriptionTb(url):
    html = urllib.urlopen(url).read()
    page = etree.HTML(html.lower().decode('gbk'))
    attrlist = page.xpath("//ul[@class='attributes-list']//li")
    for i in attrlist:
        print i.text
    mainTitle = page.xpath("//h3[@class='tb-main-title']")
    for i in mainTitle:
        print i.text
getdescrptionTmall('https://detail.tmall.com/item.htm?spm=a230r.1.14.70.1gy6cm&id=41803189529&ns=1&abbucket=16')
    #TODO:写入csv文件，实现一键复制店铺信息

#getdescrptionapi('https://detail.tmall.com/item.htm?spm=a230r.1.14.37.hIJluL&id=537078569720&ns=1&abbucket=16')
#set_fodlerName()
#getRealimg(getRealurl('https://detail.tmall.com/item.htm?spm=a230r.1.14.37.hIJluL&id=537078569720&ns=1&abbucket=16'))
#getdescriptinApi('https://detail.tmall.com/item.htm?spm=a230r.1.14.1.tl9oK9&id=537078569720&cm_id=140105335569ed55e27b&abbucket=8')
'''
#以下是图形化界面
def callback():
    rtnkey()
def rtnkey(event=None):
    set_fodlerName()
    getRealimg(getRealurl(e.get()))
    getSamilImg(e.get())
    getColorImg(e.get())
root = Tk()
root.title('imageSpider')
e = StringVar()
entry = Entry(root, validate='key', text=e, width=50).pack()
Button(root, text="抓取淘宝店铺图片", fg="blue",bd=2,width=28,command=callback).pack()
root.mainloop()
'''
