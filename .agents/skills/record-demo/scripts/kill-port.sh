#!/usr/bin/env bash
# Stops whatever listens on a TCP port. Safer than `pkill -f <pattern>`, which also matches
# the shell running it whenever the pattern appears in the command line.
# Usage: kill-port.sh <port>
set -euo pipefail

pids=$(ss -ltnpH "sport = :$1" | grep -o 'pid=[0-9]*' | cut -d= -f2 | sort -u)
[ -n "$pids" ] || exit 0
kill $pids
for _ in $(seq 1 20); do
  ss -ltnH "sport = :$1" | grep -q . || exit 0
  sleep 0.25
done
kill -9 $pids 2>/dev/null || true
