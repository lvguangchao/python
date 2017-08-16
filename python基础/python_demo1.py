#coding=utf-8
import  random
import re
#去重list
old_list=[1,2,3,4,1,5]
new_list=list(set(old_list))
new_list.sort(old_list.index)
print new_list

#根据2个list 构建一个dict
a=['name','sex']
b=['lgc','male']
m=dict(zip(a,b))
zip(a,b)
print m


#大量字符串拼接
a=["a","b","c"]
print ",".join(a)

#GIL 一个全局的排它锁，避免多线程数据同步
#元类 用来创建类的东西


#items 一次性迭代出所有数据，iteritems 生成一个迭代对象，每次取出一个
a={"a":"A","b":"B"}
print type(a.items())
print type(a.iteritems())

#随机数
a=[1,2,3,4]
print  random.choice(a)
random.shuffle(a)
print a
#倒序
print a[::-1]
a.reverse()
print a


obj1=re.match(r"python","Programing Python, should be pythonic")
print obj1
obj2=re.search(r"python","Programing Python, should be pythonic")
print obj2.group()

a_list=[1,2,3,4,5]
print  tuple(a_list)

a=("a",)
print type(list(a))

#read()
# readline()  内存不够时候用
#readlines()

#列表的交集，并集，差
a=[1,2,3]
b=[2,3,5]
tmp=[val for val in a  if val in b]
print tmp

print list(set(a).union(set(b)))

print list(set(a).difference(set(b)))

print  map(str,[1,2,3,4])
def add(x,y):
    return x+y

print reduce(add,[1,2,3,4])

a=[x+y for x in range(1,10) for y in range(1,10)]
print a


#装饰器
def d(fp):
    def f(*arg,**kwargs):
        print "start"
        fp(*arg,**kwargs)
        print "end"
    return f
@d
def a():
    print "i will go away"

a()
