Run create_spider.sh to make the spider.
Max the variable max_depth in spider1.py equal to however many pages you want to scrape.
Then, to run the spider, enter the directory create_spider.sh created and enter scrapy crawl fanficnet -o items.csv -t csv in your terminal.
Place the output csv file in the same directory as the analyzecsv.py, and run analyzecsv.py

Dependencies:
Scrapy, matplotlib, scipy, dateutil, and numpy

I think the rest of the things I imported are native libraries. Here is a list of everything else I import:
unicodedata, re, time, csv, re, operator, math

You can discuss this program here http://www.reddit.com/r/HPMOR/comments/1h10vl/harry_potter_fanfiction_data_most_popular/ or contact me at David.Weinstein@ncf.edu


