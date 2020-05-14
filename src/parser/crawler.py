import logging
from scrapy.crawler import CrawlerProcess
import src.parser.functions as func
import datetime
import src.parser.parser.spiders.articles as articles
import src.parser.parser.spiders.authors as authors

def reading():
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
        return newData

def upload_new_data_to_DB(newData, fullFilenameDB):
    # upload new data to DB
    data = func.json_reader(fullFilenameDB)
    if not newData:
        logging.info('All data is updated already')
        return
    else:
        for row in newData:
            data.append(row)
        sortedData = sort_json_by_date(data)
        func.json_writer(fullFilenameDB, sortedData)

def do_crawler():
    filenameArt = "articles"
    fullFilenameDBArt = "./src/parser/resources/" + filenameArt + ".json"
    fullFilenameSiteArt = "./src/parser/resources/temp/" + filenameArt + "_temp.json"

    filenameAuth = "authors"
    fullFilenameDBAuth = "./src/parser/resources/" + filenameAuth + ".json"
    fullFilenameSiteAuth = "./src/parser/resources/temp/" + filenameAuth + "_temp.json"

    logging.info('********* STEP 3. Read the data from the site *********')
    reading()

    logging.info('********* STEP 4. Check new data *********')
    newDataArt = get_new_data(fullFilenameSiteArt, fullFilenameDBArt)
    logging.info('New articles was found')

    newDataAuth = get_new_data(fullFilenameSiteAuth, fullFilenameDBAuth)
    logging.info('New authors was found')

    logging.info('********* STEP 5. Upload the new data to json-DB *********')

    upload_new_data_to_DB(newDataArt, fullFilenameDBArt)
    sort_and_rewrite_json_file(fullFilenameDBArt)
    logging.info('New articles was uploaded in database')

    upload_new_data_to_DB(newDataAuth, fullFilenameDBAuth)
    logging.info('New authors was uploaded in database')

    return 0
