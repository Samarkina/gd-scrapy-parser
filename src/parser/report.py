import src.parser.crawler as crawler
import logging
import os
import database

if __name__ == "__main__":
    # subprocess.call(crawler.main())
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    logging.info('********* STEP 0. Program is starting... *********')

    database.create_database()

    logging.info('********* STEP 2. Start crawling... *********')

    crawler.main()

    logging.info('********* STEP 6. Do the report *********')
    # TODO : do report

    logging.info('********* STEP 7. Upload the report to the json-DB *********')
    # TODO