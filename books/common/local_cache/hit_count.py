import time
from functools import wraps
from collections import defaultdict


cached = defaultdict(int)


def counter_view(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        cached[int(time.time())] += 1
        return f(*args, **kwargs)
    return wrapper
