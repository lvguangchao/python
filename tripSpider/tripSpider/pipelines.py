# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import uuid
import cx_Oracle
import datetime
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class TripspiderPipeline(object):
    count=0
    def __init__(self):
        pass
        # self.conn = cx_Oracle.connect('lab/Welc0melab@dev.imyway.cn:1521/XE')
        # self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        pass
        # print "*"*10
        # print json.dumps(dict(item))
        # self.count+=1
        # print "正在把第%d条数据 插入数据库"%self.count
        # try:
        #     self.cursor.execute("INSERT INTO v4crm_hotel_products (id, hotel_id, hotel_name, hotel_name_en, address, tel, website, picture, grade, longitude, latitude, hotel_level,"
        #                         " room_type, room_count, top_info,hotel_info, room_info, activity_info, descrip, order_option, locations, current_url, extract_date,gcode) "
        #                         "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
        #                         % (uuid.uuid1(),"".join(item["code"]),"".join(item["cName"]),"".join(item["eName"]),"".join(item["address"]),"","",",".join(item["imgUrl"]),item["score"],"","",item["hotel_level"]
        #                            , ",".join(item["room_types"]), ",".join(item["number_of_rooms"]),
        #                            ",".join(item["top_amenities"]), ",".join(item["hotel_amenities"]),
        #                            ",".join(item["room_amenities"]), ",".join(item["things_to_do"]),"".join(item["location"]),"".join(item["httpUrl"]),datetime.datetime.now(),"".join(item["gCode"])))
        #     self.conn.commit()
        # except Exception as e:
        #     self.conn.rollback()
        #     print("Error insert, the reason:", str(e))
        #     self.write_err(item)
        # finally:
        #     return item

    def close_spider(self, spider):
        pass
        # self.cursor.close()
        # self.conn.close()

    def write_err(self,item):
        f = open("error.txt", 'a')
        comment="".join(item["httpUrl"])+"\n"
        f.write(comment)
        f.close()