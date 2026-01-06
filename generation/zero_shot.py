import json
import os
import ollama
from datetime import datetime
from backports.zoneinfo import ZoneInfo

MODEL_NAME = "llama3.2:3b"
TEMPERATURE = 0.5
MAX_TOKENS = 800

DISHES = [
    "Vegetarian Lasagne",
    "Pepperoni Pizza",
    "Chicken Burger"
]

PROMPT_TEMPLATE = (
    "Give me a clear, step-by-step recipe for {dish}.\n"
    "Include ingredients and cooking instructions.\n"
    "Return your output strictly in the following format:\n"
    "{{\"ingredients\": [\"ingredient 1\", \"ingredient 2\", ...], \"steps\": [\"step 1\", \"step 2\", ...]}}\n"
    "Do not include any text outside this JSON object."
)

OUT_PATH = "results/zero_shot.json"

def generate_recipe(dish):
    prompt = PROMPT_TEMPLATE.format(dish=dish)

    response = ollama.generate(
        model=MODEL_NAME,
        prompt=prompt,
        options={
            "temperature": TEMPERATURE,
            "num_predict": MAX_TOKENS
        }
    )

    return prompt, response["response"]

def main():
    os.makedirs("results", exist_ok=True)

    outputs = {
        "version": "pilot",
        "condition": "zero_shot",
        "model": MODEL_NAME,
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "timestamp": datetime.now(ZoneInfo("Europe/Berlin")).isoformat(),
        "results": []
    }

    for dish in DISHES:
        print(f"Generating zero shot recipe for {dish}")

        prompt, output = generate_recipe(dish)

        outputs["results"].append({
            "dish_name": dish,
            "prompt": prompt,
            "output": output
        })

    with open(OUT_PATH, "w") as f:
        json.dump(outputs, f, indent=2)

    print(f"\nSaved zero shot results to {OUT_PATH}")

if __name__ == "__main__":
    main()