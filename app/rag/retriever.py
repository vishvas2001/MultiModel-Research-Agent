from app.rag.vectorstore import load_vectorstore

vectorstore = None


def get_vectorstore():
    global vectorstore

    if vectorstore is None:
        print("[Retriever] Loading vectorstore...")
        vectorstore = load_vectorstore()

    return vectorstore


def retrieve(query: str, k: int = 3):
    vs = get_vectorstore()

    results = vs.similarity_search_with_score(query, k=k)

    contexts = []
    scores = []

    for doc, score in results:
        contexts.append(" ".join(doc.page_content.split()))
        scores.append(float(score))

    return {
        "contexts": contexts,
        "scores": scores
    }