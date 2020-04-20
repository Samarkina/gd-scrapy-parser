import json
import os

def do_urls(references):

    url = 'https://blog.griddynamics.com/'
    urls = []
    for ref in references:
        urls.append(url + ref)

    return urls

def json_reader(fullFilename):
    with open(fullFilename) as outfile:
        return json.load(outfile)

def json_writer(self, fullFilename, data):
    with open(fullFilename, "w") as outfile:
        json.dump(data, outfile)
    self.log('File %s was updated' % fullFilename)

def upload_data(self, filename, data):
    fullFilename = "./resources/" + filename + ".json"
    filesize = os.path.getsize(fullFilename)
    self.log('%s file size is %d' % (fullFilename, filesize))

    if (filesize):
        oldData = json_reader(fullFilename)
        if not isinstance(oldData, list):
            newData = []
            newData.append(oldData)
            oldData = newData
    else:
        self.log('%s file is empty ' % fullFilename)
        oldData = []
    oldData.append(data)
    json_writer(self, fullFilename, oldData)
