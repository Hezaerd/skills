#!/usr/bin/env python3
"""Fail unless every manifest gives each plugin the same name and version.

Checks plugins/<name>/.claude-plugin/plugin.json, plugins/<name>/.codex-plugin/plugin.json,
and the plugin's entry in .claude-plugin/marketplace.json and .agents/plugins/marketplace.json.
"""

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def load(path):
    return json.loads((REPO / path).read_text(encoding="utf-8"))


def main():
    errors = []
    claude_market = {p["name"]: p for p in load(".claude-plugin/marketplace.json")["plugins"]}
    codex_market = {p["name"]: p for p in load(".agents/plugins/marketplace.json")["plugins"]}
    if claude_market.keys() != codex_market.keys():
        errors.append(f"marketplaces list different plugins: {sorted(claude_market)} vs {sorted(codex_market)}")

    for name, entry in claude_market.items():
        root = REPO / entry["source"]
        claude = load(root.relative_to(REPO) / ".claude-plugin/plugin.json")
        codex_path = root.relative_to(REPO) / ".codex-plugin/plugin.json"
        if not (REPO / codex_path).exists():
            errors.append(f"{name}: missing {codex_path.as_posix()}")
            continue
        codex = load(codex_path)
        versions = {
            ".claude-plugin/plugin.json": claude.get("version"),
            ".codex-plugin/plugin.json": codex.get("version"),
            "Claude marketplace entry": entry.get("version"),
        }
        if len(set(versions.values())) != 1:
            errors.append(f"{name}: versions differ: {versions}")
        if claude.get("name") != name or codex.get("name") != name:
            errors.append(f"{name}: manifest names differ: {claude.get('name')!r}, {codex.get('name')!r}")
        codex_entry = codex_market.get(name)
        if codex_entry and (REPO / codex_entry["source"]["path"]).resolve() != root.resolve():
            errors.append(f"{name}: marketplaces point at different folders")

    for error in errors:
        print(f"error: {error}", file=sys.stderr)
    if errors:
        sys.exit(1)
    print("manifests agree: " + ", ".join(f"{n} {e.get('version')}" for n, e in claude_market.items()))


if __name__ == "__main__":
    main()
