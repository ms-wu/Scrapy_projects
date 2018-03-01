# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import datetime
import scrapy
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from ArticleSpider.utils.common import extract_num
from ArticleSpider.settings import SQL_DATETIME_FORMAT, SQL_DATE_FORMAT
from w3lib.html import remove_tags


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def date_convert(value):
    try:
        date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        date = datetime.datetime.now().date()
    return date


def get_nums(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        value = int(match_re.group(1))
    else:
        value = 0
    return value


def return_value(value):
    return value


class ArticleItemLoader(ItemLoader):
    #自定义Itemloader
    default_output_processor = TakeFirst()


class JobBoleAritcleItem(scrapy.Item):
    title = scrapy.Field(
    )
    create_date = scrapy.Field(
        input_processor = MapCompose(date_convert),
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor = MapCompose(return_value),
    )
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor = MapCompose(get_nums),
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums),
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums),
    )
    content = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                    insert into jobbole_article(title, create_date, url, fav_nums)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE fav_nums=VALUES(fav_nums)
                        """
        params = (self["title"], self["create_date"], self["url"], self["fav_nums"])
        return insert_sql, params


class ZhihuQuestionItem(scrapy.Item):
    #知乎问题 item
    zhihu_id = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    answer_num = scrapy.Field()
    comments_num = scrapy.Field()
    watch_user_num = scrapy.Field()
    click_num = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        # 插入知乎question表的sql结构
        insert_sql = """
                   insert into zhihu_question(zhihu_id, topics, url, title, content, answer_num, comments_num, 
                   watch_user_num, click_num, crawl_time
                   ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                   ON DUPLICATE KEY UPDATE content=VALUES(content), answer_num=VALUES(answer_num), comments_num=VALUES(comments_num), 
                   watch_user_num=VALUES(watch_user_num), click_num=VALUES(click_num)
        """

        zhihu_id = self["zhihu_id"][0]
        topics = ",".join(self["topics"])
        url = self["url"][0]
        title = "".join(self["title"])
        content = "".join(self["content"])
        answer_num = self["answer_num"][0]
        comments_num=extract_num("".join(self["comments_num"]))
        watch_user_num = self["watch_user_num"][0]
        if len(self["watch_user_num"]) == 2:
            click_num = self["watch_user_num"][1]
        else:
            click_num = 0
        crawl_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)

        params = (zhihu_id, topics, url, title, content, answer_num, comments_num,
                  watch_user_num, click_num, crawl_time)
        return insert_sql, params

class ZhihuAnswerItem(scrapy.Item):
    #知乎回答 item
    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    praise_num = scrapy.Field()
    comments_num = scrapy.Field()
    create_time = scrapy.Field()
    updata_time = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        # 插入知乎question表的sql结构
        insert_sql = """
                   insert into zhihu_answer(zhihu_id, url, question_id, author_id, content, praise_num, comments_num, 
                   create_time, updata_time, crawl_time
                   ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                   ON DUPLICATE KEY UPDATE content=VALUES(content), comments_num=VALUES(comments_num), praise_num=VALUES(praise_num),  
                   updata_time=VALUES(updata_time)
        """

        create_time = datetime.datetime.fromtimestamp(self["create_time"]).strftime(SQL_DATETIME_FORMAT)
        updata_time = datetime.datetime.fromtimestamp(self["updata_time"]).strftime(SQL_DATETIME_FORMAT)
        params = (
            self["zhihu_id"], self["url"], self["question_id"],
            self["author_id"], self["content"], self["praise_num"],
            self["comments_num"], create_time, updata_time,
            self["crawl_time"].strftime(SQL_DATETIME_FORMAT)
        )

        return insert_sql, params

def remove_splash(value):
    # 去掉工作城市中的斜线
    return value.replace("/", "")

def handle_workaddr(value):
    addr_list = value.split("\n")
    addr_list = [item.strip() for item in addr_list if item.strip()=="查看地图"]
    return "".join(addr_list)


class LagouJobItemLoader(ItemLoader):
    #自定义Itemloader
    default_output_processor = TakeFirst()

class LagouJobItem(scrapy.Item):
    # 拉勾网信息
    url = scrapy.Field()
    url_id = scrapy.Field()
    title = scrapy.Field()
    salary = scrapy.Field()
    work_place = scrapy.Field(
        input_processor = MapCompose(remove_splash),
    )
    work_years = scrapy.Field(
        input_processor = MapCompose(remove_splash),
    )
    degree_need = scrapy.Field(
        input_processor = MapCompose(remove_splash),
    )
    job_type = scrapy.Field()
    publish_time = scrapy.Field()
    tags = scrapy.Field(
        input_processor = Join(",")
    )
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field()
    work_addr = scrapy.Field(
        input_processor=MapCompose(remove_tags, handle_workaddr),
    )
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
              insert into lagou(url, url_id, title, salary, work_place, work_years, degree_need,
               job_type, publish_time, tags, job_advantage, job_desc, job_addr, crawl_time)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               ON DUPLICATE KEY UPDATE salary=VALUES(salary), job_desc=VALUES(job_desc), crawl_time=VALUES(crawl_time),  
                   job_advantage=VALUES(job_advantage)
        """
        params = (
            self["url"], self["url_id"], self["title"], self["salary"], self["work_place"],
            self["work_years"], self["degree_need"], self["job_type"], self["publish_time"],
            self["tags"], self["job_advantage"], self["job_desc"], self["crawl_time"].strftime(SQL_DATETIME_FORMAT)
        )

        return insert_sql, params


