import hoser

"""
Filters cat from a document containing lines of words

Run using `hoser run example.json <file.txt -hoser.filter='cats'` which will filters out any lines from file.txt that contain
cats and output it stdout.
"""

def filter(inp: hoser.Stream, filter: str) -> hoser.Stream:
    return hoser.exec("grep", ["-v", filter], stdin=inp)

@hoser.pipe
def filter_catsdogs(catsdogs: hoser.Stream) -> hoser.Stream:
    return filter(filter(catsdogs, "cats"), "dogs")

hoser.run(filter_catsdogs(hoser.stdin()))