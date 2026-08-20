"""WESAD pickle loader."""

import pickle
import numpy as np
from collections.abc import Mapping
from pathlib import Path
from typing import Any
from loguru import logger

from .model import WESADDataset


def _read_pickle(path: Path) -> Any:
    """Loads a WESAD subject synchronized pickle as a Python object."""
    with path.open("rb") as stream:
        return pickle.load(stream, encoding="latin1")


def format_uri(subject: str) -> Path:
    """Constructs the URI to a subject's pickle"""

    return Path(f"data/WESAD/{subject}/{subject}.pkl")


def load_dataset(pkl_path: str | Path) -> WESADDataset:
    """Load one subject from Python pickle to Python dataclass."""

    path = Path(pkl_path)
    logger.info(f"Loading pickle object from '{path}'")
    return WESADDataset(_read_pickle(path))
