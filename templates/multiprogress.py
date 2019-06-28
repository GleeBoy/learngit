# coding: utf-8

# from  multiprocessing import Pool, Lock, Process, Semaphore
from  multiprocessing import *
import time
import random
import pickle
import os
import _thread
import queue
import threading

path1 = r'C:\Users\lu\Desktop\multi1.txt'
path2 = r'C:\Users\lu\Desktop\multi2.txt'
path3 = r'C:\Users\lu\Desktop\multi3.txt'
path4 = r'C:\Users\lu\Desktop\multi4.txt'
def foo(data, path, lock=None):
    if lock:
        print(lock)
        lock.acquire()
    with open(path, 'a') as f:
        f.write("%s processing %s" % (data, data) + '***************\n')
    if lock:
        lock.release()

def f00():
    while True:
        with open(path3, 'a') as f:
            for i in range(100):
                f.write("%s processing %s" % (i, i) + '***************\n')
    time.sleep(10)
    # p.addThread()

def f11(i):
    with Lock():
        with open(path4, "a+") as fs:
            fs.write("%s processing %s" % (i, i) + '***************\n')

def timeDecorate(func):
    def wrapper():
        t_start=time.time()
        print(t_start)
        func()

        t_end = time.time()
        t = t_end - t_start

        print('the program time is :%s' %t)
    return wrapper

@timeDecorate
def testPool():
    lock = Lock()   # 传不了lock参数

    pool = Pool()
    for i in range(10000):
        pool.apply_async(func=f11, args=(i,))  # 维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
    pool.close()
    pool.join()  # 进程池中进程执行完毕后再关闭，如果注释，那么程序直接关闭。

def testProcess():
    lock = multiprocessing.Lock()
    w = multiprocessing.Process(target=worker_with, args=(lock, f))
    nw = multiprocessing.Process(target=worker_no_with, args=(lock, f))

    w.start()
    nw.start()

    w.join()
    nw.join()


@timeDecorate
def original():
    for i in range(10000):
        foo(i, path1)

@timeDecorate
def testthreading():
    t = threading.Thread(target=f00)
    t.start()
    print(t.getName())
    t.join()
    print(t.isDaemon())


class ThreadPool(object):
    def __init__(self, maxsize):
        self.maxsize = maxsize
        self._q = queue.Queue(self.maxsize)
        for i in range(self.maxsize):
            self._q.put(threading.Thread)

    def getThread(self):
        return self._q.get()

    def addThread(self):
        self._q.put(threading.Thread)


def fun(num, p):
    print('this is thread [%s]' % num)
    time.sleep(1)
    p.addThread()

@timeDecorate
def testTH():
    pool = ThreadPool(10)
    for i in range(1000):
        t = pool.getThread()
        a = t(target=f00, args=(i, pool))
        a.start()
        a.join()
    print(pool._q.empty())


def worker_with(lock):
    for i in range(5000):
        with lock:
            with open(path4, "a+") as fs:
                fs.write("%s processing %s" % (i, i) + '***************\n')



def worker_no_with(lock):
    for i in range(5000):
        lock.acquire()
        with open(path4, "a+") as fs:
            fs.write("%s processing %s" % (i, i) + '***************\n')
        lock.release()


@timeDecorate
def testtowProcess():
    lock = Lock()

    w = Process(target=worker_with, args=(lock,))
    nw = Process(target=worker_no_with, args=(lock,))

    w.start()
    nw.start()

    w.join()
    nw.join()


def worker(s,i):
    s.acquire()
    with open(path4, "a+") as fs:
        fs.write("%s processing %s" % (i, i) + '***************\n')
    s.release()

@timeDecorate
def testSemaphore():
    s = Semaphore(4)
    for i in range(1000):
        p = Process(target=worker, args=(s,i))
        p.start()
        p.join()

if __name__ == '__main__':
    # original()
    testPool()
    # testProcess()
    # testthreading()
    # testTH()
    # foo(1,path2,lock=Lock())
    # testtowProcess()
    # testSemaphore()
    time.sleep(1)
    print(111111)
