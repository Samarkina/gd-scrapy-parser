import unittest
import json
import src.parser.crawler as crawler


class CrawlerTest(unittest.TestCase):

    def setUp(self):
        db_file_template = "./resources/template/articles_template.json"
        db_file = "./resources/articles.json"
        with open(db_file_template) as template_file:
            data_template = json.load(template_file)
            with open(db_file, "w") as articles_file:
                json.dump(data_template, articles_file)

    def test_date_convert(self):
        result = crawler.date_convert("May 12 2020")
        self.assertEqual(result, "2020/05/12")
        print("%s is May 12 2020" % result)

    def test_sort_json_by_date(self):
        sorted_file = "./resources/articles.json"
        not_sorted_file = "./resources/articlesNotSorted.json"
        with open(not_sorted_file) as outfile:
            not_sorted_file = json.load(outfile)
            result = crawler.sort_json_by_date(not_sorted_file)
            with open(sorted_file) as outfile2:
                sorted_data = json.load(outfile2)
                self.assertEqual(result, sorted_data)
                print("Sort json file works" % result)

    def test_not_isExistArticle(self):
        article_file = "./resources/newArticle.json"
        db_file = "./resources/articles.json"
        with open(article_file) as outfile:
            article = json.load(outfile)
            result = crawler.isExistArticle(article, db_file)
            self.assertEqual(result, False)
            print("%s article doesn't exist in %s file" % (article_file, db_file))

    def test_isExistArticle(self):
        article_file = "./resources/oldArticle.json"
        db_file = "./resources/articles.json"
        with open(article_file) as outfile:
            article = json.load(outfile)
            result = crawler.isExistArticle(article, db_file)
            self.assertEqual(result, True)
            print("%s article exist in %s file" % (article_file, db_file))

    def test_get_new_data(self):
        full_filename_site = "./resources/articlesSiteFile.json" # with new article
        full_filename_db = "./resources/articles.json"
        delta_between_articles_and_articlessitefile = "./resources/delta.json"
        result = crawler.get_new_data(full_filename_site, full_filename_db)
        with open(delta_between_articles_and_articlessitefile) as outfile:
            delta = json.load(outfile)
            self.assertEqual(result, delta)
            print("New article found")

    def test_count_delta_2_record(self):
        full_filename_site = "./resources/articlesSiteFile2NewRecord.json" # with 2 new article
        full_filename_db = "./resources/articles.json"
        delta_between_articles_and_articlessitefile = "./resources/delta2NewRecord.json"
        result = crawler.get_new_data(full_filename_site, full_filename_db)
        with open(delta_between_articles_and_articlessitefile) as outfile:
            delta = json.load(outfile)
            self.assertEqual(result, delta)
            print("New articles found")

    def test_count_delta_no_one_record(self):
        full_filename_db = "./resources/articles.json"
        result = crawler.get_new_data(full_filename_db, full_filename_db)
        self.assertEqual(result, None)
        print("New articles doesn't found")

    def test_upload_new_data_to_DB(self):
        new_data_file = "./resources/delta2NewRecord.json"
        full_filename_db = "./resources/articles.json"

        new_db = "./resources/articlesWithDelta2Records.json"
        with open(new_data_file) as outfile:
            new_data = json.load(outfile)
            crawler.upload_new_data_to_DB(new_data, full_filename_db)
            # function is rewriting fullFilenameDB file

            with open(new_db) as newDBfile:
                data_new_db = json.load(newDBfile)

                with open(full_filename_db) as fullFilenameDBFile:
                    data_db = json.load(fullFilenameDBFile)
                    self.assertEqual(data_db, data_new_db)
                    print("New data was uploaded successfully")
