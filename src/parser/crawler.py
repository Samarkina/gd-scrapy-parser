import logging
import scrapy
import subprocess
import os
from scrapy.crawler import CrawlerProcess
from parser.spiders.articles import ArticlesSpider
from parser.spiders.authors import AuthorsSpider
import parser.spiders.common.functions as func
import datetime

def reading():
    # read the data from blog
    # os.system("./scrapy-spider.sh")

    spiders = [ArticlesSpider, AuthorsSpider]
    crawler = CrawlerProcess()

    for spider in spiders:
        crawler.crawl(spider)
    crawler.start()
    logging.info('All the site data was writting in JSON files in resource directory')

def date_convert(date):
    newDate = datetime.datetime.strptime(date, '%b %d %Y').strftime('%Y/%m/%d')
    return newDate

def extract_date(json):
    try:
        return date_convert(json['date'])
    except KeyError:
        return 0

def sort_json_by_date(fullFilename):
    # sort json file by date
    # needs sort just articles
    articlesJson = func.json_reader(fullFilename)
    articlesJson.sort(key=extract_date, reverse=False)

    logging.info('%s file was sorted by date', fullFilename)
    func.json_writer(fullFilename, articlesJson)

def get_last_db_date(fullFilename):
    # get_last_db_date in db json file
    articlesJson = func.json_reader(fullFilename)
    lastDate = extract_date(articlesJson[len(articlesJson) - 1])

    logging.info('Last date was found')
    logging.info('Last date is %s in json-DB', lastDate)
    return lastDate


def check_data():
    filename = "articles"
    fullFilename = "./resources/" + filename + ".json"

    logging.info('Check the data from json-DB')

    sort_json_by_date(fullFilename)
    lastDBDate = get_last_db_date(fullFilename)

    logging.info('Check the new data from site')

    # TODO : check the data from the site



def crawler(last_date):
    # check new articles

    # a) If there are no new posts, log in console says there are no new
    # blog posts since the last date.

    # b) If there are new posts write them to data (file/db) and for each author
    # - update information (articles counter, or add new author if not exist).
    # Only for authors of this posts.



    # last blog post date must be extracted.

    # start parsing data from Blog.
    print("123www")

    # Crawler needs to append only new data that’s older than the most recent blog-post date.

    # if posts is newer than last_date-post, then return to report.py
    # while пока reading

    #return your data to report.py




    # return data






def main():
    # last_date = get_last_date() # return the last date of publish
    #
    #
    # posts = crawler(last_date)

    logging.info('********* STEP 1. Read the data from the site *********')
    # reading()



    logging.info('********* STEP 2. Check new data *********')
    check_data()


    logging.info('********* STEP 3. Upload the new data to json-DB *********')

    return 0
