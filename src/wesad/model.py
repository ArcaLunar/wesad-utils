"""Raw per-subject records loaded from the synchronized WESAD pickle."""

import numpy as np
from dataclasses import dataclass
from loguru import logger


def _missing(shape: tuple[int, ...]) -> np.ndarray:
    """Represent an absent signal without storing a NumPy type object."""

    return np.empty(shape, dtype=np.float64)


@dataclass
class ChestSignals:
    ACC: np.ndarray
    ECG: np.ndarray
    EMG: np.ndarray
    EDA: np.ndarray
    TEMP: np.ndarray
    RESP: np.ndarray

    def __init__(self, sample: dict):
        # Chest pickle keys use mixed case ("Temp", "Resp") unlike wrist ("TEMP").
        self.ACC = sample.get("ACC", _missing((0, 3)))
        self.ECG = sample.get("ECG", _missing((0, 1)))
        self.EMG = sample.get("EMG", _missing((0, 1)))
        self.EDA = sample.get("EDA", _missing((0, 1)))
        self.TEMP = sample.get("Temp", _missing((0, 1)))
        self.RESP = sample.get("Resp", _missing((0, 1)))

        logger.info("ChestSignals data shape")
        logger.info(f"  - ACC: {self.ACC.shape}")
        logger.info(f"  - ECG: {self.ECG.shape}")
        logger.info(f"  - EMG: {self.EMG.shape}")
        logger.info(f"  - EDA: {self.EDA.shape}")
        logger.info(f"  - TEMP: {self.TEMP.shape}")
        logger.info(f"  - RESP: {self.RESP.shape}")


@dataclass
class WristSignals:
    ACC: np.ndarray
    BVP: np.ndarray
    EDA: np.ndarray
    TEMP: np.ndarray

    def __init__(self, sample: dict):
        self.ACC = sample.get("ACC", _missing((0, 3)))
        self.BVP = sample.get("BVP", _missing((0, 1)))
        self.EDA = sample.get("EDA", _missing((0, 1)))
        self.TEMP = sample.get("TEMP", _missing((0, 1)))

        logger.info("WristSignals data shape")
        logger.info(f"  - ACC: {self.ACC.shape}")
        logger.info(f"  - BVP: {self.BVP.shape}")
        logger.info(f"  - EDA: {self.EDA.shape}")
        logger.info(f"  - TEMP: {self.TEMP.shape}")


@dataclass
class SubjectData:
    """
    Dataclass modeling one subject's raw data read from the provided synchronized pickle.
    """

    subject: str
    """The experiment subject"""

    label: np.ndarray
    """Label for each timestamp"""

    chest: ChestSignals
    """Time series data"""

    wrist: WristSignals
    """Time series data"""

    def __init__(self, sample: dict):
        logger.info("Constructing SubjectData.")
        self.subject = sample.get("subject", "")
        self.label = sample.get("label", _missing((0,)))
        logger.info("Label data shape")
        logger.info(f"  - label: {self.label.shape}")

        signal = sample.get("signal", {})
        self.chest = ChestSignals(signal.get("chest", {}))
        self.wrist = WristSignals(signal.get("wrist", {}))
