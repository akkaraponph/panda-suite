# Slug usage

```python
from slug import slugify

slugify("Café déjà vu!")  # "cafe-deja-vu"
```

Verification command, run from this directory:

```sh
python3 -c "from slug import slugify; print(slugify('Café déjà vu!'))"
```

Status: verified locally; exit status 0, output `cafe-deja-vu`.

`python3 -m unittest -v` passed all 5 supplied tests. Six additional local
boundary assertions passed, including empty input and decomposed accents.
The external integration suite was not run because its runner is unavailable.
