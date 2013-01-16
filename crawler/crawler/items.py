# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

#SC, CR, PS, and DS
class Question(Item):
    id = Field()
    type = Field()
    set = Field()
    rating = Field()
    content = Field()
    answer = Field()
    explaination = Field()
    correct_rate = Field()

#IR and RC
class CompoundQuestion(Question):
    article = Field()
    sub_questions = Field()

#AWA
class Argument(Item):
    id = Field()
    rating = Field()
    essay = Field()
    
