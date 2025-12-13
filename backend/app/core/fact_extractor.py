def extract_facts(content: str, llm):
    prompt = f"Extract key facts, quotes, and numbers from this article: {content}"
    response = llm.generate(prompt)
    # Парсим ответ (упрощено)
    return {"facts": response.split("\n")}