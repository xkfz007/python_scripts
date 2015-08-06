#!/usr/bin/python
import threading
from time import ctime, sleep
from random import randint


class MyThread(threading.Thread):
  def __init__(self, func, args, name=''):
    threading.Thread.__init__(self)
    self.name = name
    self.func = func
    self.args = args

  def getResults(self):
    return self.res

  def run(self):
    print 'staring [', self.name, '] at: ', ctime()
    self.res = self.func(*self.args)
    print '\t [', self.name, '] done at: ', ctime()


def fib(x):
  sleep(0.005)
  if x < 2: return 1
  return (fib(x - 2) + fib(x - 1))


def fac(x):
  sleep(0.1)
  if x < 2: return 1
  return (x * fac(x - 1))


def sum(x):
  sleep(0.1)
  if x < 2: return 1
  return (x + sum(x - 1))


def Test1():
  funcs = (fib, fac, sum)
  n = 10

  nfuncs = range(len(funcs))
  print '*** SINGLE THREAD'
  for i in nfuncs:
    print 'starting ', funcs[i].__name__, 'at: ', ctime()
    print funcs[i](n)
    print funcs[i].__name__, 'done at: ', ctime()

  print '*** MULTIPLE THREADS'
  threads = []

  for i in nfuncs:
    t = MyThread(funcs[i], (n,), funcs[i].__name__)
    threads.append(t)

  for i in nfuncs:
    threads[i].start()

  for i in nfuncs:
    threads[i].join()
    print threads[i].getResults()

  print 'All Done'


def writeQ(queue):
  print 'producing object for Q...'
  queue.put('xxx', 1)
  print 'size now ', queue.qsize()


def readQ(queue):
  val = queue.get(1)
  print 'consumed object from Q..., size now', queue.qsize()


def writer(queue, loops):
  for i in range(loops):
    writeQ(queue)
    sleep(randint(1, 3))


def reader(queue, loops):
  for i in range(loops):
    readQ(queue)
    sleep(randint(2, 5))


from Queue import Queue


def Test2():
  funcs = (writer, reader)
  nfuncs = range(len(funcs))
  nloops = randint(2, 5)
  q = Queue(32)
  threads = []
  for i in nfuncs:
    t = MyThread(funcs[i], (q, nloops), funcs[i].__name__)
    threads.append(t)

  for i in nfuncs:
    threads[i].start()

  for i in nfuncs:
    threads[i].join()

  print "All Done"


Test2()
