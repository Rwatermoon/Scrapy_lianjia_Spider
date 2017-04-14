import scrapy
import time
import selenium
from pymongo import MongoClient


# class QuotesSpider(scrapy.Spider):
class LJSpider(scrapy.Spider):
    name = "LJspider"

    def start_requests(self):
        urls = [
            'http://bj.lianjia.com/ershoufang/'
        ]
        try:
            client = MongoClient('localhost', 27017)
            print(client)
        except:
            print("Error to connect to Database!")
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse,dont_filter=True)

    def parse(self, response):
        page = response.url.split("/")[-2]
        print(response)
        test=response.xpath('/html/body/div[4]/div[1]/ul/li')

        for houseList in response.xpath('//li[@class="clear"]'):
            yield {
            'title':houseList.xpath('div[1]/div[1]/a/text()').extract(),
            'url': houseList.xpath('a/@href').extract(),
            'name':houseList.xpath('div[1]/div[2]/div/a/text()').extract(),
            'detials':houseList.xpath('div[1]/div[2]/div/text()').extract(),
            'location': houseList.xpath('div[1]/div[3]/div/a/text()').extract(),
            'total_price':houseList.xpath('div[1]/div[6]/div[1]/span/text()').extract(),
            'single_price':houseList.xpath('div[1]/div[6]/div[2]/span/text()').extract(),
            'claw_time':time.localtime()
            }


        next_page_url = response.xpath('//div[@class="page-box fr"]/div/a/@href').extract()
        try:
            if next_page_url is not None and len(next_page_url)>0:
                yield scrapy.Request(response.urljoin(next_page_url[-1]))
        except:
            print(next_page_url)
            print(houseList)
            print(response)

        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)