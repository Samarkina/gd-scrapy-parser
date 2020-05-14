# GD_Scrapy_parser
Parse GridDynamics Blog with Scrapy and visualize it

### Run the project
`python3 src/parser/report.py`


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


#### In report:

1) Top-5 Authors (based on articles counter)
2) Top-5 New Articles (based on publish data)
3) Plot with counts of 7 popular tags:
    - it must be a bar chart (column plot) where each column is for one tag
    - Tag bar must have name in plot.
    - X-axis - counter with articles of tag theme