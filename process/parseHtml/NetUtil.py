import urllib

class NetUtil:
	def download(self,url, localFileName = None):
		# req = urllib.Request(url)
		r = urllib.urlopen(url)
		f = open(localFileName, 'wb')
		f.write(r.read())
		f.close()