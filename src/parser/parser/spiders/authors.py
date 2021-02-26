import scrapy
import functions as func
import parser.items as items


class AuthorsSpider(scrapy.Spider):
    name = "authors"
    custom_settings = {
        "ITEM_PIPELINES": {
            "parser.pipelines.AuthorsPipeline": 300,
        }
    }

    def start_requests(self):
        """Start the parsing

        :return:
        """
        url = "https://blog.griddynamics.com/all-authors/"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """Parsing author urls

        :param response:
        :return:
        """
        refs_authors = response.css('.row.viewmore a[href]::attr(href)').extract()

        full_urls_authors = func.do_urls(refs_authors)

        for url in full_urls_authors:
            yield scrapy.Request(url=url, callback=self.parse_authors)

    def parse_authors(self, response):
        """Parsing the authors from urls

        :param response:
        :return:
        """
        name = response.css('.authorcard.popup .titlewrp h3::text').extract()  # 1
        job_title = response.css('.authorcard.popup .titlewrp p[class*=jobtitle]::text').extract()  # 2
        linkedIn = response.css('.authorcard.popup .socicon.li a[href]::attr(href)').extract()  # 3
        counter_articles = len(response.css('.authorcard.popup .postsrow a[href]::attr(href)').extract())  # 4

        data = items.AuthorItem()
        data['name'] = name
        data['jobTitle'] = job_title
        data['linkedIn'] = linkedIn
        data['counterArticles'] = counter_articles

        yield data
