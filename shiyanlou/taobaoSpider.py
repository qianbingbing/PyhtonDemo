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
def getPageSource(url):
     html = urllib.urlopen(url).read()
     return html
#创建图片存放目录
def set_fodlerName(html):
    global PICPATH
    foldername = getTitle(html)
    PICPATH = 'F:\\taobaoImage\\%s\\' % (foldername) #下载到的本地目录
    if not os.path.exists(PICPATH):   #路径不存在时创建一个
        os.makedirs(PICPATH)
    return PICPATH
#获取详细描述的链接
def getRealurl(html):
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
#根据详细描述的链接得到详细描述图片
def getRealimg(descurl):
    global PICPATH
    html = http_get1('http:'+descurl)
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
#抓取颜色文字及颜色图片链接
def getColorImg(html):
    reg = r'background:url\((.*?\.jpg)'
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    page = etree.HTML(html.lower().decode('gbk'))
    titles_of_Tmall = page.xpath("//dl[@class='tb-prop tm-sale-prop tm-clear tm-img-prop ']//li//span")
    print titles_of_Tmall
    titles_of_Taobao = page.xpath('//dl[@class="J_Prop tb-prop tb-clear  J_Prop_Color"]')
    print titles_of_Taobao
    if titles_of_Tmall:
        for title in titles_of_Tmall:
            print title.text
    else:
        for title in titles_of_Taobao:
            print title.text
    for image in imglist:
        #getimg(image,u'颜色图%s.jpg'%x)
        print image
#获取标题文字
def getTitle(html):

     #淘宝
     reg1 = r'"title":"(.*?)"'
     imgre = re.compile(reg1)
     imglist = re.findall(imgre,html.decode('gbk', 'ignore'))
     print imglist[0].encode('utf-8')
     #天猫
     page = etree.HTML(html.lower().decode('gbk'))
     mainTitle = page.xpath("//h3[@class='tb-main-title']")
     for i in mainTitle:
         print i.text
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
#获取产品参数信息
def getdescription(html):
    page = etree.HTML(html.lower().decode('gbk'))
    attrlist = page.xpath("//ul[@class='attributes-list']//li")
    for i in attrlist:
        print i.text
#获取宝贝标题
def getTitles(html):
     reg1 = r'"title":"(.*?)"'
     imgre = re.compile(reg1)
     mainTitle = re.findall(imgre,html.decode('gbk', 'ignore'))
     if mainTitle:
         print mainTitle[0].encode('utf-8').strip()
     else:
         page = etree.HTML(html.lower().decode('gbk'))
         mainTitle = page.xpath("//h3[@class='tb-main-title']")
         for i in mainTitle:
            print i.text.strip()
#天猫获shopSetapi
def getTShopSetup(html):
    reg1 = r'"api":[\s\S]+"valTimeLeft":'
    imgre = re.compile(reg1)
    imglist = re.findall(imgre,html)
    api  = '{'+imglist[0]+'0}'
    return api
'''
    jo = json.loads(s,encoding='GB2312')
    for i in jo['valItemInfo']['skuList']:
        pvs = i['pvs']
        for key,value in jo['propertyPics'].items():
            if  key[:-1] in pvs:
                getimg(value[0],i['names']+'.jpg')
                print u"颜色:"+i['names']
        for key,value in jo['valItemInfo']['skuMap'].items():
            if pvs in key:
                print u"价格："+ value['price']
                print u"库存："+ str(value['stock'])
'''
#获取主图
def getAuctionImages(url):
    html = urllib.urlopen(url).read()
    reg1 = r'auctionImages    : \[(.*?)\]'
    imgre = re.compile(reg1)
    auctionImages = re.findall(imgre,html)
    if auctionImages:
        for image in auctionImages[0].split(","):
            getimg(image,u'详情图%s.jpg')
    else:
        setup = getTShopSetup(html)
        jo = json.loads(setup,encoding='GB2312')
        for image in jo['propertyPics']['default']:
            getimg(image,u'详情图%s.jpg')
#获取宝贝类别
def getCid(url):
     html = urllib.urlopen(url).read()
     setup = getTShopSetup(html)
     jo = json.loads(setup,encoding='GB2312')
     print jo['rootCatId']



getCid('https://item.taobao.com/item.htm?spm=a219r.lm5693.14.1.7BQHI1&id=537192815463&ns=1&abbucket=18#detail')
#getAuctionImages('https://detail.tmall.com/item.htm?id=539564000825&ali_refid=a3_430583_1006:1104510775:N:%E5%B8%BD:82262d7b2fdfbfb85a8440a08c6f1fd1&ali_trackid=1_82262d7b2fdfbfb85a8440a08c6f1fd1&spm=a230r.1.14.3.4T1s5k&sku_properties=20509:12430610')
#set_fodlerName()
#getdescrptionTmall('https://detail.tmall.com/item.htm?id=21340371599&spm=a223v.7835278.t0.2.Zul21A&pvid=912c9641-1244-42e4-9c6f-9e719782898c&scm=1007.12144.63460.8949_0&skuId=3150516165611')
#getTShopSetup('https://detail.tmall.com/item.htm?id=21340371599&spm=a223v.7835278.t0.2.Zul21A&pvid=912c9641-1244-42e4-9c6f-9e719782898c&scm=1007.12144.63460.8949_0&skuId=3150516165611')
#getdescrptionTmall('https://detail.tmall.com/item.htm?spm=a230r.1.14.70.1gy6cm&id=41803189529&ns=1&abbucket=16')
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
