# Comparing Unix pipes vs. custom runtime

### Why Unix pipes with OS scheduler

Main concerns:
- Get the job done over performance (if it takes 10 minutes vs. 10 seconds is not as big a deal)
- Correctness by default (no segfaults, hard to debug errors, simple dataflow)
- Easy to use with existing programs and utilities (want to use AWS CLI)

Cons:
- A lot more work
- Limited to runtime's support and features
- No support for existing products and CLI tools

### Why custom runtime

Pros:
- Control over records for correctness (no worries about binary files not having correct line separators)
- Faster (maybe)
- Single static binary instead of complicated runtime dependencies
- Better cross platform support

Unix pipes are less work and provide more pros than cons. How to mitigate cons?

Mitigations:
- Records: Most data is text based, newline works 99% of the time (JSON lines)
- Deployment: Use docker