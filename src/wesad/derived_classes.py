"""Derived classes from raw WESAD dataset."""

import numpy as np
from dataclasses import dataclass
from pydantic import BaseModel, ConfigDict
from typing_extensions import Literal

CONDITION_ID_TYPE = Literal[1, 2, 3, 4]
CONDITION_NAME_TYPE = Literal["baseline", "stress", "amusement", "meditation"]


class ConditionInterval(BaseModel):
    model_config = ConfigDict(frozen=True)

    condition_id: CONDITION_ID_TYPE
    """1=baseline, 2=stress, 3=amusement, 4=meditation"""

    start_timestamp: float
    """Start time (in seconds)"""

    end_timestamp: float
    """End time (in seconds)"""

    @property
    def duration(self) -> float:
        """The duration of the interval (in seconds)"""

        return self.end_timestamp - self.start_timestamp


class SignalStats(BaseModel):
    model_config = ConfigDict(frozen=True)

    mean: float
    std: float
    minimum: float
    maximum: float
    slope_per_second: float


class WESADWindow(BaseModel):
    model_config = ConfigDict(frozen=True)

    subject: str

    condition_id: CONDITION_ID_TYPE
    condition_name: CONDITION_NAME_TYPE

    start_timestamp: float
    end_timestamp: float

    target_hz: int

    series: dict[str, np.ndarray]
    statistics: dict[str, SignalStats]
