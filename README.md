# skills

Personal [Cursor Agent Skills](https://cursor.com/docs) used across projects.

## Install

Clone this repo into your Cursor personal skills directory:

```bash
git clone https://github.com/Hezaerd/skills.git ~/.cursor/skills
```

If `~/.cursor/skills` already exists, clone elsewhere and symlink individual skills:

```bash
git clone https://github.com/Hezaerd/skills.git ~/Developer/skills
mkdir -p ~/.cursor/skills
ln -s ~/Developer/skills/conventional-commits ~/.cursor/skills/conventional-commits
```

Update later with:

```bash
cd ~/.cursor/skills && git pull
# or, if you cloned to ~/Developer/skills:
cd ~/Developer/skills && git pull
```

## Skills

| Skill | When it runs |
| ----- | ------------ |
| [`conventional-commits`](./conventional-commits/) | Commit / commit-message requests (agent-invoked) |

## Force auto-use on commit

Skills are discovered from their `description`. To make commits reliably load
`conventional-commits`, add a **User Rule** in Cursor Settings:

> Whenever I ask to commit, create a commit, or write/fix a commit message:
> read and follow the `conventional-commits` skill first, then run the normal
> git commit safety protocol.

## Agent invocation

These skills omit `disable-model-invocation`, so the agent can load them from
context (not only via `/skill-name`). Keep descriptions specific: include both
**what** the skill does and **when** to use it.
