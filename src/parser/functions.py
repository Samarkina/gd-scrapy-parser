import json
import os
import logging
import src.parser.vars as vars


def do_urls(references):
    """doing urls for GD blog for crawling

    :param references: last part for urls
    """

    url = 'https://blog.griddynamics.com/'
    urls = []
    for ref in references:
        urls.append(url + ref)

    return urls


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


def upload_data(self, filename, data):
    """uploading data into temp file during crawling

    :param self:
    :param filename: filename for uploading
    :param data: data for uploading
    """

    full_filename = vars.RESOURCE_TEMP_PATH.format(filename)
    filesize = os.path.getsize(full_filename)
    self.log('{0} file size is {1}'.format(full_filename, filesize))

    if (filesize):
        old_data = json_reader(full_filename)
        if not isinstance(old_data, list):
            new_data = []
            new_data.append(old_data)
            old_data = new_data
    else:
        self.log('{} file is empty '.format(full_filename))
        old_data = []
    old_data.append(data)
    json_writer(full_filename, old_data)
