import scrapy

from recipe.items import RecipeItem

class RSpider(scrapy.Spider):
    name = "toscrape"
    start_urls = [
        "https://www.douguo.com/cookbook/755193.html",
        "https://www.douguo.com/cookbook/1048927.html"
    ]

    def parse(self, response):
            item = RecipeItem()
            #食谱名字
            item["name"] = response.xpath('//div[@class="recinfo"]//h1/text()').extract_first().strip()
            #食谱主要描述
            if response.xpath('//div[@class="retew r3 pb25 mb20"]//div[@class="xtip hidden"]/text()').extract_first() is not None:
                item["description"] = response.xpath('//div[@class="retew r3 pb25 mb20"]//div[@class="xtip hidden"]/text()').extract_first().strip()
            #难度
            if response.xpath('//table[@class="retamr"]//tr[1]//td[@class="lirre"]/text()').extract_first() is not None:
                item["difficulty"] = response.xpath('//table[@class="retamr"]//tr[1]//td[@class="lirre"]/text()').extract_first().strip()
            #时间
            if response.xpath('//table[@class="retamr"]//span[contains(text(), "时间：")]').extract_first() is not None:
                # item["time"] = response.xpath('//table[@class="retamr"]//span[contains(text(), "时间：")]').extract_first()             
                item["time"] = response.xpath('//table[@class="retamr"]//span[contains(text(), "时间：")]//../text()').extract()[2].strip().lstrip().rstrip(',')
            # #主料
            data = response.xpath('//table[@class="retamr"]//a[@target="_blank"]//..//..')
            item["main_ingredient"] = data.xpath('string(.)').extract()[0].strip().lstrip().rstrip(',')
            # #辅料
            # minor_ingredient = scrapy.Field()
            return item
