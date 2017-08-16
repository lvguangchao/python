#coding=utf-8
import  scrapy
from  tripSpider.items import TripspiderItem
import urllib2
from scrapy.utils.project import get_project_settings
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os

class TripListSpider(scrapy.Spider):
    name = 'tripList'
    allowed_domains = ['tripadvisor.cn']
    start_urls = ["https://www.tripadvisor.cn/Hotel_Review-g317043-d3484639-Reviews-Vava_u_Villa-Neiafu_Vava_u_Islands.html"]
    IMAGES_STORE = get_project_settings().get("IMAGES_STORE")

    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    def parse(self, response):
        trip_list_urls=response.xpath("//div[@class='listing easyClear  p13n_imperfect hideUrgencyMessaging']//div[@class='illisting ilCR addprice center with_datepickers ']"
                       "/div[@class='hotel_content easyClear sem']//div[@class='prw_rup prw_common_short_cell_thumbnail_default_image']/a/@href").extract()

        for trip in trip_list_urls:
             yield scrapy.Request("https://www.tripadvisor.cn/"+trip, callback=self.paseDetails)

        #获取总页数
        pageCount=response.xpath("//div[@class='prw_rup prw_common_standard_pagination']//div[@class='pageNumbers']//a/@data-page-number").extract()
        sta = str(response.url).index("-g")
        end = str(response.url).find("-", sta + 2)
        geo = response.url[sta + 2:end]

        pageCounts=pageCount[-1:] if pageCount else 0
        pageCounts= int("".join(pageCounts))
        if pageCounts:
            for page in range(pageCounts):
                formData={"seen":"0","sequence":"2","geo":str(geo),"requestingServlet":"Hotels","refineForm":"true","hs":"",
                          "adults":"","rooms":"","rad":"0","dateBumped":"NONE","displayedSortOrder":"availability","o":"a"+str(page*30)}
                url="https://www.tripadvisor.cn/Hotels"
                yield scrapy.FormRequest(
                    url=url,
                    formdata=formData,
                    callback=self.parse)

    def paseDetails(self,response):
        item = TripspiderItem()
        item["cName"] = ""
        item["eName"] = ""
        item["address"] = ""
        item["imgUrl"] = ""
        item["score"] = ""
        item["description"] = ""
        item["httpUrl"] = ""
        item["coordinate"] = ""
        item["top_amenities"] = ""
        item["hotel_amenities"] = ""
        item["room_amenities"] = ""
        item["things_to_do"] = ""
        item["room_types"] = ""
        item["location"] = ""
        item["number_of_rooms"] = ""
        item["code"] = ""
        item["reservation_options"] = ""
        item["tel"] = ""
        item["hotel_level"] = ""

        item["httpUrl"] = response.url

        # 酒店名称
        cName = response.xpath("//h1/text()").extract()
        if cName:
            item["cName"] = cName[0]
        eName = response.xpath(
            "//div[@id='taplc_hr_atf_north_star_nostalgic_0']//span[@class='altHead']/text()").extract()
        if eName:
            item["eName"] = eName[0]

        # 地址
        address = response.xpath("//div[contains(@class,'blEntry address  clickable')]//text()").extract()
        # address = response.xpath("//div[@class='prw_rup prw_common_atf_header_bl headerBL']")
        # street_address = address.xpath("//span[@class='street-address']/text()")
        # extended_address = address.xpath("//span[@class='extended-address']/text()")
        # locality = address.xpath("//span[@class='locality']/text()")
        # country_name = address.xpath("//span[@class='country-name']/text()")
        # item["address"] = street_address.extract()[0] + extended_address.extract()[0] + locality.extract()[0] +country_name.extract()[0]
        item["address"] = ",".join(address)
        # 图片
        imgs = response.xpath(
            "//div[@class='atf_meta_and_photos ui_container is-mobile easyClear']//div[@class='carousel_images']//div[@class='page_images']//div[@class='prw_rup prw_common_centered_image photo']"
            "//span[@class='imgWrap ']//img[@class='onDemandImg centeredImg']/@data-src")
        imgsUrls = []
        num = 1
        for img in imgs:
            imgsUrl = img.extract()
            imgsUrls.append(imgsUrl)
            self.saveImg(imgsUrl, self.IMAGES_STORE + "/" + item["cName"], str(num) + ".jpg")
            num += 1
        item["imgUrl"] = imgsUrls
        score = response.xpath(
            "//div[@class='ppr_rup ppr_priv_location_detail_overview']//div[@class='ui_columns is-multiline is-mobile reviewsAndDetails']"
            "//div[@class='rating']//span[@class='overallRating']/text()").extract()
        if score:
            item["score"] = score[0]

        # 酒店描述
        requestUrl = "https://www.tripadvisor.cn/MetaPlacementAjax"
        sta = str(item["httpUrl"]).index("-d")
        end = str(item["httpUrl"]).find("-", sta + 2)
        id = item["httpUrl"][sta + 2:end]
        item["code"] = id

        sta2 = str(item["httpUrl"]).index("-g")
        end2 = str(item["httpUrl"]).find("-", sta2 + 2)
        item["gCode"] = item["httpUrl"][sta2+2:end2]
        url = "https://www.tripadvisor.cn/MetaPlacementAjax?detail=%s&placementName=hr_btf_north_star_about&more_content_request=true" % id
        print url
        headers = {'User-Agent': self.user_agent}
        try:
            req = urllib2.Request(url, headers=headers)
            u = urllib2.urlopen(req)
            item["description"] = u.read()
        except Exception, e:
            pass

        # 顶级设置
        top_amenities = response.xpath("//ul[@class='list top_amenities']//text()").extract()
        hotel_amenities = response.xpath("//ul[@class='list hotel_amenities']//text()").extract()
        room_amenities = response.xpath("//ul[@class='list room_amenities']//text()").extract()
        things_to_do = response.xpath("//ul[@class='list things_to_do']//text()").extract()
        # 客房类型[0]
        room_types = response.xpath("//ul[@class='list room_types']//text()").extract()
        # 房间数
        number_of_rooms = response.xpath("//ul[@class='list number_of_rooms']//text()").extract()
        # 位置[0]
        location = response.xpath("//ul[@class='list location']//text()").extract()
        # 预订选项

        reservation_options = response.xpath("//ul[@class='list reservation_options']//text()").extract()

        phoneNum = response.xpath("//div[@class='blEntry phone']//text()").extract()

        # jwd=response.xpath("//div[@class='overviewContent']//div[@class='prv_map clickable']//img/@src")

        xj = response.xpath("//div[@class='starRating detailListItem']//text()").extract()

        if top_amenities and len(top_amenities) > 1:
            item["top_amenities"] = top_amenities[1:]
        if hotel_amenities and len(hotel_amenities) > 1:
            item["hotel_amenities"] = hotel_amenities[1:]
        if room_amenities and len(room_amenities) > 1:
            item["room_amenities"] = room_amenities[1:]
        if things_to_do and len(things_to_do) > 1:
            item["things_to_do"] = things_to_do[1:]
        if room_types and len(room_types) > 1:
            item["room_types"] = room_types[1:]
        if number_of_rooms and len(number_of_rooms) > 1:
            item["number_of_rooms"] = number_of_rooms[1:]
        if location and len(location) > 1:
            item["location"] = location[1:]
        if reservation_options and len(reservation_options) > 1:
            item["reservation_options"] = reservation_options[1:]
        if phoneNum and len(phoneNum) > 1:
            item["tel"] = phoneNum[1]
        if xj and len(phoneNum) > 1:
            item["hotel_level"] = xj[1]
        yield item

    def saveImg(self, imageURL, filePath, fileName):
        if imageURL:
            try:
                u = urllib2.urlopen(imageURL)
                data = u.read()
                if not os.path.isdir(filePath):
                    os.makedirs(filePath)
                f = open(filePath + "/" + fileName, 'wb')
                f.write(data)
            except urllib2.URLError, e:
                print "The reason:", e.reason
            finally:
                f.close()
