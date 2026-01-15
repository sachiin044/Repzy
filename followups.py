from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate


FOLLOWUP_PROMPT = """
You are an expert developer assistant.

Given the user's question and the answer provided,
generate EXACTLY 3 engaging follow-up questions.

Rules:
- Questions must be directly related to the repository/code.
- They should encourage deeper exploration.
- Make them natural, curious, and click-worthy.
- Do NOT repeat the original question.
- Do NOT include numbering or bullet points.
- Each question must end with a '?'.

User Question:
{question}

Answer:
{answer}

Return ONLY the questions, one per line.
"""


def generate_followups(question: str, answer: str):
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7  # creativity dial
    )

    prompt = PromptTemplate(
        input_variables=["question", "answer"],
        template=FOLLOWUP_PROMPT
    )

    response = llm.invoke(
        prompt.format(question=question, answer=answer)
    ).content

    followups = [
        line.strip()
        for line in response.split("\n")
        if line.strip().endswith("?")
    ]

    # Hard guarantee: always return 3
    return followups[:3]
