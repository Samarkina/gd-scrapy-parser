import logging
from scrapy.crawler import CrawlerProcess
import src.parser.functions as func
import datetime
import src.parser.parser.spiders.articles as articles
import src.parser.parser.spiders.authors as authors

def reading():
    # read the data from blog
    # os.system("./scrapy-spider.sh")

    spiders = [articles.ArticlesSpider, authors.AuthorsSpider]
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

def sort_json_by_date(articlesJson):
    # sort json file by date
    # needs sort just articles
    logging.info("Json file is sorting")
    articlesJson.sort(key=extract_date, reverse=False)
    return articlesJson

def sort_and_rewrite_json_file(fullFilename):
    articlesJson = func.json_reader(fullFilename)
    sortedData = sort_json_by_date(articlesJson)
    logging.info('%s file was sorted by date' % fullFilename)

    func.json_writer(fullFilename, sortedData)

def isExistArticle(article, fullFilenameDB):
    # checking exist article in DB or not
    data = func.json_reader(fullFilenameDB)

    if article in data:
        return True
    else:
        return False


def get_new_data(fullFilenameSite, fullFilenameDB):
    logging.info('Counting the delta from the site and the database')
    newData = []

    data = func.json_reader(fullFilenameSite)

    for article  in data:
        if not isExistArticle(article, fullFilenameDB):
            newData.append(article)
    if not newData:
        logging.info('Site has NO new articles')
        return None
    else:
        logging.info('Site has new articles')
        return sort_json_by_date(newData)

def upload_new_articles_to_DB(newData, fullFilenameDB):
    # upload new data to DB
    sort_and_rewrite_json_file(fullFilenameDB)
    data = func.json_reader(fullFilenameDB)

    for row in newData:
        data.append(row)

    sortedData = sort_json_by_date(data)
    func.json_writer(fullFilenameDB, sortedData)
    logging.info('New articles was uploaded in database')

def upload_new_authors_to_DB(newData, fullFilenameDB):
    # TODO
    logging.info('Check exist this author in database')

    print("13")

    logging.info('Upload the author in database')






def upload_new_data_to_DB(newData, fullFilenameDB):
    logging.info('Upload the delta from the site to the database')

    # TODO : count the delta

    # вычислить дельту в данных сайта и данных, которые есть в DB. Upload данные дельты в DB.
    # На всякий случай чекать, есть ли уже эта запись в DB.

    upload_new_articles_to_DB(newData, fullFilenameDB)

    # И в этот момент проверить, точно ли нет такого автора. И если нет, то добавить и его

    upload_new_authors_to_DB(newData, fullFilenameDB)

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
    filename = "articles"
    fullFilenameDB = "./src/parser/resources/" + filename + ".json"
    fullFilenameSite = "./src/parser/resources/temp/" + filename + "_temp.json"

    logging.info('********* STEP 1. Read the data from the site *********')
    reading()

    logging.info('********* STEP 2. Check new data *********')
    newData = get_new_data(fullFilenameSite, fullFilenameDB)

    logging.info('********* STEP 3. Upload the new data to json-DB *********')
    upload_new_data_to_DB(newData, fullFilenameDB)

    return 0
