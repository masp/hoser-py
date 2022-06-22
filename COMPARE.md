### How to extend a simple pipe
A pipe (summarize_pgn) that takes in a bz2 compressed stream of pgn files and transforms it to a summary of wins, losses, draws.

Perform on one file:

```python
hoser.run(summarize_pgn(hoser.stdin()))
```

Perform on TCP stream:

```python
hoser.run(summarize_pgn(http.stream("http://website.org/a.pgn.bz2")))
```

Perform on list of files, one at a time:
```python
files = hoser.stream("""
a.pgn.bz2
b.pgn.bz2
""")

def file_per_line(files: hoser.Stream):
    hoser.run(summarize_pgn(hoser.file(files)))

hoser.run(file_per_line(files))
```

Input file of complex parameters per line, each pipe does a complex calculation and outputs to a common shared output

Subpipes
```
file = "a.txt"
hoser.run(summarize_pgn(hoser.file(file))
```


Different ways to divide:

1 record at a time (equivalent to xargs)
```
files = """
a.txt
b.txt
"""
errdump = hoser.Stream()
summarize(hoser.divide(files), factor=2, err=errdump))
```

1 records processed by X processes at a time (equilvane to parallel)
```
summarize(hoser.divide(files, parallel=X), factor=2, err=errdump))
```

X records processed by 1 process a time (batch processing)
```
summarize(hoser.divide(files, n=X), factor=2, err=errdump)
```

X records processed by X process at a time
```
summarize(hoser.divide(files, n=X, parallel=X), factor=2, err=errdump)
```

