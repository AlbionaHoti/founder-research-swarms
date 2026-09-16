# Founder Research Swarms

Ask the question once. Let ten agents answer it.

A research swarm splits one founder question into pieces, sends an agent after each piece, lets a skeptic try to kill every claim, and writes what survives into **one markdown file you own**.

You do not need a harness, a Python repo, or a vector database. You need a good question, one prompt, and a folder. This repo is the questions worth asking, the prompt to paste, the rule that keeps the pile of files useful, and a cron script so it runs while you are away from your laptop.

The same content as a one-page visual: open `index.html`.

## Four moves, every time

| | Move | What happens |
|---|---|---|
| A | **Split** | One question becomes 4 to 8 sub-questions that, answered together, answer the whole thing. |
| B | **Fan out** | One agent per sub-question. Primary sources only: docs, papers, founder posts, filings, forum threads. Every claim carries a URL and a quote. |
| C | **Attack** | A separate skeptic agent tries to refute every claim. Keep, revise, or drop. It may not skip a claim quietly. |
| D | **File** | One markdown file: surviving claims with sources, dropped claims with reasons, and a last section titled "What this cannot tell you." |

The skeptic is the part most people skip, and it is the part that makes the output worth acting on. One agent grading its own homework is a summary. Two agents disagreeing on the record is research.

## Before you build

Replace the bracketed parts.

| Stage | Ask the swarm | Paste this |
|---|---|---|
| **Idea** (demand exists?) | Who already pays to make this pain go away, and with what? | Find every way people currently solve **[pain]** without a dedicated product: spreadsheets, freelancers, consultants, Notion templates, Reddit workarounds. For each: what it costs them in money or hours, and a link to one person complaining about it. Rank by money already being spent. |
| **Customer** (their words) | Where do my first 100 users already gather, and what exact words do they use? | List 15 places where **[ICP]** talk about **[pain]**: subreddits, Discords, Slack groups, newsletters, YouTube channels. For each: size, a verbatim quote of someone describing the pain, and the phrase they use for it. Their words, not mine. |
| **Graveyard** (who died of what) | What did the last five companies that tried this die of? | Find 5 dead or stalled products in **[space]** from the last 8 years. For each: what they built, who funded them, their last public update, and the most credible post-mortem. Then name the one cause that repeats. |
| **Build** (can one person?) | Can this be built solo with today's APIs, and what breaks first? | For **[core feature]**, list the APIs, models, and libraries that do it today: pricing, rate limits, and the terms-of-service clause that could shut me down. Then name the single dependency I would be most exposed to. |

Why these four: money already moving is the only demand signal you can trust before a product exists; your landing page is already written in your users' quotes; graveyards teach faster than unicorns; and you want to know who can pull the plug before you build on them.

## Before you sell

| Stage | Ask the swarm | Paste this |
|---|---|---|
| **Positioning** (unclaimed slot) | What can I say that nobody else in the category can? | Pull the hero headline and first three claims from the 10 most visited **[category]** sites. Put them in one table. Mark every claim that all of them make. What is left unclaimed is where I stand. |
| **Pricing** (existing budget line) | What do they already pay for the thing next to mine? | For **[ICP]**, list the tools and services they pay for that sit next to **[product]**: name, price, billing model, and one public complaint about the price. Show me which budget line already exists. |
| **Distribution** (channel with proof) | Which channel actually grew a product like mine, with numbers? | Find 5 products with a similar buyer and price to **[product]** that reached 1,000 paying customers. For each: the first channel that worked, the evidence (founder post, interview, public metric), and whether it kept working. Flag founder-claimed vs third-party numbers. |
| **Fundraising** (who wrote the check) | Who funded this exact category recently, and what did they say about why? | List investors who led pre-seed or seed rounds in **[category]** in the last 18 months. For each: fund, partner, company, round size if public, and one quote from the partner on why. Skip anyone with no investment in the category in that window. |

## Files, not chats

