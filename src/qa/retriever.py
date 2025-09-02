def get_retriever(vectorstore, k=3):
    """Return retriever from vectorstore."""
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    return retriever
