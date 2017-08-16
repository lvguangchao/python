#coding=utf-8
#coding=utf-8
import  scrapy
from  tripSpider.items import TripspiderItem
from tripSpider.pipelines import TripspiderPipeline
import urllib2
from scrapy.utils.project import get_project_settings
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
chau=""
class Country(scrapy.Spider):
    name = 'country'
    allowed_domains = ['tripadvisor.cn']
    start_urls = ["https://www.tripadvisor.cn/Lvyou"]
    IMAGES_STORE = get_project_settings().get("IMAGES_STORE")

    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    count=0
    def parse(self, response):
        to_place_list = response.xpath("//div[@class='mod-d-wrapper']//div[@id='tab-body-wrapper']//a")
        for place in to_place_list:
            global chau
            url=place.xpath("./@href").extract()[0]
            start = url.index("-g")
            end = url[start + 2:].index("-")
            code = url[start + 2:end + start + 2]

            yield scrapy.Request(url="https://www.tripadvisor.cn"+url, callback=self.place_item,meta={"code":code})


    def place_item(self,response):
        code = response.meta["code"]
        detail_url=response.xpath("//*[@id='BODYCON']/div[1]/div[1]/div/div[2]/div[2]/ul/li[1]/a/@href").extract()
        if detail_url:
            yield scrapy.Request(url="https://www.tripadvisor.cn"+detail_url[0], callback=self.parseforList,meta={"code":code})
        else:
            detail_url= response.xpath("//*[@id='BODYCON']/div[1]/div[3]/div/div/div/div[2]/a/@href").extract()
        if detail_url:
            yield scrapy.Request(url="https://www.tripadvisor.cn" + detail_url[0], callback=self.parseforList,meta={"code":code})


    def parseforList(self,response):
        chau = response.meta["code"]
        #第一种情况
        place_list=response.xpath("//*[@id='BROAD_GRID']/div/div/div/div/a")
        for place in place_list:
            name = place.xpath("./text()").extract()[0]
            url = place.xpath("./@href").extract()[0]
            start = url.index("-g")
            end = url[start + 2:].index("-")
            code = url[start + 2:end + start + 2]
            str=name+","+code+","+chau+","+url+"\n"
            self.save_country(str)

         ##第二种情况
        if len(place_list)==0:
            place_second=response.xpath("//div[@id='LOCATION_LIST']/div[@id='BROAD_GRID']/div[@class='geos_grid']//div[@class='geo_wrap']//div[@class='geo_name']/a")
            if place_second and len(place_second)>0:
                for place_second_item in place_second:
                    place_second_url=place_second_item.xpath("./@href").extract()[0]
                    place_second_start = place_second_url.index("-g")
                    place_second_end = place_second_url[place_second_start + 2:].index("-")
                    place_second_code = place_second_url[place_second_start + 2:place_second_end + place_second_start + 2]

                    place_second_name=place_second_item.xpath("./text()").extract()[0]
                    place_second_str = place_second_name + "," + place_second_code + "," + chau + ","+place_second_url+"\n"
                    self.save_country(place_second_str)

                place_second_page=response.xpath("//div[@class='pageNumbers']/a/@data-page-number").extract()
                if place_second_page and len(place_second_page)>0:
                    for page_second in place_second_page:
                        try:
                            now_page_select= response.xpath("//div[@class='pageNumbers']/span/@data-page-number").extract()
                            now_page=now_page_select[0] if len(now_page_select)>0 else 0
                            if int(page_second)>int(now_page):
                                page_url = "https://www.tripadvisor.cn/Hotels-g%s-oa20-Pakistan-Hotels.html#LEAF_GEO_LIST" % (chau,)
                                yield scrapy.Request(url=page_url, callback=self.parseforList,meta={"code":chau})
                        except:
                            self.save_error(response.url+"\n")


        #判断多少页
        page_count=response.xpath("//div[@class='deckTools btm leaf_geos_override']//div[@class='pageNumbers']//a/@data-page-number").extract()
        if page_count and len(page_count)>0:
             page_url="https://www.tripadvisor.cn/Hotels-g%s-oa20-Pakistan-Hotels.html#LEAF_GEO_LIST"%(chau,)
             yield scrapy.Request(url=page_url, callback=self.parseforList,meta={"code":chau})


    def save_country(self,comment):
        with open("country.txt", "a") as f:
            f.write(comment)

    def save_error(self,comment):
        with open("error_city.txt", "a") as f:
            f.write(comment)




