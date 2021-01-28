import logging
import os
import shutil
import src.parser.vars as vars


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

    dir_path = vars.DEFAULT_PATH_TEMP
    try:
        shutil.rmtree(dir_path)
    except OSError as e:
        print("Error: {0}: {1}".format(dir_path, e.strerror))

    logging.info('All temp files was removed')


def create_database():
    """creating the database and temp files for crawling
    """

    logging.info('********* STEP 1. Create json-DB (articles, authors and report) if it is not exist *********')
    filenames = []

    filenames.append(vars.FULL_FILENAME_DB_ART)
    filenames.append(vars.FULL_FILENAME_TEMP_ART)

    filenames.append(vars.FULL_FILENAME_DB_AUTH)
    filenames.append(vars.FULL_FILENAME_TEMP_AUTH)

    filenames.append(vars.FULL_FILENAME_DB_REP)

    dirs = []
    dirs.append(vars.DEFAULT_PATH)
    dirs.append(vars.DEFAULT_PATH_TEMP)
    dirs.append(vars.DEFAULT_PATH_IMG)

    for dir in dirs:
        create_dir(dir)

    for filename in filenames:
        if_not_exist(filename)
