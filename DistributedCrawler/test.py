from twisted.internet import reactor
import MySQLdb
from MySQLdb.cursors import DictCursor
from twisted.enterprise import adbapi

host = 'localhost'
db = 'taobao'
user = 'scrapy'
passwd = '123456'
dbpool = adbapi.ConnectionPool('MySQLdb', host = host, user = user, passwd = passwd, db = db, charset = 'utf8')

def _insert__(conn, ite):
    sql = 'insert into product values("%s")' % ite['product']
    conn.execute('insert into product values("%s")' % item['product'])
    conn.execute('insert into store values("%s")' % item['store'])
    conn.execute('insert into rank(`rank`, `store`, `product`) values(%f, "%s", "%s")' % (item['rank'], item['store'], item['product']))
    print "??"



item = {'product' : 'product', 'store' : 'store', 'rank' : 0.5}
dbpool.runInteraction(_insert__, item)
reactor.run()
