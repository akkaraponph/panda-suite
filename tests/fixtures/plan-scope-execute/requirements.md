# Current snapshot invalidation

After sync, invalidate the current snapshot before attempting refresh. If
refresh fails, a read must not return stale cached content. Historical snapshots
must remain untouched.

Python 3 standard library only. No startup migration or legacy repair is in
scope.
