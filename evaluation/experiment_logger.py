"""
Experiment logging and timing utilities for report generation.
Tracks runtime, model configs, and experiment metadata.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from backports.zoneinfo import ZoneInfo
from dataclasses import dataclass, asdict

@dataclass
class ExperimentMetadata:
    """Metadata for a single experiment run."""
    experiment_name: str
    condition: str  # e.g., "zero_shot", "few_shot_RAG"
    model: str
    temperature: float
    max_tokens: int
    retrieval_model: str = None  # e.g., "gte-large-en-v1.5" or None for zero-shot
    k_retrieval: int = None  # number of retrieved items
    start_time: str = None
    end_time: str = None
    total_duration_seconds: float = None
    num_samples: int = None
    timezone: str = "Europe/Berlin"
    
    def to_dict(self):
        return asdict(self)

class ExperimentTimer:
    """Context manager for timing experiments."""
    
    def __init__(self, metadata: ExperimentMetadata):
        self.metadata = metadata
        self.start_time = None
        self.end_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        tz = ZoneInfo(self.metadata.timezone)
        self.metadata.start_time = datetime.now(tz).isoformat()
        print(f"\n{'='*60}")
        print(f"Started: {self.metadata.experiment_name}")
        print(f"Condition: {self.metadata.condition}")
        print(f"Start time: {self.metadata.start_time}")
        print(f"{'='*60}\n")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        tz = ZoneInfo(self.metadata.timezone)
        self.metadata.end_time = datetime.now(tz).isoformat()
        self.metadata.total_duration_seconds = self.end_time - self.start_time
        
        hours, remainder = divmod(self.metadata.total_duration_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        print(f"\n{'='*60}")
        print(f"Completed: {self.metadata.experiment_name}")
        print(f"Condition: {self.metadata.condition}")
        print(f"End time: {self.metadata.end_time}")
        print(f"Duration: {int(hours)}h {int(minutes)}m {seconds:.1f}s")
        if self.metadata.num_samples:
            avg_time = self.metadata.total_duration_seconds / self.metadata.num_samples
            print(f"Avg time per sample: {avg_time:.2f}s")
        print(f"{'='*60}\n")

def save_experiment_metadata(metadata: ExperimentMetadata, output_dir: Path = Path("results")):
    """Save experiment metadata to JSON for report generation."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create filename with timestamp
    timestamp = datetime.now(ZoneInfo("Europe/Berlin")).strftime("%Y%m%d_%H%M%S")
    filename = f"metadata_{metadata.condition}_{timestamp}.json"
    
    filepath = output_dir / filename
    with open(filepath, "w") as f:
        json.dump(metadata.to_dict(), f, indent=2)
    
    print(f"Metadata saved to: {filepath}")
    return filepath

def load_experiment_metadata(filepath: Path) -> ExperimentMetadata:
    """Load experiment metadata from JSON."""
    with open(filepath, "r") as f:
        data = json.load(f)
    return ExperimentMetadata(**data)
