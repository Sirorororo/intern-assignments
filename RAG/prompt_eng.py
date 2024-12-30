def build_prompt(query,top_k):
    formatted_input = "Context:\n"
    for idx, result in enumerate(top_k, 1):
        formatted_input += f"{idx}. {result}\n"

    full_prompt = f"""
    You are given a context based on a paper or document. Your task is to answer the following question based on the provided context. 
    If the context does not contain relevant information, please respond with "I cannot answer based on the given context."

    {formatted_input}

    Question:
    {query}

    Instructions:
    - Identify the most relevant points from Context to answer the question and provide a concise, clear and relevant answer based on it.
    - If the query is communicative then reply to that query only using your communicative skills.
    """

    return full_prompt

def generate_response(cohere_client,full_prompt):
    response = cohere_client.generate(
        model="command",
        prompt=full_prompt,
        max_tokens=1000
    )
    return response.generations[0].text
