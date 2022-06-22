# Unix pipes vs. ZeroMQ

Using nanomsg or similar instead of Unix pipes as the underlying transport layer has some advantages:

Pros: 
- Works well on Unix, Windows, etc...
- Works across nodes (cool and useful!)
- Frame concept is very useful and bypasses problems with defining separators everywhere

Cons:
- Existing processes don't read from zeromq channel
- Easy to add on top of hoser based on unix pipes
- Extra overhead, not always needed
- How does recordless formats like compressed files work? (maybe treat it as a single frame?)


### Implementation questions
1. Should processes directly subscribe using the library or rely on stdin?

Stdin is ubiquitous and many programs designed for the unix environment already work very well with stdin. Forcing all programs to switch their transport layer seems unreasonable. Requires the hoser runtime to do an additional copy for each frame for each process which may be prohibitively expensive.


### Example

Each process defines its record format (by default line per record a.k.a lines). Argument to hoser.run()

```
@hoser.pipe
def filter_cats(in: hoser.Stream) -> hoser.Stream:
    return hoser.run("grep", stdin=in, argv=["-F", "cats"], sep="\n")
```

grep process
