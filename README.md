# GD Scrapy parser

This project is a parser for GridDynamics blog and it creates a report which contains following bullets:
- Top-5 Authors,
- Top-5 New Articles,
- Plot with articles counter of 7 most popular tags

Crawler is based on Scrapy, with items to load data to storage.
Storage is implemented as JSON file and stored in `<project-dir>/src/parser/resources`.
Main script with report generator is `<project-dir>/src/parser/report.py`.

### Storage contains:

#### Articles (blog post):

example, of articles page: https://blog.griddynamics.com/create-image-similarity-function-with-tensorflow-for-retail/

Extract to storage:

1) Title
2) url to full version
3) First 160 symbols of text
4) publication date
5) Author (full name)
6) Tags


#### Authors:

example of author page: https://blog.griddynamics.com/author/anton-ovchinnikov/

All authors page: https://blog.griddynamics.com/all-authors/

Extract to storage:

1) Full name
2) Job Title
3) Linked-in url to user profile
4) Counter with articles


#### In report:

1) Top-5 Authors (based on articles counter)
2) Top-5 New Articles (based on publish data)
3) Plot with counts of 7 popular tags:
    - it must be a bar chart (column plot) where each column is for one tag
    - Tag bar must have name in plot.
    - X-axis - counter with articles of tag theme

## Tests:
You can run the tests with following command:
`cd src/parser`
`python3 -m unittest tests/test_crawler.py`

![tests](https://github.com/Samarkina/gd-scrapy-parser/blob/master/tests.png?raw=true)


## Installation
Project requires [pip3](https://pypi.org/project/pip/) and [python3](https://www.python.org/downloads/) installation.
Python 3.9.1 version is preferable.
1. `git clone git@github.com:gridu/PYTHON-esamarkina.git`
2. `pip3 install -r requirements.txt`

Also, you can use [virtual env](https://docs.python.org/3/tutorial/venv.html)
instead of Python installed on your computer.
Steps for using virtual-env:
1. Create the virtual-env `python3 -m venv <your-virtual-env-name>`
2. Activate the virtual-env `source <your-virtual-env-name>/bin/activate`
3. After that you can install all the libraries necessary for the work.

## Run the project
`cd src/parser/`
`python3 report.py`
