import logging
import scrapy
import subprocess
import os

def reading():
    # read the data from blog
    os.system("./scrapy-spider.sh")


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


def get_last_date():
    # get_last_date in inner data

    # return the last date in your data (SQL)
    return "123"



def main():
    # last_date = get_last_date() # return the last date of publish
    #
    #
    # posts = crawler(last_date)

    reading()
    return 0
