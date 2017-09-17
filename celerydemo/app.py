#coding=utf-8
from tornado import web
import task

class TestHandler(web.RequestHandler):

    @web.asynchronous
    def get(self):
        task.mytask0.apply_async(
            args=['task0'],
                  callback=self.on_success)
    def on_success(self, result):
        print("callback success")
        self.finish({'task':result.result})