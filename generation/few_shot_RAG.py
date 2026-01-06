import json
import os
import ollama
from datetime import datetime
from backports.zoneinfo import ZoneInfo
from retrieval.recipe_retriever import RecipeRetriever

MODEL_NAME = "llama3.2:3b"
TEMPERATURE = 0.5
MAX_TOKENS = 800

DISHES = [
    "Vegetarian Lasagne",
    "Pepperoni Pizza",
    "Chicken Burger"
]

OUT_PATH = "results/few_shot_RAG.json"

PROMPT_TEMPLATE = (
    "Give me a clear, step-by-step recipe for {dish}.\n"
    "Below is a similar recipe for reference.\n"
    "Use it only as inspiration. Do not copy it verbatim.\n\n"
    "REFERENCE RECIPE:\n"
    "{retrieved_recipe}\n\n"
    "Return your output strictly in the following format:\n"
    "{{\"ingredients\": [\"ingredient 1\", \"ingredient 2\", ...], \"steps\": [\"step 1\", \"step 2\", ...]}}\n"
    "Do not include any text outside this JSON object."
)

def generate_recipe(dish, retriever):
    retrieved_text, retrieved_id, retrieved_name = retriever.retrieve(dish, k=1)[0]

    prompt = PROMPT_TEMPLATE.format(
        dish=dish,
        retrieved_recipe=retrieved_text
    )

    response = ollama.generate(
        model=MODEL_NAME,
        prompt=prompt,
        options={
            "temperature": TEMPERATURE,
            "num_predict": MAX_TOKENS
        }
    )

    return prompt, retrieved_id, retrieved_name, response["response"]

def main():
    os.makedirs("results", exist_ok=True)

    retriever = RecipeRetriever()

    outputs = {
        "version": "pilot",
        "condition": "few_shot_RAG",
        "model": MODEL_NAME,
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "timestamp": datetime.now(ZoneInfo("Europe/Berlin")).isoformat(),
        "results": []
    }

    for dish in DISHES:
        print(f"Generating few-shot RAG recipe for {dish}")

        prompt, retrieved_id, retrieved_name, output = generate_recipe(dish, retriever)

        outputs["results"].append({
            "dish_name": dish,
            "prompt": prompt,
            "retrieved_recipe_id": retrieved_id,
            "retrieved_dish_name": retrieved_name,
            "output": output
        })

    with open(OUT_PATH, "w") as f:
        json.dump(outputs, f, indent=2)

    print(f"\nSaved few-shot RAG results to {OUT_PATH}")

if __name__ == "__main__":
    main()