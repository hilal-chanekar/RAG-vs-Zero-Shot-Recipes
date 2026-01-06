import json
import os
import pandas as pd
import random

# Configuration
TOTAL_RECIPES = 1000
RANDOM_SEED = 42

# Categories for diverse sampling (keyword -> category name)
# Recipes will be sampled proportionally from each category
CATEGORIES = {
    "chicken": ["chicken", "poultry"],
    "beef": ["beef", "steak"],
    "pork": ["pork", "bacon", "ham", "sausage"],
    "seafood": ["fish", "salmon", "shrimp", "tuna", "seafood", "crab", "lobster"],
    "vegetarian": ["vegetable", "veggie", "vegan", "tofu", "lentil", "bean"],
    "pasta": ["pasta", "spaghetti", "lasagna", "lasagne", "noodle", "macaroni"],
    "soup": ["soup", "stew", "chowder", "broth"],
    "salad": ["salad"],
    "dessert": ["cake", "cookie", "pie", "brownie", "chocolate", "ice cream", "dessert"],
    "bread": ["bread", "muffin", "biscuit", "roll", "loaf"],
    "breakfast": ["pancake", "waffle", "omelette", "omelet", "egg", "breakfast"],
    "rice": ["rice", "risotto", "fried rice"],
    "pizza": ["pizza"],
    "sandwich": ["sandwich", "wrap", "burger"],
    "other": []  # Catch-all for unmatched recipes
}

def categorize_recipe(title):
    """Assign a recipe to a category based on title keywords."""
    title_lower = title.lower()
    for category, keywords in CATEGORIES.items():
        if category == "other":
            continue
        for keyword in keywords:
            if keyword in title_lower:
                return category
    return "other"

def filter_quality_recipes(df):
    """Filter for recipes with reasonable complexity."""
    def count_items(s):
        try:
            return len(json.loads(s))
        except:
            return 0
    
    df = df.copy()
    df['n_ingredients'] = df['ingredients'].apply(count_items)
    df['n_steps'] = df['directions'].apply(count_items)
    
    # Keep recipes with 4-20 ingredients and 3-15 steps
    quality = df[(df['n_ingredients'] >= 4) & (df['n_ingredients'] <= 20) & 
                 (df['n_steps'] >= 3) & (df['n_steps'] <= 15)]
    
    return quality

def sample_diverse_recipes(df, total=TOTAL_RECIPES):
    """Sample recipes with category diversity."""
    random.seed(RANDOM_SEED)
    
    # Categorize all recipes
    df = df.copy()
    df['category'] = df['title'].apply(categorize_recipe)
    
    # Count per category
    category_counts = df['category'].value_counts()
    print("\nRecipes per category (before sampling):")
    for cat, count in category_counts.items():
        print(f"  {cat}: {count}")
    
    # Calculate samples per category (proportional)
    non_other_categories = [c for c in CATEGORIES.keys() if c != "other"]
    
    if total < len(non_other_categories):
        raise ValueError(f"total recipes ({total}) must be >= number of categories ({len(non_other_categories)})")
    
    base_per_category = total // len(non_other_categories)
    
    sampled = []
    total_sampled = 0
    
    for category in non_other_categories:
        cat_recipes = df[df['category'] == category]
        n_sample = min(base_per_category, len(cat_recipes))
        if n_sample > 0:
            sampled.append(cat_recipes.sample(n=n_sample, random_state=RANDOM_SEED))
            total_sampled += n_sample
            print(f"  Sampled {n_sample} from {category}")
    
    # Fill remaining from "other" category
    remaining = total - total_sampled
    if remaining > 0:
        other_recipes = df[df['category'] == 'other']
        n_sample = min(remaining, len(other_recipes))
        if n_sample > 0:
            sampled.append(other_recipes.sample(n=n_sample, random_state=RANDOM_SEED))
            print(f"  Sampled {n_sample} from other")
    
    return pd.concat(sampled, ignore_index=True)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(script_dir, "full_dataset.csv")
    
    print(f"Loading dataset from {dataset_path}...")
    dataset = pd.read_csv(dataset_path, delimiter=',')
    
    # Filter to Recipes1M source only
    dataset = dataset[dataset['source'] == "Recipes1M"]
    print(f"Recipes1M recipes: {len(dataset)}")
    
    # Filter for quality
    quality_df = filter_quality_recipes(dataset)
    print(f"Quality filtered recipes with 4-20 ingredients and 3-15 steps: {len(quality_df)}")
    
    # Sample diverse recipes
    sampled_df = sample_diverse_recipes(quality_df, TOTAL_RECIPES)
    print(f"\nTotal sampled recipes: {len(sampled_df)}")
    
    # Build output
    recipes_out = {
        "version": "pilot",
        "total_recipes": len(sampled_df),
        "recipes": []
    }
    
    for _, row in sampled_df.iterrows():
        dish_id = str(row['Unnamed: 0'])
        
        recipes_out["recipes"].append({
            "dish_id": dish_id,
            "dish_name": row["title"],
            "category": row["category"],
            "ingredients": row["ingredients"],
            "steps": row["directions"]
        })

    out_path = os.path.join(script_dir, "recipes.json")
    
    with open(out_path, "w") as f:
        json.dump(recipes_out, f, indent=2)

    print(f"\nSaved {len(recipes_out['recipes'])} recipes to {out_path}")
    
    # Print category distribution in final output
    from collections import Counter
    cats = Counter(r['category'] for r in recipes_out['recipes'])
    print("\nFinal category distribution:")
    for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")

if __name__ == "__main__":
    main()