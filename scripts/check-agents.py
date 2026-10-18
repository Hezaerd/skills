#!/usr/bin/env python3
"""Fail unless each Codex agent in plugins/hstack/codex/agents/*.toml matches
its Claude Code source in plugins/hstack/agents/*.md: same name, description
and prompt.
"""

import sys
import tomllib
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CLAUDE_DIR = REPO / "plugins" / "hstack" / "agents"
CODEX_DIR = REPO / "plugins" / "hstack" / "codex" / "agents"


def parse_markdown(path):
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    head, sep, body = text.removeprefix("---\n").partition("\n---\n")
    if not text.startswith("---\n") or not sep:
        sys.exit(f"{path}: missing YAML frontmatter")
    fields = {}
    for line in head.splitlines():
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip().strip("\"'")
    return fields, body.strip()


def main():
    errors = []
    claude = {p.stem: p for p in CLAUDE_DIR.glob("*.md")}
    codex = {p.stem: p for p in CODEX_DIR.glob("*.toml")}
    if claude.keys() != codex.keys():
        errors.append(f"agents differ: {sorted(claude)} in agents/ vs {sorted(codex)} in codex/agents/")

    for name in sorted(claude.keys() & codex.keys()):
        fields, body = parse_markdown(claude[name])
        toml = tomllib.loads(codex[name].read_text(encoding="utf-8"))
        for key in ("name", "description"):
            if fields.get(key) != toml.get(key):
                errors.append(f"{name}: `{key}` differs")
        if body != toml.get("developer_instructions", "").strip():
            errors.append(f"{name}: prompt differs from {claude[name].relative_to(REPO).as_posix()}")

    if errors:
        sys.exit("\n".join(errors))
    print(f"{len(claude)} agent(s) in sync")


if __name__ == "__main__":
    main()
