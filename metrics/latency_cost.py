import time

def measure_latency(fn):
    start = time.time()
    fn()
    return round(time.time() - start, 3)


def estimate_cost(tokens, cost_per_1k=0.002):
    return round((tokens / 1000) * cost_per_1k, 6)