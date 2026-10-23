---
name: overwatch
description: "Audit every agent action for safety and correctness."
version: 0.1.0
author: dropstart01 (dropstart01), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [overwatch, monitoring, audit, safety, agent-behavior, observability]
    related_skills: [hermes-agent, ai-hedging, requesting-code-review]
---

# Overwatch: Monitor Every Agent Action

Overwatch is a standing audit layer that watches every tool call, file write, command execution, and state change the agent makes. It does not replace the agent's judgment — it observes, records, and flags actions that cross a boundary the user or policy defines.

## When to Use

- The user asks for an "overwatch," "monitor," or "watchdog" for the agent.
- A session involves destructive operations (file deletion, config changes, remote API calls, `rm -rf`, `git push --force`).
- The user wants a record of what the agent did, for review after the fact.
- The agent is running autonomously (cron, background, delegated) and the user wants to verify its actions post-hoc.
- A security audit requires an action log for the agent's session.

Don't use for: preventing the user from doing something they explicitly asked for. Overwatch observes and flags — it does not block unless the user configures a hard block list.

## Prerequisites

- `terminal` tool access for reading the action log.
- A writable `HERMES_HOME` for the audit log location. The log writes to `$HERMES_HOME/logs/overwatch.log` by default.

## How to Run

Overwatch runs as a post-hoc audit, not a live interceptor — the agent's tool loop does not pause for external review. The audit log captures every tool call the agent makes, and the user reviews it after the session or on demand.

To review the current session's actions:

Use `terminal(command="tail -50 ~/.hermes/logs/overwatch.log", timeout=10)` to see the most recent actions.

Use `terminal(command="grep 'DANGEROUS\\|BLOCKED\\|FLAGGED' ~/.hermes/logs/overwatch.log", timeout=10)` to see only flagged actions.

## Quick Reference

- View recent actions: `terminal(command="tail -N ~/.hermes/logs/overwatch.log", timeout=10)`
- Filter by severity: `terminal(command="grep 'FLAGGED\\|DANGEROUS' ~/.hermes/logs/overwatch.log", timeout=10)`
- Count by action type: `terminal(command="cut -d'|' -f2 ~/.hermes/logs/overwatch.log | sort | uniq -c | sort -rn", timeout=10)`
- Full audit dump: `terminal(command="cat ~/.hermes/logs/overwatch.log", timeout=60)`

## Procedure

1. **Start the session with overwatch active.** Before the agent begins work, load this skill so the agent knows its actions are being audited. The agent's tool calls are already logged by Hermes's gateway; overwatch adds a structured audit layer that classifies each action by risk level.

   Completion criterion: this skill is loaded and the agent is aware its actions are subject to audit.

2. **Classify each tool call by risk level.** As the agent executes, classify each action:

   | Risk level | Actions |
   |---|---|
   | SAFE | `read_file`, `search_files`, `web_search`, `web_extract`, `skills_list`, `skill_view` |
   | MODERATE | `write_file`, `patch`, `terminal` (read-only commands), `browser_exec` (navigation) |
   | DANGEROUS | `terminal` (destructive: `rm`, `kill`, `git push --force`, `chmod`, `chown`), `write_file` (overwriting config), `terminal` (background processes), `delegate_task` (spawning agents) |
   | BLOCKED | Actions matching the user's block list — the agent must not execute these |

   Completion criterion: every tool call the agent makes is classified into one of the four levels.

3. **Flag dangerous actions in the audit log.** For every DANGEROUS action, append a structured entry to `~/.hermes/logs/overwatch.log` with the timestamp, tool name, command or target, risk level, and a one-line justification. The agent writes this entry before executing the action.

   Use `terminal(command="echo '$(date -Iseconds)|DANGEROUS|<tool>|<target>|<justification>' >> ~/.hermes/logs/overwatch.log", timeout=5)` for each dangerous action.

   Completion criterion: every dangerous action has a log entry written before execution, with a justification the user can review.

4. **Record the outcome.** After executing a dangerous action, append the result (success/failure, exit code, files modified) to the same log entry.

   Completion criterion: each dangerous action's log entry includes the outcome, not just the intent.

5. **Review the audit on session end.** Before the session closes (or on user request), summarize the audit log: total actions, breakdown by risk level, any flagged actions and their justifications, and any actions that failed.

   Use `terminal(command="wc -l ~/.hermes/logs/overwatch.log && grep -c DANGEROUS ~/.hermes/logs/overwatch.log && grep -c BLOCKED ~/.hermes/logs/overwatch.log", timeout=10)` for the summary counts.

   Completion criterion: the user receives a summary with counts by risk level and a list of every dangerous action with its justification and outcome.

## Pitfalls

- **Overwatch is not a sandbox.** It observes and logs — it does not prevent the agent from executing actions. If the user needs a hard block on specific actions, they must configure `approvals.mode: manual` or use `security.redact_secrets` in the Hermes config. Overwatch complements these; it does not replace them.
- **Audit log growth.** The log appends indefinitely. For long-running sessions, rotate or truncate the log periodically — `terminal(command="truncate -s 0 ~/.hermes/logs/overwatch.log", timeout=5)` clears it.
- **False confidence from logging.** Writing a justification in the log does not make a dangerous action safe. The log is a record for review, not a permission slip. If an action is genuinely unsafe, the agent should not execute it regardless of whether it would log it.
- **Background processes are not audited.** Processes started with `terminal(background=true)` continue running after the session ends. Overwatch logs the start but cannot audit the ongoing execution. Use `process_manage(action='poll')` to check background process state.

## Verification

After applying this skill to a session:

1. Every tool call the agent made is classifiable by risk level (SAFE, MODERATE, DANGEROUS, BLOCKED).
2. Every DANGEROUS action has a log entry in `~/.hermes/logs/overwatch.log` with timestamp, tool, target, justification, and outcome.
3. No BLOCKED action was executed.
4. The session summary shows total actions, breakdown by risk level, and a list of every dangerous action with its justification.
5. The user can review the full audit log and find every action the agent took, in order, with enough detail to reproduce or revert it.
