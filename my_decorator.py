import logging
# 装饰器  增强函数的功能，确切的说，可以装饰函数，也可以装饰类。
# 装饰器最大的优势是用于解决重复性的操作，其主要使用的场景有如下几个：
    # 计算函数运行时间
    # 给函数打日志
    # 类型检查
def use_logging1(func):

    def wrapper(*args,**kwargs):
        logging.warn("%s is running"%func.__name__)
    return wrapper

def bar1():
    print("i am bar")

bar1 = use_logging1(bar1)
bar1()

# 直接使用装饰器标注可减少一行代码。bar = use_logging(bar)   采用语法糖@符号​​​​​​​
@use_logging1
def bar2():
    print("i am bar2")

bar2()



# 带参数的装饰器，多装饰一层，  形成参数闭包
def use_logging2(level):
    def decorator(func):
        def wrapper(*args,**kwargs):
            if level == "warn":
                logging.warn("%s is running"%func.__name__)
        return wrapper
    return decorator

@use_logging2(level = "info")
def foo(name="foo"):
    print("i am %s",name)

foo()



# 类装饰器
class Foo(object):
    def __init__(self,func):
        self._func = func
    def __call__(self):
        print("class decorator running")
        self._func()
        print("class decorator ending")

@Foo
def bar():
    print("bar")

bar()
print("--------------------")
# python2 使用装饰器极大的复用了代码，但带来一个缺点，就是原函数的元信息不见了，如函数的__doc__、__name__、参数列表
# python3 
def logged(func):
    def with_logging(*args,**kwargs):
        print(func.__name__+" wa called")
        print(func.__doc__+" was called")
        return func(*args,**kwargs)
    return with_logging

@logged
def f(x):
    """does some thing"""
    return x+x*x

print(f.__name__)   # witgh logging
print(f.__doc__)    # None

print('---------------------')

# 可使用functools.wraps来解决，他能把原函数的源信息拷贝到装饰器函数中，使得装饰器函数有和原函数一样元信息
from functools import wraps
def logged2(func):
    @wraps(func)
    def with_logging(*args,**kwargs):
        print(func.__name__+" wa called")
        print(func.__doc__+" was called")
        return func(*args,**kwargs)
    return with_logging

@logged2
def f2(x):
    """does some thing"""
    return x+x*x

print(f2.__name__)   # f2
print(f2.__doc__)    # does some thing

print('---------------------')
# 常见 内置装饰器有三种，@property,@staticmethod,@classmethod

# @property
# 把类内方法当成  属性  来使用，必须要有返回值，相当于getter；

# @staticmethod
# 静态方法，不需要表示自身对象的self和自身类的cls参数，就跟使用函数一样。

# @classmethod
# 类方法，不需要self参数，但第一个参数需要是表示自身类的cls参数
class Demo(object):
    text = "三种方法比较"

    def instance_method(self):
        print("call instance")

    @classmethod
    def class_method(cls):
        print('call class method')
        print('in class method call class attribute text: {}'.format(cls.text))
        print('in class method call instance method: {}'.format(cls().instance_method()))

    @staticmethod
    def static_method():
        print('call static method')
        print('in static method call class attribute text: {}'.format(Demo.text))
        print('in static method call class instance method: {}'.format(Demo().instance_method()))

if  __name__ == "__main__":
    d = Demo()
    print(d.text)

    d.instance_method()

    d.class_method()

    d.static_method()

    print('call class attribute ')
    print(Demo.text)

    Demo.static_method()

    Demo.class_method()

# 总结：
# 假如不需要用到与类相关的属性或方法时，就用静态方法@staticmethod；
# 假如需要用到与类相关的属性或方法，然后又想表明这个方法是整个类通用的，而不是对象特异的，就可以使用类方法@classmethod