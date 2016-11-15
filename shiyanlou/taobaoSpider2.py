#encoding=utf8
import urllib
import re
import httplib2
import os
from PIL import Image
import time
from datetime import datetime
from Tkinter import *
import json
import sys
'''
Created on May 10, 2016
@author: qianbingbing
@funcation:get image from taobao
parameter:url
return:image
'''
TIMEOUT = 5
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-us,en;q=0.5',
    'Accept-Encoding': 'gzip',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
    'Keep-Alive': '115',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Host':'cbu01.alicdn.com'
}
FODLER_NAME = ''
PICPATH = ''
def http_get(url):
        conn = httplib2.Http(timeout=TIMEOUT)
        content = conn.request(uri=url, method='GET', body=None, headers=DEFAULT_HEADERS)
        return content
#创建图片存放目录
def set_fodlerName():
    global FODLER_NAME,PICPATH
    #foldername = datetime.now().strftime('%Y-%m-%d-%H-%M')
    PICPATH = 'F:\\taobaoImage\\%s\\' % (FODLER_NAME) #下载到的本地目录
    if not os.path.exists(PICPATH):   #路径不存在时创建一个
        os.makedirs(PICPATH)
    return PICPATH
#获取详细描述的api
def getRealurl(url):
    html = urllib.urlopen(url).read()
    #天猫店铺
    #reg1 = r'"descUrl":"(.*?)"'
    reg2 = r'descUrl          : location\.protocol===\'http\:\' \? \'(.*?\')'
    imgre = re.compile(reg2)
    imglist = re.findall(imgre,html)
    print imglist
    return imglist[0]
#根据详细描述的api得到所有详细描述中图片
def getRealimg(url):
    html = urllib.urlopen(url).read()
    set_fodlerName()
    reg1 = r'src="(.*?\.jpg)" '
    reg2 = r'src=\\"(.*?\.jpg)'
    imgre = re.compile(reg1)
    imglist = re.findall(imgre,html)
    '''
	多次调试发现，有些商品的地址src后面带\\所以
	如果通过第一个正则匹配不到内容则尝试使用第二个正则来匹配
	'''
    if imglist:
        print imglist
        pass
    else:
        imgre = re.compile(reg2)
        imglist = re.findall(imgre,html)
        print imglist
    x = 1
    for image in imglist:
        getimg(image,u'详情图%s.jpg'%x)
        x += 1
#抓取颜色分类图片
def getColorImg(url):
    html = urllib.urlopen(url).read()
    reg3 = r'background:url\((.*?\.jpg)'
    imgre = re.compile(reg3)
    imglist = re.findall(imgre,html)

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
        x = 1
        for image in imglist:
            getimg(image,u'缩略图%s.jpg'%x)
            x += 1
    else:
        return
#保存图片
def getimg(imageURL,fileName):
    global PICPATH
    if  'http'in imageURL:
        pass
    else:
        imageURL = 'http:'+imageURL
    image_name =PICPATH + fileName
    content = http_get(imageURL)
    with open(image_name, 'wb') as f:
        f.write(content[1])
    print u'保存图片%s'%fileName
def getdescrptionapi(url):
     html = urllib.urlopen(url).read()
     reg1 = r'"newProGroup"[\s\S]+"weight":'
     imgre = re.compile(reg1)
     imglist = re.findall(imgre,html)
     s = '{'+imglist[0]+'0}'
     jo = json.loads(s,encoding='GB2312')
     print jo
     for group in jo['newProGroup']:
         for j in group['attrs']:
             print j['name']+':'+j['value']



getdescrptionapi("https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.4.XyH34l&id=538355680030&skuId=3215190806779&user_id=1646524828&cat_id=2&is_b=1&rn=0858a604c2a9b420094386fa965b3ae8")
'''
def callback():
    rtnkey()
def rtnkey(event=None):
    getRealimg(getRealurl(e.get()))
    getSamilImg(e.get())
root = Tk()
root.title('imageSpider')
e = StringVar()
entry = Entry(root, validate='key', text=e, width=50).pack()
Button(root, text="抓取图片", fg="blue",bd=2,width=28,command=callback).pack()
root.mainloop()
'''

