import os

class FileUtil:
	def getFileList(self, rootDir):
		list = os.listdir(rootDir)
		return list