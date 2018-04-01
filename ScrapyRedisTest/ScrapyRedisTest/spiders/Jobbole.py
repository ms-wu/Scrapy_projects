from urllib import parse
from scrapy.http import Request
from scrapy_redis.spiders import RedisSpider


class JobboleSpider(RedisSpider):
    name = 'Jobbole'
    allowed_domains = ['blog.jobbole.com']
    redis_key = 'Jobbole:start_urls'

    def parse(self, response):
        """
        1:获取文章列表的url并交给scrapy进行下载
        2：获取下一页的url并进行下载，下载完成后交给parse
        """

        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            image_url = parse.urljoin(response.url, image_url)
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={'front_image_url': image_url},
                          callback=self.parse_detail)

        next_urls = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_urls:
            yield Request(url=parse.urljoin(response.url, next_urls), callback=self.parse)

    def parse_detail(self, response):
        """
        提取文章
        """
        pass