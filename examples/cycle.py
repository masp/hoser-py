import hoser as hs

@hs.pipe
def b(input: hs.Stream) -> hs.Stream:
    return a(input)

@hs.pipe
def a(input: hs.Stream) -> hs.Stream:
    return b(input)

hs.run(a(hs.file("test.txt")))