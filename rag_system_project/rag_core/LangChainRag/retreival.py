from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from sklearn.metrics import precision_score, recall_score, f1_score

def load_chroma_db(persist_directory="docs/chroma/"):
    """
    Load the ChromaDB vector store from the specified directory.

    Args:
        persist_directory (str): Directory where the ChromaDB is stored.

    Returns:
        Chroma: The loaded ChromaDB vector store.
    """
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    return vectordb

def retrieve_similar_documents(query, vectordb, top_k=5):
    """
    Retrieve the most similar documents to the query from the vector store.

    Args:
        query (str): The query string.
        vectordb (Chroma): The ChromaDB vector store.
        top_k (int): Number of top similar documents to retrieve.

    Returns:
        list: List of retrieved documents.
    """
    results = vectordb.similarity_search(query, k=top_k)
    return results

def evaluate_retrieval(test_queries, vectordb, top_k=5):
    """
    Evaluate the retrieval system using precision, recall, and F1 score.

    Args:
        test_queries (list): List of queries with ground truth.
        vectordb (Chroma): The ChromaDB vector store.
        top_k (int): Number of top results to retrieve.

    Returns:
        dict: Precision, recall, and F1 score for each query.
    """
    results = []
    for test_query in test_queries:
        query = test_query["query"]
        relevant_docs = set(test_query["relevant_docs"])
        
        # Retrieve top_k results
        retrieved_docs = vectordb.similarity_search(query, k=top_k)
        retrieved_ids = set([doc.metadata["id"] for doc in retrieved_docs])
        
        # Calculate precision, recall, and F1
        true_positives = len(relevant_docs & retrieved_ids)
        precision = true_positives / len(retrieved_ids) if retrieved_ids else 0
        recall = true_positives / len(relevant_docs) if relevant_docs else 0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0
        
        results.append({
            "query": query,
            "precision": precision,
            "recall": recall,
            "f1": f1
        })
    
    return results

# Example usage:
if __name__ == "__main__":
    # Load the ChromaDB
    persist_directory = "docs/chroma/"
    vectordb = load_chroma_db(persist_directory)

    # Define a query
    query = "机器学习相关的内容"

    # Retrieve similar documents
    top_k = 3
    results = retrieve_similar_documents(query, vectordb, top_k)

    # Print the results
    print(f"Top {top_k} similar documents:")
    for i, result in enumerate(results):
        print(f"\n--- Result {i+1} ---")
        print(result.page_content)

    # Evaluation
    test_queries = [
        {"query": "机器学习相关的内容", "relevant_docs": [1, 2, 3]},
        {"query": "深度学习的应用", "relevant_docs": [4, 5]},
    ]
    evaluation_results = evaluate_retrieval(test_queries, vectordb, top_k=3)
    for result in evaluation_results:
        print(result)