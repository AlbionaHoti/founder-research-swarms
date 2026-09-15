# Inspirations: open-source deep-research systems, and what this repo took from each

Surveyed 2026-09-15 to 16. Stars, last push and license from `api.github.com/repos/<owner>/<repo>` on 2026-09-15; files cited were fetched from raw.githubusercontent.com. Benchmarks are each repo's own claims, not re-verified.

## Table

| Repo | Stars | Last push | License | Architecture | Verify? | The one mechanism to steal |
|---|---|---|---|---|---|---|
| bytedance/deer-flow | 82,495 | 2026-09-15 | MIT | coordinator → planner → human plan review → research team → reporter (v1 on `main-1.x`) | human plan gate; strict `has_enough_context` | planner's 8-dimension checklist + mandatory `need_search` step |
| ItzCrazyKns/Perplexica (now Vane) | 36,874 | 2026-09-01 | MIT | SearxNG meta-search + rerank + LLM | none | numbered inline citations UI only |
| stanford-oval/storm (STORM, Co-STORM) | 31,389 | 2025-09-30 | MIT | perspective-guided simulated conversations → outline → article | grounding per sentence, no judge | personas generated from analog articles' tables of contents |
| assafelovic/gpt-researcher | 29,466 | 2026-08-27 | Apache-2.0 | planner–executor; recursive deep tree; reviewer/reviser/fact-checker | guideline reviewer; internal fact-checker | reviewer that must return `None` unless there is a violation |
| huggingface/smolagents (open_deep_research example) | 29,339 | 2026-08-25 | Apache-2.0 | CodeAgent manager + browser subagent | none | subagent may return a clarification request instead of an answer |
| camel-ai/owl | 20,139 | 2026-08-27 | unreported | role-playing pairs + toolkits | none | skip |
| dzhng/deep-research | 19,678 | 2026-04-11 | MIT | recursive breadth/depth; learnings feed the next level | none | query + `researchGoal` pairs; learnings must carry entities, exact numbers, dates |
| SakanaAI/AI-Scientist | 14,560 | 2025-12-19 | custom | idea → novelty → experiment → paper → automated reviewer | reviewer ensemble + meta-review + reflection | ensemble with a meta-reviewer |
| langchain-ai/open_deep_research | 12,680 | 2026-08-10 | MIT | supervisor → parallel researchers → compress → report (API: archived; successor `deepagents`) | `think_tool` reflection | verbatim compression before synthesis; "bias towards single agent" |
| LearningCircuit/local-deep-research | 9,095 | 2026-09-15 | MIT | pluggable strategies | entity-coverage tracking; verification searches after iteration 3 | entity extraction → underexplored-entity search suggestions |
| InternLM/MindSearch | 6,923 | 2025-07-04 | Apache-2.0 | planner writes a DAG as code; searchers run nodes in parallel | none | one question per node; edges are dependencies |
| nickscamara/open-deep-research | 6,283 | 2025-05-07 | unresolved | Firecrawl + reasoning model chat | none | skip |
| SamuelSchmidgall/AgentLaboratory | 5,849 | 2025-08-20 | MIT | role pipeline with 3 reviewers | 3 persona reviewers, weighted | deliberately divergent reviewer personas |
| jina-ai/node-DeepResearch | 5,227 | 2026-05-01 | Apache-2.0 | single ReAct loop under a token budget | five evaluators incl. a hostile "strict" one | question-typed evaluator set that rejects answers with a "to pass you must" plan |
| u14app/deep-research | 4,684 | 2026-06-18 | MIT | plan → queries → learnings → review plan vs learnings → report | plan-vs-learnings review | re-diff the plan against findings before reporting |
| sentient-agi/OpenDeepSearch | 3,837 | 2025-04-04 | Apache-2.0 | search tool in a ReAct loop; "pro mode" crawls + chunk-reranks | none | crawl → chunk → rerank instead of SERP snippets |
| mshumer/OpenDeepResearcher | 2,794 | 2025-05-02 | MIT | notebook loop with a per-page usefulness judge | per-page gate | usefulness gate before a page enters context |
| HKUDS/Auto-Deep-Research | 1,741 | 2025-10-16 | none | AutoAgent orchestrator | none | skip |
| Anthropic, "How we built our multi-agent research system" (post) | — | 2025 | — | orchestrator–worker; 3 to 5 parallel subagents; CitationAgent | five-criterion LLM judge | effort-scaling table; delegation contract; CitationAgent |
| OpenAI Deep Research system card (PDF) | — | 2025-02-25 | — | RL-trained browsing; separate CoT summarizer | safety evals only | nothing architectural |

## Per-system notes (the parts that matter for a market-research swarm)

**deer-flow (v1, `src/prompts/planner.md`, `src/graph/nodes.py`).** `has_enough_context` is true only if ALL conditions hold; "when in doubt, gather more". Every plan must include at least one `need_search: true` step. Eight analysis dimensions: historical, current, future, stakeholders, quantitative, qualitative, comparative, risk. A human plan-review interrupt (`[ACCEPTED]` / `[EDIT_PLAN]`). Reporter receives "Available Source References" appended last to curb URL hallucination. Do not copy: end-of-document reference lists that detach claims from sources.

