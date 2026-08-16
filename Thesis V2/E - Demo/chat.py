"""
CyberSentinel-EU - Terminal Chat Interface
MSc AI Thesis Fatema Husain Hasan (202508958) Bahrain Polytechnic

Ask questions about 3,201 GDPR enforcement records in plain language.
Answers are grounded in retrieved records and cited by ETid.

Usage:  python chat.py
"""

import os
import sys
import textwrap
import chromadb
from openai import AzureOpenAI
from dotenv import load_dotenv

# ---------------------------------------------------------------- config
load_dotenv()
ENDPOINT   = os.getenv("AZURE_OPENAI_ENDPOINT")
API_KEY    = os.getenv("AZURE_OPENAI_API_KEY")
EMBED_MODEL = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-small")
CHAT_MODEL  = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT", "gpt-5-mini")
API_VERSION = "2024-10-21"
STORE_PATH  = "./chroma_gdpr"
TOP_K       = 5

SYSTEM_PROMPT = """You are CyberSentinel-EU, an assistant that answers questions about GDPR
enforcement decisions using ONLY the retrieved records provided.

Rules:
1. Answer ONLY from the retrieved records. Never use outside knowledge.
2. Cite every claim with the record ID in square brackets, e.g. [ETid 2521].
3. If the retrieved records do not contain the answer, reply exactly:
   "Insufficient evidence in the corpus to answer this question."
4. If the question contains a false premise, correct it based on the records.
5. Be concise and factual. State uncertainty where it exists.
"""

# ---------------------------------------------------------------- setup
def connect():
    if not API_KEY or not ENDPOINT:
        sys.exit("ERROR: Azure credentials missing. Create a .env file (see .env.example).")
    client = AzureOpenAI(azure_endpoint=ENDPOINT, api_key=API_KEY, api_version=API_VERSION)

    if not os.path.exists(STORE_PATH):
        sys.exit(f"ERROR: vector store not found at {STORE_PATH}. Unzip chroma_gdpr.zip here first.")
    store = chromadb.PersistentClient(path=STORE_PATH)
    collection = store.get_collection("gdpr_enforcement")
    return client, collection


# ---------------------------------------------------------------- core
def retrieve(client, collection, question, k=TOP_K):
    """Semantic search over the enforcement corpus."""
    vector = client.embeddings.create(model=EMBED_MODEL, input=question).data[0].embedding
    result = collection.query(query_embeddings=[vector], n_results=k)

    records = []
    for text, meta, distance in zip(result["documents"][0],
                                    result["metadatas"][0],
                                    result["distances"][0]):
        records.append({
            "etid":       meta["ETid"],
            "country":    meta["country"],
            "sector":     meta["sector"],
            "year":       meta["year"],
            "similarity": round(1 - distance, 3),
            "text":       text,
        })
    return records


def build_context(records):
    return "\n\n".join(
        f"[ETid {r['etid']}] ({r['country']}, {r['sector']}, {r['year']})\n{r['text']}"
        for r in records
    )


def answer(client, question, records):
    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": f"Retrieved records:\n\n{build_context(records)}"
                                          f"\n\nQuestion: {question}"},
        ],
    )
    return response.choices[0].message.content


# ---------------------------------------------------------------- display
LINE = "-" * 78

def show_answer(text):
    print("\nCyberSentinel-EU:")
    for paragraph in text.split("\n"):
        print(textwrap.fill(paragraph, 76) if paragraph.strip() else "")


def show_sources(records):
    print(f"\n{LINE}\nSources retrieved:")
    for n, r in enumerate(records, 1):
        print(f"  {n}. [ETid {r['etid']}]  {r['country']} · {r['sector']} · {r['year']}"
              f"   (similarity {r['similarity']})")
    print(LINE)


# ---------------------------------------------------------------- main
def main():
    client, collection = connect()

    print("=" * 78)
    print("  CyberSentinel-EU  |  GDPR Cyber-Incident Intelligence")
    print("  3,201 enforcement records  |  ask anything, or type 'exit'")
    print("=" * 78)

    while True:
        try:
            question = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye.")
            break

        if not question:
            continue
        if question.lower() in {"exit", "quit", "q"}:
            print("Goodbye.")
            break

        try:
            print("  ...searching corpus")
            records = retrieve(client, collection, question)
            reply   = answer(client, question, records)
            show_answer(reply)
            show_sources(records)
        except Exception as error:
            print(f"  Error: {error}")


if __name__ == "__main__":
    main()
