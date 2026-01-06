## Project Overview
This is an NLP research project comparing **zero-shot** vs **RAG-enhanced** (few-shot) recipe generation using Ollama with `llama3.2:3b`. The goal is to evaluate whether retrieval-augmented generation reduces "culinary hallucinations" in LLM outputs.

## Data

### Source Dataset
This project uses the **RecipeNLG** dataset (2.2M recipes). The full dataset (`full_dataset.csv`, ~2.2GB) is not included in this repository due to size limits.

**To obtain the data:**
1. Download from [Kaggle: RecipeNLG](https://www.kaggle.com/datasets/saldenisov/recipenlg) or the [original source](https://recipenlg.cs.put.poznan.pl/dataset)
2. Place `full_dataset.csv` in the `data/` folder
3. Run `python data/extract_recipes.py` to generate the curated `recipes.json`

### Included Data
- `data/recipes.json`: Curated 1000 recipes (71 per category × 14 categories) filtered from Recipes1M subset
- Categories: chicken, beef, pork, seafood, vegetarian, pasta, soup, salad, dessert, bread, breakfast, rice, pizza, sandwich

### Citation
```bibtex
@inproceedings{bien-etal-2020-recipenlg,
    title = "{R}ecipe{NLG}: A Cooking Recipes Dataset for Semi-Structured Text Generation",
    author = "Bie{\'n}, Micha{\l} and Gilski, Micha{\l} and Maciejewska, Martyna and Taisner, Wojciech and Wisniewski, Dawid and Lawrynowicz, Agnieszka",
    booktitle = "Proceedings of the 13th International Conference on Natural Language Generation",
    year = "2020"
}
```

## Architecture & Data Flow
```
data/recipes.json → retrieval/recipe_retriever.py → generation/{zero_shot,few_shot_RAG}.py → results/*.json
```

1. **Case Base** (`data/recipes.json`): Ground-truth recipes extracted from Recipes1M dataset
2. **Retriever** (`retrieval/recipe_retriever.py`): Uses `sentence-transformers/all-MiniLM-L6-v2` for semantic similarity search
3. **Generation**: Two conditions:
   - `zero_shot.py`: LLM generates from internal knowledge only
   - `few_shot_RAG.py`: LLM gets k=1 similar recipe as context
4. **Results**: JSON files with prompts, outputs, and metadata

## Key Patterns

### LLM Output Format
All generation scripts expect structured JSON output:
```json
{"ingredients": ["..."], "steps": ["..."]}
```
Prompts explicitly request this format—maintain this pattern when adding new generation conditions.

### Adding New Dishes
Edit the `DISHES` list in generation scripts. For RAG, ensure similar recipes exist in `data/recipes.json`:
```python
DISHES = ["Vegetarian Lasagne", "Pepperoni Pizza", "Chicken Burger"]
```

### Retrieval API
```python
from retrieval.recipe_retriever import RecipeRetriever
retriever = RecipeRetriever()
similar_recipes = retriever.retrieve("Chicken Curry", k=1)  # Returns formatted strings
```

## Running Experiments

### Prerequisites
- Ollama running locally with `llama3.2:3b` model pulled
- Python dependencies: `ollama`, `sentence-transformers`, `backports.zoneinfo`

### Commands
```bash
# Run from project root
python generation/zero_shot.py      # Outputs to results/zero_shot.json
python generation/few_shot_RAG.py   # Outputs to results/few_shot_RAG.json

# Rebuild case base from full dataset
python data/extract_recipes.py      # Requires data/full_dataset.csv
```

## Conventions
- **Model config**: `TEMPERATURE = 0.5`, `MAX_TOKENS = 800` (defined per-script)
- **Timestamps**: Use `Europe/Berlin` timezone via `backports.zoneinfo`
- **dish_id format**: lowercase with underscores (`chicken_burger`)
- **Results metadata**: Include `version`, `condition`, `model`, `temperature`, `timestamp`

## Evaluation (TBD)
The `evaluation/` directory is a placeholder for scoring scripts. Planned metrics from README:
- Ingredient coverage, factual grounding, culinary coherence, semantic similarity (BERTScore/ROUGE)