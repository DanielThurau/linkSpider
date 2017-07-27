from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


global_start_url = raw_input("Enter starting URL: ");
global_allowed_domain = raw_input("Enter allowed domains: ");

class someSpider(CrawlSpider):
  name = 'crawltest'
  global global_start_url; 
  global global_allowed_domain;
  
  start_urls = []
  start_urls.append(global_start_url);
  
  
  allowed_domains = []
  allowed_domains.append(global_allowed_domain);
  
  rules = (Rule(LinkExtractor(allow=()), callback='parse_obj', follow=True),)


  def parse_obj(self,response):
    yield {
       'url' : response.url
    }    
