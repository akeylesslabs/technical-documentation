# Akeyless command-path check

- Files scanned: 0
- Command paths checked: 0
- Failures: 0

## Runtime error

```
Traceback (most recent call last):
  File "/home/runner/work/technical-documentation/technical-documentation/.github/scripts/check_akeyless_command_paths.py", line 219, in main
    if subprocess.run(["akeyless", "-h"], capture_output=True).returncode != 0:
       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/subprocess.py", line 548, in run
    with Popen(*popenargs, **kwargs) as process:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/subprocess.py", line 1026, in __init__
    self._execute_child(args, executable, preexec_fn, close_fds,
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/subprocess.py", line 1955, in _execute_child
    raise child_exception_type(errno_num, err_msg, err_filename)
FileNotFoundError: [Errno 2] No such file or directory: 'akeyless'
```

No invalid command paths found.
