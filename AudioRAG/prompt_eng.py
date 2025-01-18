from spellchecker import SpellChecker

def search_word_in_sentence(sentence,target_words,replace="summary or abstract"):
    spell = SpellChecker()
    words = sentence.split()
    corrected_words = [spell.correction(word) if spell.correction(word) is not None else word for word in words]
    print(corrected_words)
    corrected_sentence = " ".join(corrected_words)
    for target_word in target_words:
        if target_word in corrected_sentence.lower():
            corrected_sentence = corrected_sentence.replace(target_word,replace)
    return corrected_sentence


def build_prompt(query_raw,top_k):
    formatted_input = "Context:\n"
    for idx, result in enumerate(top_k, 1):
        formatted_input += f"{idx}. {result}\n"

    full_prompt = f"""
    You are given a context based on a paper or document. Your task is to answer the following question based on the provided context and document. 

    {formatted_input}

    Question:
    {query_raw}

    Instructions:
    - If the query is communicative, then reply to that query only using your communicative skills.
    - If the context does not contain relevant information, respond with "I cannot answer based on the given context."
    - Use only the most relevant points from the context to answer the question.
    - Provide a concise, clear, and relevant answer based on those context.

    """

    return full_prompt

def generate_response(cohere_client,full_prompt):
    response = cohere_client.generate(
        model="command",
        prompt=full_prompt,
        max_tokens=500
    )
    return response.generations[0].text
