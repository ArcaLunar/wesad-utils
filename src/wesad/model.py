import numpy as np
from dataclasses import dataclass
from loguru import logger


def _missing(shape: tuple[int, ...], name: str) -> np.ndarray:
    """Represent an absent signal without storing a NumPy type object."""

    logger.warning(f"Missing field when constructing {name}")
    return np.empty(shape, dtype=np.float64)


@dataclass
class ChestSignals:
    ACC: np.ndarray
    ECG: np.ndarray
    EMG: np.ndarray
    EDA: np.ndarray
    Temp: np.ndarray
    Resp: np.ndarray

    def __init__(self, sample: dict):
        self.ACC = sample.get("ACC", _missing((0, 3), "ChestSignals.ACC"))
        self.ECG = sample.get("ECG", _missing((0, 1), "ChestSignals.ECG"))
        self.EMG = sample.get("EMG", _missing((0, 1), "ChestSignals.EMG"))
        self.EDA = sample.get("EDA", _missing((0, 1), "ChestSignals.EDA"))
        self.Temp = sample.get("Temp", _missing((0, 1), "ChestSignals.Temp"))
        self.Resp = sample.get("Resp", _missing((0, 1), "ChestSignals.Resp"))

        logger.info("ChestSignals data shape")
        logger.info(f"  - ACC: {self.ACC.shape}")
        logger.info(f"  - ECG: {self.ECG.shape}")
        logger.info(f"  - EMG: {self.EMG.shape}")
        logger.info(f"  - EDA: {self.EDA.shape}")
        logger.info(f"  - Temp: {self.Temp.shape}")
        logger.info(f"  - Resp: {self.Resp.shape}")


@dataclass
class WristSignals:
    ACC: np.ndarray
    BVP: np.ndarray
    EDA: np.ndarray
    Temp: np.ndarray

    def __init__(self, sample: dict):
        self.ACC = sample.get("ACC", _missing((0, 3), "WristSignals.ACC"))
        self.BVP = sample.get("BVP", _missing((0, 1), "WristSignals.BVP"))
        self.EDA = sample.get("EDA", _missing((0, 1), "WristSignals.EDA"))
        self.Temp = sample.get("TEMP", _missing((0, 1), "WristSignals.Temp"))

        logger.info("WristSignals data shape")
        logger.info(f"  - ACC: {self.ACC.shape}")
        logger.info(f"  - BVP: {self.BVP.shape}")
        logger.info(f"  - EDA: {self.EDA.shape}")
        logger.info(f"  - Temp: {self.Temp.shape}")


@dataclass
class WESADDataset:
    """
    Dataclass to model raw data read from provided synchronized pickle.
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
        logger.info("Constructing WESADDataset.")
        self.subject = sample.get("subject", "")
        self.label = sample.get("label", _missing((0,), "WESADDataset.label"))
        logger.info("Label data shape")
        logger.info(f"  - label: {self.label.shape}")

        signal = sample.get("signal", {})
        self.chest = ChestSignals(signal.get("chest", {}))
        self.wrist = WristSignals(signal.get("wrist", {}))
