# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from items import ParsehtmlItem

class ParsehtmlPipeline(object):
	
    def process_item(self, item, spider):
    	if isinstance(item, ParsehtmlItem):
    		print 'tetetetete'
        	
        	return item
