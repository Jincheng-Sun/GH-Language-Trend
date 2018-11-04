#coding:utf-8
#!/usr/bin/env python
#author:Z0fr3y
#update:2015-10-7
#version:2.4
#name:GitHubSpider
#运行scrapy crawl github
import urllib
from scrapy import Request
from scrapy.spider import Spider
from scrapy.selector import Selector
#from scrapy.spiders import CrawlSpider, Rule
from items import Github_Item
#import pymongo

import sys
import os
reload (sys)
sys.setdefaultencoding("utf-8")#这句话让爬到的内容是utf-8的
#PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))#返回绝对路径（#返回文件路径）

host="https://github.com"
global a
a=1
global b#抓取了多少人
b=0
global c#想抓取几人信息
c=10
global f_newlist#文件名（不包含后缀），避免重复爬取。
f_newlist=[]
class GithubSpider(Spider):
    """
    爬取GitHub网站中用户信息
    """
    name = 'github'
    allowed_domains = ['github.com']
    headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip,deflate",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Connection": "keep-alive",
    "Content-Type":" application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
    }
    start_urls = ["https://github.com/ruanyf",]#GitHub下随便哪个人的主页
    #def __init__(self,category=None,*args,**kwargs):
        #super(GithubSpider,self).__init__(*args,**kwargs)

    def getfile(self):#获取文件名（不包含后缀)
        path = r'/Users/sunjincheng/Desktop/pocprogram/gituserinfo/gituserinfo/download'
        f_list = os.listdir(path)
        print f_list
        global f_newlist
        for i in range(0,len(f_list)):
            l,b=os.path.splitext(f_list[i])#将名与后缀分开
            f_newlist.append(l)
        return f_newlist
    def parse(self,response):
        print "~"*60+"start"
        print response.url
        people_mainpage=Selector(response)
        self.getfile()
        global f_newlist
        people=Github_Item()#以下是爬取用户的详细信息
        people_profile=people_mainpage.xpath('//div[@class="column one-fourth vcard"]')
        people['image_urls'] = people_profile.xpath('a[1]/img/@src').extract()
        x1=people_profile.xpath('h1/span[@class="vcard-fullname"]/text()').extract()
        if x1==[]:#避免fullname为空
            people['fullname']="None"
        else:
            people['fullname']=x1[0]
        for i in range(0,len(f_newlist)):#如果名字与已存在的txt文件一致，就选择不爬取，跳到第一个主页的followers页面，从新爬取。
            if (people['fullname']==f_newlist[i]):
                yield Request(url="https://github.com/ruanyf/followers",callback=self.parse_two,dont_filter=True)
        x2=people_profile.xpath('h1/span[@class="vcard-username"]/text()').extract()[0]
        if x2==[]:
            people['username']="None"
        else:
            people['username']=x2[0]
        x3=people_profile.xpath('//li/@title').extract()
        if x3==[]:
            people['organization']="None"
        else:
            people['organization']=x3[0]
        x4=people_profile.xpath('//a[@class="email"]/text()').extract()
        if x4==[]:
            people['mail']="None"
        else:
            people['mail']=x4[0]
        people['joined']=people_profile.xpath('//time[@class="join-date"]/text()').extract()[0]
        people['followers']=people_profile.xpath('div[@class="vcard-stats"]/a[1]/strong[@class="vcard-stat-count"]/text()').extract()[0]
        people['starred']=people_profile.xpath('div[@class="vcard-stats"]/a[2]/strong[@class="vcard-stat-count"]/text()').extract()[0]
        people['following']=people_profile.xpath('div[@class="vcard-stats"]/a[3]/strong[@class="vcard-stat-count"]/text()').extract()[0]

        popular_repo=people_mainpage.xpath('//div[@class="columns popular-repos"]/div[@class="column one-half"][1]')
        people['popular_repos']=" "
        for i in range(1,6):#这是popular_repos数据
            people['popular_repos']=people['popular_repos']+" "+' '.join(popular_repo.xpath('div/ul[@class="boxed-group-inner mini-repo-list"]/li['+str(i)+']/a/span[2]/span/text()').extract())
        repo_contribution=people_mainpage.xpath('//div[@class="columns popular-repos"]/div[@class="column one-half"][2]')
        people['repo_contributions']=" "
        for i in range(1,6):#这是repo_contributions数据
            people['repo_contributions']=people['repo_contributions']+" "+' '.join(repo_contribution.xpath('div/ul[@class="boxed-group-inner mini-repo-list"]/li['+str(i)+']/a/span[2]/span[1]/text()').extract())+"/"+' '.join(repo_contribution.xpath('div/ul[@class="boxed-group-inner mini-repo-list"]/li['+str(i)+']/a/span[2]/span[2]/text()').extract())

        followers_page=host+''.join(people_mainpage.xpath('//a[@class="vcard-stat"][1]/@href').extract())
        xxxx=people
        #'../media.people/'GitHub\media\people
        fh=open('/Users/sunjincheng/Desktop/pocprogram/gituserinfo/gituserinfo/download'+people['fullname']+'.txt','w')
        fh.write(str(xxxx))#将爬取下来的信息保存到文件
        fh.close()
        global b
        global c
        if b<c:
            b+=1
            print str(b)+" "+ "people Detail information"
            yield Request(url=followers_page,callback=self.parse_followers,dont_filter=True)
        print "~"*60+"over"
        if (b<=c):
            yield people


    def parse_followers(self,response):
        print "~"*60+"parse_followers"
        print response.url
        people_parse_one=Selector(response)
        followers_parse_one_link=host+''.join(people_parse_one.xpath('//ol[@class="follow-list clearfix"]/li[1]/a/@href').extract())
        print followers_parse_one_link
        yield Request(url=followers_parse_one_link,callback=self.parse_one,dont_filter=True)

    def parse_one(self,response):
        print "~"*60+"parse_one_start"
        print response.url
        people_parse_one=Selector(response)
        x=people_parse_one.xpath('//div[@class="vcard-stats"]/a[1]/strong[@class="vcard-stat-count"]/text()').extract()
        #print "x=:"+x[0]
        #y=int(''.join([str(t) for t in x]))
        #print "y=:"+y
        print "x=:"
        print x
        if (x!= ["0"]):
            print "followers is not 0 ....Go to--->"
            yield Request(url=response.url,callback=self.parse,dont_filter=True)
        else:
            yield Request(url="https://github.com/ruanyf/followers",callback=self.parse_two,dont_filter=True)
    def parse_two(self,response):
        print "~"*60+"parse_two_start"#主页面人的followers页
        print response.url
        people_parse_two=Selector(response)
        global a
        a+=1
        print "global a: "
        print a
        if (a<10):
            followers_parse_two_link=host+''.join(people_parse_two.xpath('//ol[@class="follow-list clearfix"]/li['+str(a)+']/a/@href').extract())
            yield Request(url=followers_parse_two_link,callback=self.parse,dont_filter=True)
