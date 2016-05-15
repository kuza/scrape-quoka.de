# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

from database.connection import db
from database.models import Quoka


class ScrapeQuokaPipeline(object):
    def process_item(self, item, spider):
        if item['OBID']:
            instance = db.query(Quoka).filter_by(
                OBID=item['OBID'], erzeugt_am=item['erzeugt_am']).first()
            if instance:
                if not instance.Telefon and item['Telefon']:
                    instance.Telefon = item['Telefon']
                    db.commit()
                    return item
                raise DropItem("Duplicate item found: %s" % item)
        instance = Quoka(**item)
        db.add(instance)
        db.commit()

        return item
