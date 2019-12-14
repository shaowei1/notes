"""
# memory
    ## requirements.txt
        pip install psutil
        pip install memory_profiler

    ## run:
        python3.6 -m memory_profiler memory_detect.py

# cpu
    # cProfile output visualization,
        pip install runsnake
        pip install wxPython
        find the max spending function, then analysis the function

        python3.6 -m cProfile -s cumulative  memory_detect.py
        
    # line_profiler analysis one by one line(cpu)
        pip install line_profiler


        - generate file
        python3.6 -m cProfile -o profile.stats memory_detect.py
    kernprof -l -v memory_detect.py


# time
    1. time_func
    2. python -m timeit -n 5 -r -s "import julia1 julia1.calc_func()"
    3. ipython (%timeit calc_func())

"""

# memory profile

if 'profile' not in dir():
    def profile(func):
        def inner(*args, **kwargs):
            return func(*args, **kwargs)

        return inner

import time
from functools import wraps
def time_func(fn):
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        print("@time:" + fn.__name__ + " took " + str(t2 - t1) + " seconds")
        return result

    return measure_time


@time_func
# @profile
def main():
    print()


if __name__ == '__main__':
    main()
