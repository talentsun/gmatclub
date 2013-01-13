from scrapy.item import Item, Field

class Question(Item):
    type = Field()
    set = Field()
    rating = Field()
    content = Field()
    answer = Field()
    explaination = Field()
    correct_rate = Field()