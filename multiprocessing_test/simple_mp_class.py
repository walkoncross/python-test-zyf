from multiprocessing import Process
import time


class MyProcess(Process):
    def __init__(self, arg):
        super(MyProcess, self).__init__()
        self.arg = arg

    def run(self):
        print 'say hi', self.arg
        time.sleep(1)


# Commenting the following 'if'-clause will raise exception on Windows
if __name__ == '__main__':
    for i in range(10):
        p = MyProcess(i)
        p.start()
