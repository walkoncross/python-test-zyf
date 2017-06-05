import multiprocessing


def worker(i):
    """worker function"""
    print('Worker id: ' + str(i))
    print('Hello!')
    print('bye!!!\n')
    return


# Commenting the following 'if'-clause will raise exception on Windows
if __name__ == '__main__':
    jobs = []
    for i in range(5):
        p = multiprocessing.Process(target=worker, args=(i,))
        jobs.append(p)
        p.start()
