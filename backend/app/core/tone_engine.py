def apply_tone(facts: dict, platform: str, llm):
    tones = {
        "telegram": "short, factual, urgent",
        "vk": "friendly, with emojis, informal",
        "business": "professional, business-focused"
    }
    tone = tones.get(platform, "default")
    prompt = f"Rewrite facts in {tone} style: {facts}"
    return llm.generate(prompt)