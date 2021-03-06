# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from urllib import parse
from scrapy.http import Request

from ArticleSpider.items import JobBoleAritcleItem, ArticleItemLoader
from ArticleSpider.utils.common import get_md5
from scrapy.loader import ItemLoader
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals


class JobboleSpider(scrapy.Spider):
    name = 'Jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']


    # def __init__(self):
    #     self.browser = webdriver.Chrome(executable_path="H:\chromedriver.exe")
    #     super(JobboleSpider, self).__init__()
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)
    #
    # def spider_closed(self, spider):
    #     # 当爬虫关闭时关闭浏览器
    #     print("spider closed")
    #     self.browser.quit()

    # 收集伯乐在线所有404错误url和页面数
    handle_httpstatus_list = [404]

    def __init__(self):
        self.fail_urls = []
        # dispatcher.connect(self.handle_spider_close, signals.spider_closed)

    # 数据收集器使用
    # def handle_spider_close(self):
    #     self.crawler.stats.set_value("failed_urls", ",".join(self.fail_urls))

    def parse(self, response):
        """
        1:获取文章列表的url并交给scrapy进行下载
        2：获取下一页的url并进行下载，下载完成后交给parse
        """
        if response.status == 404:
            self.fail_urls.append(response.url)
            self.crawler.stats.inc_value("failed_url")

        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            image_url = parse.urljoin(response.url, image_url)
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url = parse.urljoin(response.url, post_url), meta = {'front_image_url':image_url}, callback=self.parse_detail)

        next_urls = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_urls:
            yield Request(url = parse.urljoin(response.url, next_urls), callback = self.parse)


    def parse_detail(self, response):
        """
        提取文章
        """
        article_item = JobBoleAritcleItem()
        # title = response.xpath('//*[@id="post-112499"]/div[1]/h1/text()').extract()[0]
        # date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].strip().replace("·", "")
        # priase_nums = int(response.xpath("//span[contains(@class, 'vote-post-up')]/h10/text()").extract()[0])
        # fav_nums = response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract()[0]
        # match_re = re.match(".*?(\d+).*", fav_nums)
        # if match_re:
        #     fav_nums = int(match_re.group(1))
        # comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
        # match_re = re.match(".*?(\d+).*", comment_nums)
        # if match_re:
        #     comment_nums = int(match_re.group(1))
        # content = response.xpath("//div[@class='entry']").extract()[0]
        # author = response.xpath("//a[@href='http://www.jobbole.com/members/hanxiaomax']/text()").extract_first("")
        # pass

        # title = response.css(".entry-header h1::text").extract()[0]
        # date = response.css("p.entry-meta-hide-on-mobile::text").extract()[0].strip().replace("·", "")
        # priase_nums = response.css(".vote-post-up h10::text").extract()[0]
        # fav_nums = response.css("span.bookmark-btn::text").extract()[0]
        # match_re = re.match(".*?(\d+).*", fav_nums)
        # if match_re:
        #     fav_nums = int(match_re.group(1))
        # else:
        #     fav_nums = 0
        # comment_nums = response.css("span.hide-on-480::text").extract()[0]
        # match_re = re.match(".*?(\d+).*", comment_nums)
        # if match_re:
        #     comment_nums = int(match_re.group(1))
        # else:
        #     comment_nums = 0
        # content = response.css("div.entry").extract()[0]
        #
        # article_item["url_object_id"] = get_md5(response.url)
        # article_item["title"] = title
        # article_item["url"] = response.url
        # try:
        #     date = datetime.datetime.strptime(date, "%Y/%m/%d").date()
        # except Exception as e:
        #     date = datetime.datetime.now().date()
        # article_item["create_date"] = date
        # article_item["front_image_url"] = [front_image_url]
        # article_item["praise_nums"] = priase_nums
        # article_item["fav_nums"] = fav_nums
        # article_item["comment_nums"] = comment_nums
        # article_item["content"] = content


        #通过Itemloader加载
        front_image_url = response.meta.get("front_image_url", "")  # 文章封面图
        item_loader = ArticleItemLoader(item = JobBoleAritcleItem(), response = response)
        item_loader.add_css('title', '.entry-header h1::text')
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_object_id', get_md5(response.url))
        item_loader.add_css('create_date', 'p.entry-meta-hide-on-mobile::text')
        item_loader.add_value('front_image_url', [front_image_url])
        item_loader.add_css('praise_nums', '.vote-post-up h10::text')
        item_loader.add_css('fav_nums', 'span.bookmark-btn::text')
        item_loader.add_css('comment_nums', 'span.hide-on-480::text')
        item_loader.add_css('content', 'div.entry')

        article_item = item_loader.load_item()

        yield article_item


