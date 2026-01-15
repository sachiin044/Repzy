def route_question(question: str):
    q = question.lower().strip()

    structural_phrases = [
        "list files",
        "directory structure",
        "repo structure",
        "how many files",
        "how many functions",
        "functions in",
        "classes in"
    ]

    content_phrases = [
        "show code",
        "give code",
        "print code",
        "full code"
    ]

    explanatory_phrases = [
        "what does",
        "what is the purpose",
        "explain",
        "how does"
    ]

    # 1️⃣ Explanatory (highest priority)
    for p in explanatory_phrases:
        if p in q:
            return "SEMANTIC"

    # 2️⃣ Content
    for p in content_phrases:
        if p in q:
            return "CONTENT"

    # 3️⃣ Structural
    for p in structural_phrases:
        if p in q:
            return "STRUCTURAL"

    # Default → semantic reasoning
    return "SEMANTIC"
