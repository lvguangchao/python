#coding=utf-8
from contextlib import contextmanager,closing
import urllib
class Query(object):
    def __init__(self,name):
        self.name=name
    # def __enter__(self):
    #     print "begin"
    #     return self
    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     if exc_tb:
    #         print "error"
    #     else:
    #         print "end"
    def query(self):
        print "query %s"%self.name

@contextmanager
def create_query(name):
    print "begin"
    q=Query(name)
    yield q
    print "end"

@contextmanager
def tag(name):
    print ("<%s>"%name)
    yield
    print ("<%s>"%name)


if __name__ == '__main__':
    # with create_query("bob") as q:
    #     q.query()

    # with tag("h1"):
    #     print "hello world"

    with closing(urllib.urlopen("http://www.baidu.com")) as page:
        for line in page:
            print line
