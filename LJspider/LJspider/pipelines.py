# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log





class LjspiderPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DATABASE']]
        self.collection = db[settings['MONGODB_COLLECTION']]



    def process_item(self, item, spider):
        if item['detials']:
            for detial_record in item['detials']:
                print(detial_record)
                print("new line")
        print(item['detials'])
                # if len(str(detial_record).split(','))>0:
                    # detial_record=str(detial_record)
                    # print(str(detial_record))
                    # print(len(str(detial_record).split(',')))

            # item['detials']=[str(detial_record).split(',')[-1]
            #                  for detial_record in item['detials']
            #                  if len(str(detial_record).split(','))>0]
        for data in item:
            if not data:
                raise DropItem("Missing data!")
        # self.collection.insert(dict(item))
        log.msg("Lianjia HousePrice Record added to MongoDB database!",
                level=log.DEBUG,spider=spider)
        return item
