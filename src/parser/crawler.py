import logging
from scrapy.crawler import CrawlerProcess
import src.parser.functions as func
import datetime
import src.parser.parser.spiders.articles as articles
import src.parser.parser.spiders.authors as authors
import src.parser.vars as vars


def reading():
    """Reads all the site pages and writes in the temp file in
    /src/parser/parser/resources/tmp/ folder
    """

    spiders = [articles.ArticlesSpider, authors.AuthorsSpider]
    crawler = CrawlerProcess()
    for spider in spiders:
        crawler.crawl(spider)
    crawler.start()
    logging.info('All the site data was writting in JSON files in resource directory')


def date_convert(date):
    """Converting date to another format
    ex. May 12 2020 to 2020/05/12

    :param date: Date in format like May 12 2020
    :return: another format date (2020/05/12)
    """

    newDate = datetime.datetime.strptime(date, '%b %d %Y').strftime('%Y/%m/%d')
    return newDate


def extract_date(json):
    """ extracting date from json

    :param json:
    :return: date
    """

    try:
        return date_convert(json['date'])
    except KeyError:
        return 0


def sort_json_by_date(articlesJson):
    """Sort json file by date
    needs sort just articles

    :param articlesJson: data from Json file
    :return: sorted data by date
    """

    logging.info("Json file is sorting")
    articlesJson.sort(key=extract_date, reverse=False)
    return articlesJson


def sort_and_rewrite_json_file(fullFilename):
    """Sorting data by date and rewrite the json file

    :param fullFilename: name of the file
    """

    articlesJson = func.json_reader(fullFilename)
    sortedData = sort_json_by_date(articlesJson)
    logging.info('%s file was sorted by date' % fullFilename)

    func.json_writer(fullFilename, sortedData)


def isExistArticle(article, fullFilenameDB):
    """Сhecking for an article in DB file

    :param article: article for checking
    :param fullFilenameDB: full path filename to DB file
    :return: bool (file existing)
    """

    data = func.json_reader(fullFilenameDB)
    return article in data


def get_new_data(full_filename_site, full_filename_db):
    """geting new data from site, which is not in the database

    :param full_filename_site: full path filename to Site file
    :param full_filename_db: path filename to DB file
    :return: new data from site
    """

    logging.info('Counting the delta from the site and the database')
    new_data = []
    data = func.json_reader(full_filename_site)
    for article in data:
        if not isExistArticle(article, full_filename_db):
            new_data.append(article)
    if not new_data:
        logging.info('Site has NO new articles')
        return None
    else:
        logging.info('Site has new articles')
        return new_data


def upload_new_data_to_DB(new_data, full_filename_db):
    """upload new data to DB

    :param newData: data for upload
    :param fullFilenameDB: path filename to DB file
    """

    data = func.json_reader(full_filename_db)
    if new_data:
        for row in new_data:
            data.append(row)
        sorted_data = sort_json_by_date(data)
        func.json_writer(full_filename_db, sorted_data)
    else:
        logging.info('All data is updated already')


def do_crawler():
    """main function for crawling
    """

    logging.info('********* STEP 3. Read the data from the site *********')
    reading()

    logging.info('********* STEP 4. Check new data *********')
    new_data_art = get_new_data(vars.FULL_FILENAME_TEMP_ART, vars.FULL_FILENAME_DB_ART)
    logging.info('New articles was found')

    new_data_auth = get_new_data(vars.FULL_FILENAME_TEMP_AUTH, vars.FULL_FILENAME_DB_AUTH)
    logging.info('New authors was found')

    logging.info('********* STEP 5. Upload the new data to json-DB *********')

    upload_new_data_to_DB(new_data_art, vars.FULL_FILENAME_DB_ART)
    sort_and_rewrite_json_file(vars.FULL_FILENAME_DB_ART)
    logging.info('New articles was uploaded in database')

    upload_new_data_to_DB(new_data_auth, vars.FULL_FILENAME_DB_AUTH)
    logging.info('New authors was uploaded in database')
