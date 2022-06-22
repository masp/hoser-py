from .compile import Stream, Input, exec

def merge(*streams: Stream, stream_names: Stream = None, sep="\n") -> Stream:
    """Takes many streams and merges them into one preserving record separators.

    stream_names is a stream of stream IDs, which will be merged with the "streams" passed in.
    
    If we just blindly write to streams, they will be all mixed up and the records are not preserved.
    """
    if len(streams) == 0:
        raise ValueError("must have at least one stream to merge")

    if len(streams) == 1:
        return streams[0] # Merging 1 stream is identity op
    
    argv: list = ["-sep", sep]
    argv += [Input(name=str(i+1), value=stream) for i, stream in enumerate(streams)]
    return exec("hoser-merge", argv, stdin=stream_names)

class Dump:
    def __init__(self, name: str) -> None:
        self.name = name
        self.streams: list[Stream] = []

    def add(self, stream: Stream):
        self.streams.append(stream)

    def merged(self) -> Stream:
        return merge(*self.streams)