#!/usr/bin/env python3
"""Install the agents in agents/*.md for Claude Code and Codex.

Each source file is a Claude Code subagent: YAML frontmatter, then the
system prompt. Claude Code gets a copy. Codex gets a TOML file with the
same name, description and prompt.

Frontmatter keys starting with `codex-` apply to Codex only:
`codex-model` and `codex-reasoning-effort`. Claude Code keys such as
`tools` and `model` are left out of the Codex file.

Usage:
  python scripts/sync-agents.py              # install for both
  python scripts/sync-agents.py --dry-run    # print what would be written
  python scripts/sync-agents.py --claude-dir .claude/agents --codex-dir .codex/agents
"""

import argparse
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SOURCE_DIR = REPO / "agents"
CODEX_KEYS = {
    "codex-model": "model",
    "codex-reasoning-effort": "model_reasoning_effort",
}


def parse(path):
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    if not text.startswith("---\n"):
        sys.exit(f"{path}: missing YAML frontmatter")
    head, sep, body = text[4:].partition("\n---\n")
    if not sep:
        sys.exit(f"{path}: unterminated YAML frontmatter")
    fields = {}
    for line in head.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, colon, value = line.partition(":")
        if not colon or line[0].isspace():
            sys.exit(f"{path}: only flat `key: value` frontmatter is supported")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        fields[key.strip()] = value
    for key in ("name", "description"):
        if not fields.get(key):
            sys.exit(f"{path}: frontmatter needs `{key}`")
    return fields, body.lstrip("\n")


def toml_string(value):
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def claude_file(fields, body):
    lines = [f"{k}: {v}" for k, v in fields.items() if not k.startswith("codex-")]
    return "---\n" + "\n".join(lines) + "\n---\n\n" + body


def codex_file(fields, body, source):
    out = [
        f"# Generated from {source} by scripts/sync-agents.py. Edit the source instead.",
        f"name = {toml_string(fields['name'])}",
        f"description = {toml_string(fields['description'])}",
    ]
    for key, codex_key in CODEX_KEYS.items():
        if fields.get(key):
            out.append(f"{codex_key} = {toml_string(fields[key])}")
    if "'''" in body:
        sys.exit(f"{source}: body contains ''' and can't be a TOML literal string")
    out.append(f"developer_instructions = '''\n{body.rstrip()}\n'''")
    return "\n".join(out) + "\n"


def write(path, content, dry_run):
    if dry_run:
        print(f"--- {path}\n{content}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    print(f"wrote {path}")


def main():
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--claude-dir", type=Path, default=Path.home() / ".claude" / "agents")
    parser.add_argument("--codex-dir", type=Path, default=codex_home / "agents")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    sources = sorted(SOURCE_DIR.glob("*.md"))
    if not sources:
        sys.exit(f"no agents in {SOURCE_DIR}")
    for source in sources:
        fields, body = parse(source)
        name = fields["name"]
        rel = source.relative_to(REPO).as_posix()
        write(args.claude_dir / f"{name}.md", claude_file(fields, body), args.dry_run)
        write(args.codex_dir / f"{name}.toml", codex_file(fields, body, rel), args.dry_run)


if __name__ == "__main__":
    main()
