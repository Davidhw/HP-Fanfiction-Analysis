from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from items import HpfanficItem

import unicodedata
import re
import time

max_depth = 24628
#max_depth =4
current_depth = 0

class spider1(BaseSpider):
      name = "fanficnet"
      allowed_domains = ["www.fanfiction.net"]
      start_urls = ["http://www.fanfiction.net/book/Harry-Potter/10/0/0/2/0/0/0/0/0/1/0/"]
      
      def parse(self, response):
            global current_depth
            global max_depth

            current_depth +=1
            hxs = HtmlXPathSelector(response)
            sites = hxs.select('/html/body/div[5]/div/div/form/div')
            if current_depth <= max_depth:

                  next_page_url = "http://www.fanfiction.net/book/Harry-Potter/10/0/0/2/0/0/0/0/0/"+str(current_depth)+"/0/"
                  time.sleep(1)
                  try:
                        yield Request(next_page_url,self.parse)
                  except:
                        yield None

            for site in sites:
                  
                  item = HpfanficItem()
                  title = site.select('a[1]/text()').extract()
                  url = site.select('a[1]/@href').extract()
                  author = site.select('a[2]/text()').extract()
                  desc = site.select('div/text()').extract()

                  if url:
                        item['url'] ="http://www.fanfiction.net"+unicodedata.normalize('NFKD', url[0]).bencode('ascii','ignore')
                  if title:
                        item['title']=unicodedata.normalize('NFKD', title[0]).encode('ascii','ignore')
                  if author:
                        item['author']=unicodedata.normalize('NFKD', author[0]).encode('ascii','ignore')
                  if desc:
                        item['desc']=unicodedata.normalize('NFKD', desc[0]).encode('ascii','ignore')
                  
                  other_info=site.select('div/div/text()').extract()
                  if other_info:
                        item['collected_info'] = str(other_info)
                        other_info = unicodedata.normalize('NFKD', other_info[0]).encode('ascii','ignore')

                        tmp = re.search(r'Rated: (\w\+*) - (\w+) - (\w+/*\w*)', other_info)
                        if tmp:
                              if tmp.group(1)[-1]=="+":
                                    item['rating'] = tmp.group(1)[-2:]
                              else:
                                    item['rating'] = tmp.group(1)[-1]

                              item['language']=tmp.group(2)

                              # check if group three is a genre or a chapter, only store if it's a genre
                              if tmp.group(3) =='Chapters':
                                    pass
                              else:
                                    item['genre']=tmp.group(3)
                        
                        tmp = re.search(r'Chapters: (\d+,*\d*) - Words: ([\d+,*]+)',other_info)
                        if tmp:
                              item['chapters']=tmp.group(1)
                              item['words']=tmp.group(2)

                        tmp = re.search(r'- Reviews: ([\d+,*]+) -',other_info)
                        if tmp:
                              item['reviews']=tmp.group(1)

                        tmp = re.search(r'- Favs: ([\d+,*]+) -',other_info)
                        if tmp:
                              item['favorites']=tmp.group(1)          

                        tmp = re.search(r'- Follows: ([\d+,*]+) -',other_info)
                        if tmp:
                              item['follows']=tmp.group(1)        

                        tmp = re.search(r' - Updated: (\d+-\d+-\d+) -',other_info)
                        if tmp:
                              item['updated']=tmp.group(1)                  

                        tmp = re.search(r'- Published: (\d+-\d+-\d+)',other_info)
                        if tmp:
                              item['published']=tmp.group(1) 

                        tmp = re.search(r'- Published: (\d+-\d+-\d+) - ((\w*\s*\.*\&*)+)',other_info)
                        if tmp:
                              if tmp =="Complete":
                                    pass
                              else:
                                    item['staringchars']=tmp.group(2)

                  
                        tmp = re.search(r'- Complete',other_info)
                        if tmp:
                              item['complete']=True              
                        else:
                              item['complete']=False
                        
                        if tmp:
                              tmp = re.search(r'[\d.].- Complete', other_info)
                              
                        

#('Rated: (\w\+*) - (\w+) - \w+/*\w*) - Chapters: (\d+,*\d*) - Words: ([\d+,*]+) - Reviews: ([\d+,*]+) - Favs: ([\d+,*]+) - Follows: ([\d+,*]+) - Updated: (\d+-\d+-\d+) - Published: (\d+-\d+-\d+) - (\w.+)', other_info)
                  if item:            
                        yield item
                  else:
                        pass

