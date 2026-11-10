"""Create a synthetic Git repository in a NEW destination, never the checkout."""
from pathlib import Path
import subprocess
import sys


def create(destination):
    destination = Path(destination).resolve()
    destination.mkdir(parents=True, exist_ok=False)

    def git(*args):
        return subprocess.run(
            ["git", "-C", str(destination), *args], check=True,
            capture_output=True, text=True,
        ).stdout

    git("init", "--quiet")
    git("config", "user.name", "Fixture Author")
    git("config", "user.email", "fixture@example.invalid")
    git("config", "commit.gpgsign", "false")
    (destination / "formatter.py").write_text(
        'def format_label(label, uppercase=False):\n'
        '    return label.upper() if uppercase else label.strip()\n'
    )
    (destination / "test_formatter.py").write_text(
        'import unittest\nfrom formatter import format_label\n\n'
        'class LabelTest(unittest.TestCase):\n'
        '    def test_default(self):\n'
        '        self.assertEqual("label", format_label(" label "))\n'
    )
    (destination / "README.md").write_text("Label formatting library.\n")
    git("add", "--", "formatter.py", "test_formatter.py", "README.md")
    git("-c", "core.hooksPath=/dev/null", "commit", "--quiet", "-m", "feat: add label formatter")
    (destination / "formatter.py").write_text(
        'def format_label(label):\n    return label.strip()\n'
    )
    git("add", "--", "formatter.py")
    (destination / "README.md").write_text("Label formatting library. Draft notes.\n")
    return destination


if __name__ == "__main__":
    print(create(sys.argv[1]))
