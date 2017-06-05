import multiprocessing as mp
import Queue


def foo(queue):
    queue.put('Hello from foo()')
    pass


# Commenting the following 'if'-clause will raise exception on Windows
if __name__ == '__main__':

    pool = mp.Pool()
    # q=Queue.Queue() # This will raise "TypeError: can't pickle thread.lock
                    # objects"
    q = mp.Manager().Queue()

    pool.map(foo, (q,))
    print(q.get())

