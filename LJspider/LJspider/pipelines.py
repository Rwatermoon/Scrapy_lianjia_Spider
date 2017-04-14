# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
from urllib.request import urlopen
from urllib.parse import quote
import re,time,json,pymongo,logging




class LjspiderPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DATABASE']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def fill_location_data(self,item):
        base_url_bdPlaceAPI="http://api.map.baidu.com/place/v2/search?region=北京&output=json&ak=c23eCGWNq4PzjmBx1uVVj6jP&q="
        # base_url_autonavi = "http://api.map.baidu.com/place/v2/search?output=json&city=北京市&ak=c23eCGWNq4PzjmBx1uVVj6jP&address="
        u = urlopen(quote(base_url_bdPlaceAPI + str(item['name'][0]).strip(), safe='!*();:@&=+$,/?%#[]'))

        # u = urlopen(quote(base_url_autonavi + str(cell_name[0]).strip() + "&city=北京市"))
        response = u.read().decode('utf-8')
        jsondata = json.loads(response)

        item['geo_location'] = jsondata["results"][0]["location"]
        return item


    def process_item(self, item, spider):
        if item['detials']:
            item['detials']=str(item['detials']).split(',')[-1]

        print(item['detials'])

        self.fill_location_data(item)

        for data in item:
            if not data:
                raise DropItem("Missing data!")
        self.collection.insert(dict(item))
        logging.log(logging.INFO,"Lianjia HousePrice Record added to MongoDB database!")
        # log.msg("Lianjia HousePrice Record added to MongoDB database!",
                # level=log.DEBUG,spider=spider)
        return item
