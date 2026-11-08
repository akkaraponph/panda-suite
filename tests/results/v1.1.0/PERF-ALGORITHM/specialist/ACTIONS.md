# Actual actions

Working directory for every shell command:
`/var/folders/dh/pyhpwt7x3y785l65wcc6gymh0000gn/T/panda-v110-trials-w4l64ir1/PERF-ALGORITHM/specialist` (pwd resolves under /private/var).

1. Ran `pwd && ls -la` to inspect only the assigned directory.
2. Ran `cat TASK.txt context.md small-plan.txt work.py test_work.py; rg --files instructions`. Read all five supplied files; discovered the supplied skill and its one reference.
3. Ran `cat instructions/panda-perf/SKILL.md instructions/panda-perf/references/profiling.md`. Applied only the identified panda-perf instructions and relevant CPU/memory profiling guidance. Did not access linked web documentation.
4. Ran a `PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'` disposable in-memory harness. Imported work, hashed work.py/test_work.py, printed runtime, ran unittest discovery, defined candidate `return list(dict.fromkeys(ids))`, checked equivalence, timed repeated comparable operations, measured separate tracemalloc allocations, and rehashed sources. The process was polled once through write_stdin until completion (exit 0). No harness or bytecode files were written.
5. Wrote ANSWER.md and this ACTIONS.md using shell heredocs. No supplied source was edited.

# Harness details and actual results

Runtime: Python 3.14.7 (v3.14.7:823f0323ee6, Aug 5 2026), Clang 21.0.0; macOS-27.2-arm64-arm-64bit-Mach-O.

`unittest.defaultTestLoader.discover('.', pattern='test_work.py')` ran 3 tests, all OK: test_generic, test_ids, test_recent_is_bounded. The latter cleared/updated in-memory RECENT only.

Candidate:
```python
def proposed(ids):
    return list(dict.fromkeys(ids))
```

Six list equivalence cases: [], [3,1,3,-1,1], [0,0], [-4,-3,-4], [-(10**100),10**100,-(10**100)], and list(iter([2,1,2])). Also checked candidate iterator output [2,1]. Used random.Random(1729) to generate 300 lists of lengths randrange(501), elements randrange(-100,101). Every original/candidate equality assertion passed. Checked original generic helper on nested lists, dicts, and [True,1,[1],[1]], preserving equality behavior.

Built mostly-distinct workload as `list(range(-9500,9500)) + list(range(-500,500))`, then shuffled using the same seeded RNG after random checks. Built duplicate-heavy workload as `[i%16 for i in range(20000)]`. Asserted equivalence for each timed workload. One warm-up each; seven samples, alternating old/new order. `timeit.timeit(lambda: fn(values), number=number)/number*1000`; number=1 for mostly distinct, 100 for duplicate-heavy and empty. Standard timeit behavior; single Python process. No production workload.

Raw milliseconds per call:

mostly_distinct_20000 original:
[739.2305829562247, 737.2405829955824, 736.388832970988, 738.3959580329247, 735.3277080110274, 742.7648750017397, 746.818583982531]

mostly_distinct_20000 proposed:
[0.3157079918310046, 0.29733404517173767, 0.3085829666815698, 0.28725003357976675, 0.34979096380993724, 0.2833339967764914, 0.3012499655596912]
Median speedup: 2451.1071948541526.

Tracemalloc separate fresh tracing session per implementation: call function, retain output, get_traced_memory, stop. Original current=153696 bytes, peak=153696; proposed current=152056, peak=884840. Both result lengths=19000. No RSS/native measurement.

duplicate_heavy_20000 original:
[0.7281941699329764, 0.7271491701249033, 0.7279820798430592, 0.7284408301347867, 0.7283550000283867, 0.727335840347223, 0.7288524997420609]

duplicate_heavy_20000 proposed:
[0.12537459027953446, 0.11592291994020343, 0.1254829199751839, 0.11835624987725168, 0.11247084010392427, 0.12198208016343415, 0.12372041994240135]
Median speedup: 5.969681521722917.

empty original:
[0.00005165988113731146, 0.0000504200579598546, 0.0000504200579598546, 0.00004582980182021856, 0.0000462500611320138, 0.00004542001988738775, 0.0000458303838968277]

empty proposed:
[0.00008333008736371994, 0.00007916009053587914, 0.00008000002708286047, 0.0000804202863946557, 0.00008167000487446785, 0.00007957976777106524, 0.00007750000804662704]
Median old/new ratio: 0.5781255684339962 (proposed slower).

Source hashes before and after matched exactly:
- work.py: 367b0450aa96c95e3fcd25412a7a33b04f52d32a102b3a64d959823e530f94b0
- test_work.py: dbf3b7115d831012c662d798c897617f4610c16ae2db79226adf0f16f02cf5cc

No network, installs, parent-project access, other-trial access, delegation, database actions, production profiling, or source changes.
