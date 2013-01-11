import MySQLdb

try:
  conn = MySQLdb.connect(host = 'localhost', user = 'crawler', passwd = 'crawler123', db='origin_data', port=3306)
  cur = conn.cursor()
  cur.execute('select * from origin')
  cur.close()
  conn.close()

except MySQLdb.Error,e:
  print "Mysql Error %d: %s" % (e.args[0], e.args[1])
