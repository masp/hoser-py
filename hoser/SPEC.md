# About

The hoser-py module takes a Python program describing a pipe and compiles it to the pipe JSON format that the hoser runtime accepts. The JSON file describes an acyclic graph where each vertex is an independent process and edges are queues of bytes connecting the processes (implementations can vary, but think Unix pipes).

# Pipe Format
The smallest pipe is a passthrough of one input and one output that looks like:

```
{
    "name": "main",
    "file": "example.py",
    "line": 32,
    "processes": [
        {"name": "start", "outports": [{"name": "stdin", "type": "stream"}]},
        {"name": "end", "inports": [{"name": "stdout", "type": "stream"}]}
    ],
    "connections": [
        {"from": {"proc": "start", "port": "stdin"}, "to": {"proc": "end", "port": "stdout"}}
    ]
}
```

This is very verbose, bug prone, and not fun to type, which is why hoser-py exists. There are always at least 2 "processes" one
representing the inputs to the root process and one representing the outputs to the root process. They are always named START and END.

Names in a pipe are unique and namespaced by the pipe name. Each port is also named and namespaced by the process it belongs to.
A full reference to a specific port is compactly written like `example/stdout[v]`.

A standard JSON pipe looks like:

```
{
    "name": "example",
    "vars": [
        {"name": "stdin", "type": "var", "out": [{"name":"o", "type": "stream"}]},
        {"name": "filter", "type": "var", "default": "cats", "out": [{"name":"o", "type": "string"}]},
        {"name": "stdout", "type": "var", "in": [{"name":"i", "type": "stream"}]}
    ],
    "procs": [
        {
            "name": "grep0",
            "type": "process",
            "exe": "grep",
            "args": ["-v", {"port": "filter"}],
            "in": [{"name": "stdin", "type": "stream"}, {"name": "filter", "type": "string"}],
            "out": [{"name": "stdout", "type": "stream"}]
        }
    ],
    "links": [
        {"from": {"node": "stdin", "port": "o"}, "to": {"node": "grep0", "port": "stdin"}},
        {"from": {"node": "filter", "port": "o"}, "to": {"node": "grep0", "port": "filter"}},
        {"from": {"node": "grep0", "port": "stdout"}, "to": {"node": "stdout", "port": "i"}}
    ]
}
```