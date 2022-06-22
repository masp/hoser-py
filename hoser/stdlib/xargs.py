import hoser

def run(lines: hoser.Stream, varname: str, pipe: hoser.Pipe, err = None) -> hoser.Stream:
    return hoser.exec("xargs", ["-I", "()", "hoser", f"$SELF:{pipe.name}", f"-v.{varname}=()"], stdin=lines, stderr=err)