from scrapy.contrib.loader import XPathItemLoader
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from parseHtml.items import HtmlContentItem,ParseFiveSelectOneItem,ParseTwoJudgementItem,ParseTwoSelectorItem,ParseTwoSixItem,ParseRcItem
from parseHtml.NetUtil import NetUtil
from parseHtml.FileUtil import FileUtil
import re
import sys
import string
import urllib
import os


class parseHtmlDemo(CrawlSpider):
	name="parseContent"
	reload(sys)
	downloadNet = NetUtil()
	sys.setdefaultencoding('utf-8')

	start_urls = ["file:///home/huwei/index.html"]
	# start_urls = ["file:///Users/huwei/python/test/parseHtml/index.html"]
	rules = (
		Rule(SgmlLinkExtractor(allow=r'(/sc|cr|ps|ds)/\d+\.html'), callback='parse_five_chose_one', follow=False),
		Rule(SgmlLinkExtractor(allow=r'/ir/\d+\.html'), callback='parse_ir', follow=False),
		Rule(SgmlLinkExtractor(allow=r'/rc/\d+\.html'), callback='parse_rc', follow=False)
	)

	def __init__(self):
		print 'init'
		super(parseHtmlDemo,self).__init__()
		f = open('TwoSelector.hmt')
		self.two_three_select_one_content = f.read()
		f.close()

		f = open('fiveOneType.hmt')
		self.five_chose_one_content = f.read()
		f.close()

		f = open('ThreeJudgement.hmt')
		self.three_judgement_content = f.read()
		f.close()

		f = open('TwoSixSelectOne.hmt')
		self.two_six_content = f.read()
		f.close()

		f = open('RcType.hmt')
		self.rc_content = f.read()
		f.close()

		fileUtil = FileUtil()
		self.fileList = fileUtil.getFileList('/home/huwei/origin/rcarticle')

		self.selectorTemplte = '<option class="option" value="{0}">{1}</option>'

		self.selectTemlete = '''<div id="question_{0}_1" class="sub-question">
	        <select name=" question_{1}_1">
	        	<option value="unselect">select..</option>
	        	{2}
	        </select>
	        <input class="c-option" name="question_{3}_1" type="hidden" value="{4}"/>
	    </div>'''
		
		self.headTemplete = '''<div class="question" id="question_{0}">'''

		self.explanationTemplete = '''<div class="explanation" style="display:none">{0}</div>'''

		self.judgemtn_templement = ''' <tr>
            <td><input name=" question_{0}_1" class="option" type="radio" value="{1}"/></td>
            <td><input name=" question_{2}_2" class="option" type="radio" value="{3}"/></td>
            <td>{4}</td>
        </tr> '''

	def parse_ir(self,response):
		loader = XPathItemLoader(item=HtmlContentItem(), response=response)
		loader.add_xpath('content', '//div[@id="QuestionContent"]')

		item =  loader.load_item()

		index = item['content'][0].find('<div class="question-table question-table-noborder')
		if index != -1:
			self.parse_three_judgement(response)
		else:
			index = item['content'][0].find('<div class="question-table">')
			if index != -1:
				self.parse_two_six(response)
			else:
				index = item['content'][0].find('<select class="question-select item">')
				if index != -1:
					self.parse_two_selector(response)
				else:
					self.parse_five_chose_one(response)

	def parse_rc(self,response):
		loader = XPathItemLoader(item=ParseRcItem(), response=response)
		id = self.parse_id_from_url(response.url)
		loader.add_value('questionId', id)
		loader.add_xpath('text', '//div[@class="text"]/text()')
		loader.add_xpath('text', '//div[@class="text"]/span/text()')
		loader.add_xpath('answerList','//div[@class="item clearfix"]/span/text()')
		loader.add_xpath('choiceList','//div[@class="item clearfix"]/b/text()')
		loader.add_xpath('answer','//div[@class="answer clearfix hidden QuesHidden"]/b/text()')
		# loader.add_xpath('explanation','//div[@id="DivExplain"]')
		item =  loader.load_item()
		if len(item['text']) ==3:
			test = item['text'][0] + '<span style="text-decoration:underline;">' + item['text'][2]  + '</span>'+ item['text'][1]
		else:
			test = item['text'][0]

		for filename in self.fileList:
			index = filename.find(id)
			if index != -1:
				f = open('/home/huwei/origin/rcarticle/' + filename)
				artile = f.read()
				f.close

		content = self.rc_content.format(artile[24:len(artile) - 4],item['questionId'][0],
			item['questionId'][0],test,
			item['questionId'][0],item['choiceList'][0],item['choiceList'][0],item['answerList'][0],
			item['questionId'][0],item['choiceList'][1],item['choiceList'][1],item['answerList'][1],
			item['questionId'][0],item['choiceList'][2],item['choiceList'][2],item['answerList'][2],
			item['questionId'][0],item['choiceList'][3],item['choiceList'][3],item['answerList'][3],
			item['questionId'][0],item['choiceList'][4],item['choiceList'][4],item['answerList'][4],
			item['questionId'][0],item['answer'][0])
		wf = open('/home/huwei/gmatclub/rc/' + id + '.html','w')
		wf.write(content)
		wf.close()
		return item

	def parse_two_six(self, response):
		print 'parse_two_six'
		loader = XPathItemLoader(item=ParseTwoSixItem(), response=response)
		id = self.parse_id_from_url(response.url)
		loader.add_value('questionId', id)
		loader.add_xpath('text', '//div[@class="text"]/text()')
		loader.add_xpath('content', '//div[@id="QuestionContent"]')
		loader.add_xpath('tableHead', '//div[@class="question-table"]/table/thead/tr/td[1]/text()')
		loader.add_xpath('tableHead', '//div[@class="question-table"]/table/thead/tr/td[2]/text()')
		loader.add_xpath('answerList', '//div[@class="question-table"]/table/tbody/tr[1]/td[3]/text()')
		loader.add_xpath('answerList', '//div[@class="question-table"]/table/tbody/tr[2]/td[3]/text()')
		loader.add_xpath('answerList', '//div[@class="question-table"]/table/tbody/tr[3]/td[3]/text()')
		loader.add_xpath('answerList', '//div[@class="question-table"]/table/tbody/tr[4]/td[3]/text()')
		loader.add_xpath('answerList', '//div[@class="question-table"]/table/tbody/tr[5]/td[3]/text()')
		loader.add_xpath('answerList', '//div[@class="question-table"]/table/tbody/tr[6]/td[3]/text()')
		loader.add_xpath('answer','//div[@class="answer clearfix hidden QuesHidden"]/b/text()')
		loader.add_xpath('explanation','//div[@id="DivExplain"]')
		tem =  loader.load_item()
		index = tem['text'][0].find('<img src="')
		print index
		if index != -1:
			loader.add_xpath('imageUrl', '//div[@class="text"]/img')
		item =  loader.load_item()

		answerCorrectList = item['answer'][0].split(',')
		count = 1 ;
		if index != -1:
			if item['imageUrl'] is None:
				print 'no image'
			else:
				for url in item['imageUrl']:
					print url
					downloadurl = 'http://www.kaogmat.com/' + url[11:len(url) - 2].replace('&amp;','&')
					print downloadurl
					self.downloadNet.download(downloadurl,'image' + str(id) + str(count) + ".jpg");
					count = count + 1;

				index = item['content'][0].find(item['imageUrl'][0])

				if index > 15:
					before = item['content'][0][index - 15:index]
				elif index > 5:
					before = item['content'][0][index - 5:index]
				else:
					before=''

		 		count = 0
				gmat_text = ''
				for text in item['text']:
					before_index = text.find(before)
					if before_index != -1:
						gmat_text =  gmat_text + text[0:before_index + len(before)] + '<img src="image' + id + '1.jpg">' + text[before_index +  + len(before) + 1 : len(text)]
						count = count + 1
					else:
						gmat_text = gmat_text + '<br>' + text
		else:
			gmat_text = ''
			for text in item['text']:
				gmat_text = gmat_text + '<br>' + text

		print len(item['answerList'])

		tableContent = ''
		for answer in item['answerList']:
			tableContent = tableContent + self.judgemtn_templement.format(item['questionId'][0],'',item['questionId'][0],'',answer)
 
		content = self.two_six_content.format(item['questionId'][0],gmat_text,
			item['questionId'][0],item['questionId'][0],answerCorrectList[0],
			item['questionId'][0],item['questionId'][0],answerCorrectList[1],
			item['tableHead'][0],item['tableHead'][1],
			tableContent,
			item['explanation'][0][21:len(item['explanation'][0]) - 6])
		wf = open('/home/huwei/gmatclub/ir/' + id + '.html','w')
		wf.write(content)
		wf.close()
		return item

	def parse_two_selector(self, response):
		print 'parse_two_selector'
		loader = XPathItemLoader(item=ParseTwoSelectorItem(), response=response)
		id = self.parse_id_from_url(response.url)
		loader.add_value('questionId', id)
		loader.add_xpath('content', '//div[@id="QuestionContent"]')
		loader.add_xpath('selectList', '//div[@class="content question"]/select')
		loader.add_xpath('answerList', '//div[@class="content question"]/select[1]/option[2]/text()')
		loader.add_xpath('answerList', '//div[@class="content question"]/select[1]/option[3]/text()')
		loader.add_xpath('answerList', '//div[@class="content question"]/select[1]/option[4]/text()')
		loader.add_xpath('answerList', '//div[@class="content question"]/select[1]/option[5]/text()')
		loader.add_xpath('answerList', '//div[@class="content question"]/select[1]/option[6]/text()')

		loader.add_xpath('answerList', '//div[@class="content question"]/select[2]/option[2]/text()')
		loader.add_xpath('answerList', '//div[@class="content question"]/select[2]/option[3]/text()')
		loader.add_xpath('answerList', '//div[@class="content question"]/select[2]/option[4]/text()')
		loader.add_xpath('answerList', '//div[@class="content question"]/select[2]/option[5]/text()')
		loader.add_xpath('answerList', '//div[@class="content question"]/select[2]/option[6]/text()')

		loader.add_xpath('imageUrl', '//div[@class="content question"]/img')
		# loader.add_xpath('answerList', '//div[@class="question-table question-table-noborder"]/table/tbody/tr[2]/td[3]/text()')
		# loader.add_xpath('answerList', '//div[@class="question-table question-table-noborder"]/table/tbody/tr[3]/td[3]/text()')
		loader.add_xpath('answer','//div[@class="answer clearfix hidden QuesHidden"]/b/text()')
		loader.add_xpath('explanation','//div[@id="DivExplain"]')
		loader.add_xpath('answerwithTag','//div[@class="answer clearfix hidden QuesHidden"]')
		item =  loader.load_item()

		answerCorrectList = item['answer'][0].split(',')

		print len(item['answerList'])
		answerSelectorList = ''
		count = 65
		for answerSelect in item['answerList'][0]:
			answerSelectorList = answerSelectorList + self.selectorTemplte.format(chr(count),answerSelect)
			count = count + 1

		selectorA = self.selectTemlete.format(item['questionId'][0],item['questionId'][0],
			answerSelectorList,
			item['questionId'][0],answerCorrectList[0])

		answerSelectorList = ''
		for answerSelect in item['answerList'][1]:
			answerSelectorList = answerSelectorList + self.selectorTemplte.format(chr(count),answerSelect)
			count = count + 1

		selectorB = self.selectTemlete.format(item['questionId'][0],item['questionId'][0],
			answerSelectorList,
			item['questionId'][0],answerCorrectList[0])

		count = 1 ;
		for url in item['imageUrl']:
			print url
			downloadurl = 'http://www.kaogmat.com/' + url[11:len(url) - 2].replace('&amp;','&')
			print downloadurl
			self.downloadNet.download(downloadurl,'image' + str(id) + str(count) + ".jpg");
			count = count + 1;

		text = item['content'][0].replace(item['selectList'][0],selectorA)
		text = text.replace(item['selectList'][1],selectorB)
		text = text.replace('<div class="content question" id="QuestionContent">',self.headTemplete.format(item['questionId'][0]))
		count = 1
		for imageUrl in item['imageUrl']:
			text = text.replace(imageUrl,'<img src="image' + str(id) + str(count) + '.jpg">')
		# text = text.replace(item['imageUrl'][1],'<img src="image2.jpg">')
		text = text.replace(item['answerwithTag'][0],'')
        
		wf = open('/home/huwei/gmatclub/ir/' +id + '.html','w')
		wf.write(text + self.explanationTemplete.format(item['explanation'][0][21:len(item['explanation'][0]) - 6]))
		wf.close()
		return item


	def parse_three_judgement(self, response):
		print 'parse_three_judgement'
		loader = XPathItemLoader(item=ParseTwoJudgementItem(), response=response)
		id = self.parse_id_from_url(response.url)
		loader.add_value('questionId', id)
		loader.add_xpath('text', '//div[@class="text"]/text()')
		loader.add_xpath('answerList', '//div[@class="question-table question-table-noborder"]/table/tbody/tr[1]/td[3]/text()')
		loader.add_xpath('answerList', '//div[@class="question-table question-table-noborder"]/table/tbody/tr[2]/td[3]/text()')
		loader.add_xpath('answerList', '//div[@class="question-table question-table-noborder"]/table/tbody/tr[3]/td[3]/text()')
		loader.add_xpath('answer','//div[@class="answer clearfix hidden QuesHidden"]/b/text()')
		loader.add_xpath('explanation','//div[@id="DivExplain"]')
		item =  loader.load_item()
		content = self.three_judgement_content.format(item['questionId'][0],item['text'][0],
			item['questionId'][0],item['questionId'][0],item['questionId'][0],item['questionId'][0],item['answerList'][0],
			item['questionId'][0],item['questionId'][0],item['questionId'][0],item['questionId'][0],item['answerList'][1],
			item['questionId'][0],item['questionId'][0],item['questionId'][0],item['questionId'][0],item['answerList'][2],
			item['explanation'][0][21:len(item['explanation'][0]) - 6])
		wf = open('/home/huwei/gmat/ir/' + id + '.html','w')
		wf.write(content)
		wf.close()
		return item

	def parse_five_chose_one(self, response):
		print 'parse_five_chose_One'
		loader = XPathItemLoader(item=ParseFiveSelectOneItem(), response=response)
		id = self.parse_id_from_url(response.url)
		loader.add_value('questionId', id)
		loader.add_xpath('text', '//div[@class="text"]/text()')
		loader.add_xpath('text', '//div[@class="text"]/span/text()')
		loader.add_xpath('answerList','//div[@class="item clearfix"]/span/text()')
		loader.add_xpath('choiceList','//div[@class="item clearfix"]/b/text()')
		loader.add_xpath('answer','//div[@class="answer clearfix hidden QuesHidden"]/b/text()')
		loader.add_xpath('explanation','//div[@id="DivExplain"]')
		item =  loader.load_item()
	        if len(item['text']) ==3:
			test = item['text'][0] + '<span style="text-decoration:underline;">' + item['text'][2]  + '</span>'+ item['text'][1]
		else:
			test = item['text'][0]
		content = self.five_chose_one_content.format(item['questionId'][0],test,
			item['questionId'][0],item['choiceList'][0],item['choiceList'][0],item['answerList'][0],
			item['questionId'][0],item['choiceList'][1],item['choiceList'][1],item['answerList'][1],
			item['questionId'][0],item['choiceList'][2],item['choiceList'][2],item['answerList'][2],
			item['questionId'][0],item['choiceList'][3],item['choiceList'][3],item['answerList'][3],
			item['questionId'][0],item['choiceList'][4],item['choiceList'][4],item['answerList'][4],
			item['questionId'][0],item['answer'][0],item['explanation'][0][21:len(item['explanation'][0]) - 6])
		wf = open('/home/huwei/gmatclub/ir/' + id + '.html','w')
		wf.write(content)
		wf.close()
		return item
		
	def parse_start_url (self, response):
		print response.url

	def parse_id_from_url(self, url):
		m = re.match('.*/(\d+)\.html', url)
		if m:
			return m.group(1)
		else:
			return None
