#coding=utf-8

#列表生成式
a=list(range(1,11))
print a

b=[x*x for x in  range(1,10)]
print b

c=[x*2 for x in range(1,10) if x%2==0]
print c

d=[m+n for m in "ABC" for n in "DEF"]
print d

for x in range(1,10):
    print x
L=["hello","world",17,"apple",None]
e=[s.lower() for s in L if  isinstance(s,str)]
print e

#生成器
f=(x for x in range(1,10))
print type(f)
for g in f:
    print g

#生成器
def fib(max):
    n,a,b=0,0,1
    while n<max:
        yield b
        print "*"*10
        a,b=b,a+b
        n=n+1
a=fib(6)
print  next(a)
print  next(a)
print  next(a)


#枚举类型
from  enum import Enum,unique
@unique
class Weekday(Enum):
    sun=0
    mon=1
    tue=2
if __name__ == '__main__':
    print Weekday.sun.value
    print Weekday.mon.value
    print Weekday.tue.value