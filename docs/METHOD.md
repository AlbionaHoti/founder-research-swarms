# The deep method: decompose, research, verify, synthesize

The heavier sibling of the one-prompt method in the README. Use it when being wrong is expensive: a build decision, a pricing call, a market you are about to spend months in. Copy this structure for any question; change the facets, never the contracts. Paste-ready version: `PROMPT-DEEP.md`. Where the mechanisms came from: `docs/INSPIRATIONS.md`.

The purpose in one sentence: find a specific buyer, a costly problem, a reachable channel, a useful outcome and viable economics, then turn the largest uncertainty into the smallest test. A swarm does not decide. It produces verified claims with their gaps stated, and a market-structure read, so the founder can decide.

---

## 1. Principles that do not bend

1. **Only keep and revise claims reach the brief.** A skeptic votes on every claim. Dropped claims appear only in "Killed in review" with the reason.
2. **Every number carries period, geography, platform and source date, or it is `unverified`.** Downloads are not users. Revenue is not profit. Annualized is not annual. A long-running ad is a clue, not proof of profitability.
3. **Primary sources only.** T1 = papers, regulator pages, filings, platform docs, the product's own store page, a developer's own postmortem. T2 = named reporters, credentialed analysts. Never SEO listicles, aggregator rewrites, or market-size press releases. Training-data-only claims are `memory` quality and guilty until grounded.
4. **A prior lane file is not a primary source.** Reuse its URLs, reopen them, cite what you opened.
5. **Negative results require methodology.** A "no competitor does X" or "no source found" claim must list the 3 to 5 distinct query phrasings tried, in the output, under `dead_ends`. Absence without the queries is not a finding.
6. **Incompleteness is stated, never hidden.** The synthesizer cannot edit down "What this brief cannot tell you". Unknown is an acceptable answer; a forced answer is not.
7. **Headline vs honest.** Expect the honest number to be 3 to 10x lower than the headline. Record both.
8. **Subagents are read-only. The main session writes every file.** That is where the permission gates live.
9. **Ads, downloads, follower counts and X posts cannot pass the payment, outcome, retention or unit-economics gates.** Only first-party evidence can.
10. **Never invent competitor funding, user counts or analog outcomes.** Cite or write `unverified`; an unverified analog scores 0.
11. **Score the wedge as it will ship, not the category.** "AI is moving fast" is mood, not a market-speed verdict.
12. **Fewer agents unless parallelism is real.** Bias towards one researcher; add more only when facets are independent. Vague delegation produces duplicate searches.

---

## 2. Effort scaling and the delegation contract

Set the swarm size from the question type before anything runs.

| Question type | Researchers | Tool calls each | Skeptics | Example |
|---|---|---|---|---|
| Single fact or price | 1 | 3 to 10 | 1 | "what does X charge and since when" |
| Comparison of 2 to 4 things | 2 to 4 | 10 to 15 | 1 per researcher | "which of these four buyers pays" |
| Open market question, several buyers, several forms | 5 to 8 | 15 to 25 | 1 per researcher | "who should we sell to and how, in 72 hours" |
| Anything larger | split into two runs | | | |

