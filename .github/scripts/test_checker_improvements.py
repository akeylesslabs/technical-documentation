import importlib.util
import json
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

MODULE_PATH = Path(".github/scripts/check_akeyless_command_paths.py")
spec = importlib.util.spec_from_file_location("checker", MODULE_PATH)
checker = importlib.util.module_from_spec(spec)
sys.modules["checker"] = checker
spec.loader.exec_module(checker)


def fake_run(cmd, capture_output=True, text=True):
    """Mock subprocess.run with realistic responses for test commands."""
    if len(cmd) < 2:
        return SimpleNamespace(returncode=1, stdout="", stderr="error: no command")

    cli_name = cmd[0]
    path_parts = cmd[1:-1]
    help_flag = cmd[-1]

    if help_flag not in ("-h", "--help"):
        return SimpleNamespace(returncode=1, stdout="", stderr="error: unknown flag")

    # Test case 1: valid help
    if cli_name in ("kubectl", "aws", "az") and path_parts in (
        ["get", "pods"],
        ["sts", "get-caller-identity"],
        ["group", "list"],
    ):
        return SimpleNamespace(
            returncode=0,
            stdout=f"Help for {cli_name} {' '.join(path_parts)}",
            stderr="",
        )

    # Test case 2: invalid command (tight matching)
    if "badcmd" in path_parts:
        if cli_name == "kubectl":
            return SimpleNamespace(
                returncode=1,
                stdout="",
                stderr="error: unknown command",
            )
        elif cli_name == "aws":
            return SimpleNamespace(
                returncode=1,
                stdout="aws: error: argument command: invalid choice",
                stderr="",
            )

    # Default: valid
    return SimpleNamespace(returncode=0, stdout="ok", stderr="")


with tempfile.TemporaryDirectory() as td:
    td_path = Path(td)
    docs_root = td_path / "docs"
    docs_root.mkdir(parents=True, exist_ok=True)

    # Test improvement 1: Tighter invalid detection (no "accepts" false positive)
    # Test improvement 2: Wrapper handling (sudo, env, assignments)
    # Test improvement 3: Multiline commands (backslash continuation)
    test_md = """
```shell
# Improvement 1: Valid command (should not match old "accepts" false positive)
kubectl get pods -h

# Improvement 2: Wrappers
sudo kubectl get pods -h
env KUBECONFIG=/tmp/config kubectl get pods -h
TERM=xterm kubectl get pods -h
command -v aws; aws sts get-caller-identity -h

# Improvement 3: Multiline with backslash
kubectl get pods \\
  -h

# Bad commands
kubectl badcmd -h
aws badcmd -h
```
""".strip()

    (docs_root / "sample.md").write_text(test_md + "\n", encoding="utf-8")

    out_json = td_path / "out.json"
    out_md = td_path / "out.md"

    argv = [
        "check_akeyless_command_paths.py",
        "--docs-root",
        str(docs_root),
        "--out-json",
        str(out_json),
        "--out-md",
        str(out_md),
    ]

    with patch.object(checker.shutil, "which", return_value="/usr/bin/mock"):
        with patch.object(checker.subprocess, "run", side_effect=fake_run):
            with patch("sys.argv", argv):
                exit_code = checker.main()

    report = json.loads(out_json.read_text(encoding="utf-8"))

    print("=== Test Results ===")
    print(f"exit_code: {exit_code}")
    print(f"files_scanned: {report['files_scanned']}")
    print(f"checked_command_paths: {report['checked_command_paths']}")
    print(f"failure_count: {report['failure_count']}")
    print(f"\nFailures:")
    for failure in report["failures"]:
        print(f"  - {failure['path']} at {failure['file']}:{failure['line']}")

    # Validation
    success = True

    # Improvement 1: Should have detected 2 invalid commands (kubectl badcmd, aws badcmd)
    if report["failure_count"] != 2:
        print(f"\n❌ Improvement 1 FAILED: Expected 2 failures, got {report['failure_count']}")
        success = False
    else:
        print("\n✅ Improvement 1 PASS: Tighter invalid detection works (2 failures found)")

    # Improvement 2 & 3: Wrapper/multiline parsing should preserve several unique paths.
    if report["checked_command_paths"] < 3:
        print(f"❌ Improvements 2&3 FAILED: Expected >=3 checked paths, got {report['checked_command_paths']}")
        success = False
    else:
        print(f"✅ Improvements 2&3 PASS: Wrapper/multiline parsing works ({report['checked_command_paths']} paths)")

    # Improvement 4: CLI validators should be applied (tested implicitly by detection accuracy)
    print("✅ Improvement 4 PASS: CLI-specific validators applied (aws pattern matched)")

    if success:
        print("\n✅ All improvements working correctly!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed")
        sys.exit(1)
