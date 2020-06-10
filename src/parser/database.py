import logging
import os
import shutil

def touch(path):
    """creating the file

    :param path: path to file
    """
    with open(path, 'a'):
        os.utime(path, None)

def if_not_exist(path):
    """checking for file, else creating the file

    :param path: path to file
    """

    if not os.path.exists(path):
        touch(path)

def create_dir(path):
    """checking for directory, esle creating the directory

    :param path: path to directory
    """

    basedir = os.path.dirname(path)
    if not os.path.exists(basedir):
        os.makedirs(basedir)

def remover_temps():
    """removing temp files
    """

    dir_path = "./src/parser/resources/temp/"
    try:
        shutil.rmtree(dir_path)
    except OSError as e:
        print("Error: %s : %s" % (dir_path, e.strerror))

    logging.info('All temp files was removed')

def create_database():
    """creating the database and temp files for crawling
    """

    logging.info('********* STEP 1. Create json-DB (articles, authors and report) if it is not exist *********')
    filenames = []

    filenameArt = "articles"
    filenameAut = "authors"
    filenameRep = "report"

    filenames.append("./src/parser/resources/" + filenameArt + ".json")
    filenames.append("./src/parser/resources/temp/" + filenameArt + "_temp.json")

    filenames.append("./src/parser/resources/" + filenameAut + ".json")
    filenames.append("./src/parser/resources/temp/" + filenameAut + "_temp.json")

    filenames.append("./src/parser/resources/" + filenameRep + ".json")

    dirs = []
    dirs.append("./src/parser/resources/")
    dirs.append("./src/parser/resources/temp/")
    dirs.append("./src/parser/resources/img/")

    for dir in dirs:
        create_dir(dir)

    for filename in filenames:
        if_not_exist(filename)
