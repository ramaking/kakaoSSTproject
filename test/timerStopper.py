import time 
from threadException import thread_with_exception
from threading import Timer

class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):         # Foo 클래스 객체에 _instance 속성이 없다면
            print("__new__ is called\n")
            cls._instance = super().__new__(cls)  # Foo 클래스의 객체를 생성하고 Foo._instance로 바인딩
        return cls._instance                      # Foo._instance를 리턴

    def __init__(self, data, thread):
        cls = type(self)
        if not hasattr(cls, "_init"):             # Foo 클래스 객체에 _init 속성이 없다면
            print("__init__ is called\n")
            self.data = data
            self.thread = thread
            cls._init = True

    def thread_stop(self):
        self.thread.raise_exception()

class timeStopper(Timer, Singleton, thread_with_exception):
  pass

# class My(Timer)