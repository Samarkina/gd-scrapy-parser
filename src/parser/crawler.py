import logging
from scrapy.crawler import CrawlerProcess
import functions as func
import parser.spiders.articles as articles
import parser.spiders.authors as authors
import vars as vars
from datetime import datetime


def find_last_date(database):
    """Find last date from database

    :return: last date from database
    """
    try:
        data = func.json_reader(database)
        logging.info('The last date from database was found')
        return extract_date(data[-1])
    except:
        return datetime.strptime("0001/01/01", '%Y/%m/%d')


def crawling():
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
    """Converting string date to datetime

    :param date: Date in string
    :return: Date in datetime
    """

    new_date: datetime = datetime.strptime(date, '%b %d %Y')
    return new_date


def extract_date(json):
    """ extracting date from json

    :param json:
    :return: date
    """

    try:
        return date_convert(json['date'])
    except KeyError:
        return datetime.strptime("0001/01/01", '%Y/%m/%d')


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


def get_new_data(full_filename_site, full_filename_db, last_date, load_type):
    """getting new data from site, which is not in the database
        and older than the most recent blog-post date
    :param full_filename_site: full path filename to Site file
    :param full_filename_db: path filename to DB file
    :param last_date: last date from database
    :param load_type: type of loading, can be "articles" or "authors"
    :return: new data from site
    """

    logging.info('Counting the delta from the site and the database')
    new_data = []
    data_site = func.json_reader(full_filename_site)
    data_db = func.json_reader(full_filename_db)

    for article in data_site:
        if article not in data_db \
                and ((extract_date(article) >= last_date and load_type == "articles")
                     or load_type == "authors"):
            new_data.append(article)
    if not new_data:
        logging.info('Site has NO new articles')
        return None
    else:
        logging.info('Site has new articles')
        return new_data


def upload_new_data_to_db(new_data, full_filename_db):
    """upload new data to DB

    :param new_data: data for upload
    :param full_filename_db: full database filename
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
    logging.info('********* STEP 3. Find last date from the database *********')
    last_date = find_last_date(vars.FULL_FILENAME_DB_ART)

    logging.info('********* STEP 4. Read the data from the site *********')
    crawling()

    logging.info('********* STEP 5. Check new data *********')
    new_data_art = get_new_data(vars.FULL_FILENAME_TEMP_ART, vars.FULL_FILENAME_DB_ART, last_date, "articles")
    logging.info('Articles was checked')

    new_data_auth = get_new_data(vars.FULL_FILENAME_TEMP_AUTH, vars.FULL_FILENAME_DB_AUTH, last_date, "authors")
    logging.info('Authors was checked')

    logging.info('********* STEP 6. Upload the new data to json-DB *********')

    upload_new_data_to_db(new_data_art, vars.FULL_FILENAME_DB_ART)
    logging.info('New articles was uploaded in database')

    upload_new_data_to_db(new_data_auth, vars.FULL_FILENAME_DB_AUTH)
    logging.info('New authors was uploaded in database')
