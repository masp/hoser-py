import json
from typing import List
import hoser
from hoser.stdlib import xargs

"""
Takes in PGN compressed files from lichess and parses them and summarizes them.
"""

stderr = hoser.Dump(name="errdump")
def errdump(proc: hoser.Process, err: hoser.Stream):
    labelled = hoser.exec("sed", [f"s/^/[{proc.name}] /"], stdin=err)
    stderr.add(labelled)

def find(path: hoser.String, pattern: hoser.String) -> hoser.Stream:
    files = hoser.exec("find", [hoser.Input("path", path), "-name", hoser.Input("pattern", pattern)])
    return files

def decompress(compressed: hoser.Stream) -> hoser.Stream:
    decomp = hoser.exec("bzip2", ["-d"], stdin=compressed, stderr=errdump)
    return decomp

def summarize(pgn: hoser.Stream) -> hoser.Stream:
    resultOnly = hoser.exec("grep", ["-F", "Result"], stdin=pgn)
    summarized = hoser.exec("mawk", ["""
/Result/ {
    split($0, a, "-");
    res = substr(a[1], length(a[1]), 1);
    if (res == 1) white++;
    if (res == 0) black++;
    if (res == 2) draw++;
}
END { print white+black+draw, white, black, draw }
"""], stdin=resultOnly, stderr=errdump)
    return summarized

@hoser.pipe
def summarize_pgn_file(compressed_pgn: hoser.Stream) -> hoser.Returns:
    rawpgn = decompress(compressed_pgn)
    summary = summarize(rawpgn)
    return {"stdout": summary, "stderr": stderr.merged()}

@hoser.pipe
def summarize_dir(path: hoser.String) -> hoser.Returns:
    pgn_files = find(path, pattern=hoser.string("*.pgn.bz2"))
    results, errs = hoser.run_lines(pgn_files, summarize_pgn_file(hoser.file(name="line")), err=True)
    return {"stdout": hoser.merge(results, stream_names=errs)}


if __name__ == "__main__":
    hoser.run(summarize_dir(hoser.string("games/")))