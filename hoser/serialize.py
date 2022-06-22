
import json
import re
from typing import Any, cast, Union
from hoser.compile import Link, Node, Pipe, Port, Process, Variable


def serialize(*args: Pipe) -> str:
    pipes = [*args]
    result: list[dict] = []
    for pipe in pipes:
        serpipe: dict[str, Any] = {
            "name": pipe.name,
        }
        serpipe["procs"] = [_serialize_node(n) for _, n in pipe.nodes.items() if isinstance(n, Process)]
        serpipe["vars"] = [_serialize_node(n) for _, n in pipe.nodes.items() if isinstance(n, Variable)]
        serpipe["links"] = [_serialize_link(l) for l in pipe.links]
        result.append(serpipe)
        pipes += pipe.children
    return json.dumps(result)

def _serialize_node(node: Node) -> dict[str, Any]:
    common: dict[str, Any] = {
        "name": node.name,
        "in": [_serialize_port(p) for p in node.inports.values()],
        "out": [_serialize_port(p) for p in node.outports.values()],
    }
    if isinstance(node, Process):
        proc = cast(Process, node)
        return {
            **common,
            "type": "process",
            "exe": proc.exe,
            "args": _serialize_args(proc.args),
        }
    elif isinstance(node, Variable):
        var = cast(Variable, node)
        return {
            **common,
            "type": "var",
            "default": var.default,
        }
    else:
        raise ValueError(f"node is neither Variable nor Process: {node}")

def _serialize_link(link: Link) -> dict[str, Any]:
    return {
        "src": {"node": link.fromnode, "port": link.fromport},
        "dst": {"node": link.tonode, "port": link.toport},
    }

def _serialize_port(port: Port, name_only=False) -> dict[str, Any]:
    r = {"name": port.name}
    if not name_only:
        r["type"] = port.typ.value.lower()
    return r

def _serialize_args(args: list[Union[Port, str]]) -> list[Union[str, dict]]:
    result: list[Union[str, dict]] = []
    for arg in args:
        if isinstance(arg, Port):
            result.append(_serialize_port(arg, name_only=True))
        else:
            result.append(arg)
    return result