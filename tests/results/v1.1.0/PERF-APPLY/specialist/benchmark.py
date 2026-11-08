"""Bounded synthetic benchmark; setup is excluded from timed calls."""
import json
import platform
import statistics
import sys
import time
import tracemalloc
import work

cases = {
    'mostly_distinct_20000': list(range(-18000, 0)) + list(range(-2000, 0)),
    'duplicates_20000': [i % 10 for i in range(20000)],
    'small_6': [3, 1, 3, -1, 0, 1],
    'empty': [],
}
report = {'python': platform.python_version(), 'concurrency': 1, 'warmups': 1, 'repetitions': 5, 'cases': {}}
for name, values in cases.items():
    expected = work.unique(values)
    assert work.unique_ids(values) == expected
    samples = []
    for _ in range(5):
        start = time.perf_counter_ns()
        result = work.unique_ids(values)
        samples.append((time.perf_counter_ns() - start) / 1e6)
        assert result == expected
    tracemalloc.start()
    result = work.unique_ids(values)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    report['cases'][name] = {'n': len(values), 'distinct': len(expected), 'samples_ms': samples, 'median_ms': statistics.median(samples), 'traced_peak_bytes': peak, 'traced_current_bytes_with_result': current}
with open(sys.argv[1], 'w') as f:
    json.dump(report, f, indent=2)
print(json.dumps(report, indent=2))
