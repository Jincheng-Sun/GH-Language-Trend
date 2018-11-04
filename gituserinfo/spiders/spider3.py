import scrapy
from scrapy.selector import Selector
import re
from .items import Github_Item
from scrapy.loader import ItemLoader
global userlist
userlist = []


class gUserInfo(scrapy.Spider):
    name = "guserinfo"
    allowed_domains = ['github.com']
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip,deflate",
        "Accept-Language": "en-US,en;q=0.8",
        "Connection": "keep-alive",
        "Content-Type": " application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
    }
    start_urls = [
        "https://www.github.com/ruanyf/",
    ]
    def parse(self, response):
        gituser=Github_Item()
        # gituser = ItemLoader(Github_Item,response=response)
        # gituser.add_xpath('fullname','//div[@class="vcard-names-container py-3 js-sticky js-user-profile-sticky-fields "]/h1[@class="vcard-names"]/span[@class="p-name vcard-fullname d-block overflow-hidden"]')
        # gituser.add_xpath('username','//div[@class="vcard-names-container py-3 js-sticky js-user-profile-sticky-fields "]/h1[@class="vcard-names"]/span[@class="p-nickname vcard-username d-block"]')
        # gituser.add_xpath('location','//ul[@class="vcard-details"]/li[@class="vcard-detail pt-1 css-truncate css-truncate-target"]/span[@class="p-label"]')
        # gituser.add_xpath('repos','//div[@class="col-9 float-left pl-2"]/div[@class="UnderlineNav user-profile-nav js-sticky top-0"]/nav[@class="UnderlineNav-body"]//span[@class="Counter"]')
        selector = Selector(response)
        fullname = selector.xpath(
            '//div[@class="vcard-names-container py-3 js-sticky js-user-profile-sticky-fields "]/h1[@class="vcard-names"]/span[@class="p-name vcard-fullname d-block overflow-hidden"]/text()').extract_first()
        username = selector.xpath(
            '//div[@class="vcard-names-container py-3 js-sticky js-user-profile-sticky-fields "]/h1[@class="vcard-names"]/span[@class="p-nickname vcard-username d-block"]/text()').extract()
        location = selector.xpath(
            '//ul[@class="vcard-details"]/li[@class="vcard-detail pt-1 css-truncate css-truncate-target"]/span[@class="p-label"]/text()').extract()
        # basicinfo = selector.xpath('//div[@class="col-9 float-left pl-2"]/div[@class="UnderlineNav user-profile-nav js-sticky top-0"]/nav[@class="UnderlineNav-body" data-pjax role="navigation"]/a[1][@class="UnderlineNav-item "]/span[@class="Counter"]text()').extract()
        basicinfo = selector.xpath('//div[@class="col-9 float-left pl-2"]/div[@class="UnderlineNav user-profile-nav js-sticky top-0"]/nav[@class="UnderlineNav-body"]//span[@class="Counter"]/text()')
        followers = basicinfo.extract()[2]
        starred = basicinfo.extract()[1]
        repos = basicinfo.extract()[0]

        gituser['fullname'] = fullname
        gituser['username'] = username
        gituser['location'] = location
        gituser['followers'] = re.sub(r'\s+','', followers)
        gituser['starred'] = re.sub(r'\s+','', starred)
        gituser['repos'] = re.sub(r'\s+','', repos)
        # print gituser
        return gituser
