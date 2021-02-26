import scrapy
import re
import functions as func
import parser.items as items


class ArticlesSpider(scrapy.Spider):
    name = "articles"
    custom_settings = {
        "ITEM_PIPELINES": {
            "parser.pipelines.ArticlesPipeline": 300,
        }
    }

    def start_requests(self):
        """Start the parsing

        :return:
        """
        url = 'https://blog.griddynamics.com/'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """Parsing article urls

        :param response:
        :return:
        """
        topics = response.css('span').xpath('@data-value').getall()

        urls = func.do_urls(topics)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_topics)

    def parse_topics(self, response):
        """Parsing the topics from urls

        :param response:
        :return:
        """
        references = response.css('div.container').css('a.card.cardtocheck').xpath('@href').extract()

        top_references = response.css('div.container').css('a.card.featured').xpath('@href').extract()

        urls = func.do_urls(references + top_references)

        # needs get only new urls
        new_urls = func.get_new_urls(urls)

        for url in new_urls:
            yield scrapy.Request(url=url, callback=self.parse_articles)

    def parse_articles(self, response):
        """Parsing the articles from urls

        :param response:
        :return:
        """
        title = response.css('h1.mb30::text').get()  # 1
        url = response.css('link[rel*=canonical]::attr(href)').get()  # 2
        first_symbols = response.css('.container p::text').get()[0:160]  # 3
        date = re.sub('[^A-Za-z0-9 ]+', '', response.css('.sdate::text').get()).strip()  # 4
        author_name = response.css('.name::text').get().strip()  # 5
        tags = response.css('meta[property*=\'article:tag\']::attr(content)').getall()  # 6

        data = items.ArticleItem()
        data['title'] = title
        data['url'] = url
        data['firstSymbols'] = first_symbols
        data['date'] = date
        data['authorName'] = author_name
        data['tags'] = tags

        yield data