> "It's 2026 and unbelievable power is in an open github repo with a few markdown files."
> Garry Tan, [X, 2026](https://x.com/garrytan/status/2032507955606860160). His own setup, [GBrain](https://github.com/garrytan/gbrain), calls the git repo "the system of record": every memory is a markdown file.

A swarm that ends in a chat window is gone tomorrow. A swarm that ends in a file compounds. The pile never stops growing, so these rules are about keeping the **index** short while the pile gets long.

```
research/
  INDEX.md                                  one line per brief, the only file you reread
  QUEUE.md                                  questions waiting for the cron job
  TEMPLATE.md                               frontmatter + the three sections every brief has
  2026-08-23-who-pays-to-fix-onboarding.md
  2026-08-24-graveyard-speaking-apps.md
  2026-09-02-who-pays-to-fix-onboarding.md  re-run, supersedes the 08-23 file
```

| Rule | Do this | Looks like |
|---|---|---|
| One question, one file | Name the file by date and question. Never `notes.md`. | `2026-08-23-who-pays-to-fix-onboarding.md` |
| Frontmatter carries the verdict | Question, date, confidence, status, source count. You scan frontmatter, not bodies. | `confidence: medium` / `status: fresh` / `sources: 14` |
| Last section is the gap | Every brief ends with what it could not check. A brief without gaps is a brief that did not look. | `## What this cannot tell you` |
| Re-run, don't rewrite | When a brief goes stale, ask the same question again. New file, old one marked superseded. History stays. | `status: superseded` / `superseded_by: 2026-09-02-...md` |
| Decisions go in the file | When you act on a brief, write the decision into its frontmatter. This turns a research pile into a log of what you decided and why. | `decision: killed the consumer angle, see graveyard brief` |

## Your first run

Paste `PROMPT.md` into Claude Code from this folder, with the first line swapped for a question from the tables above:

```
Research question: [one question from this page]

1. Split it into 5 sub-questions that, answered together, answer the whole thing. Show me the split before you continue.
2. For each sub-question, spawn one read-only subagent. Primary sources only: docs, papers, founder posts, filings, forum threads. Return claims as bullets, each with a URL and a direct quote.
3. Spawn one skeptic subagent. For every claim, try to refute it. Verdict per claim: keep / revise / drop, plus what you checked. You may not skip a claim.
4. Write research/YYYY-MM-DD-<slug>.md with frontmatter (question, date, confidence, status: fresh, sources), surviving claims with sources, dropped claims with reasons, and a final section "What this cannot tell you".
5. Append one line to research/INDEX.md: date, question, confidence, file.
```

Without Claude Code or Codex: open four chat tabs, give each one sub-question, paste the answers into a fifth tab and ask it to refute them. Save the result as a file. Same shape, more copy-paste.

## Run it while you're away

The interesting version of this is not you typing prompts. It is a queue of questions and a cron job that answers one per night. You write a question on the train. A file is waiting in the morning.

1. Add a line to `research/QUEUE.md`: `- [ ] Who already pays to fix onboarding for 5-person agencies?`
2. `crontab -e` and add:
   ```
   0 2 * * *  cd ~/founder-research-swarms && ./scripts/nightly-swarm.sh >> logs/nightly.log 2>&1
   ```
3. `scripts/nightly-swarm.sh` takes the first unchecked line, runs `PROMPT.md` through `claude -p` with subagents allowed, writes the brief, and ticks the line with the file path.

Three things change when research runs on a schedule. You stop asking questions you can answer in one search, because the queue makes you pick. The pile grows on its own, which is why the index rules matter. And your phone becomes the input: a queue line is a sentence, and a sentence is all the job needs.

## Going deeper

The one-prompt method above is enough for most questions. When being wrong is expensive, there is a heavier version with the same four moves and stricter contracts:

- `PROMPT-DEEP.md`: paste-ready. Adds an effort table (1, 2 to 4, or 5 to 8 researchers by question type), a JSON claim contract with period, geography, platform and date on every number, a `dead_ends` list so "nobody does this" carries the queries tried, a mechanical link check before any skeptic runs, question-typed evaluators (definitive, freshness, plurality, completeness, strict), a synthesizer with no web tools, and a citation pass that marks any sentence with no claim behind it.
- `docs/METHOD.md`: the full skeleton. Principles, roles, stages, contracts, decision gates, a freshness table by claim type, the run folder, a close-out checklist, and the failure modes each rule exists to stop.
- `docs/INSPIRATIONS.md`: the open-source deep-research systems this borrows from, with stars, dates, and the one mechanism taken from each.
- `scripts/linkcheck.py` and `scripts/archive.py`: the two mechanical steps. HEAD-check every source URL, and save every fetched page into `knowledge/` so the next run starts local.
- `research/TEMPLATE-DEEP.md`: frontmatter that carries the outcome line (researchers, skeptics, claims kept, revised, dropped, grounding score).

Run it on a schedule with `PROMPT_FILE=PROMPT-DEEP.md ./scripts/nightly-swarm.sh`.

## Questions people ask

**Do I need to code?** No. Claude Code or Codex can spawn the agents for you. Without either, four chat tabs and one skeptic tab.

**How is this different from the deep research button?** One agent, one pass, grading itself. A swarm splits the question, lets a second agent attack the answers, and writes to your folder instead of a chat you will never find again.

**How many sub-questions?** 4 to 8. Past 8 the agents start repeating each other.

**What if the skeptic drops half the claims?** Good. The half that survives is what you act on. The half that died is the list of things you almost believed.

**When should I not do this?** When the answer is one search away, or when it lives inside a customer's head. Nothing here replaces talking to five users.

**Can I do this with a full-time job?** Yes. Write the question in the morning, read one file at night. The swarm does not need you in the room.
