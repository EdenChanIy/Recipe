import scrapy
import csv

from recipe.items import RecipeItem

class RSpider(scrapy.Spider):
    start_urls = []
    csv_file = csv.reader(open('urls.csv', 'r'))
    for i,rows in enumerate(csv_file):
        if i != 0:
            start_urls.append(rows[1])
    print(start_urls)

    name = "toscrape"
    # start_urls = [
    #     "https://www.douguo.com/cookbook/755193.html",
    #     "https://www.douguo.com/cookbook/1048927.html"
    # ]

    # print(start_urls)

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
            datass = response.xpath('//table[@class="retamr"]//h3[contains(text(), "辅料")]//..//..//preceding-sibling::tr')
            content = ''
            if datass:
                for datas in datass:
                    datas = datass.xpath('.//td')
                    content = ''
                    order = 1
                    for data in datas:
                        # data_e = data.xpath('string(.)').extract()
                        ingredient = data.xpath(".//a/text() | .//label/text()").extract_first()
                        numbers = data.xpath('.//span[@class="right"]/text()').extract_first()
                        if ingredient:
                            # content.append({
                            #     '主料'+str(order): ingredient,
                            #     '数量': numbers
                            # })
                            content += ingredient + ': ' + numbers + "; "
                            order += 1
            else:
                datass = response.xpath('//table[@class="retamr"]//h3[contains(text(), "主料")]//..//..//following-sibling::tr')  
                for datas in datass:
                    datas = datass.xpath('.//td')
                    content = ''
                    order = 1
                    for data in datas:
                        # data_e = data.xpath('string(.)').extract()
                        ingredient = data.xpath(".//a/text() | .//label/text()").extract_first()
                        numbers = data.xpath('.//span[@class="right"]/text()').extract_first()
                        if ingredient:
                            # content.append({
                            #     '主料'+str(order): ingredient,
                            #     '数量': numbers
                            # })
                            content += ingredient + ': ' + numbers + "; "
                            order += 1
            item["main_ingredient"] = content 
            #辅料
            datass = response.xpath('//table[@class="retamr"]//h3[contains(text(), "辅料")]//..//..//following-sibling::tr')
            content_ = ''
            for datas in datass:
                datas = datass.xpath('.//td')
                content_ = ''
                order = 1
                for data in datas:
                    ingredient = data.xpath(".//label/text() | .//a/text()").extract_first()
                    numbers = data.xpath('.//span[@class="right"]/text()').extract_first()
                    if ingredient:
                        # content_.append({
                        #     '辅料'+str(order): ingredient,
                        #     '数量': numbers
                        # })
                        content_ += ingredient + ': ' + numbers + '; '
                        order += 1
            item["minor_ingredient"] = content_  
            #小贴士
            text = response.xpath('//h3[@id="tips"]//..//p/text()').extract()
            content = ''
            if text:
                content = "\n".join(text)
            item["tips"] = content
            #分类
            datas = response.xpath('//h4[contains(text(), "分类： ")]//..//span')
            content = ''
            order = 1
            if datas:
                for data in datas:
                    tag = data.xpath('.//a/text()').extract_first()
                    # content.append({
                    #     '分类' + str(order): tag
                    # })
                    content += tag + ';'
                    order += 1
            item["tags"] = content
            #url
            item["url"] = response.url
            item['image_urls'] = response.xpath('//img[@itemprop="image"]/@src').extract_first(),
            return item
