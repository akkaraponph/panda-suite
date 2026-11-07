# Slug usage

```python
from slug import slugify
slugify("Café déjà vu")  # "cafe-deja-vu"
```

Verified locally: `python3 -c 'from slug import slugify; print(slugify("Café déjà vu"))'` exited 0 and printed `cafe-deja-vu`.
`python3 -m unittest -v` exited 0: all four supplied tests passed.
External integration: not run; the runner is unavailable.
