import json
import os
import logging
import vars as vars


def do_urls(references):
    """doing urls for GD blog for crawling

    :param references: last part for urls
    """

    url = 'https://blog.griddynamics.com/'
    urls = []
    for ref in references:
        urls.append(url + ref)

    return urls


def get_new_urls(site_urls):
    """getting only new urls that have never been in the database

    :param site_urls: urls from site
    :return: new urls from site (they are not in database)
    """
    db_urls = []
    data_db_articles = json_reader(vars.FULL_FILENAME_DB_ART)
    for article in data_db_articles:
        db_urls.append(article["url"])

    new_urls = []
    for site_url in site_urls:
        if site_url not in db_urls:
            new_urls.append(site_url)

    return new_urls


def json_reader(full_filename):
    """reading json file

    :param full_filename: full path filename for reading
    :return: data from the file
    """

    if os.stat(full_filename).st_size == 0:
        return []
    else:
        with open(full_filename) as outfile:
            return json.load(outfile)


def json_writer(full_filename, data):
    """writing to json file

    :param full_filename: full path filename for writing
    :param data: data for writing
    """

    with open(full_filename, "w") as outfile:
        json.dump(data, outfile)
    logging.info('File {} was updated'.format(full_filename))
