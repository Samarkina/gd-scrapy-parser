import src.parser.crawler as crawler
import logging
import os


if __name__ == "__main__":
    # subprocess.call(crawler.main())
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    logging.info('********* STEP 0. Start crawling... *********')

    crawler.main()

    logging.info('********* STEP 4. Do the report *********')
    # do report

    logging.info('********* STEP 5. Upload the report to the json-DB *********')
    # write to SQL