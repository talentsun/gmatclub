from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from crawler.items import Question, CompoundQuestion, Argument
import re

class KaogmatSpider(CrawlSpider):
    name = 'kaogmat'
    allowed_domains = ['kaogmat.com']
    start_urls = ['http://www.kaogmat.com/cr/','http://www.kaogmat.com/rc/','http://www.kaogmat.com/ps/','http://www.kaogmat.com/ds/','http://www.kaogmat.com/ir/','http://www.kaogmat.com/awa/']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'/(sc|cr|ps|ds)/\d+\.html'), callback='parse_question', follow=False),
        Rule(SgmlLinkExtractor(allow=r'/(rc|ir)/\d+\.html'), callback='parse_compound_question', follow=False),
        Rule(SgmlLinkExtractor(allow=r'/awa/\d+\.html'), callback='parse_argument', follow=False),
        Rule(SgmlLinkExtractor(allow=r'/question\?p=\d+'), callback=None, follow=True),
    )

    def parse_question(self, response):
        loader = XPathItemLoader(item=Question(), response=response)
        id = self.parse_id_from_url(response.url)
        if id:
            loader.add_value('id', id)
        else:
            loader.add_value('id', -1)
        loader.add_xpath('type', '//div[@class="title"]/h1/a/text()')
        loader.add_xpath('set', '//div[@class="title"]/span/a/text()')
        loader.add_xpath('rating', '//b[@id="QuestionRateValue"]/text()')
        loader.add_xpath('content', '//div[@id="QuestionContent"]')
        loader.add_xpath('answer', '//div[@class="answer clearfix hidden QuesHidden"]/b/text()')
        loader.add_xpath('explaination', '//div[@id="DivExplain"]')
        loader.add_xpath('correct_rate', '//div[@class="w-stat hidden QuesHidden"]/div[@class="info"]/b/text()')
        return loader.load_item()
    def parse_compound_question(self, response):
        loader = XPathItemLoader(item=CompoundQuestion(), response=response)
        id = self.parse_id_from_url(response.url)
        if id:
            loader.add_value('id', id)
        else:
            loader.add_value('id', -1)
        loader.add_xpath('type', '//div[@class="title"]/h1/a/text()')
        loader.add_xpath('set', '//div[@class="title"]/span/a/text()')
        loader.add_xpath('rating', '//b[@id="QuestionRateValue"]/text()')
        loader.add_xpath('content', '//div[@id="QuestionContent"]')
        loader.add_xpath('answer', '//div[@class="answer clearfix hidden QuesHidden"]/b/text()')
        loader.add_xpath('explaination', '//div[@id="DivExplain"]')
        loader.add_xpath('correct_rate', '//div[@class="w-stat hidden QuesHidden"]/div[@class="info"]/b/text()')
        loader.add_xpath('article', '//div[@class="article rt"]')
        loader.add_xpath('sliding_questions', '//div[@class="title"]/h1/*[position()>1]/text()')
        return loader.load_item()
    def parse_argument(self, response):
        loader = XPathItemLoader(item=Argument(), response=response)
        id = self.parse_id_from_url(response.url)
        if id:
            loader.add_value('id', id)
        else:
            loader.add_value('id', -1)
        loader.add_xpath('rating', '//b[@id="QuestionRateValue"]/text()')
        loader.add_xpath('essay', '//div[@class="essay"]')
        return loader.load_item()
    def parse_id_from_url(self, url):
        m = re.match('.*/(\d+)\.html', url)
        if m:
            return m.group(1)
        else:
            return None
