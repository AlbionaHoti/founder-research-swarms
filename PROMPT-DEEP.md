Research question: [one question; see README for the eight worth asking]
Effort: [fact = 1 researcher · comparison = 2 to 4 · open market question = 5 to 8]

Rules for every agent: primary sources only (docs, papers, filings, regulator pages, the product's own store or pricing page, a developer's own postmortem). Every number carries period, geography, platform and source date, or goes in "unverified". A "nobody does X" claim must list the 3 to 5 query phrasings tried. Unknown is an acceptable answer. Subagents are read-only; you write every file.

1. Decompose. Run the eight dimensions over the question (historical, current, future, stakeholders, quantitative, qualitative, comparative, risk) and split it into 3 to 8 facets, each a question, independently researchable. Mark any facet that depends on another. Fix the candidate set now (buyers, products, forms); nobody adds candidates later. Show me the facets before you continue.

2. Research. Spawn one read-only researcher per facet, all at once. Each prompt carries: the facet verbatim, the overall question, the recency window, local-first (read research/INDEX.md and knowledge/INDEX.md before the web), and the boundaries (what belongs to other facets). Start wide, then narrow. Expand each query into 4 to 6 phrasings before trusting an absence. Open pages; a snippet is not a source. Stop when the facet can be answered confidently or the last two searches returned the same material. Each researcher returns ONLY this JSON:

{ "facet": "<verbatim>",
  "claims": [ { "claim": "<one falsifiable sentence with number and date>", "source_url": "", "source_title": "", "source_date": "YYYY-MM-DD", "period": "", "geography": "", "platform": "", "quote_or_number": "", "quality": "T1|T2|memory", "confidence": "low|medium|high", "load_bearing": true, "retrieval": "local|web|fetched_page|search_snippet" } ],
  "dead_ends": [ { "finding": "", "queries_tried": ["", "", ""] } ],
  "unverified": [], "gaps": [], "surprises": [],
  "clarification_needed": "" }

Write each to research/runs/YYYY-MM-DD-<slug>/researchers/F<n>.json.

3. Link check. Run `python3 scripts/linkcheck.py research/runs/YYYY-MM-DD-<slug>/researchers/*.json`. Any claim whose source is MISSING is now "unverified" and the skeptic is told so.

4. Verify. Spawn one skeptic per facet, as each facet lands. The skeptic is the opposition. Per claim: open the exact cited URL (not a search summary of it); run at least one disconfirming search; check for overclaim (one study → "research shows"; one review → "players"); treat "memory" claims as guilty until grounded; give load-bearing claims three votes (source says this / current and period-consistent / applies to this segment), keep if two survive; then the evaluators by claim type: definitive, freshness (ad counts 7 days, prices 30, policy pages 90, surveys until superseded with the year stated, papers no limit but name follow-ups), plurality, completeness, strict (argue against the claim with the strongest case, then for). Never omit a claim. Each skeptic returns ONLY this JSON:

{ "facet": "<verbatim>",
  "verdicts": [ { "claim_index": 1, "verdict": "keep|revise|drop", "revised_claim": "", "checks_performed": [], "headline_vs_honest": "", "reason": "" } ],
  "unchecked": [], "grounding_score": 0, "prompt_tweak": "" }

Write each to research/runs/YYYY-MM-DD-<slug>/skeptics/F<n>.json.

5. Synthesize. Spawn one synthesizer with NO web tools. Give it the question, every researcher JSON and every skeptic JSON. Only keep and revise claims enter the brief, in the revised wording. Disagreement is its own section. It may not shorten "What this cannot tell you". It returns markdown in this shape:

# Brief: <question>
## Answer in three sentences
## What we know (by theme, not by facet)
## Dossiers (one per candidate: headline vs honest, verdict, confidence, skeptic critique, sources)
## Where sources disagree
## What this cannot tell you (every gap, unverified, unchecked and dead end)
## Surprises
## Killed in review (claim → skeptic reason)
## Market-structure block (what 5x capital could lock, which power is forming and its barrier, multi-homing cheap or costly, analogs with pattern, verdict, scarce asset, drift trigger)
## Next smallest test (hypothesis, population, recruitment, offer, metric with denominator, pass / fail / inconclusive rules, timebox, budget, evidence artifact)
## Sources (deduplicated, primary first, dated)
## Outcome line: N researchers · N skeptics · N claims → keep / revise / drop

6. Citation pass. Read the brief against the claim JSONs. Every load-bearing sentence gets a claim reference; any sentence with none is marked [no claim]. Return nothing else unless there is a violation.

7. File. Write research/YYYY-MM-DD-<slug>.md using research/TEMPLATE-DEEP.md frontmatter (question, date, confidence, status: fresh, sources, researchers, skeptics, claims kept/revised/dropped, grounding). Append one line to research/INDEX.md. Run `python3 scripts/archive.py <every source_url>` so the next run starts local.
