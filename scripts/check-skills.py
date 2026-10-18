#!/usr/bin/env python3
"""Fail unless every hstack skill has a matching Codex agents/openai.yaml and no
pstack or Cursor leftovers survive in the plugin.

openai.yaml must carry the skill's name as display_name, its
metadata.short-description as short_description, and
policy.allow_implicit_invocation: false exactly when the skill sets
disable-model-invocation: true. Pass --write to regenerate the files instead.
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PLUGIN = REPO / "plugins" / "hstack"
SKILLS = PLUGIN / "skills"

# Each pattern names what replaces it, so the error says how to fix the line.
LEFTOVERS = [
    (r"poteto", "hez (hez-mode, hez-agent, hez-help)"),
    (r"pstack-models|~/\.cursor/rules", "the hstack model file, docs/delegation.md#pick-the-models"),
    (r"~/\.cursor|\.cursor/(skills|rules|plugins|automations|projects)", "the hstack path in docs/harness.md#paths"),
    (r"agent-transcripts", "T3 threads, docs/harness.md#transcripts"),
    (r"\bgeneralPurpose\b|\breadonly: (true|false)\b|run_in_background|cloud_base_branch|environment: \"(cloud|local)\"", "a pointer to docs/delegation.md"),
    (r"\bAskQuestion\b", "ask the user (docs/harness.md#tools)"),
    (r"\bTask (tool|call|spawn|subagent)s?\b|`Task`", "spawn a subagent per docs/delegation.md"),
    (r"\bgrok-\d|claude-opus-\d-\d-|composer-\d", "a T3 value such as codex/gpt-6.1-sol reasoningEffort=xhigh"),
    (r"[Ww]ithout T3 Code|T3 Code is absent|if T3 Code is (missing|not)", "nothing: hstack always runs in T3 Code"),
    (r"cursor-team-kit|\bdeslop\b|control-ui|control-cli", "T3 Code preview or device tools, or a terminal"),
    (r"\bOrigin\b|origin pr ", "gh"),
    (r"/setup-pstack|setup-pstack", "/hstack:setup-hstack"),
]


def frontmatter(path):
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    if not text.startswith("---\n"):
        sys.exit(f"{path}: missing YAML frontmatter")
    head = text[4:].split("\n---\n", 1)[0]
    fields, parent = {}, None
    for line in head.splitlines():
        if not line.strip():
            continue
        key, _, value = line.partition(":")
        value = value.strip()
        if line.startswith((" ", "\t")) and parent:
            fields[f"{parent}.{key.strip()}"] = unquote(value)
        else:
            parent = key.strip() if not value else None
            fields[key.strip()] = unquote(value)
    return fields


def unquote(value):
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1].replace('\\"', '"')
    return value


def expected_yaml(fields):
    lines = [
        "interface:",
        f'  display_name: "{fields["name"]}"',
        f'  short_description: "{fields["metadata.short-description"]}"',
    ]
    if fields.get("disable-model-invocation") == "true":
        lines += ["policy:", "  allow_implicit_invocation: false"]
    return "\n".join(lines) + "\n"


def main():
    write = "--write" in sys.argv[1:]
    errors = []
    skills = sorted(p.parent for p in SKILLS.glob("*/SKILL.md"))
    for skill in skills:
        rel = skill.relative_to(REPO).as_posix()
        fields = frontmatter(skill / "SKILL.md")
        if fields.get("name") != skill.name:
            errors.append(f"{rel}: name {fields.get('name')!r} differs from its folder")
            continue
        if not fields.get("metadata.short-description"):
            errors.append(f"{rel}: missing metadata.short-description")
            continue
        want = expected_yaml(fields)
        yaml_path = skill / "agents" / "openai.yaml"
        have = yaml_path.read_text(encoding="utf-8").replace("\r\n", "\n") if yaml_path.exists() else None
        if have != want:
            if write:
                yaml_path.parent.mkdir(exist_ok=True)
                yaml_path.write_text(want, encoding="utf-8", newline="\n")
            else:
                errors.append(f"{rel}/agents/openai.yaml: out of date, run python scripts/check-skills.py --write")

    for path in sorted(PLUGIN.rglob("*")):
        if path.suffix not in {".md", ".yaml", ".toml", ".json", ".tsv", ".sh"} or "node_modules" in path.parts:
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for pattern, fix in LEFTOVERS:
                if re.search(pattern, line):
                    errors.append(f"{path.relative_to(REPO).as_posix()}:{number}: pstack leftover /{pattern}/, use {fix}")

    if errors:
        sys.exit("\n".join(errors))
    print(f"{len(skills)} skill(s) in sync, no pstack leftovers")


if __name__ == "__main__":
    main()
