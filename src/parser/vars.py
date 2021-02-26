import json

# Reading variables from json file
with open('../../config.json') as json_file:
    data = json.load(json_file)

    DEFAULT_PATH = data['default_path']
    DEFAULT_PATH_TEMP = DEFAULT_PATH + "temp/"
    DEFAULT_PATH_IMG = DEFAULT_PATH + "img/"

    FILENAME_ART = data['filename']['articles']
    FILENAME_AUTH = data['filename']['authors']
    FILENAME_REP = data['filename']['report']

    RESOURCE_PATH = DEFAULT_PATH + "{0}.json"
    RESOURCE_TEMP_PATH = DEFAULT_PATH_TEMP + "{0}.json"
    RESOURCE_TEMP_PATH_TEMP = DEFAULT_PATH + "temp/{0}_temp.json"

    FULL_FILENAME_DB_ART = RESOURCE_PATH.format(FILENAME_ART)
    FULL_FILENAME_TEMP_ART = RESOURCE_TEMP_PATH_TEMP.format(FILENAME_ART)

    FULL_FILENAME_DB_AUTH = RESOURCE_PATH.format(FILENAME_AUTH)
    FULL_FILENAME_TEMP_AUTH = RESOURCE_TEMP_PATH_TEMP.format(FILENAME_AUTH)

    FULL_FILENAME_DB_REP = RESOURCE_PATH.format(FILENAME_REP)
