# skills

Personal agent skills for Claude Code, Codex and other agents that read `SKILL.md`.

| Skill | What it does |
| --- | --- |
| `bro` | Restates the last message in plain language, with no jargon. |
| `unslop` | Cuts AI tells from any writing. |

## Install

With the [skills CLI](https://www.skills.sh/):

```bash
npx skills add hezaerd/skills -g
```

Or clone and symlink into each agent:

```bash
git clone https://github.com/hezaerd/skills ~/skills
for s in ~/skills/.agents/skills/*/; do
  n=$(basename "$s")
  ln -sfn "$s" ~/.claude/skills/$n
  ln -sfn "$s" ~/.agents/skills/$n
done
```
