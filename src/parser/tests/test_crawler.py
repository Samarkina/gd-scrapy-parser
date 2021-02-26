import datetime
import unittest
import json
import crawler as crawler


class CrawlerTest(unittest.TestCase):

    def setUp(self):
        db_file_template = "./tests/resources/template/articles_template.json"
        db_file = "./tests/resources/articles_2.json"
        with open(db_file_template) as template_file:
            data_template = json.load(template_file)
            with open(db_file, "w") as articles_file:
                json.dump(data_template, articles_file)

    def test_date_convert(self):
        result = crawler.date_convert("May 12 2020")
        self.assertEqual(result, datetime.datetime(2020, 5, 12, 0, 0))
        print("%s is May 12 2020" % result)

    def test_sort_json_by_date(self):
        sorted_file = "./tests/resources/articles_2.json"
        not_sorted_file = "./tests/resources/articlesNotSorted.json"
        with open(not_sorted_file) as outfile:
            not_sorted_file = json.load(outfile)
            result = crawler.sort_json_by_date(not_sorted_file)
            with open(sorted_file) as outfile2:
                sorted_data = json.load(outfile2)
                self.assertEqual(result, sorted_data)
                print("Sort json file works" % result)

    def test_get_new_data(self):
        full_filename_site = "./tests/resources/articlesSiteFile.json"  # with new article
        full_filename_db = "./tests/resources/articles.json"
        delta_between_articles_and_articlessitefile = "./tests/resources/delta.json"
        last_date = datetime.datetime(2019, 8, 21, 0, 0)
        result = crawler.get_new_data(full_filename_site, full_filename_db, last_date, "articles")
        with open(delta_between_articles_and_articlessitefile) as outfile:
            delta = json.load(outfile)
            self.assertEqual(result, delta)
            print("New article found")

    def test_count_delta_2_record(self):
        full_filename_site = "./tests/resources/articlesSiteFile2NewRecord.json"  # with 2 new article
        full_filename_db = "./tests/resources/articles.json"
        delta_between_articles_and_articlessitefile = "./tests/resources/delta2NewRecord.json"
        last_date = datetime.datetime(2019, 8, 21, 0, 0)
        result = crawler.get_new_data(full_filename_site, full_filename_db, last_date, "articles")
        with open(delta_between_articles_and_articlessitefile) as outfile:
            delta = json.load(outfile)
            self.assertEqual(result, delta)
            print("New articles found")

    def test_count_delta_no_one_record(self):
        full_filename_db = "./tests/resources/articles.json"
        last_date = datetime.datetime(2020, 1, 22, 0, 0)
        result = crawler.get_new_data(full_filename_db, full_filename_db, last_date, "articles")
        self.assertEqual(result, None)
        print("New articles doesn't found")

    def test_upload_new_data_to_db(self):
        new_data_file = "./tests/resources/delta2NewRecord_2.json"
        full_filename_db = "./tests/resources/articles_2.json"

        new_db = "./tests/resources/articlesWithDelta2Records.json"
        with open(new_data_file) as outfile:
            new_data = json.load(outfile)
            crawler.upload_new_data_to_db(new_data, full_filename_db)
            # function is rewriting fullFilenameDB file

            with open(new_db) as newDBfile:
                data_new_db = json.load(newDBfile)

                with open(full_filename_db) as fullFilenameDBFile:
                    data_db = json.load(fullFilenameDBFile)
                    self.assertEqual(data_db, data_new_db)
                    print("New data was uploaded successfully")

    def test_find_last_date(self):
        full_filename_db = "./tests/resources/articles.json"
        actual = crawler.find_last_date(full_filename_db)
        expected = datetime.datetime(2019, 8, 21, 0, 0)
        self.assertEqual(actual, expected)
