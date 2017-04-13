# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
from MySQLdb.cursors import DictCursor
from twisted.enterprise import adbapi
from twisted.internet import reactor

class DistributedCrawlerPipeline(object):
    def __init__(self, dbpools):
        self.dbpools = dbpools

    @classmethod
    def from_settings(cls, settings):
        dbpools = {}
        host = settings['MYSQL_HOST']
        dbs = settings['MYSQL_DBS']
        user = settings['MYSQL_USER']
        passwd = settings['MYSQL_PASSWD']
        for db in dbs.split(','):
            dbpools[db] = adbapi.ConnectionPool('MySQLdb',
                    host = host, user = user,
                    passwd = passwd, db = db, cursorclass = DictCursor,
                    charset = 'utf8')
        return cls(dbpools)

    def _insert(self, conn, item):
        print "item: " + str(item)
        conn.execute('insert ignore into product values("%s")' % item['product'])
        conn.execute('insert ignore into store values("%s")' % item['store'])
        conn.execute('insert ignore into rank(`rank`, `store`, `product`) values(%f, "%s", "%s")' % (item['rank'], item['store'], item['product']))

    def process_item(self, item, spider):
        #print 'hahaha'
        try:
            reactor.run()
        except Exception, e:
            print "reactor already run"
        db = item['resource']
        print db
        self.dbpools[db].runInteraction(self._insert, item)
        return item

