#!/usr/bin/python
from os import system as sys

# copy over output just in case you realized you wanted it
sys('cp output.csv .output.csv.backup');
sys('rm output.csv')
# Run scrapy and output to output.csv
sys('scrapy runspider link_spider.py -o output.csv --set="ROBOTSTXT_OBEY=False"');
# Parse all urls and give number
sys('python parse.py');
