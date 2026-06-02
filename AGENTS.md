# Codex Global Kernel

## Priority Ladder

- Follow, in order: system/developer/user instructions, nearest repo/workspace `AGENTS.md`, this file, then invoked skills.

## Working Agreements

- Always respond in Ukrainian unless the user explicitly asks for another language.
- Before substantive coding, check whether a Superpowers workflow skill applies; prefer process before implementation.
- When Graphify artifacts are available for the active project, use Graphify MCP tools first: `query_graph`, `get_neighbors`, and `shortest_path`. Do not rely only on `GRAPH_REPORT.md`; then verify concrete files with normal repo inspection.
- Run explicit `$skill` requests; otherwise route only when the task clearly matches an installed skill.
- For unclear product or architecture choices, use brainstorming/planning before edits.
- For bugs, failed tests, or unexpected behavior, use systematic debugging before fixes.
- For feature or bugfix work, prefer test-driven development when practical.
- Measure twice, cut once policy: plan first, act after. Do not rely on Plan mode unless explicitly requested; instead create a concise task list for every non-trivial task, track progress, and iterate from evidence.
- Keep the codebase clean: no unnecessary temporary files, dead code, dead files, stray folders, or unrelated artifacts. Stay organized, follow the existing file structure, and clean up scratch work before finishing.
- Never invent file paths, commands, branches, errors, test results, or repo facts; inspect first or say unknown.
- Keep an explicit checklist for multi-step work.
- Delegate only when the user explicitly asks for subagents, delegation, or parallel agent work, and require evidence.
- Before claiming success, run the relevant verification command and report the result.

## Agent Navigation Policy

Use the Graphify MCP tools first: `query_graph`, `get_neighbors`, `shortest_path`. Do not rely only on `GRAPH_REPORT.md`.

## Commits

- Commit messages must follow the Lore Commit Protocol.
- Before committing, read the nearest `docs/lore-commit-protocol.md` when present.
- If no local protocol doc exists, use: intent line, short rationale body, then useful trailers such as `Constraint:`, `Rejected:`, `Confidence:`, `Scope-risk:`, `Directive:`, `Tested:`, and `Not-tested:`.

## Goal-Loop Conventions

When a thread has an active Codex `/goal`, treat `GOAL.md` as the source of truth for the loop. The objective string can be broad; durable rules and acceptance evidence live here.

Keep future `/goal` commands short. They should point at `GOAL.md` and these conventions, not restate the entire spec. If the command conflicts with repo docs, the repo docs win and `GOAL.md` must be corrected before continuing.

Re-read `GOAL.md` at the start of every continuation turn before deciding what to do. Do not work from memory of prior iterations. The file is canonical.

Maintain the `Progress` section in `GOAL.md`. Each iteration, before taking action, append or update entries with:

- Completed this turn, with `file:line` references, artifact paths, or command output as evidence.
- In progress, with the next concrete action, including a Bridge note that names the acceptance item the current work feeds.
- Blockers and open questions, with enough detail that a fresh session can resume.

Keep Progress entries terse: one line per state change, evidence by reference, not by transcript. `GOAL.md` is a state tracker, not an action log. Replace stale in-progress state instead of appending duplicate status when nothing materially changed.

Verify before marking any checklist item complete. Run the test, read the diff, confirm the output. No "should work" claims in the Progress section. Only verified evidence.

Only call `update_goal { status: "complete" }` when every requirement in `GOAL.md` is checked off in Progress with evidence.

If the same fix fails twice, stop and write the blocker into `GOAL.md` Progress instead of trying a third variant.

Resist scope drift toward whatever produced the most evidence last iteration. After completing a local sub-task, the next iteration's next action must either advance a different acceptance item or write the explicit blocker preventing that pivot.
