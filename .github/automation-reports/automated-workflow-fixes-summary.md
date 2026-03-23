# Automated Workflow Fixes Summary

## Link Check
- 2396 replacements across Markdown files
- 0 links normalized across 0 markdown files
- 3 links checked, 0 broken

## Markdown Lint
- markdownlint found violations after --fix

## Spell Check
- 0 spelling issues found in Markdown files

## CLI Command Path Check
- Scanned 0 markdown files, checked 0 unique command paths, found 1 failures

## Top CSpell Findings


## Top CLI Command Path Failures
validator did not produce json output\nTraceback (most recent call last):
  File "/home/runner/work/technical-documentation/technical-documentation/.github/scripts/check_akeyless_command_paths.py", line 249, in <module>
    raise SystemExit(main())
                     ^^^^^^
  File "/home/runner/work/technical-documentation/technical-documentation/.github/scripts/check_akeyless_command_paths.py", line 204, in main
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
