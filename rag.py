import os
import chromadb
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

KNOWLEDGE_DIR = "knowledge"
CHROMA_DIR = "chroma_db"

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = Chroma(
    collection_name="business_knowledge",
    embedding_function=embeddings,
    persist_directory=CHROMA_DIR
)


def load_knowledge():
    documents = []

    for filename in os.listdir(KNOWLEDGE_DIR):
        if filename.endswith(".txt"):
            path = os.path.join(KNOWLEDGE_DIR, filename)

            with open(path, "r", encoding="utf-8") as file:
                content = file.read()

            documents.append(content)

    return documents


def ingest_knowledge():
    documents = load_knowledge()

    if not documents:
        print("No knowledge documents found.")
        return

    vectorstore.add_texts(
        texts=documents,
        ids=[f"knowledge_{i}" for i in range(len(documents))]
    )

    print(f"Added {len(documents)} knowledge document(s) to ChromaDB.")


def search_knowledge(question: str, k: int = 3):
    results = vectorstore.similarity_search(
        question,
        k=k
    )

    return [
        document.page_content
        for document in results
    ]


if __name__ == "__main__":
    ingest_knowledge()

    results = search_knowledge(
        "What does high revenue with low profit mean?"
    )

    print("\nRAG Search Results:\n")

    for result in results:
        print(result)
        print("-" * 50)
