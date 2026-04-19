def build_prompt(query, context):
    context_text = "\n\n".join(context)

    return f"""
You are a helpful AI assistant.

Answer the question using ONLY the context below.
If the answer is not in the context, say you don't know.

Context:
{context_text}

Question:
{query}

Answer:
"""