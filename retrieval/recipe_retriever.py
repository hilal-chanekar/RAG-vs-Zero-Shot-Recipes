import json
import torch
from pathlib import Path
from sentence_transformers import SentenceTransformer, util

DATA_PATH = Path("data/recipes.json")
EMBEDDINGS_CACHE_PATH = Path("data/embeddings_cache.pt")

class RecipeRetriever:
    def __init__(self, data_path=DATA_PATH, cache_path=EMBEDDINGS_CACHE_PATH):
        with open(data_path, "r") as f:
            data = json.load(f)

        self.recipes = data["recipes"]
        self.cache_path = cache_path

        # normalize ingredients and steps
        for r in self.recipes:
            if isinstance(r.get("ingredients"), str):
                r["ingredients"] = json.loads(r["ingredients"])

            if isinstance(r.get("steps"), str):
                r["steps"] = json.loads(r["steps"])

        # Build searchable documents
        self.documents = []
        for r in self.recipes:
            text = (
                r.get("dish_name", "") + " "
                + " ".join(r.get("ingredients", [])) + " "
                + " ".join(r.get("steps", []))
            )
            self.documents.append(text)

        self.model = SentenceTransformer('Alibaba-NLP/gte-large-en-v1.5', trust_remote_code=True)
        self.doc_embeddings = self._load_or_compute_embeddings()

    def _load_or_compute_embeddings(self):
        """Load cached embeddings or compute and cache them."""
        if self.cache_path.exists():
            print("Loading cached embeddings...")
            return torch.load(self.cache_path)
        
        print("Computing embeddings (this may take a while)...")
        embeddings = self.model.encode(self.documents, convert_to_tensor=True)
        
        # Ensure cache directory exists
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        torch.save(embeddings, self.cache_path)
        print(f"Embeddings cached to {self.cache_path}")
        
        return embeddings

    def retrieve(self, query, k=1):
        """
        Returns the k most similar recipes as tuples of (formatted_string, dish_id, dish_name)
        suitable for prompt injection.
        """

        query_embedding = self.model.encode(query, convert_to_tensor=True)

        scores = util.cos_sim(query_embedding, self.doc_embeddings)[0]

        best_indices = scores.argsort(descending=True)[:k].cpu().numpy()
        recipes = [self.recipes[i] for i in best_indices]

        return [
            (self.format_recipe(r), r.get("dish_id", ""), r.get("dish_name", ""))
            for r in recipes
        ]

    def format_recipe(self, recipe):
        """
        Converts a recipe dict into a readable text block
        for inclusion in the prompt.
        """
        ingredients = recipe.get("ingredients", [])
        steps = recipe.get("steps", [])

        ingredients_text = "\n".join(f"- {i}" for i in ingredients)
        steps_text = "\n".join(f"{idx+1}. {s}" for idx, s in enumerate(steps))

        formatted = (
            f"Dish Name: {recipe.get('dish_name', '')}\n"
            f"Ingredients:\n{ingredients_text}\n"
            f"Steps:\n{steps_text}"
        )

        return formatted