import scrapy

from recipe.items import RecipeItem

class RSpider(scrapy.Spider):
    name = "toscrape"
    start_urls = [
        "https://www.douguo.com/cookbook/1048927.html"
    ]

    def parse(self, response):
            item = RecipeItem()
            #食谱名字
            item["name"] = response.xpath('//div[@class="recinfo"]//h1/text()').extract_first().strip()
            #食谱主要描述
            item["description"] = response.xpath('//div[@class="retew r3 pb25 mb20"]//div[@class="xtip hidden"]/text()').extract_first().strip()
            #难度
            item["difficulty"] = response.xpath('//table[@class="retamr"]//tr[1]//td[@class="lirre"]/text()').extract_first().strip()
            #时间
            item["time"] = response.xpath('//table[@class="retamr"]//tr[1]//td[2]/text()').extract()[1].strip().lstrip().rstrip(',')
            # #主料
            # item["time"] = response.xpath('//table[@class="retamr"]//tr[2]//h3[@class="zfliao"]/text()').extract_first().strip()
            # main_ingredient = scrapy.Field()
            # #辅料
            # minor_ingredient = scrapy.Field()
            return item
