import threading
import time
from threadException import thread_with_exception
from timerStopper import timeStopper

thread_list = {}

def a(name):
    t1 = MyThread2(str(name)+str(1))
    t1.start()

class MyThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self) 
        self.name = name 

    def run(self):
        # t1 = timeStopper(5,a,args=(self.name,))
        # t1.start()
        time.sleep(2)
        t2 = MyThread2(str(self.name)+str(1))
        t2.start()
        while True:
            print(self.name)
            time.sleep(2)
            
        
class MyThread2(MyThread, thread_with_exception):
 pass

def f1(thread):
    thread.raise_exception()


t1 = MyThread2(1)
thread_list[0] = t1
t1.start()
time.sleep(11)
f1(thread_list[0])