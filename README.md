# CyberSentinel-EU
MSc AI Thesis - Fatema Hasan, 202508958, Bahrain Polytechnic

# CyberSentinel-EU
AI-Assisted Analysis of GDPR Cyber-Incident Records Using NLP,
Explainable AutoML and Retrieval-Augmented Generation

MSc in Artificial Intelligence - Thesis Project
Fatema Husain Hasan (202508958), Bahrain Polytechnic
Supervisor: Dr. David Gulua
June – August 2026

## Project overview
A three-stage pipeline: (1) feasibility audit and construction of a
labelled GDPR cyber-incident dataset, (2) explainable AutoML
classification with leakage-aware evaluation, (3) a RAG conversational
interface over the enforcement corpus evaluated against a BM25 baseline.

## Data

### data/gdpr_enforcement_tracker_full.csv
Full snapshot of the GDPR Enforcement Tracker (enforcementtracker.com,
a service by CMS Law). 3,202 records, 12 columns including per-record
Summary text, Type of Violation, and source URLs.
- Extracted: 15 July 2026, using Claude.
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
- Files kept with original filenames; schemas vary by quarter
  (harmonised in the data pipeline).

## Repository structure (will grow as the project progresses)
- data/ — source datasets (snapshots, never modified)
- notebooks/ — analysis and pipeline notebooks
- src/ — pipeline code
- outputs/ — labelled dataset, figures, results

## Licence and use
Source data remain the property of their publishers (CMS Law / ICO) and
are included here as research snapshots. The labelled dataset produced
by this project will be released under CC BY 4.0.
