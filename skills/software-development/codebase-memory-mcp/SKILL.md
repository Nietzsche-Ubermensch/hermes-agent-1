---
name: codebase-memory-mcp
description: "Use when indexing, querying, or managing the codebase-memory-mcp MCP server for AI coding agents. Covers installation, project indexing, graph queries, and MCP integration."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [mcp, code-intelligence, tree-sitter, knowledge-graph, lsp, indexing]
    related_skills: [hermes-agent, plan, spike]
---

# Codebase Memory MCP

## Overview

[codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp) is a pure-C code intelligence engine that builds a persistent knowledge graph from your codebase using tree-sitter AST parsing across 158 languages, enhanced with Hybrid LSP semantic type resolution for 9 major languages. It exposes 14 MCP tools for structural queries (search, trace, architecture, impact analysis, Cypher, dead code detection, cross-service HTTP linking, ADR management) and ships as a single static binary with zero dependencies.

This skill covers installation, project indexing, MCP server management, and common query patterns for AI-assisted development.

## When to Use

- Setting up codebase-memory-mcp for a new project
- Indexing a repository (first time or incremental)
- Querying the knowledge graph via MCP tools
- Configuring MCP integration with coding agents (Claude Code, OpenCode, etc.)
- Troubleshooting indexing or query issues
- Managing the graph visualization UI

Don't use for: general code search without the MCP server (use grep/rg), or when the codebase is too small to benefit from graph queries.

## Quick Start

### Install

```bash
# One-liner (standard variant)
curl -fsSL https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh | bash

# With graph visualization UI
curl -fsSL https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh | bash -s -- --ui

# From local build (after cloning)
cd /path/to/codebase-memory-mcp
make -f Makefile.cbm cbm
./build/c/codebase-memory-mcp install
```

### First Index

```bash
cd /path/to/your/project
codebase-memory-mcp
# Say "Index this project" to your coding agent
```

The MCP server runs on stdio. Your agent connects automatically via the installed configuration.

### Verify Installation

```bash
codebase-memory-mcp --version
# codebase-memory-mcp dev (or version tag)
```

## MCP Tools Reference

| Tool | Purpose |
|------|---------|
| `index_repository` | Full or incremental index of a project |
| `search_graph` | Structural search across the knowledge graph |
| `query_graph` | Cypher queries against the graph |
| `trace_path` | Trace call chains and data flow |
| `get_code_snippet` | Extract code for a symbol |
| `get_graph_schema` | Inspect graph node/edge types |
| `get_architecture` | High-level architecture overview |
| `search_code` | Text search with AST context |
| `list_projects` | List indexed projects |
| `delete_project` | Remove a project from the graph |
| `index_status` | Check indexing progress |
| `detect_changes` | Detect file changes for incremental index |
| `manage_adr` | Architecture Decision Records |
| `ingest_traces` | Import runtime traces |

## Common Workflows

### Index a New Project

```bash
cd /path/to/project
codebase-memory-mcp
# In agent: "Index this project"
```

### Incremental Re-index

```bash
cd /path/to/project
codebase-memory-mcp
# In agent: "Re-index changed files"
# Or use detect_changes tool
```

### Query Architecture

```bash
# In agent: "Show me the architecture of this project"
# Uses get_architecture tool
```

### Find Call Chains

```bash
# In agent: "Trace the call path from main() to database connect"
# Uses trace_path tool
```

### Search for Patterns

```bash
# In agent: "Find all HTTP route handlers"
# Uses search_graph with node type filter
```

### Run Cypher Query

```bash
# In agent: "Show all functions that call redisClient.get"
# Uses query_graph tool
```

## Graph Visualization UI

If installed with `--ui`:

```bash
codebase-memory-mcp --ui=true
# Opens http://localhost:9749
```

3D interactive graph showing:
- Files, functions, classes as nodes
- Calls, imports, inheritance as edges
- Filter by language, directory, node type
- Click to explore code snippets

## Configuration

The binary stores config in `~/.config/codebase-memory-mcp/config.json`:

```json
{
  "projects": [{"path": "/home/user/project", "name": "my-project"}],
  "ui": {"enabled": false, "port": 9749},
  "indexing": {"parallelism": 4, "batch_size": 1000}
}
```

Override with env vars:
- `CBM_CONFIG_DIR` — config directory
- `CBM_LOG_LEVEL` — debug, info, warn, error

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| "No projects indexed" | Run `index_repository` first |
| Slow indexing | Increase `parallelism`, exclude `node_modules`, `target`, `.git` |
| MCP connection failed | Restart agent; check `~/.claude/.mcp.json` or equivalent |
| UI won't start | Check port 9749 free; try `--port=9750` |
| Binary not found | Re-run `install.sh` or add `~/.local/bin` to PATH |

## Updating

```bash
# Via installer (fetches latest release)
curl -fsSL https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh | bash

# From source
cd /path/to/codebase-memory-mcp
git pull
make -f Makefile.cbm cbm
./build/c/codebase-memory-mcp install
```

## Uninstall

```bash
codebase-memory-mcp uninstall
# Removes binary, agent configs, hooks, PATH entry
```

## Common Pitfalls

1. **Forgetting to restart the agent after install** — MCP configs are read at agent startup. Restart or `/reset`.
2. **Indexing huge repos without exclusions** — Add `.cbmignore` or configure exclusions; `node_modules`, `target`, `dist`, `.git` slow things down.
3. **Running multiple MCP servers on same stdio** — Each agent gets its own server instance; don't run manually in parallel.
4. **Expecting instant results on cold start** — First index of large repos (Linux kernel) takes ~3 min. Subsequent incremental indexes are seconds.
5. **Using wrong tool for the question** — `search_graph` for structural queries, `search_code` for text+AST, `query_graph` for complex Cypher.

## Verification Checklist

- [ ] Binary installed at `~/.local/bin/codebase-memory-mcp`
- [ ] `codebase-memory-mcp --version` prints version
- [ ] Agent config updated (Claude Code: `~/.claude/.mcp.json`, OpenCode: `~/.config/opencode/opencode.json`)
- [ ] PATH includes `~/.local/bin` (restart shell)
- [ ] Project indexed successfully (`index_status` shows complete)
- [ ] Test query works: "Show architecture of this project"

## One-Shot Recipes

### Index and Query in One Session

```bash
cd /path/to/project
codebase-memory-mcp install --skip-config  # if not installed
codebase-memory-mcp
# Agent: "Index this project, then show me all database-related functions"
```

### Compare Two Approaches (Spike)

```bash
# Spike: compare codebase-memory-mcp vs. ctags for navigation
mkdir -p spikes/001-cbm-vs-ctags
cd spikes/001-cbm-vs-ctags
# Build spike for each, run head-to-head
```

### CI Integration

```yaml
# .github/workflows/cbm-index.yml
- uses: actions/checkout@v4
- run: curl -fsSL ... | bash -s -- --skip-config
- run: codebase-memory-mcp cli index_repository '{"path": "."}'
```

## Reference

- Repository: https://github.com/DeusData/codebase-memory-mcp
- Research paper: https://arxiv.org/abs/2603.27277
- Release binaries: https://github.com/DeusData/codebase-memory-mcp/releases
- Graph UI screenshot: `docs/graph-ui-screenshot.png` in repo