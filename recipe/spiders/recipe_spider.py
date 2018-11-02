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
                item["time"] = response.xpath('//table[@class="retamr"]//span[contains(text(), "时间：")]//../text()').extract()[2].strip().lstrip().rstrip(',')
            #主料
            datas = response.xpath('//table[@class="retamr"]//h3[contains(text(), "主料")]//..//..//following-sibling::tr[1]//td')
            content = []
            order = 1
            for data in datas:
                # data_e = data.xpath('string(.)').extract()
                ingredient = data.xpath(".//a/text()").extract_first()
                numbers = data.xpath('.//span[@class="right"]/text()').extract_first()
                if ingredient:
                    content.append({
                        '主料'+str(order): ingredient,
                        '数量': numbers
                    })
                    order += 1
            item["main_ingredient"] = content           
            #辅料
            datass = response.xpath('//table[@class="retamr"]//h3[contains(text(), "辅料")]//..//..//following-sibling::tr')
            for datas in datass:
                datas = datass.xpath('.//td')
                content = []
                order = 1
                for data in datas:
                    ingredient = data.xpath(".//label/text() | .//a/text()").extract_first()
                    numbers = data.xpath('.//span[@class="right"]/text()').extract_first()
                    if ingredient:
                        content.append({
                            '辅料'+str(order): ingredient,
                            '数量': numbers
                        })
                        order += 1
            item["minor_ingredient"] = content  
            return item
