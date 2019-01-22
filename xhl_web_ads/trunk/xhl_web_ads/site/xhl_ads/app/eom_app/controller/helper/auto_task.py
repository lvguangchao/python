#!/usr/bin/env python
# encoding: utf-8

"""
@author: lvguangchao
@email: guangchao.lv@qq.com
@file: auto_task.py
@time: 2018/1/11 10:16
"""

import time, threading, datetime
from eom_app.orm.db import app_db
from eom_app.orm.tables import TaskPlayLog, PlayLogAuto, Adresult, AdsOpLog
from eom_common.eomcore.logger import log
from sqlalchemy import func, or_, and_, distinct, case, desc


class AutoTask(object):
    def __init__(self):
        self.db_ads = None
        self.db_detect = None

    def db_ads_db(self):
        self.db_ads = app_db().get_Ads_DBSession()

    def db_detect_db(self):
        self.db_detect = app_db().get_detect_DBSession()

    # 定时任务函数
    def auto_task(self, hour, *fun):
        while True:
            now_hour = datetime.datetime.now().hour
            if now_hour == hour:
                for f in fun:
                    f()
                    time.sleep(10)
                time.sleep(86300)
            time.sleep(100)

    def start(self):
        t = threading.Thread(target=self.auto_task, args=(5, self.autoreview_log, self.playLogAudit))
        t.setDaemon(True)
        t.start()

    # 插入自动化审核操作日志
    def autoreview_log(self):
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yestorday = today - oneday

        self.db_ads_db()
        num = self.db_ads.query(PlayLogAuto).filter(PlayLogAuto.auto_date == yestorday).count()
        if num <= 0:
            max = self.db_ads.query(TaskPlayLog).filter(and_(TaskPlayLog.create_time == yestorday)).count()
            now = self.db_ads.query(TaskPlayLog).filter(
                and_(TaskPlayLog.create_time == yestorday, TaskPlayLog.verify_status == 1)).count()
            verify_num = self.db_ads.query(TaskPlayLog).filter(
                and_(TaskPlayLog.create_time == yestorday, TaskPlayLog.verify_status == 1,
                     TaskPlayLog.verify_result == 0)).count()
            account_num = self.db_ads.query(TaskPlayLog).filter(
                and_(TaskPlayLog.create_time == yestorday,
                     TaskPlayLog.verify_status == 1,
                     TaskPlayLog.close_account == 1,
                     TaskPlayLog.verify_result == 0)).count()
            count_money_num = self.db_ads.query(TaskPlayLog).filter(
                and_(TaskPlayLog.create_time == yestorday,
                     TaskPlayLog.verify_status == 1,
                     TaskPlayLog.close_account == 1,
                     TaskPlayLog.is_count_money == 1,
                     TaskPlayLog.verify_result == 0)).count()
            pa = PlayLogAuto()
            pa.auto_max = max
            pa.auto_now = now
            pa.auto_date = yestorday
            pa.verify_num = verify_num
            pa.account_num = account_num
            pa.count_money_num = count_money_num
            pa.update_time = datetime.datetime.now()
            pa.auto_status = 0

            self.db_ads.add(pa)
            try:
                self.db_ads.commit()
            except Exception as e:
                self.db_ads.rollback()
                log.e(e)
            finally:
                self.db_ads.close()

    def playLogAudit(self):
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yestorday = today - oneday

        # 获取连接
        self.db_ads_db()
        self.db_detect_db()

        results = self.db_ads.query(TaskPlayLog).filter(
            and_(TaskPlayLog.create_time == yestorday, TaskPlayLog.verify_status == 0)).all()
        for ret in results:
            p_data = self.db_ads.query(TaskPlayLog).filter(TaskPlayLog.play_id == ret.play_id).first()
            ad_results = self.db_detect.query(Adresult).filter(Adresult.ad_key == ret.play_id).all()
            if ad_results:
                # 更新自动化审核进度
                res_list = list()
                for ad in ad_results:
                    res_list.append(ad.is_ad)
                p_data.verify_user = 0
                p_data.verify_status = 1
                p_data.verify_result = 0 if 1 in res_list else -3
            else:
                p_data.verify_status = 1
                p_data.verify_result = -2
                p_data.verify_user = 0

        # 修改 is_count_money
        sql_count = 'SELECT task_id,sum(verify_result) as verify_result from ads_task_play_log ' \
                    'where create_time=\'{}\' GROUP BY task_id'.format(yestorday)
        task_counts = self.db_ads.execute(sql_count).fetchall()

        sql_update_count = 'update ads_task_play_log set is_count_money={} where task_id={}'

        for t in task_counts:
            task_id, verify_result = t
            verify_result = 1 if verify_result == 0 else 0
            temp_sql = sql_update_count.format(verify_result, task_id)
            self.db_ads.execute(temp_sql)

        # 添加自动化审核日志
        oplog = AdsOpLog()
        oplog.op_type = 6
        # user = self.get_current_user()
        oplog.op_user_id = 0
        oplog.op_user_name = 'root'
        oplog.op_desc = '用户root 自动化审核 日期:{}'.format(str(yestorday))
        oc = {"user_id": 0, 'datetime': datetime.datetime.now()}
        oplog.op_content = str(oc)
        oplog.createtime = datetime.datetime.now()
        self.db_ads.add(oplog)

        # 更新自动化审核数据信息
        query = self.db_ads.query(TaskPlayLog).filter(
            and_(TaskPlayLog.create_time == yestorday,
                 TaskPlayLog.verify_status == 1))
        now = query.count()
        query = query.filter(
            TaskPlayLog.verify_result == 0)
        verify_num = query.count()
        query = query.filter(TaskPlayLog.is_count_money == 1)
        count_money_num = query.count()
        query = query.filter(TaskPlayLog.close_account == 1)
        account_num = query.count()

        self.db_ads.query(PlayLogAuto).filter(PlayLogAuto.auto_date == yestorday).update({
            PlayLogAuto.auto_status: 1,
            PlayLogAuto.auto_now: now,
            PlayLogAuto.account_num: account_num,
            PlayLogAuto.count_money_num: count_money_num,
            PlayLogAuto.verify_num: verify_num,
            PlayLogAuto.update_time: datetime.datetime.now(),
            PlayLogAuto.auto_user: 'root'
        })

        try:
            self.db_ads.commit()
            log.w('root自动化审核 日期:{}  播放记录成功，.\n'.format(yestorday))
        except Exception as e:
            self.write_json(-1, '自动化审核失败')
            self.db_ads.rollback()
            log.e(e)
        finally:
            self.db_ads.close()
            self.db_detect.close()
