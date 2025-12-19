from __future__ import annotations

from pathlib import Path
import yaml

from coffea.workflow.config import load_workflow_config
from coffea.workflow import to_ir
from coffea.workflow.backends.local import LocalBackend

# Ensure step handlers are registered (import side effects)
import coffea.workflow.analysisSteps.dataset_creation  # noqa: F401
import coffea.workflow.analysisSteps.partition         # noqa: F401
import coffea.workflow.analysisSteps.coffea_run        # noqa: F401
import coffea.workflow.analysisSteps.merge             # noqa: F401

from pathlib import Path
import sys

repo_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root))  # <-- add agc-dev/ to import path

def main():
    repo_root = Path(__file__).resolve().parents[1]  # agc-dev/
    cfg_path = repo_root / "workflows" / "agc_ttbar.yaml"
    workspace = repo_root / "workdir"

    with open(cfg_path, "r") as f:
        raw = yaml.safe_load(f)

    cfg = load_workflow_config(raw)   # <-- expects dict
    graph = to_ir(cfg)

    backend = LocalBackend()
    artifacts = backend.run(graph, workspace=str(workspace))

    print("\nWorkflow finished. Artifacts:")
    for k, v in artifacts.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
