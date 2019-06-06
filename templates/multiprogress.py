# coding: utf-8

from  multiprocessing import Pool
import time
import random


def Foo(i):
    with open(r'C:\Users\lu\Desktop\multi.txt', 'a') as f:
        f.write(str(i)+time.strftime('  %M:%S  ') + str(time.time())+ '\n')
    r = random.choice([0,1,2,3,4,5,6,7,8,9])

    raise Exception('random Exception')


if __name__ == '__main__':
    t_start=time.time()
    print(t_start)
    pool = Pool()

    for i in range(10000):
        pool.apply_async(func=Foo, args=(i,))#维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
        # Foo(i)
    pool.close()
    pool.join()  # 进程池中进程执行完毕后再关闭，如果注释，那么程序直接关闭。
    t_end=time.time()
    t=t_end-t_start
    print(t_end)
    print('the program time is :%s' %t)