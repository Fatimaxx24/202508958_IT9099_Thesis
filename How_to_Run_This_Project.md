##How to Run This Project

The list of notebooks is shown in the order they were carried out to obtain the results mentioned in the thesis. This is because each notebook is fed its inputs directly from this repository (using raw GitHub URLs), so no transfer of files is required beyond API credentials.

Prerequisites
An Azure OpenAI resource with two models deployed:
text-embedding-3-small (embeddings)
a chat model such as gpt-5-mini (generation)
A local .env file with your credentials copy .env.example and fill in your own values. Never commit this file.
Python packages: pip install -r requirements.txt

------------------------------------------------------------------------------------------------------------------------
##Run Order

##Stage 1 - Dataset (reference only already completed)

labelling_sample_80_REVIEWED.csv
labelling_batch2_120_labelled.csv
labelling_master_1000_labelled.csv These are the manually labelled outputs no notebook needs to be run to reproduce these, as they represent human judgement, not computation.

##Stage 2 - Classification

1. baseline_v0.ipynb - original baseline on 74 labels
2. STAGE2_COMPLETE Updated.ipynb - full classification pipeline on 891 labels: hybrid features, grouped CV, five-configuration leakage ablation, five-seed stability check, Wilcoxon test, SHAP analysis, temporal holdout. This is the canonical notebook for all Chapter 5 classification results.

##Stage 3 - Retrieval-Augmented Generation 3. 

3. STAGE3_part1_vectorstore.ipynb - embeds the full 3,201-record corpus into ChromaDB and saves it as chroma_gdpr.zip.
4. STAGE3_part2_chatbot.ipynb - interactive RAG chatbot with BM25 baseline demonstrates citation, refusal, and false-premise correction behaviour. 
5. STAGE3_part3_evaluation.ipynb - runs the frozen 15-question benchmark through both RAG and BM25 systems, producing rag_benchmark_results.csv.

##Evaluation (manual step, not a notebook)

RAG_Benchmark_Scored.xlsx - the 30 responses from step 5, scored by hand on four dimensions (correctness, faithfulness, citation validity, retrieval recall).
rag_kappa_subset_SCORED_second_assessor.csv an independent assessor's blind rescoring of a 5-question subset.

chat.py (in the local demo setup - see thesis Chapter 4) runs the RAG interface as a terminal chatbot, using the vector store built in step 3.

##Verifying Results Without Running Anything

All notebooks are saved with the output of the cells shown. Screenshots of key results are also provided in Screenshots/. The complete reporting numbers can thus be read from the repository and don't require API credentials or a re-run of any code.
