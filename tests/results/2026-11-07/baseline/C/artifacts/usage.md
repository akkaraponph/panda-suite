# Slug usage

From this directory:

```sh
python3 -B -c 'from slug import slugify; result = slugify("Café déjà vu"); assert result == "cafe-deja-vu"; print(result)'
```

Verified by execution: exit status 0; output:

```text
cafe-deja-vu
```

Local verification: `python3 -B -m unittest -v` exited 0, with all four supplied tests passing. The external integration runner was unavailable and was not run.
