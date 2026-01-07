#!/usr/bin/env python3
"""
Verification script to ensure all report generation infrastructure is ready.
"""

from pathlib import Path
import sys

def check_file(path, description):
    """Check if a file exists and report status."""
    if path.exists():
        print(f"✅ {description}: {path}")
        return True
    else:
        print(f"❌ {description}: {path}")
        return False

def main():
    print("\n" + "="*70)
    print("REPORT GENERATION INFRASTRUCTURE VERIFICATION")
    print("="*70 + "\n")
    
    base_path = Path(__file__).parent
    all_good = True
    
    # Check new evaluation scripts
    print("📋 NEW EVALUATION SCRIPTS:")
    scripts = [
        (base_path / "evaluation" / "experiment_logger.py", "Experiment logger"),
        (base_path / "evaluation" / "metrics_calculator.py", "Metrics calculator"),
        (base_path / "evaluation" / "run_experiments.py", "Experiment runner"),
    ]
    
    for path, desc in scripts:
        all_good &= check_file(path, desc)
    
    # Check generation scripts
    print("\n📝 GENERATION SCRIPTS:")
    gen_scripts = [
        (base_path / "generation" / "zero_shot.py", "Zero-shot generation"),
        (base_path / "generation" / "few_shot_RAG.py", "Few-shot RAG generation"),
    ]
    
    for path, desc in gen_scripts:
        all_good &= check_file(path, desc)
    
    # Check data
    print("\n📊 DATA & CONFIGURATION:")
    data_files = [
        (base_path / "data" / "recipes.json", "Recipe dataset"),
        (base_path / "data" / "embeddings_cache.pt", "Embedding cache"),
        (base_path / "retrieval" / "recipe_retriever.py", "Retrieval system"),
    ]
    
    for path, desc in data_files:
        all_good &= check_file(path, desc)
    
    # Check results directory
    print("\n📂 RESULTS DIRECTORY:")
    results_dir = base_path / "results"
    if results_dir.exists():
        print(f"✅ Results directory exists: {results_dir}")
        results_files = list(results_dir.glob("*.json"))
        print(f"   Found {len(results_files)} JSON files:")
        for f in results_files:
            print(f"   - {f.name}")
    else:
        print(f"❌ Results directory missing: {results_dir}")
        all_good = False
    
    # Check guides
    print("\n📖 DOCUMENTATION:")
    guides = [
        (base_path / "REPORT_GENERATION_GUIDE.md", "Report generation guide"),
        (base_path / "REPORT_SETUP_READY.md", "Setup ready status"),
    ]
    
    for path, desc in guides:
        all_good &= check_file(path, desc)
    
    # Final status
    print("\n" + "="*70)
    if all_good:
        print("✅ ALL SYSTEMS READY FOR REPORT GENERATION")
        print("\n📌 Next step: Run experiments with")
        print("   python evaluation/run_experiments.py --condition both --compare")
    else:
        print("⚠️  Some files are missing. Check paths above.")
        sys.exit(1)
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
