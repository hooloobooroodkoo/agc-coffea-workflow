from __future__ import annotations

from typing import Any, Dict, Optional


def make_fileset(
    *,
    n_files_max_per_sample: int,
    use_xcache: bool = False,
    af_name: str = "",
    local_data_cache: Optional[str] = None,
    input_from_eos: bool = False,
    xcache_atlas_prefix: Optional[str] = None,
    utils_module: Any = None,
) -> Dict[str, Any]:
    """
    Thin wrapper around AGC's utils.file_input.construct_fileset with a stable signature
    for workflow configs.

    Parameters mirror the underlying construct_fileset:
      - n_files_max_per_sample: number of files per sample (or -1 for all)
      - use_xcache, af_name, local_data_cache, input_from_eos, xcache_atlas_prefix

    utils_module:
      If provided, used as `utils` (handy in notebooks/tests). Otherwise imports `utils`.

    Returns
    -------
    fileset : dict
      {
        "<process>__<variation>": {
          "files": [...],
          "metadata": {"process": ..., "variation": ..., "nevts": ..., "xsec": ...}
        },
        ...
      }
    """
    from utils.file_input import construct_fileset

    return construct_fileset(n_files_max_per_sample=n_files_max_per_sample, use_xcache=use_xcache, af_name=af_name, local_data_cache=local_data_cache, input_from_eos=input_from_eos, xcache_atlas_prefix=xcache_atlas_prefix)


def make_processor(use_inference: bool, use_triton: bool, *, utils_module: Any = None):
    """
    Factory returning the Processor instance for the AGC CMS Open Data ttbar analysis.

    This is intentionally a thin wrapper so your workflow YAML can reference it as:
      "agc_ttbar.entrypoints:make_processor"

    Parameters
    ----------
    use_inference:
        Enable ML inference path in the processor.
    use_triton:
        If inference is enabled, use NVIDIA Triton server for inference.

    utils_module:
        Optional injected `utils` module (handy for notebooks/tests). If not provided,
        the local `utils` package is imported.

    Returns
    -------
    TtbarAnalysis
        An initialized ProcessorABC implementation.
    """

    from .ttbar_processor import TtbarAnalysis

    return TtbarAnalysis(use_inference=use_inference, use_triton=use_triton)
