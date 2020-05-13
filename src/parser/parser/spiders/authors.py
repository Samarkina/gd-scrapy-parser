import scrapy
import src.parser.functions as func

class AuthorsSpider(scrapy.Spider):
    name = "authors"

    def start_requests(self):
        urls = [
            "https://blog.griddynamics.com/all-authors/"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        refsAuthors = response.css('.row.viewmore a[href]::attr(href)').extract()

        fullUrlsAuthors = func.do_urls(refsAuthors)

        for url in fullUrlsAuthors:
            yield scrapy.Request(url=url, callback=self.parse_authors)


    def parse_authors(self, response):
        name = response.css('.authorcard.popup .titlewrp h3::text').extract() # 1
        jobTitle = response.css('.authorcard.popup .titlewrp p[class*=jobtitle]::text').extract() # 2
        linkedIn = response.css('.authorcard.popup .socicon.li a[href]::attr(href)').extract() # 3
        counterArticles = len(response.css('.authorcard.popup .postsrow a[href]::attr(href)').extract()) # 4

        data = {"name": name, "jobTitle": jobTitle, "linkedIn": linkedIn, "counterArticles": counterArticles}
        func.upload_data(self, "authors_temp", data)




