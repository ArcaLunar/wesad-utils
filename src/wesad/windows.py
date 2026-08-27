"""Window/interval types derived from a subject record."""

import numpy as np
from pydantic import BaseModel, ConfigDict
from typing_extensions import Literal

ConditionId = Literal[1, 2, 3, 4]
ConditionName = Literal["baseline", "stress", "amusement", "meditation"]


class ConditionInterval(BaseModel):
    model_config = ConfigDict(frozen=True)

    condition_id: ConditionId
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
    min: float
    max: float
    slope_per_second: float


class WESADWindow(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        arbitrary_types_allowed=True,
    )

    subject: str

    condition_id: ConditionId
    condition_name: ConditionName

    start_timestamp: float
    end_timestamp: float

    target_hz: int

    series: dict[str, np.ndarray]
    statistics: dict[str, SignalStats]
