import hoser

@hoser.pipe
def dumptest() -> hoser.Stream:
    f1 = hoser.file("testdata/a.txt")
    f2 = hoser.file("testdata/b.txt")
    return hoser.merge(f1, f2, sep="\n")

hoser.run(dumptest())