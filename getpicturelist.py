import requests
from bs4 import BeautifulSoup, UnicodeDammit
import os
import re
import random
from random import choice
import pymysql

try:
    db = pymysql.connect(host="localhost", user="root", passwd="0030", database="picture-db", charset='utf8')
    cursor = db.cursor()
    print('connectsuccess')
except:
    print('Oops..there is some error')


def open_url(url):
    # heads = {}
    # heads['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    # req = requests.get(url, headers=heads).content
    # return req
    UserAgent = [
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
        'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
        'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
        'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
        'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
        'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
        'Mozilla/5.0 (iPhone; U; CPU like Mac OS X) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/4A93 Safari/419.3',
        'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Version/3.1 Safari/525.13'
    ]
    user_agent = choice(UserAgent)
    headers = {'User-Agent': user_agent}
    html = requests.get(url, headers=headers).content
    return html


def find_href(req):
    soup = BeautifulSoup(req, 'lxml')
    hreflist = []
    for each in soup.find_all('tr', class_='tr3 t_one'):

        links = each.a.get('href')
        # r = r'(htm_data/[^"]+\.html)'
        r = r'^htm_data/.+?\.html$'
        R = re.findall(r, links)
        for i in R:
            href = "http://1024.chxdoa.pw/pw/" + i
            if href:
                hreflist.append(href)
    return hreflist


def find_img(hreflist):
    print(len(hreflist))
    #datalist = []
    titlelist = []
    for i in hreflist:
        html = open_url(i)
        srclist = []
        soup = BeautifulSoup(html, 'lxml')
        title = soup.find('h1').get_text().strip()
        #cursor.execute("DROP TABLE IF EXISTS `"+title+"`")
        sql = """CREATE TABLE IF NOT EXISTS `"""+title+"""`(
            ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            href char(100)
            
            
            )"""
            
        try:
            cursor.execute(sql)
        except:
            print('error')
        
        #strip去除多余的空格(\n)
        titlelist.append(title.strip())
        for each in soup.select('div[class=f14] > img'):      
            src = each.get('src').strip()
            srclist.append(src)
        for e in srclist:
            
            data = "INSERT INTO `"+title+"`(`href`) VALUES ('"+str(e)+"');"
                    
            try:
                cursor.execute(data)
                db.commit()

            except:
                #print('faild')
                db.rollback()
    db.close()
       
        #datalist.append(srclist)
    #print(titlelist)
    #return datalist ,titlelist
    #return titlelist
#def getdata(titlelist):
    #datalist =[]
    #for title in titlelist:
        #data = "SELECT * FROM `"+title+"`;"
        #cursor.execute(data)
        #datas = cursor.fetchone()
        #datalist.append(datas)
        
    #print(datalist)
    
        

#def createdb(t):
    #for i in t[1]:
        # 使用 execute() 方法执行 SQL，如果表存在则删除
        #cursor.execute("DROP TABLE IF EXISTS" +str(i)+"")
        #sql = """CREATE TABLE `"""+str(i)+"""`(
            #id char(20) not null,
            #href char(100) 

            #)"""
        #cursor.execute(sql)


    #for a in t[0]:
         #for e in a:
             #data = """INSERT INTO """+str(i)+"""(href)
                     #VALUES("""+e+""")"""
             #cursor.execute(data)
             #db.commit()

if __name__ == '__main__':
    url = 'http://1024.chxdoa.pw/pw/thread.php?fid=14'
    find_img(find_href(open_url(url)))
