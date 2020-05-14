import unittest
import json
import src.parser.crawler as crawler

class CrawlerTest(unittest.TestCase):

    def setUp(self):
        dbFileTemplate = "./resources/template/articles_template.json"
        dbFile = "./resources/articles.json"
        with open(dbFileTemplate) as templateFile:
            dataTemplate = json.load(templateFile)
            with open(dbFile, "w") as articlesFile:
                json.dump(dataTemplate, articlesFile)

    def test_date_convert(self):
        result = crawler.date_convert("May 12 2020")
        self.assertEqual(result, "2020/05/12")
        print("%s is May 12 2020" % result)

    def test_sort_json_by_date(self):
        sortedFile = "./resources/articles.json"
        notSortedFile = "./resources/articlesNotSorted.json"
        with open(notSortedFile) as outfile:
            notSortedData = json.load(outfile)
            result = crawler.sort_json_by_date(notSortedData)
            with open(sortedFile) as outfile2:
                sortedData = json.load(outfile2)
                self.assertEqual(result, sortedData)
                print("Sort json file works" % result)

    def test_not_isExistArticle(self):
        articleFile = "./resources/newArticle.json"
        dbFile = "./resources/articles.json"
        with open(articleFile) as outfile:
            article = json.load(outfile)
            result = crawler.isExistArticle(article, dbFile)
            self.assertEqual(result, False)
            print("%s article doesn't exist in %s file" % (articleFile, dbFile))

    def test_isExistArticle(self):
        articleFile = "./resources/oldArticle.json"
        dbFile = "./resources/articles.json"
        with open(articleFile) as outfile:
            article = json.load(outfile)
            result = crawler.isExistArticle(article, dbFile)
            self.assertEqual(result, True)
            print("%s article exist in %s file" % (articleFile, dbFile))

    def test_get_new_data(self):
        fullFilenameSite = "./resources/articlesSiteFile.json" # with new article
        fullFilenameDB = "./resources/articles.json"
        deltaBetweenArticlesAndArticlesSiteFile = "./resources/delta.json"
        result = crawler.get_new_data(fullFilenameSite, fullFilenameDB)
        with open(deltaBetweenArticlesAndArticlesSiteFile) as outfile:
            delta = json.load(outfile)
            self.assertEqual(result, delta)
            print("New article found")

    def test_count_delta_2_record(self):
        fullFilenameSite = "./resources/articlesSiteFile2NewRecord.json" # with 2 new article
        fullFilenameDB = "./resources/articles.json"
        deltaBetweenArticlesAndArticlesSiteFile = "./resources/delta2NewRecord.json"
        result = crawler.get_new_data(fullFilenameSite, fullFilenameDB)
        with open(deltaBetweenArticlesAndArticlesSiteFile) as outfile:
            delta = json.load(outfile)
            self.assertEqual(result, delta)
            print("New articles found")

    def test_count_delta_no_one_record(self):
        fullFilenameDB = "./resources/articles.json"
        result = crawler.get_new_data(fullFilenameDB, fullFilenameDB)
        self.assertEqual(result, None)
        print("New articles doesn't found")


    def test_upload_new_data_to_DB(self):
        newDataFile = "./resources/delta2NewRecord.json"
        fullFilenameDB = "./resources/articles.json"

        newDB = "./resources/articlesWithDelta2Records.json"
        with open(newDataFile) as outfile:
            newData = json.load(outfile)
            crawler.upload_new_data_to_DB(newData, fullFilenameDB)
            # function is rewriting fullFilenameDB file

            with open(newDB) as newDBfile:
                dataNewDB = json.load(newDBfile)

                with open(fullFilenameDB) as fullFilenameDBFile:
                    dataDB = json.load(fullFilenameDBFile)
                    self.assertEqual(dataDB, dataNewDB)
                    print("New data was uploaded successfully")







