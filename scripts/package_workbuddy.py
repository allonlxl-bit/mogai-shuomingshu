"""Build the WorkBuddy upload from the same sources used by Codex."""
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "task-first-manual"
OUTPUT = ROOT / "docs" / "task-first-manual.zip"


def main():
    files = [(SKILL / "SKILL.md", "SKILL.md"), (ROOT / "LICENSE", "LICENSE")]
    for directory, pattern in (("references", "*.md"), ("scripts", "*.py")):
        for source in sorted((SKILL / directory).rglob(pattern)):
            files.append((source, source.relative_to(SKILL).as_posix()))

    with ZipFile(OUTPUT, "w") as archive:
        for source, name in files:
            entry = ZipInfo(name)
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, source.read_bytes(), compress_type=ZIP_DEFLATED)


if __name__ == "__main__":
    main()
