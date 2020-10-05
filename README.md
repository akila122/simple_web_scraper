# Simple Web Scraper
  A command line tool for scraping an University Staff Directory pages and printing out the staff contact information for the specified sport developed in Python.
## Input
Input format:
python scrape.py --url=page_url --sport=sport_name \
or:
python scrape.py --url=page_url --sport=sport_name --html-element=element_name --html-element-id=element_id \
or:
python scrape.py --url=page_url --sport=sport_name --html-element=element_name --html-element-index=element_index \
or:
python scrape.py --url=page_url --sport=sport_name --html-element=element_name --html-element-class=element_class \
Input parameters:\
(required) page_url - the Staff Directory page URL to be scraped (e.g. each one of the Test URLs below)\
(required) sport_name - the sport name to be filtered (case insensitive, e.g. "volleyball")\
(optional) element_name - the name of the HTML element to be searched for (e.g. "tr" or "table")\
(optional, mutually exclusive) element_id, element_index, or element_class - the id, index, or HTML style class of the specified HTML element to be searched for (e.g. id "Table1", or index 1, or HTML style class "redrow")

## Filters explained
### --element_name="table"
#### --element_index=N
Tool will only analyze N-th table in all tables that were found in the passed .html response if it exists
#### --element_class=C
Tool will only analyze tables that contain class C and were found in the .html response
#### --element_id=I
Tool will only analyze tables that have the same id attribute as I and were found in the passed .html response
### --element_name="tr"
#### --element_index=N
Tool will only analyze N-th row in every table that is filtered by the given sport
#### --element_class=C
Tool will only analyze rows that contain class C and were found in tables filterd by the given sport
#### --element_id=I
Tool will only analyze rows that have the same id attribute as I and were found in tables filterd by the given sport

## Examples
Note that all arguments passed that contain whitespace tokens or symbols such as ' or , should be encapsulated in "argument" format (e.g. "Basketball, Women's")
### py scrape.py http://www.goseattleu.com/StaffDirectory.dbml  volleyball --element_name=table --element_class=collapse-on-medium
[
    {
        "sport": "volleyball",
        "name": "Michelle Cole",
        "position": "Head Coach",
        "phone": "(206) 296-6426",
        "email": "mcole1@seattleu.edu"
    },
    {
        "sport": "volleyball",
        "name": "Michael Hobson",
        "position": "Assistant Coach",
        "phone": "",
        "email": "mhobson@seattleu.edu"
    },
    {
        "sport": "volleyball",
        "name": "Amber Cannady",
        "position": "Assistant Coach",
        "phone": "",
        "email": "acannady@seattleu.edu"
    }
]
### py scrape.py http://www.goseattleu.com/StaffDirectory.dbml  volleyball --element_name=tr --element_index=2
[
    {
        "sport": "volleyball",
        "name": "Amber Cannady",
        "position": "Assistant Coach",
        "phone": "",
        "email": "acannady@seattleu.edu"
    }
]
## Test URLs
Seattle University Staff Directory (http://www.goseattleu.com/StaffDirectory.dbml) \
Arkansas State Red Wolves Athletic Staff Directory (http://www.astateredwolves.com/ViewArticle.dbml?ATCLID=207138) \
Arizona Wildcats Athletics Staff Directory (https://athletics.arizona.edu/StaffDirectory/index.asp) \
Arizona Wildcats Athletics Staff Directory Bonus (https://arizonawildcats.com/sports/2007/8/1/207969432.aspx)
