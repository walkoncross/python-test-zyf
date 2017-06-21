from multiprocessing import Process
import os

def info(title):
    print title
    print 'module name:', __name__
    if hasattr(os, 'getppid'):  # only available on Unix
        print 'parent process:', os.getppid()
    print 'process id:', os.getpid()

def f(name):
    info('==function f()')
    print 'hello', name

if __name__ == '__main__':
    info('==main line')
    p = Process(target=f, args=('bob',))
    p.start()
    
    print("This message might be printed either before or after fuction f()")
    p.join()
    print('main line exit') # mind the whether this message is printed at the end of the console with/without p.join()