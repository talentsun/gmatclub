import MySQLdb
import urllib

types = ['sc', 'cr', 'rc', 'ps', 'ds', 'ir', 'awa']

def test_db():
  try:
    conn = MySQLdb.connect(host = 'localhost', user = 'crawler', passwd = 'crawler123', db='origin_data', port=3306)
    cur = conn.cursor()
    cur.execute('select * from origin')
    cur.close()
    conn.close()

  except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def url_for(type, page):
  return "http://www.kaogmat.com/" + type + "?p=" + str(page)

def urls_for(type):
  max_page = 10
  i = 1
  while i < max_page:
    url = url_for(type, i)
    f = urllib.urlopen(url)
    print f.read()
    i = i + 1

def start_fetch():
  for type in types:
    urls_for(type)
  print "start fetch"

def fetch_urls():
  fobj = file(str('/home/jianfeng/temp/t.html'))
  strContent = fobj.read()
  print strContent

if __name__ == "__main__":
  #start_fetch()
  fetch_urls()
