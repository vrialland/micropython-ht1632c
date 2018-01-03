import utime


def timeit(func, *args, **kwargs):
    start = utime.ticks_ms()
    func(*args, **kwargs)
    stop = utime.ticks_ms()
    return utime.ticks_diff(stop, start)
