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