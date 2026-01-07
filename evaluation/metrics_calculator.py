"""
Metrics calculation and comparison for report generation.
Compares zero-shot vs RAG-enhanced recipe generation.
"""

import json
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class RecipeMetrics:
    """Metrics for a single recipe."""
    dish_name: str
    num_ingredients: int
    num_steps: int
    has_json_error: bool = False  # if output couldn't be parsed
    error_message: str = None

class MetricsCalculator:
    """Calculate metrics from generation results."""
    
    def __init__(self, results_file: Path):
        """Load results from JSON file."""
        with open(results_file, "r") as f:
            self.results = json.load(f)
        self.condition = self.results.get("condition", "unknown")
    
    def calculate_recipe_metrics(self) -> List[RecipeMetrics]:
        """Extract and calculate metrics for each recipe."""
        metrics = []
        
        for result in self.results.get("results", []):
            dish_name = result.get("dish_name", "unknown")
            output = result.get("output", "{}")
            
            try:
                # Parse JSON output
                parsed = json.loads(output)
                ingredients = parsed.get("ingredients", [])
                steps = parsed.get("steps", [])
                
                metric = RecipeMetrics(
                    dish_name=dish_name,
                    num_ingredients=len(ingredients),
                    num_steps=len(steps),
                    has_json_error=False
                )
            except (json.JSONDecodeError, ValueError) as e:
                metric = RecipeMetrics(
                    dish_name=dish_name,
                    num_ingredients=0,
                    num_steps=0,
                    has_json_error=True,
                    error_message=str(e)
                )
            
            metrics.append(metric)
        
        return metrics
    
    def get_summary_stats(self) -> Dict:
        """Get summary statistics."""
        metrics = self.calculate_recipe_metrics()
        
        valid_metrics = [m for m in metrics if not m.has_json_error]
        error_count = len([m for m in metrics if m.has_json_error])
        
        if not valid_metrics:
            return {
                "condition": self.condition,
                "total_recipes": len(metrics),
                "parsing_errors": error_count,
                "valid_recipes": 0,
                "avg_ingredients": 0,
                "avg_steps": 0
            }
        
        avg_ingredients = sum(m.num_ingredients for m in valid_metrics) / len(valid_metrics)
        avg_steps = sum(m.num_steps for m in valid_metrics) / len(valid_metrics)
        
        return {
            "condition": self.condition,
            "total_recipes": len(metrics),
            "parsing_errors": error_count,
            "valid_recipes": len(valid_metrics),
            "avg_ingredients": round(avg_ingredients, 2),
            "avg_steps": round(avg_steps, 2),
            "min_ingredients": min(m.num_ingredients for m in valid_metrics),
            "max_ingredients": max(m.num_ingredients for m in valid_metrics),
            "min_steps": min(m.num_steps for m in valid_metrics),
            "max_steps": max(m.num_steps for m in valid_metrics)
        }

def compare_conditions(zero_shot_file: Path, rag_file: Path) -> Dict:
    """Compare metrics between zero-shot and RAG conditions."""
    calc_zero = MetricsCalculator(zero_shot_file)
    calc_rag = MetricsCalculator(rag_file)
    
    stats_zero = calc_zero.get_summary_stats()
    stats_rag = calc_rag.get_summary_stats()
    
    return {
        "zero_shot": stats_zero,
        "few_shot_RAG": stats_rag,
        "comparison": {
            "ingredient_delta": round(stats_rag["avg_ingredients"] - stats_zero["avg_ingredients"], 2),
            "step_delta": round(stats_rag["avg_steps"] - stats_zero["avg_steps"], 2),
            "error_difference": stats_rag["parsing_errors"] - stats_zero["parsing_errors"]
        }
    }

def save_metrics_report(metrics_dict: Dict, output_path: Path = Path("results/metrics_comparison.json")):
    """Save metrics comparison to JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(metrics_dict, f, indent=2)
    print(f"Metrics report saved to: {output_path}")
    return output_path

# Usage example
if __name__ == "__main__":
    zero_shot_path = Path("results/zero_shot.json")
    rag_path = Path("results/few_shot_RAG.json")
    
    if zero_shot_path.exists() and rag_path.exists():
        comparison = compare_conditions(zero_shot_path, rag_path)
        save_metrics_report(comparison)
        
        print("\n" + "="*60)
        print("METRICS SUMMARY")
        print("="*60)
        print(json.dumps(comparison, indent=2))
