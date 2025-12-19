from __future__ import annotations

import importlib
from typing import Any, Callable


def import_from_string(path: str) -> Any:
    """
    Import 'pkg.module:obj' or 'pkg.module.obj'.
    """
    if ":" in path:
        module_name, attr = path.split(":", 1)
    else:
        module_name, attr = path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    return getattr(module, attr)


def load_callable(path: str) -> Callable[..., Any]:
    obj = import_from_string(path)
    if not callable(obj):
        raise TypeError(f"Imported object is not callable: {path}")
    return obj
