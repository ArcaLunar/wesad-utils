"""WESAD pickle loader."""

import pickle
from pathlib import Path
from typing import Any
from loguru import logger

from .model import SubjectData


def _read_pickle(path: Path) -> Any:
    """Loads a WESAD subject synchronized pickle as a Python object."""
    with path.open("rb") as stream:
        return pickle.load(stream, encoding="latin1")


def pickle_path(subject: str) -> Path:
    """Constructs the default path to a subject's pickle"""

    return Path(f"data/WESAD/{subject}/{subject}.pkl")


def load_subject(pkl_path: str | Path) -> SubjectData:
    """Load one subject from Python pickle to Python dataclass."""

    path = Path(pkl_path)
    logger.info(f"Loading pickle object from '{path}'")
    return SubjectData(_read_pickle(path))
