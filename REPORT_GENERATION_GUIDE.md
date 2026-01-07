# Experiment Report Generation Checklist

## Overview
This document outlines what data needs to be collected for generating a comprehensive experiment report similar to the reference report.

---

## ✅ Data Collection Requirements

### 1. **Experiment Metadata** (Auto-collected)
- [x] Experiment name
- [x] Condition (zero-shot, few-shot_RAG)
- [x] Model name and version
- [x] Temperature
- [x] Max tokens
- [x] Retrieval model (if RAG)
- [x] Number of retrieved items (k)
- [x] Start timestamp
- [x] End timestamp
- [x] Total duration (seconds)
- [x] Number of samples processed

**Collected via**: `evaluation/experiment_logger.py`  
**Output**: `results/metadata_[condition]_[timestamp].json`

---

### 2. **Generation Results** (Already Available)
- [x] Input prompts
- [x] Generated outputs
- [x] Retrieved recipes (for RAG)
- [x] Recipe names/IDs
- [x] Model configuration

**Current location**: 
- `results/zero_shot.json`
- `results/few_shot_RAG.json`

---

### 3. **Quality Metrics** (Auto-calculated)
- [x] Number of ingredients per recipe
- [x] Number of steps per recipe
- [x] JSON parsing errors
- [x] Valid vs invalid outputs

**Calculated via**: `evaluation/metrics_calculator.py`  
**Output**: `results/metrics_comparison.json`

---

### 4. **Retrieval Performance** (Optional for baseline)
For a more detailed report, consider adding:
- [ ] Similarity scores of retrieved recipes
- [ ] Top-k retrieval accuracy
- [ ] Recipe category matching

**Location**: `retrieval/recipe_retriever.py` (can extend if needed)

---

### 5. **Evaluation Metrics** (Optional - Requires additional scripts)
Advanced metrics for a richer report:
- [ ] Ingredient overlap between generated and retrieved recipes
- [ ] Novel ingredients introduced (hallucinations)
- [ ] Semantic similarity to base recipe
- [ ] Constraint violations (if task-specific)

**Future**: Create `evaluation/semantic_evaluator.py` if needed

---

## 📋 Report Structure (How data will be used)

```
EXPERIMENT REPORT
├── Executive Summary
│   ├── Key findings from metrics_comparison.json
│   ├── Duration from metadata JSON
│   └── Sample count
├── Research Question & Hypothesis
│   └── Auto-inserted from template
├── Experiment Design
│   ├── Task description
│   ├── Conditions (from metadata)
│   ├── Controlled variables
│   └── Dataset info (from recipes.json)
├── Dataset
│   ├── Source: recipes.json
│   ├── Total recipes
│   ├── Categories
│   └── Filtering criteria
├── Retrieval Method
│   ├── Model: gte-large-en-v1.5 (from metadata)
│   ├── k value (from metadata)
│   └── Similarity metric
├── Evaluation Metrics
│   └── Quality metrics (from metrics_comparison.json)
├── Results
│   ├── Summary statistics
│   ├── Comparison table (zero-shot vs RAG)
│   ├── Key findings
│   └── Charts/visualizations (optional)
├── Experiment Details
│   ├── Runtime (from metadata)
│   ├── Model configuration
│   ├── Completion date
│   └── Number of LLM calls
├── Limitations
│   └── Auto-inserted
├── Next Steps
│   └── Auto-inserted
├── Reproducibility
│   ├── Model details (from metadata)
│   ├── Code locations
│   ├── Random seed info
│   └── Results files
└── Appendices
    ├── Prompt templates (from generation/*.py)
    └── Sample outputs (from results/*.json)
```

---

## 🚀 How to Run Experiments

### Step 1: Run both conditions with logging
```bash
cd /Users/hilal/Documents/Python Projects/NLP/RAG-vs-Zero-Shot-Recipes
source .venv/bin/activate
PYTHONPATH="$PWD" python evaluation/run_experiments.py --condition both --compare
```

This will:
- ✅ Run zero-shot generation
- ✅ Run few-shot RAG generation
- ✅ Collect timing metadata
- ✅ Save metadata JSONs
- ✅ Calculate comparison metrics
- ✅ Save metrics report

### Step 2: Verify outputs
```
results/
├── zero_shot.json              ← Generation results
├── few_shot_RAG.json           ← Generation results
├── metadata_zero_shot_[ts].json ← Timing & config
├── metadata_few_shot_RAG_[ts].json ← Timing & config
└── metrics_comparison.json     ← Quality metrics
```

### Step 3: Generate report
Once experiments complete, prompt:
```
"Generate the experiment report using the data from results/ folder"
```

---

## 📊 Data Available NOW

### Already in repo:
- ✅ Prompt templates (generation/*.py)
- ✅ Model configuration
- ✅ Recipe dataset (recipes.json, ~1000 recipes)
- ✅ Retrieval method (recipe_retriever.py)
- ✅ Generation results (results/*.json)

### Will be created after experiments:
- ⏳ Timing metadata
- ⏳ Quality metrics
- ⏳ Comparison analysis

---

## 🎯 Next Steps

1. **Run the experiments** using the command above
2. **Verify all output files** exist in `results/`
3. **Prompt to generate report** with all collected data

The system is now ready to generate a comprehensive report after you run the experiments!
