import crawler as crawler
import logging
import database
import pandas as pd
import functions as func
import matplotlib.pyplot as plt
import json
import vars as vars


def authors_report(filename_db_auth):
    """creating authors report
    1) Top-5 Authors (based on articles counter)

    :param filename_db_auth: filename for authors database
    :return: sorted authors dataframe
    """

    authors_data = func.json_reader(filename_db_auth)
    authors_df = pd.DataFrame(data=authors_data)
    authors_df_sorted = authors_df.sort_values(by=['counterArticles'], ascending=False)[0:5]
    return authors_df_sorted


def articles_report(filename_db_art):
    """creating articles report
    2) Top-5 New Articles (based on publish data)

    :param filename_db_art: filename for articles database
    :return: sorted articles dataframe
    """

    articles_data = func.json_reader(filename_db_art)
    article_df_sorted = pd.DataFrame(data=articles_data)[-5:]
    return article_df_sorted


def tags_report(filename_db_art):
    """creating tags report
    3) Plot with counts of 7 popular tags:
       - it must be a bar chart (column plot) where each column is for one tag
       - Tag bar must have name in plot.
       - X-axis - counter with articles of tag theme

    :param filename_db_art: filename for articles database
    :return: path to image with report
    """

    articles_data = func.json_reader(filename_db_art)
    article_df = pd.DataFrame(data=articles_data)

    column_names = ["tags"]
    tags = pd.DataFrame(columns=column_names)

    for k, v in article_df['tags'].items():
        for tag in v:
            tags = tags.append({'tags': tag}, ignore_index=True)
    tags_with_count = tags.groupby('tags', as_index=False)['tags'].size().rename(columns={"size": "count"}).reset_index()
    sorted_tags = tags_with_count.sort_values(by=['count'])[-7:]

    sorted_tags['tags'] = sorted_tags['tags'].str.wrap(12)
    sorted_tags.plot.barh(x='tags', y='count', title='7 popular tags')

    plt.tight_layout()
    path = vars.DEFAULT_PATH_IMG + 'tags.png'
    plt.savefig(path)

    return path


def create_report(filename_db_art, filename_db_auth):
    """creating all reports
       1) Top-5 Authors (based on articles counter)
       2) Top-5 New Articles (based on publish data)
       3) Plot with counts of 7 popular tags:
       - it must be a bar chart (column plot) where each column is for one tag
       - Tag bar must have name in plot.
       - X-axis - counter with articles of tag theme

    :param filename_db_art: filename for articles database
    :param filename_db_auth: filename for authors database
    :return: all reports
    """

    authors_report_data = authors_report(filename_db_auth)
    articles_report_data = articles_report(filename_db_art)
    tags_report_data = tags_report(filename_db_art)

    authors_report_data = json.loads(authors_report_data.to_json(orient='records'))
    articles_report_data = json.loads(articles_report_data.to_json(orient='records'))

    report = {"authors": authors_report_data, "articles": articles_report_data, "tags": tags_report_data}

    return report


def report_print(report: dict):
    """Printing report to standard output

    :param report: dict with format like {
                                    "authors": authors_report_data,
                                    "articles": articles_report_data,
                                    "tags": tags_report_data
                                    }
    :return:
    """
    for row in report:
        print("************************************ {} ************************************".format(row))
        if row == "tags":
            print("Path to image: {}".format(report[row]))
        else:
            df = pd.DataFrame.from_dict(report[row])
            pd.set_option('display.max_columns', None)
            print(df)


if __name__ == "__main__":
    logging.disable(logging.DEBUG)

    logging.info('********* STEP 0. Program is starting... *********')
    database.create_database()

    logging.info('********* STEP 2. Start crawling... *********')
    crawler.do_crawler()

    logging.info('********* STEP 7. Do the report *********')
    report = create_report(vars.FULL_FILENAME_DB_ART, vars.FULL_FILENAME_DB_AUTH)

    logging.info('********* STEP 8. Upload the report to the json-DB *********')
    func.json_writer(vars.FULL_FILENAME_DB_REP, report)

    logging.info('********* STEP 9. Print report to standard output *********')
    report_print(report)

    database.remover_temps()
