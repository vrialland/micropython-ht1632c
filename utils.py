import utime


def timeit(func, iterations=1, *args, **kwargs):
    start = utime.ticks_ms()
    for i in range(iterations):
        func(*args, **kwargs)
    stop = utime.ticks_ms()
    diff = utime.ticks_diff(stop, start)
    print('{0} iteration(s) took {1:.3}ms'.format(iterations, diff))
