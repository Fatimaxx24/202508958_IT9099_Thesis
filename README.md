# CyberSentinel-EU
MSc AI Thesis - Fatema Hasan, 202508958, Bahrain Polytechnic
AI-Assisted Analysis of GDPR Cyber-Incident Records Using NLP, Machine Learning and Retrieval-Augmented Generation

Fatema Husain Hasan (202508958), Bahrain Polytechnic
Supervisor: Dr. David Gulua
June – August 2026

## Project overview
A three-stage pipeline: 
(1) feasibility audit and construction of a labelled GDPR cyber-incident dataset 
(2) machine-learning classification with leakage-aware evaluation 
(3) a RAG conversational interface over the enforcement corpus evaluated against a BM25 baseline.

##Final Results (24 Aug 2026)

Classification (891 labelled records):

Hybrid features (structured + text embeddings): 0.808 macro-F1 (stratified 5-fold CV)
Grouped CV by organisation: 0.784 | Temporal holdout (train ≤2022, test ≥2023): 0.727
Wilcoxon signed-rank test (H1): p < 0.00001, effect size 0.988, across 25 paired folds (5 seeds × 5 folds)
Leakage ablation (5 configurations, 5 seeds): mean difference 0.4 ± 0.8 points — statistically indistinguishable from zero

##RAG Evaluation (15-question benchmark, 4 dimensions):

RAG: 1.80/2.00 (90.0%) vs BM25: 1.68/2.00 (84.2%)
Independent reliability check: Cohen's κ = 1.000 (5-question blind rescoring subset)

See the final thesis document for full methodology, discussion, and limitations.


##Data
### gdpr_enforcement_tracker_full.csv
Full snapshot of the GDPR Enforcement Tracker (enforcementtracker.com,
a service by CMS Law). 3,202 records, 12 columns including per-record
Summary text, Type of Violation, and source URLs.
- Extracted: 15 July 2026 using AI and verified by the author. 
- Encoding: UTF-8
- Known issues: 143 records without a fine amount (treated as missing);
  22 records with unknown decision dates; 1 date typo (ETid 2322);
  3 records with encoding artefacts (ETids 2622, 2643, 2737).

### ICO/ (Cyber Incidents & Cyber Investigation)
UK Information Commissioner's Office cyber data sets - 39 quarterly CSV
files (19 cyber incidents, 20 cyber investigations), 2021 to 2025/26,
~1,736 records total. Every record is a pre-confirmed cyber case.
- Downloaded: 15 July 2026 from
  https://ico.org.uk/action-weve-taken/complaints-and-concerns-data-sets/cyber-investigations/
- Files kept with original filenames; schemas vary by quarter. Evaluated but not used in the final pipeline. 

## Repository structure
All files are in the repository root, except:
- ICO/ -- ICO cyber datasets (evaluated, not used in the final pipeline)
- Screenshots/ -- results evidence for each stage

Key files:
- Data: gdpr_enforcement_tracker_full.csv
- Labels: labelling_sample_80_REVIEWED.csv, labelling_batch2_120_labelled.csv, labelling_master_1000_labelled.csv
- Notebooks: baseline_v0.ipynb, pipeline_v2_1000.ipynb, STAGE2_COMPLETE.ipynb, STAGE3_part1_vectorstore.ipynb, STAGE3_part2_chatbot.ipynb, STAGE3_part3_evaluation.ipynb
- Vector store: chroma_gdpr.zip
- Config: requirements.txt, .env.example, .gitignore, LICENSE

## Licence and use
Source data remain the property of their publishers (CMS Law / ICO) and
are included here as research snapshots. The labelled dataset produced
by this project will be released under CC BY 4.0.

## Baseline v0 (16 Jul 2026, superseded by final results below)
- baseline_v0.ipynb - keyword screening of the full corpus (482/3,202
  records flagged, 15.1%), manual labelling of an 80-record stratified
  sample, and comparison of six classifiers on structured features.
- Best model: Decision Tree, macro-F1 = 0.816 (5-fold CV, 74 labels).
  Indicative only given sample size.
- labelling_sample_80_REVIEWED.csv - manually reviewed starter labels.

## Stage 1 - Labelled dataset (Aug 2026)

**labelling_master_1000_labelled.csv** - 1,000 records manually labelled by the author.

| Label | Count |
|---|---|
| cyber_malicious | 194 |
| cyber_nonmalicious | 401 |
| not_cyber | 296 |
| unclear (excluded) | 109 |
| **Usable** | **891** |

Sampling stratified by keyword signal and violation type, weighted toward ambiguous
records. Confidence ratings: 632 High / 233 Medium / 135 Low. All 200 records from
the initial audit were reviewed and confirmed by the supervisor.

Note: following supervisor guidance in Week 8, the project uses the Tracker as a
single data source. The ICO datasets were evaluated but excluded from the final
pipeline, as they lack the free-text descriptions required for embedding-based
classification and retrieval. Retained here as a documented fallback.

## Stage 2 - Classification (STAGE2_COMPLETE.ipynb)

Structured features + Azure OpenAI text-embedding-3-small (PCA 100 components, 77.2% variance).

| Experiment | macro-F1 |
|---|---|
| Cyber vs non-cyber - structured only | 0.736 |
| Cyber vs non-cyber - embeddings only | 0.805 |
| Cyber vs non-cyber - hybrid | 0.804 |
| Malicious vs non-malicious - structured | 0.699 |
| Malicious vs non-malicious - hybrid | 0.713 |
| Grouped CV by organisation (hybrid) | 0.785 |
| Leakage ablation (no fine/articles) | 0.767 |
| Temporal holdout (train ≤2022, test 2023+) | 0.730 |

Key findings: text embeddings substantially outperform structured metadata; the
leakage ablation shows only a ~1.8-point drop without post-incident regulatory
features, and SHAP ranks text components ~8× above log_fine - the model classifies
on incident descriptions, not regulatory outcomes.

## Stage 3 - RAG interface

**STAGE3_part1_vectorstore.ipynb** - embeds all 3,201 records (one record = one chunk)
into ChromaDB with metadata. Vector store archived as `chroma_gdpr.zip`.

**STAGE3_part2_chatbot.ipynb** - RetrievalQA using Azure OpenAI gpt-5-mini with a
system prompt enforcing per-claim citation and explicit refusal. BM25 (rank-bm25)
baseline over the same corpus, using the same LLM so only retrieval differs.

Demonstrated behaviours (see Screenshots/): accurate cited answers; exclusion of
retrieved-but-irrelevant records; refusal on unanswerable questions; correction of false premises.

Note: gpt-4o-mini (named in the proposal) was deprecated on Azure during the project gpt-5-mini was used instead.


