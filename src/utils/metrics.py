from prometheus_client import Counter, Histogram
import time

# Metrics
REQUEST_COUNT = Counter(
    "request_count", "Total request count", ["method", "endpoint", "status"]
)
REQUEST_LATENCY = Histogram(
    "request_latency_seconds", "Request latency", ["endpoint"]
)
RETRIEVAL_LATENCY = Histogram(
    "retrieval_latency_seconds", "Time taken to retrieve documents"
)
GENERATION_LATENCY = Histogram(
    "generation_latency_seconds", "Time taken to generate answer"
)

def track_latency(histogram):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            latency = time.time() - start_time
            histogram.observe(latency)
            return result
        return wrapper
    return decorator
