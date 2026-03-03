import pathlib
import re
import sys


ROOT = pathlib.Path("docs/Integrations & Plugins/cli-reference")
HEADING_PATTERN = re.compile(r"^(#{3,5})\s+`([^`]+)`\s*$")


def main() -> int:
    violations = []

    for file_path in sorted(ROOT.rglob("*.md")):
        lines = file_path.read_text(encoding="utf-8").splitlines()
        for line_number, line in enumerate(lines, start=1):
            match = HEADING_PATTERN.match(line)
            if not match:
                continue

            heading_value = match.group(2)
            if any(char.isupper() for char in heading_value):
                violations.append((file_path.as_posix(), line_number, heading_value))

    if not violations:
        print("CLI command heading case check passed.")
        return 0

    print("Found capitalized CLI command headings (must be lowercase):")
    for path, line_number, heading_value in violations:
        print(f"- {path}:{line_number} -> `{heading_value}`")

    return 1


if __name__ == "__main__":
    sys.exit(main())
