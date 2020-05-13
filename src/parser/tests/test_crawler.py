import unittest
import json
from src.parser.crawler import isExistArticle

class CrawlerTest(unittest.TestCase):

    def test_not_isExistArticle(self):
        articleFile = "./resources/newArticle.json"
        dbFile = "./resources/articles.json"
        with open(articleFile) as outfile:
            article = json.load(outfile)
            result = isExistArticle(article, dbFile)
            self.assertEqual(result, False)
            print("%s article doesn't exist in %s file" % (articleFile, dbFile))

    def test_isExistArticle(self):
        articleFile = "./resources/oldArticle.json"
        dbFile = "./resources/articles.json"
        with open(articleFile) as outfile:
            article = json.load(outfile)
            result = isExistArticle(article, dbFile)
            self.assertEqual(result, True)
            print("%s article exist in %s file" % (articleFile, dbFile))
