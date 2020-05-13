import logging
from scrapy.crawler import CrawlerProcess
import src.parser.functions as func
import datetime
from src.parser.parser.spiders.articles import ArticlesSpider
from src.parser.parser.spiders.authors import AuthorsSpider

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
    sort_json_by_date(fullFilename)

    articlesJson = func.json_reader(fullFilename)
    lastDate = extract_date(articlesJson[len(articlesJson) - 1])

    logging.info('Last date was found')
    logging.info('Last date is %s in json-DB', lastDate)
    return lastDate

def isExistArticle(article, fullFilenameDB):
    # checking exist article in DB or not
    data = func.json_reader(fullFilenameDB)

    if article in data:
        return True
    else:
        return False


def count_delta(fullFilenameSite, lastSiteDate, lastDBDate):
    logging.info('Counting the delta from the site and the database')
    newData = []
    filename = "articles"
    fullFilenameDB = "./src/parser/resources/" + filename + ".json"

    if (lastSiteDate >= lastDBDate):

        data = func.json_reader(fullFilenameSite)

        for article in data:
            if article['date'] >= lastDBDate and isExistArticle(article, fullFilenameDB):
                    newData.append(article)
    if not newData:
        logging.info('Site has NO new articles')
    else:
        logging.info('Site has new articles')
        return newData

def upload_new_data(newData):
    # upload new data to DB
    filename = "articles"
    fullFilenameDB = "./src/parser/resources/" + filename + ".json"

    data = func.json_reader(fullFilenameDB)

    # TODO : upload








def check_data():
    filename = "articles"
    fullFilenameDB = "./src/parser/resources/" + filename + ".json"

    logging.info('Check the data from json-DB')
    lastDBDate = get_last_db_date(fullFilenameDB)

    logging.info('Check the new data from site')
    fullFilenameSite = "./src/parser/resources/temp/" + filename + "_temp.json"
    lastSiteDate = get_last_db_date(fullFilenameSite)


    # TODO : count the delta

    # вычислить дельту в данных сайта и данных, которые есть в DB. Upload данные дельты в DB.
    # На всякий случай чекать, есть ли уже эта запись в DB.
    # И в этот момент проверить, точно ли нет такого автора. И если нет, то добавить и его

    newData = count_delta(fullFilenameSite, lastSiteDate, lastDBDate)

    upload_new_data(newData)

    logging.info('Upload the delta from the site to the database')

    logging.info('Check exist this author in database')

    logging.info('Upload the author in database')



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
    reading()



    logging.info('********* STEP 2. Check new data *********')
    check_data()


    logging.info('********* STEP 3. Upload the new data to json-DB *********')

    return 0
