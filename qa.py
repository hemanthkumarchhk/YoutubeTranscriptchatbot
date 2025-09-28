import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
SYSTEM_PROMPT = "You are a helpful assistant answering questions about a YouTube transcript."

def build_prompt(question, chunks):
    context = ""
    for i, c in enumerate(chunks, start=1):
        context += f"\n---\n[Chunk {i}] {c['metadata']['text']}"
    return f"{SYSTEM_PROMPT}\n\nContext:{context}\n\nQuestion: {question}\nAnswer:"

def answer_with_openai(openai, question, chunks, model=OPENAI_MODEL):
    prompt = build_prompt(question, chunks)
    resp = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "system", "content": SYSTEM_PROMPT},
                  {"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.2
    )
    return resp["choices"][0]["message"]["content"].strip()
