def format_docs(documents):
    return "\n\n".join(document.page_content for document in documents)
