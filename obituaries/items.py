import scrapy


class ObituariesItem(scrapy.Item):
    full_name = scrapy.Field()
    date_of_birth = scrapy.Field()
    date_of_death = scrapy.Field()
    obituary_text = scrapy.Field()