Every subagent prompt carries the four-part contract: **objective** (the facet, verbatim), **output format** (the JSON contract, nothing else), **sources and tools** (local-first paths, the search recipes, the recency window, what is blocked), **boundaries** (what is another facet's job; return a clarification request rather than guessing when the facet is ambiguous).

Token cost is real: a multi-agent run costs roughly fifteen times a single chat. Spend it on questions where being wrong is expensive.

---

## 3. Roles

| Role | Count | Model | Tools | Returns |
|---|---|---|---|---|
| Coordinator (main session) | 1 | any | everything | facet plan, all file writes, the run folder, the trace, the archive |
| Researcher | 1 per facet | sonnet | Read, Grep, Glob, WebSearch, WebFetch | JSON claim contract, 5 to 15 claims, `dead_ends`, gaps, surprises, lane scores |
| Link checker (mechanical) | 1 script | none | HTTP HEAD | for every `source_url`: OK / MISSING / ERROR; MISSING flips the claim to `unverified` before any skeptic sees it |
| Skeptic | 1 per facet | sonnet | same as researcher, read-only | keep / revise / drop per claim, `checks_performed`, `unchecked`, adjusted lane scores, one prompt tweak, grounding score 1 to 5 |
| Moderator (optional) | 1 | sonnet | Read only | surfaces evidence that was fetched but never cited, so synthesis is not starved by the researchers' framing |
| Synthesizer | 1 | opus | Read only, no web | the brief in the fixed shape |
| Citation pass | 1 | sonnet | Read only | every load-bearing sentence in the brief is matched to a claim ID and a URL; unmatched sentences are flagged, not deleted |
| End-state judge (optional, high stakes) | 1 to 3 | sonnet | Read only | five scores 0 to 1 plus pass/fail; three divergent personas and a meta-review when the verdict will drive a build |

Lanes never share a researcher, so acquisition signal cannot leak into revenue signal. The four-kinds-of-evidence lanes are market growth, ad patterns, actual experience, business plausibility; add claims/science, feasibility, and a kill-check lane when the question needs them.

---

## 4. The stages, in order

**Stage 0, scope.** Write the decision in one sentence, the buyer situation, and the evidence that would change the choice. Record what is unknown (revenue target, deadline, rules) rather than inventing it. Read what already exists first: `research/INDEX.md`, prior briefs, `knowledge/INDEX.md`; local search before web search, always. Pick the effort row from section 2. Decide the delegation posture (advice / scoped / deliverable / autonomous); default deliverable: present the facet plan in one message, then proceed.

**Stage 1, decompose.** 3 to 8 facets, each a question, independently researchable, non-overlapping. Run the eight-dimension checklist over the question before fixing facets: historical, current, future, stakeholders, quantitative, qualitative, comparative, risk. If a facet depends on another's answer, mark the edge and run it second; everything else runs in parallel. Fix the candidate set (buyers, products, forms) before research so nobody adds candidates mid-run. Where the topic has close analogs, read the analogs' structure (their tables of contents, their pricing pages, their store listings) to generate the perspectives the facets should carry, with a basic-facts facet always present. Every plan must include at least one facet that requires new search; "enough context already" is true only when every condition holds.

**Stage 2, research (parallel).** One researcher per facet, all launched in one message. Each prompt carries the four-part contract from section 2. Researchers start wide (short, broad queries), evaluate what exists, then narrow. They expand each query into 4 to 6 phrasings for variety before trusting an absence. They open pages, chunk and rerank against the facet; a snippet is not a source. A page enters a claim only if it is useful for the facet. Learnings carry entities, exact numbers and dates. Stop rules: stop when the facet can be answered confidently; stop when the last two searches returned the same material; simple facets 2 to 3 searches, complex ones at most 5 rounds. Every search runs with the temporal rule: any query carrying "latest", "current", "this month", "as of" or a year within one of today bypasses the cache. Do not read raw search results yourself. If a researcher returns malformed JSON, re-prompt once, then record the facet as failed.

**Stage 2b, mechanical check.** Before any skeptic runs, HEAD-check every `source_url` in every researcher JSON. MISSING or ERROR flips that claim to `unverified` and records it. This is a script, not a model.

**Stage 2c, compression (when researcher output is long).** Rewrite findings verbatim into a cleaner format with numbered sources; never summarize, never paraphrase. The synthesizer must see the source's words, not a researcher's gloss.

**Stage 3, verify (parallel).** One skeptic per facet, launched as each facet lands. Per claim: open the cited URL or archive path (the exact page, not a search summary of it); run at least one disconfirming search; check for overclaim (one study → "research shows"; one review → "players"; one thread → "not subscriptions"); treat `memory` claims as guilty until grounded; give load-bearing claims three votes: source says this / current and period-consistent / applies to this segment; keep if two survive. Then the evaluator pass, chosen by claim type: definitive (reject hedged numbers), freshness (the max-age table in section 7), plurality (does the count match the source's count), completeness (are all named aspects covered), strict (argue against the claim with the strongest case, then for). Fail one, revise or drop, with a "to pass you must" note. The skeptic ends with one quotable prompt tweak and a grounding score 1 to 5. Skeptic verdicts are final. When torn between keep and revise, revise. Never omit a claim; a skipped claim goes in `unchecked` with the reason.

**Stage 3b, moderator (optional).** Read every fetched page and every claim; list evidence that was fetched but never cited and that bears on the question. Hand it to the synthesizer as "uncited evidence"; it cannot become a claim without a skeptic, but it can become a gap or a surprise.

**Stage 4, synthesize (once).** Synthesizer gets the question, every researcher JSON, every skeptic JSON, and any moderator list. No web. Only keep and revise claims, in the revised wording. Disagreement is content: write conflicts as their own section. Brief shape in section 8. Save to `research/<date>-<slug>.md` and append one line to `research/INDEX.md`.

**Stage 4b, citation pass.** A second read of the brief against the claim JSONs: every load-bearing sentence gets its claim ID and URL; any sentence with no matching claim is flagged in the brief as `[no claim]`. The reviewer returns nothing unless there is a violation; no rewriting for style.

**Stage 5, judge (high stakes only).** Score the brief 0 to 1 on factual accuracy, citation accuracy, completeness, source quality, tool efficiency, with pass/fail. When the verdict will drive a build, run three divergent reviewers (harsh but fair; harsh on impact; open to what is new) and a meta-review that reconciles them. Log the scores beside the run.

**Stage 6, close the run.** Archive every source URL, check the archive is text, append trace rows if hooks did not fire, write the run README with the outcome line, write the decision into the brief's frontmatter when you act on it. State what was inspected, what was inaccessible, what is hypothesis.

Then your own build gates. The market-structure block in the brief is an input to them, not a substitute for them.

---

## 5. Contracts (copy exactly)

**Researcher returns only:**
```json
{ "facet": "<verbatim>",
  "claims": [ { "claim": "<one falsifiable sentence with number and date>", "source_url": "", "source_title": "", "source_date": "YYYY-MM-DD", "period": "", "geography": "", "platform": "", "quote_or_number": "", "quality": "T1|T2|memory", "confidence": "low|medium|high", "load_bearing": true, "retrieval": "local|web|fetched_page|search_snippet" } ],
  "dead_ends": [ { "finding": "<what was not found>", "queries_tried": ["", "", ""] } ],
  "unverified": [], "gaps": [], "surprises": [],
  "clarification_needed": "<empty, or the question the coordinator must answer before this facet can proceed>",
  "lane_scores": { "<axis>": 0 } }
```

**Skeptic returns only:**
```json
{ "facet": "<verbatim>",
  "verdicts": [ { "claim_index": 1, "verdict": "keep|revise|drop", "revised_claim": "", "checks_performed": ["fetched source", "disconfirming search: <query>", "3-vote: source pass/fail, current pass/fail, segment pass/fail", "evaluators: definitive pass, freshness pass, plurality n/a, completeness pass, strict pass"], "headline_vs_honest": "", "reason": "" } ],
  "unchecked": [],
  "lane_scores_adjusted": { "<axis>": 0 },
  "grounding_score": 0,
  "prompt_tweak": "<one sentence the next researcher prompt should add>" }
```
Never omit a claim. A skipped claim goes in `unchecked` with the reason.

**Lane axes (1 to 10):** growth: `growth_direction, scale, data_consistency` · ads: `ad_longevity, hook_clarity, owned_channel_fit` · experience: `time_to_first_result, loop_depth, retention_hooks` · plausibility: `buildability, asset_fit, operating_burden (10 = light), clock_fit` · claims: `claim_safety, mechanic_evidence, buildability` · feasibility: `time_to_first_dollar, delivery_friction, analog_strength`. Use the skeptic-adjusted scores, never the researcher's.

---

## 6. Decision gates

| Gate | Passes only with | Never passes with |
|---|---|---|
| Problem | recent first-party incidents in the segment | one viral post, a survey, a persona |
| Reach | our measured access with a denominator | competitor followers, impressions, "the niche is loud" |
| Payment | our completed charges | competitor prices, "I would pay" |
| Outcome | our measured result vs a named alternative | app score, testimonial |
| Retention | dated return at the job's natural recurrence | likes, one day's engagement |
| Unit economics | our measured contribution and CAC | assumed LTV, someone else's MRR |

`build_pilot` requires problem, reach and payment. `scale` requires all six. Research alone ends at `research`, `test`, `park` or `kill`. Every test names its denominator and an inconclusive rule that separates recruitment failure from product failure.

---

## 7. Freshness: max age by claim type

The freshness evaluator rejects a claim whose source is older than its max age unless the claim says so.

| Claim type | Max age | Why |
|---|---|---|
| Active ad count, ad creatives | 7 days | inventories churn daily |
| Prices, in-app purchase ladders, plan tiers | 30 days | change without notice |
| Platform policy (store rules, payout terms) | 90 days, and re-fetch the page | policies are re-issued |
| Company revenue, funding, headcount | the latest filing or release; mark the quarter | stale figures mislead by 2x within a year |
| Survey statistics (national surveys) | until superseded; always state the fielding year | a 2022 survey is still the best source if none newer exists |
| Peer-reviewed findings | no max age; state follow-ups that revised them | the original can be walked back by its own authors |
| App-store reviews, forum posts | dated per item; never aggregated into prevalence | one review is one report |

---

## 8. The brief shape (synthesizer output)

```
# Brief: <question>
## Answer in three sentences
## What we know (by theme, not by facet)
## Dossiers (one per candidate: headline vs honest, verdict FLAGSHIP PICK / SLEEPER / BIG-TAM TRAP / PASS, confidence, skeptic critique, sources)
## Where sources disagree
## What this brief cannot tell you (every gap, unverified, unchecked and dead_end)
## Surprises
## Killed in review (claim → skeptic reason)
## Market-structure block (5x-capital answer, power + barrier, Blitzscaling boxes with the PMF box, multi-homing, analogs with pattern, scorecard NE/Scale/Multi-home/Analogs/CAC = /10, verdict, scarce asset, studio call, held asset, drift triggers)
## Next smallest test (hypothesis, population, recruitment, offer, metric with denominator, pass/fail/inconclusive, timebox, budget, evidence artifact)
## Sources (deduplicated, T1 first, dated)
## Outcome line: N researchers · N skeptics · N claims → keep / revise / drop · candidates → finalists → kept
```

---

## 9. Run folder, archive and trace

```
research/runs/<date>-<slug>/
  README.md          question, effort row, stages run, execution disclosure, outcome line
  researchers/F1.json … Fn.json
  linkcheck.json     HEAD results per source_url
  skeptics/F1.json … Fn.json
  moderator.json     (optional) uncited evidence
  BRIEF.md           also copied to research/<date>-<slug>.md
  judge.json         (optional) end-state scores
  artifacts/         economics scenarios, captures, ledgers
knowledge/<date>-<slug>.md   one file per fetched page; frontmatter url, title, fetched, content hash; same hash = do not rewrite, new content = new dated file
knowledge/INDEX.md           grep here before the web; also index search hits that were never fetched
traces/trace.jsonl           one row per agent: stage, model, facet, prompt hash, duration, ok; plus dead_ends count and grounding score per run
```

Archive rules: canonicalize URLs (strip tracking parameters, fragments, trailing slashes) before hashing; store the extractor used; a PDF is saved as extracted text, never bytes; search hits are indexed even when never fetched so the next adjacent run starts local.

---

## 10. Checklist before calling a run done

- [ ] Effort row chosen and written in the README; agent count matches output files
- [ ] Every claim in the brief is keep or revise; drops are in "Killed in review"
- [ ] Every number has period, geography, platform, source date
- [ ] Every absence claim lists its `dead_ends` queries
- [ ] Link check ran; MISSING sources are `unverified` in the brief
- [ ] Skeptic-adjusted scores used, not researcher scores
- [ ] Freshness table applied; stale claims say their date
- [ ] "What this brief cannot tell you" merges every gap, unverified, unchecked and dead_end
- [ ] Citation pass ran; `[no claim]` sentences are visible, not hidden
- [ ] Sources archived as text; canonical URLs; content hashes
- [ ] Trace rows exist for every agent (hooks, or by hand); grounding scores logged
- [ ] Execution disclosure: what ran sequentially, what was blocked, which agents produced no output
- [ ] Market-structure block present with a named scarce asset and a drift trigger
- [ ] Next smallest test has a denominator and an inconclusive rule
- [ ] No claim the run was not asked to substantiate appears as a product promise

---

## 11. Known failure modes, and the fix built in

| Failure | Fix |
|---|---|
| A PDF archived as raw bytes; skeptics could not grep it | After archiving, open the file; re-save PDFs with `pdftotext -layout` |
| A researcher cited a precise statistic that did not exist on the cited page | Link check plus the skeptic's targeted string search on the cited page for every load-bearing number |
| Correct numbers under the wrong citation | The skeptic opens the exact cited URL, not a search summary of it |
| A researcher cited a prior lane file as its source | Principle 4: reopen and cite the primary |
| "No one does this" with no queries listed | Principle 5: `dead_ends` with 3 to 5 phrasings, or it is not a finding |
| A chart extracted by pdftotext had scrambled column labels | The skeptic checks that category percentages sum to 100 before trusting a chart read |
| Market speed scored on the category, not the wedge | Score the wedge as it will ship; the synthesizer re-scores if the coordinator drifted |
| A decision gate with no denominator | Every test names its denominator and an inconclusive rule |
| Trace hooks did not fire | Append trace rows by hand if your harness has no hooks |
| The agent count in public copy included the coordinator | Count agents by output files, and say which swarms |
| An AI-summarized search result invented a statistic with a named institution | Anything from a search summary that was not opened is `unverified`; `retrieval: search_snippet` makes it visible |
| Too many subagents for a simple question | The effort table in section 2; bias towards one researcher |
| Duplicate searches across researchers | The four-part delegation contract with explicit boundaries |
| Endless search for a source that does not exist | Stop rules in Stage 2; `dead_ends` records the attempt and the run moves on |
| Synthesis drifted from what sources said | Verbatim compression; the citation pass flags `[no claim]` sentences |
| The same model that wrote the claims judged them and was gentle | Skeptic is a separate agent with a disconfirming brief; for build decisions, three divergent reviewers and a meta-review |
| A forced answer where "unknown" was the truth | Principle 6; no beast mode in a market brief |

---

## 12. Where each mechanism came from

Negative-result methodology, cache-first search with temporal bypass, a write-through archive with content hashes and indexed-but-unfetched search hits, an agent-callable link verifier, and a critique that ends in a one-sentence prompt tweak plus a grounding score: an open-source ReAct research agent with a local archive. Effort scaling, the delegation contract, start-wide-then-narrow, the citation pass, the five-criterion judge and the failure modes about subagent count and vague delegation: Anthropic's post on their multi-agent research system. Question-typed evaluators and the freshness max-age idea: jina node-DeepResearch. Perspective generation from analog structure and the uncited-evidence moderator: STORM and Co-STORM. Verbatim compression, per-researcher stop rules and the single-agent bias: langchain open_deep_research. The eight-dimension decomposition checklist and the mandatory search step: deer-flow. Divergent reviewer personas and the meta-review: AgentLaboratory and AI-Scientist. Null-default reviewer: gpt-researcher. Learnings as entities, exact numbers and dates: dzhng/deep-research. Crawl, chunk and rerank over snippets: OpenDeepSearch. Repos, stars, dates and file paths in `docs/INSPIRATIONS.md`.

---

Run folder layout in section 9 assumes `research/research/runs/<date>-<slug>/` inside this repo; the brief itself goes to `research/` so the index rule from the README still holds.
