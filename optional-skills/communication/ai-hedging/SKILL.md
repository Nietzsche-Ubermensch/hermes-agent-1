---
name: ai-hedging
description: "Detect and reduce AI hedging in agent responses."
version: 0.1.0
author: dropstart01 (dropstart01), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hedging, directness, communication, epistemics, anti-pattern]
    related_skills: [humanizer, one-three-one-rule]
---

# AI Hedging: Replace Qualification with Directness

AI hedging is the pattern of qualifying statements the agent has sufficient evidence to make plainly. It sounds like "I think this might be..." when the tool output says it is. Hedging erodes trust, wastes tokens, and buries the answer under disclaimers the reader did not ask for.

This skill does not suppress genuine uncertainty. If you do not know, say so. The anti-pattern is blurring the line — wrapping a fact in the language of speculation, or wrapping a speculation in the language of fact.

## When to Use

- The user asks to make the agent "more direct" or "stop hedging."
- A response contains qualifiers the evidence does not justify ("I believe the file exists..." when `read_file` returned its contents).
- Reviewing or editing agent output for clarity before delivering it.
- Configuring agent behavior to be direct by default.

Don't use for: medical, legal, or safety-critical advice where disclaimers are professionally required. Don't use for: genuine uncertainty — if you don't know, say "I don't know," not "I think it might be."

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

1. **Identify the evidence level.** For each claim, check: does a tool result, file content, or command output support it directly? If yes, the claim is a fact — state it as one. If not, the claim is speculation — label it as such or omit it.

   Completion criterion: every claim in the response is either backed by tool output or explicitly labeled as uncertain.

2. **Strip qualifiers from backed claims.** Remove "I think," "it appears," "might be," "could potentially" from statements that have direct evidence. Replace with the bare indicative.

   Completion criterion: no hedging qualifier precedes a claim that a tool result confirms.

3. **Preserve genuine uncertainty.** If you lack evidence, say "I don't know" or "I haven't verified this." Do not convert uncertainty into hedged confidence — "I'm not sure, but it might be X" is worse than "I don't know; I can check."

   Completion criterion: uncertain claims use "I don't know" or "not verified," not soft qualifiers.

4. **Cut unnecessary disclaimers.** Remove boilerplate that adds no information: "Please note that...", "It's important to keep in mind...", "Be aware that..." If the content after the disclaimer is self-evident, the disclaimer is noise.

   Completion criterion: every disclaimer carries information the reader would not otherwise infer.

5. **Re-read the response.** After editing, ask: does this sound like someone who did the work, or someone who heard about the work? The first is the target.

   Completion criterion: the response reads as direct testimony from someone who ran the commands, not a summary of what someone might have found.

## Pitfalls

- **Overcorrecting into false confidence.** Stripping a hedge from a genuinely uncertain claim creates a fabrication. The procedure strips qualifiers only from backed claims — unbacked claims get labeled uncertain, not promoted to fact.
- **Confusing hedging with caution.** Caution is "I haven't tested this in production" when you haven't. Hedging is "I think this might work" when the test passed. Keep the first; cut the second.
- **Hedging as tone-matching.** If the user is uncertain and exploratory, matching their tone is appropriate. But do not import their uncertainty into your own claims — answer their question directly even if they asked it hesitantly.
- **Disclaimers required by domain.** Medical, legal, and financial advice carries professional obligations. This skill does not override those — see When to Use above.

## Verification

After applying this skill to a response:

1. Every factual claim traces to a tool result, file read, or command output — or is explicitly labeled "not verified."
2. No "I think," "it appears," "might be," or "could potentially" precedes a backed claim.
3. Genuine uncertainty is stated as "I don't know" or "not verified," not as soft confidence.
4. The response is shorter than the hedged version — hedging adds words; directness removes them.
5. A reader can act on the response without first filtering out qualifiers.
