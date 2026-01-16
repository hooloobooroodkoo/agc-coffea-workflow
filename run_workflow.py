from __future__ import annotations

from pathlib import Path
import yaml

from coffea.workflow.config import load_workflow_config
from coffea.workflow import to_ir
from coffea.workflow.backends.local import LocalBackend

# analysisSteps handlers
import coffea.workflow.analysisSteps.dataset_creation 
import coffea.workflow.analysisSteps.partition 
import coffea.workflow.analysisSteps.coffea_run  
import coffea.workflow.analysisSteps.merge 
import coffea.workflow.analysisSteps.validate_histograms
import coffea.workflow.analysisSteps.plot_histograms

from pathlib import Path
import sys

# muted warnings
from coffea.nanoevents import NanoAODSchema
NanoAODSchema.warn_missing_crossrefs = False

repo_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root))  

def main():
    repo_root = Path(__file__).resolve().parents[1]  
    cfg_path = repo_root / "agc-coffea-workflow" / "agc_ttbar.yaml"
    workspace = repo_root /  "agc-coffea-workflow" / "workdir"

    with open(cfg_path, "r") as f:
        raw = yaml.safe_load(f)

    cfg = load_workflow_config(raw)
    graph = to_ir(cfg)

    backend = LocalBackend()
    artifacts = backend.run(graph, workspace=str(workspace))

    print("\nWorkflow finished. Artifacts:")
    for k, v in artifacts.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
