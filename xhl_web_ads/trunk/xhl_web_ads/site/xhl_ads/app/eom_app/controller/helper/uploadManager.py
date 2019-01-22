#!/usr/bin/env python
# encoding: utf-8

"""
@author: lvguangchao
@email: guangchao.lv@qq.com
@file: uploadManager.py
@time: 2017/10/12 18:41
"""
import time
import threading
from .uploadFile import UploadSSH


class UploadManager(object):
    def __init__(self):
        self.task_dict = dict()
        self.task_gen = 0

    def create_task(self):
        temp_gen = self.task_gen
        temp_task = task(temp_gen)
        self.task_dict[temp_gen] = temp_task
        self.task_gen += 1
        return temp_gen

    def find_task(self, task_id):
        task_id = int(task_id)
        task = self.task_dict.get(task_id)
        task._last_access_time = time.time()
        return task

    def find_Process(self, task_id):
        task_id = int(task_id)
        task = self.task_dict.get(task_id)
        task.last_access_time = time.time()
        sftp = self.task_dict.get(task_id). \
            uploadSSH.sftp
        if sftp:
            return sftp.transfer_size
        else:
            return 0

    def check_task(self):
        while True:
            self.task_dict = {
                k: v for k,
                v in self.task_dict.items() if time.time() -
                v.last_access_time < 200}
            time.sleep(10)

    def task_destroy(self):
        t = threading.Thread(target=self.check_task)
        t.setDaemon(True)
        t.start()


class task(object):
    def __init__(self, task_id):
        self._task_id = task_id
        self.last_access_time = time.time()
        self._status = 0  # 0 初始化，开始上传，上传结束
        self._process = 0
        self.uploadSSH = UploadSSH()


_upManager = UploadManager()
del UploadManager


def app_upManager():
    global _upManager
    return _upManager
