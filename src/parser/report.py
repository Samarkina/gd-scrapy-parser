import src.parser.crawler as crawler
import logging
import os
import database
import pandas as pd
import numpy as np
import functions as func
import matplotlib.pyplot as plt
import json

def authors_report(filenameDBAuth):
    # 1) Top-5 Authors (based on articles counter)
    authorsData = func.json_reader(filenameDBAuth)
    authorsDF = pd.DataFrame(data=authorsData)
    authorsDFSorted = authorsDF.sort_values(by=['counterArticles'], ascending=False)[0:5]
    return authorsDFSorted

def articles_report(filenameDBArt):
    # 2) Top-5 New Articles (based on publish data)
    articlesData = func.json_reader(filenameDBArt)
    articleDFSorted = pd.DataFrame(data=articlesData)[-5:]
    return articleDFSorted

def tags_report(filenameDBArt):
    # 3) Plot with counts of 7 popular tags:
    #  - it must be a bar chart (column plot) where each column is for one tag
    #  - Tag bar must have name in plot.
    #  - X-axis - counter with articles of tag theme
    articlesData = func.json_reader(filenameDBArt)
    articleDF = pd.DataFrame(data=articlesData)

    columnNames = ["tags"]
    tags = pd.DataFrame(columns=columnNames)

    for k, v in articleDF['tags'].items():
        for tag in v:
            tags = tags.append({'tags': tag}, ignore_index=True)
    tagsWithCount = tags.groupby('tags', as_index=False)['tags'].size().to_frame('count').reset_index()
    sortedTags = tagsWithCount.sort_values(by=['count'])[-7:]

    sortedTags['tags'] = sortedTags['tags'].str.wrap(12)
    sortedTags.plot.barh(x='tags', y='count', title='7 popular tags')

    plt.tight_layout()
    path = './src/parser/resources/img/tags.png'
    plt.savefig(path)

    return path

def create_report(filenameDBArt, filenameDBAuth):
    #  1) Top-5 Authors (based on articles counter)
    #  2) Top-5 New Articles (based on publish data)
    #  3) Plot with counts of 7 popular tags:
    #  - it must be a bar chart (column plot) where each column is for one tag
    #  - Tag bar must have name in plot.
    #  - X-axis - counter with articles of tag theme
    authorsReport = authors_report(filenameDBAuth)
    articlesReport = articles_report(filenameDBArt)
    tagsReport = tags_report(filenameDBArt)

    authorsReport = json.loads(authorsReport.to_json(orient='records'))
    articlesReport = json.loads(articlesReport.to_json(orient='records'))

    report = {"authors": authorsReport, "articles": articlesReport, "tags": tagsReport}

    return report

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    logging.info('********* STEP 0. Program is starting... *********')
    database.create_database()

    logging.info('********* STEP 2. Start crawling... *********')
    crawler.do_crawler()

    logging.info('********* STEP 6. Do the report *********')
    filenameDBArt = "./src/parser/resources/articles.json"
    filenameDBAuth = "./src/parser/resources/authors.json"
    report = create_report(filenameDBArt, filenameDBAuth)

    logging.info('********* STEP 7. Upload the report to the json-DB *********')
    func.json_writer("./src/parser/resources/report.json", report)

    database.remover_temps()
