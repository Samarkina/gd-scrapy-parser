import logging
import os

def touch(path):
    with open(path, 'a'):
        os.utime(path, None)

def if_not_exist(path):
    if not os.path.exists(path):
        touch(path)

def create_dir(path):
    basedir = os.path.dirname(path)
    if not os.path.exists(basedir):
        os.makedirs(basedir)

def create_database():
    logging.info('********* STEP 1. Create json-DB if it is not exist *********')
    filenames = []

    filenameArt = "articles"
    filenameAut = "authors"
    filenames.append("./src/parser/resources/" + filenameArt + ".json")
    filenames.append("./src/parser/resources/temp/" + filenameArt + "_temp.json")
    filenames.append("./src/parser/resources/" + filenameAut + ".json")
    filenames.append("./src/parser/resources/temp/" + filenameAut + "_temp.json")

    dirs = []
    dirs.append("./src/parser/resources/")
    dirs.append("./src/parser/resources/temp/")

    for dir in dirs:
        create_dir(dir)

    for filename in filenames:
        if_not_exist(filename)

