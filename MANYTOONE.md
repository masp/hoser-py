It seems to be a recurring desire to have many processes write concurrently to the same pipe as a way to "collect" results. For example, with errors:

```
errdump = hoser.Stream()

out = procA(stderr=errdump)
procB(stdin=out, stderr=errdump) # could concurrently overwrite with procA to errdump

return {"stderr": errdump}
```

How to prevent write conflicts?

# Ideas

1. When the process writes to a link, it actually writes to a proxy in the hoser runtime that makes sure writes are atomic.

Cons:
- Overhead from additional buffering (correctness over performance)
- Each line (record) must be completely storable in memory (no 100GB records)
- Adds hidden complexity to the communication patterns

Pros:
- All done implicitly (developer doesn't have to worry, simpler)


Mitigations:
- Overhead can be limited to only if multiple processes write to the same link

2. Disallow multiple processes writing to same link, use helper process that submits record through other mechanism explicitly (like ZeroMQ)

Cons:
- Extra dependencies and all explicit (how common is this case? If very common, unnecessary burden on users)


```
errdump = hoser.run(")
```
