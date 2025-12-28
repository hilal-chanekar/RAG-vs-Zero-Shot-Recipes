# RecipeRAG: Evaluating Grounded Generation in Culinary Tasks

This repository contains the experimental setup, dataset, and evaluation scripts for investigating the question **Does retrieval-augmented generation improve the quality and factual accuracy of LLM-generated recipes?**

## Motivation
LLMs often struggle with "culinary hallucinations"—suggesting impossible cooking times, nonsensical ingredient ratios, or missing critical steps. This project tests whether providing "cases" (similar recipes) as context grounds the LLM’s output in reality.

## Experimental Design
Two recipe generation conditions are compared:

| Condition | Description | Prompt Strategy |
| :--- | :--- | :--- |
| **A: Baseline** | Zero-shot generation | Internal knowledge only (Dish + Ingredients) |
| **B: RAG-Enhanced** | Few-shot with context | Request + $k$ similar recipes retrieved from a Case Base |

<!--## Evaluation Metrics
To measure "Quality" and "Factual Accuracy," the following are used:
- **Ingredient Coverage:** Percentage of required ingredients correctly utilized in instructions.
- **Factual Grounding:** Presence of "impossible" instructions (checked via LLM-as-a-judge).
- **Culinary Coherence:** Logical flow and step-by-step feasibility.
- **Semantic Similarity:** BERTScore/ROUGE comparison against original dataset ground truth.-->

## Project Structure
```text
├── data/               # Recipe case base (e.g., Recipe1M+)
├── retrieval/          # Retrieval algorithm
├── generation/         # LLM pipeline (Condition A vs B)
├── evaluation/         # Scoring scripts (TBD)
├── results/            # CSVs of generated recipes and scores
