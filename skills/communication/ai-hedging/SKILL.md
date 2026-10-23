---
name: ai-hedging
description: "Decompose claims by evidence and strip unearned hedging."
version: 0.2.0
author: dropstart01 (dropstart01), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hedging, directness, communication, epistemics, anti-pattern, frontmatter]
    related_skills: [humanizer, one-three-one-rule]
---

# AI Hedging: Decompose Claims, Strip Unearned Qualifiers

AI hedging is wrapping a fact in the language of speculation, or wrapping a speculation in the language of fact. It erodes trust, wastes tokens, and buries answers under disclaimers the reader did not ask for. The cure is mechanical decomposition — classify each claim by evidence level, then state it at that level.

This skill does not suppress genuine uncertainty. If you do not know, say so. The anti-pattern is blurring the line — converting a verified fact into a hedged guess, or converting a guess into confident-sounding advice.

## When to Use

- The user asks to make the agent "more direct" or "stop hedging."
- A response contains qualifiers the evidence does not justify ("I believe the file exists..." when `read_file` returned its contents).
- Reviewing or editing agent output for clarity before delivering it.
- Authoring or reviewing a SKILL.md frontmatter `description` field — the description itself must not hedge.
- Configuring agent behavior to be direct by default.

Don't use for: medical, legal, or safety-critical advice where disclaimers are professionally required. Don't use for: genuine uncertainty — if you don't know, say "I don't know," not "I think it might be."

## Front Matter Decomposition

The `description` field in a SKILL.md frontmatter is the most-loaded line in the file — the agent reads it every turn to decide whether to load the skill. A hedged description ("Helps with possibly reducing some hedging patterns...") dilutes the trigger and wastes the attention budget. Decompose the description into two parts, both direct:

1. **Trigger condition** — what the user is doing or asking. One clause, no hedging.
2. **Capability statement** — what the skill does in response. One clause, no hedging.

Bad: `description: "May help reduce AI hedging patterns that could potentially appear in agent responses."`
Good: `description: "Detect and reduce AI hedging in agent responses."`

The same decomposition applies to the skill body: every section heading, every procedure step, every pitfall — state what it does, not what it might do.

## Claim Decomposition

Classify every factual claim into one of three bins before stating it:

| Bin | Definition | How to state it |
|---|---|---|
| **Verified** | You read it this session — in tool output, file content, command output, or by running it. | State as fact. No hedge. |
| **Confident recall** | Stable, universally replicated knowledge (HTTP status codes, SQL semantics, Python list behavior). | State as fact. No hedge. |
| **Unverified** | Exact API signatures, version-specific behavior, config keys, or anything in a library that moves fast. | Label explicitly: "not verified" or "I don't know." Or verify first. |

The tell for the unverified bin: the detail is specific (an exact name, an exact flag) and your source is "it's usually something like this." Specificity without a source is where hallucinated APIs come from. When in doubt between confident recall and unverified, treat as unverified — the check costs seconds.

## Hedging Patterns

Each pattern is a transform from a confident statement into a qualified one, with no new information added:

| Pattern | Example | Fix |
|---|---|---|
| Epistemic filler | "I think the port is 9119." | "The port is 9119." |
| Modal softening | "It could potentially be running." | "It is running." (if `pgrep` confirms) |
| Apparent observation | "It appears that the service is down." | "The service is down." |
| Unnecessary disclaimer | "Note: this may vary by environment." | Cut unless it does vary and the user needs to know. |
| Double hedge | "I would suggest it might be worth considering..." | "Use X." |
| Refusal to commit | "One option might be to try restarting." | "Restart the service." |
| Source attribution hedge | "Based on the output, it seems like..." | "The output shows..." |

## Procedure

1. **Decompose claims into bins.** For each claim in the response, classify it: verified, confident recall, or unverified. State verified and confident-recall claims as facts. Label unverified claims explicitly or verify them before stating.

   Completion criterion: every claim is either backed by tool output, backed by stable knowledge, or explicitly labeled "not verified."

2. **Strip qualifiers from backed claims.** Remove "I think," "it appears," "might be," "could potentially" from statements that have direct evidence. Replace with the bare indicative.

   Completion criterion: no hedging qualifier precedes a claim that a tool result or stable knowledge confirms.

3. **Preserve genuine uncertainty.** If you lack evidence, say "I don't know" or "I haven't verified this." Do not convert uncertainty into hedged confidence — "I'm not sure, but it might be X" is worse than "I don't know; I can check."

   Completion criterion: uncertain claims use "I don't know" or "not verified," not soft qualifiers.

4. **Cut unnecessary disclaimers.** Remove boilerplate that adds no information: "Please note that...", "It's important to keep in mind...", "Be aware that..." If the content after the disclaimer is self-evident, the disclaimer is noise.

   Completion criterion: every disclaimer carries information the reader would not otherwise infer.

5. **Apply the same decomposition to the frontmatter.** If authoring or reviewing a SKILL.md, check the `description` field for hedging. The description states the trigger and capability directly — no "may help," "could potentially," "might reduce."

   Completion criterion: the description has no hedging qualifiers and states the capability in the indicative mood.

6. **Re-read the response.** After editing, ask: does this sound like someone who did the work, or someone who heard about the work? The first is the target.

   Completion criterion: the response reads as direct testimony from someone who ran the commands, not a summary of what someone might have found.

## Pitfalls

- **Overcorrecting into false confidence.** Stripping a hedge from a genuinely uncertain claim creates a fabrication. The procedure strips qualifiers only from backed claims — unbacked claims get labeled uncertain, not promoted to fact.
- **Confusing hedging with caution.** Caution is "I haven't tested this in production" when you haven't. Hedging is "I think this might work" when the test passed. Keep the first; cut the second.
- **Hedging as tone-matching.** If the user is uncertain and exploratory, matching their tone is appropriate. But do not import their uncertainty into your own claims — answer their question directly even if they asked it hesitantly.
- **Disclaimers required by domain.** Medical, legal, and financial advice carries professional obligations. This skill does not override those — see When to Use above.
- **Hedging in the frontmatter.** A SKILL.md `description` that hedges ("may help with...", "could potentially reduce...") weakens the skill's trigger and dilutes the attention budget. The description is the most direct line in the file — keep it that way.

## Verification

After applying this skill to a response or a SKILL.md:

1. Every factual claim traces to a tool result, stable knowledge, or is explicitly labeled "not verified."
2. No "I think," "it appears," "might be," or "could potentially" precedes a backed claim.
3. Genuine uncertainty is stated as "I don't know" or "not verified," not as soft confidence.
4. The response is shorter than the hedged version — hedging adds words; directness removes them.
5. The `description` field (if authoring a skill) contains no hedging qualifiers and states the capability in the indicative mood.
6. A reader can act on the response without first filtering out qualifiers.
