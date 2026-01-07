"""
Unified experiment runner for both zero-shot and RAG conditions.
Collects timing, logging, and metrics for comprehensive report generation.
"""

import json
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from evaluation.experiment_logger import ExperimentMetadata, ExperimentTimer, save_experiment_metadata
from evaluation.metrics_calculator import MetricsCalculator, compare_conditions, save_metrics_report
from generation.zero_shot import main as run_zero_shot, MODEL_NAME as ZS_MODEL, TEMPERATURE, MAX_TOKENS, DISHES
from retrieval.recipe_retriever import RecipeRetriever

def run_experiment_with_logging(condition: str, num_samples: int = None):
    """
    Run an experiment (zero-shot or RAG) with full logging.
    
    Args:
        condition: "zero_shot" or "few_shot_RAG"
        num_samples: number of samples (defaults to using all DISHES)
    """
    
    if num_samples is None:
        num_samples = len(DISHES)
    
    # Prepare metadata
    if condition == "zero_shot":
        metadata = ExperimentMetadata(
            experiment_name="Zero-Shot Recipe Generation",
            condition="zero_shot",
            model=ZS_MODEL,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            retrieval_model=None,
            k_retrieval=None,
            num_samples=num_samples
        )
    elif condition == "few_shot_RAG":
        retriever = RecipeRetriever()
        metadata = ExperimentMetadata(
            experiment_name="Few-Shot RAG Recipe Generation",
            condition="few_shot_RAG",
            model=ZS_MODEL,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            retrieval_model="Alibaba-NLP/gte-large-en-v1.5",
            k_retrieval=1,
            num_samples=num_samples
        )
    else:
        raise ValueError(f"Unknown condition: {condition}")
    
    # Run with timing
    with ExperimentTimer(metadata) as timer:
        if condition == "zero_shot":
            run_zero_shot()
        elif condition == "few_shot_RAG":
            from generation.few_shot_RAG import main as run_rag
            run_rag()
    
    # Save metadata
    save_experiment_metadata(metadata)
    
    return metadata

def compare_experiment_results():
    """Compare zero-shot and RAG results and generate metrics report."""
    zero_shot_path = Path("results/zero_shot.json")
    rag_path = Path("results/few_shot_RAG.json")
    
    if not zero_shot_path.exists():
        print(f"❌ Missing: {zero_shot_path}")
        return None
    
    if not rag_path.exists():
        print(f"❌ Missing: {rag_path}")
        return None
    
    print("\n📊 Comparing results...")
    comparison = compare_conditions(zero_shot_path, rag_path)
    save_metrics_report(comparison)
    
    return comparison

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run RAG experiments with logging")
    parser.add_argument("--condition", choices=["zero_shot", "few_shot_RAG", "both"],
                        default="both", help="Which condition to run")
    parser.add_argument("--compare", action="store_true", 
                        help="Compare results after running experiments")
    
    args = parser.parse_args()
    
    if args.condition in ["zero_shot", "both"]:
        print("🚀 Running zero-shot experiment...")
        run_experiment_with_logging("zero_shot")
    
    if args.condition in ["few_shot_RAG", "both"]:
        print("🚀 Running few-shot RAG experiment...")
        run_experiment_with_logging("few_shot_RAG")
    
    if args.compare or args.condition == "both":
        compare_experiment_results()
