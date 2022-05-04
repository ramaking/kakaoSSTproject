import time 
from threadException import thread_with_exception

class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):         # Foo 클래스 객체에 _instance 속성이 없다면
            print("__new__ is called\n")
            cls._instance = super().__new__(cls)  # Foo 클래스의 객체를 생성하고 Foo._instance로 바인딩
        return cls._instance                      # Foo._instance를 리턴

    def __init__(self, data):
        cls = type(self)
        if not hasattr(cls, "_init"):             # Foo 클래스 객체에 _init 속성이 없다면
            print("__init__ is called\n")
            self.data = data
            cls._init = True

class MyClass(thread_with_exception, Singleton):
  pass


# s1 = Singleton(3)
# s2 = Singleton(4)
# print(s1.data)
# print(s2.data)

s1 = MyClass('3')

# print(s1.data)
# print(s2.data)
s1.start() 
time.sleep(2) 
print('111')
# s1.raise_exception() 

s2 = MyClass('4')
s2.raise_exception() 
s2.start()
time.sleep(2)
s2.raise_exception()  
# s1.raise_exception() 
# s2.start() 
# time.sleep(1) 

# s1.join() 
# s2.join()
print('aa')