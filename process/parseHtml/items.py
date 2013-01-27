# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class BaseItem(Item):
    text = Field()
    answer = Field()
    answerList = Field()
    questionId = Field()
    explanation = Field()

class ParseFiveSelectOneItem(BaseItem):
    choiceList = Field()


class ParseTwoJudgementItem(BaseItem):
    pass

class ParseTwoSelectorItem(BaseItem):
    imageUrl = Field()
    selectList = Field()
    content = Field()
    answerwithTag = Field()


class ParseTwoSixItem(BaseItem):
    imageUrl = Field()
    tableHead = Field()
    content = Field()
    pass

class ParseRcItem(BaseItem):
    article = Field()
    choiceList = Field()
    pass

class HtmlContentItem(Item):
    content = Field()

