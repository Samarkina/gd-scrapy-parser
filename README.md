# GD_Scrapy_parser
Parse GridDynamics Blog with Scrapy and visualize it

### Run the project
`python3 report.py`


### Description of the project

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