import scrapy
import re
import parser.spiders.common.functions as func

class ArticlesSpider(scrapy.Spider):
    name = "articles"

    def start_requests(self):
        urls = [
            'https://blog.griddynamics.com/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        topics = response.css('span').xpath('@data-value').getall()

        urls = func.do_urls(topics)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_topics)



    def parse_topics(self, response):
        references = response.css('div.container').css('a.card.cardtocheck').xpath('@href').extract()

        topReferences = response.css('div.container').css('a.card.featured').xpath('@href').extract()

        urls = func.do_urls(references + topReferences)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_articles)

    def parse_articles(self, response):
        title = response.css('h2.mb30::text').get() # 1
        url = response.css('link[rel*=canonical]::attr(href)').get() # 2
        firstSymbols = response.css('.container p::text').get()[0:160] # 3
        date = re.sub('[^A-Za-z0-9 ]+', '', response.css('.sdate::text').get()).strip() # 4
        authorName = response.css('.name::text').get().strip() # 5
        tags = response.css('meta[property*=\'article:tag\']::attr(content)').getall() # 6

        data = {"title": title, "url": url, "firstSymbols": firstSymbols, "date": date, "authorName": authorName,
                "tags": tags}

        func.upload_data(self, "articles", data)