**STORM / Co-STORM (`persona_generator.py`, `knowledge_curation.py`, `co_storm_agents.py`).** Personas are read off the tables of contents of related articles, always with a "Basic fact writer" first; one writer↔expert conversation per persona in parallel; every sentence must be supported by gathered information. Co-STORM's Moderator ranks retrieved-but-uncited snippets to inject perspectives and avoid stagnation. Do not copy: no adversarial pass.

**gpt-researcher (`skills/deep_research.py`, `multi_agents/agents/reviewer.py`, `fact_checker.py`).** Breadth 4, depth 2, breadth halves per level; queries as Query/Goal pairs; learnings tagged with source URLs. Reviewer returns `None` unless a guideline is violated; a second pass only if critical. Do not copy: a "fact check" that only reads the draft's own context and never re-opens a source.

**langchain open_deep_research (`prompts.py`).** Clarify → research brief ("avoid unwarranted assumptions", prefer official sites over aggregators) → lead researcher with `ConductResearch` / `ResearchComplete` / `think_tool`, "bias towards single agent unless clear opportunity for parallelization", hard cap on concurrent units → per-researcher stop rules ("stop when you can answer confidently"; "the last 2 searches returned similar information"; 2 to 3 calls for simple, at most 5 for complex) → compression that rewrites findings verbatim with numbered sources → report. Do not copy: no adversarial or citation-check pass.

**jina node-DeepResearch (`src/agent.ts`, `src/tools/evaluator.ts`).** A `gaps` array of open questions rotated each step; a diary of failed attempts; action toggles (search off after a search, off past 50 URLs); at 85% of the token budget, "beast mode" forces an answer. Evaluators chosen per question type: definitive (reject hedging), freshness (max-age table: finance 0.1 day, tutorials 180 days), plurality (count), completeness (named aspects), strict ("argue AGAINST the answer with the strongest case, then FOR"); fail one, return immediately, with a "to pass you must" plan. Do not copy: beast mode; a market brief must be able to say unknown.

**dzhng/deep-research (`src/deep-research.ts`).** Queries carry a `researchGoal`; learnings must be "as detailed and information dense as possible: entities, exact metrics, numbers, dates"; breadth halves per level; concurrency 2. Do not copy: sources as a flat list unattached to claims.

**Anthropic post.** Lead agent plans in extended thinking and spawns 3 to 5 subagents, each given an objective, an output format, guidance on tools and sources, and clear boundaries. Effort scaling: simple fact = 1 agent, 3 to 10 tool calls; comparison = 2 to 4 subagents, 10 to 15 calls each; complex = more than 10 subagents. "Start with short, broad queries, evaluate what is available, then narrow." A CitationAgent post-processes the report against the documents. End-state judge scores factual accuracy, citation accuracy, completeness, source quality, tool efficiency, 0 to 1 plus pass/fail. Token use: agents about 4x chat, multi-agent about 15x; token use explained 80% of BrowseComp variance. Failure modes: 50 subagents for a simple query; endless search for sources that do not exist; duplicate searches from vague delegation; agents distracting each other with updates.

**Reviewer ensembles (AI-Scientist `perform_review.py`, AgentLaboratory `agents.py`).** Ensemble reviews at temperature 0.75 with mean scores and an area-chair meta-review; three deliberately different personas (harsh but fair; harsh on impact; open-minded on novelty). AI-Scientist's README warns of "positivity bias" in some models. Do not copy: paper rubrics.

**Others.** MindSearch: one question per DAG node, edges are dependencies, unrelated nodes run in parallel. local-deep-research: original query always in iteration 1; entity extraction and "underexplored entity" suggestions; verification searches after iteration 3. u14app: `reviewSerpQueriesPrompt` diffs the plan against learnings before reporting. OpenDeepSearch pro mode: crawl every source, chunk, rerank, never trust the snippet. OpenDeepResearcher: a per-page "is this useful" judge before ingestion. smolagents: a subagent may `final_answer` with a clarification request.

## Ranked: the eight mechanisms adopted into the skeleton

1. Question-typed evaluators as the skeptic's second pass: definitive, freshness (max-age table), plurality, completeness, strict. jina `src/tools/evaluator.ts`.
2. Effort-scaling table and the four-part delegation contract. Anthropic post; mirrored by "bias towards single agent" in langchain `prompts.py`.
3. Perspective personas read off the structure of analog topics. STORM `persona_generator.py`.
4. Verbatim compression before synthesis, numbered sources carried through. langchain `prompts.py`.
5. Post-hoc citation pass plus the five-criterion end-state judge. Anthropic post.
6. Planner decomposition checklist with a mandatory search step and strict "enough context". deer-flow `src/prompts/planner.md`.
7. Divergent reviewer personas with a meta-reviewer for high-stakes verdicts. AgentLaboratory `agents.py`, AI-Scientist `perform_review.py`.
8. A moderator that surfaces retrieved-but-uncited evidence between research and synthesis. Co-STORM `co_storm_agents.py`.

Runner-ups: DAG-as-code decomposition (MindSearch); crawl → chunk → rerank (OpenDeepSearch); entity-coverage gap tracker (local-deep-research); null-default reviewer (gpt-researcher).

## Caveats
langchain open_deep_research is flagged archived by the API with no README notice; camel-ai/owl and HKUDS report no license; all benchmark figures are self-reported; Anthropic's "90%" and "15x" are the post's own numbers.
