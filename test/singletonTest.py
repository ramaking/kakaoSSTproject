import threading 
import ctypes 
import time 
from threadException import thread_with_exception

class SingletonInstane:
  __instance = None

  @classmethod
  def __getInstance(cls):
    return cls.__instance

  @classmethod
  def instance(cls, *args, **kargs):
    cls.__instance = cls(*args, **kargs)
    cls.instance = cls.__getInstance
    return cls.__instance

class MyClass(thread_with_exception, SingletonInstane):
  pass

# c = MyClass.instance('')
t1 = MyClass.instance('Thread 1') 
t1.start() 
time.sleep(0.5) 
print('111')
t1.raise_exception() 
t2 = MyClass


t2.start() 
time.sleep(1) 
t2.raise_exception() 
t1.join() 
t2.join()
print('aa')