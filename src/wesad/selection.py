"""Condition-window selection on the WESAD label clock."""

import numpy as np
import random
from loguru import logger
from .metadata import LABEL_HZ
from .windows import ConditionInterval, ConditionId

# =============================================
# Label Processing
# =============================================


def find_condition_runs(
    labels: np.ndarray, condition_id: ConditionId
) -> list[ConditionInterval]:
    """
    Return all contiguous runs of a condition.
    By protocol, there's only one such interval for 1/2/3, but two for 4.
    """

    start, total = 0, len(labels)
    results: list[ConditionInterval] = []
    while start < total:
        end = start

        # find exclusive right endpoint
        while end < total and labels[end] == labels[start]:
            end += 1

        if labels[start] == condition_id:
            results.append(
                ConditionInterval(
                    condition_id=condition_id,
                    start_timestamp=start / LABEL_HZ,
                    end_timestamp=end / LABEL_HZ,
                )
            )

        start = end

    logger.info(f"Found {len(results)} intervals with condition id {condition_id}.")
    for cond in results:
        logger.info(f"  from {cond.start_timestamp:.2f} to {cond.end_timestamp:.2f}")

    assert len(results) >= 1
    return results


def random_subinterval(interval: ConditionInterval, duration: float) -> ConditionInterval:
    """
    Sample a segment of length `duration` from within `interval`
    """

    assert interval.duration >= duration

    start_timestamp = random.uniform(
        interval.start_timestamp, interval.end_timestamp - duration
    )
    return ConditionInterval(
        condition_id=interval.condition_id,
        start_timestamp=start_timestamp,
        end_timestamp=start_timestamp + duration,
    )


def select_windows(
    labels: np.ndarray,
    condition_ids: tuple[ConditionId, ...],
    duration: float,
) -> list[ConditionInterval]:
    """
    For each condition, select a random window from one of its runs.
    """

    selected: list[ConditionInterval] = []

    for cond_id in condition_ids:
        runs = find_condition_runs(labels, cond_id)
        interval = random.choice(runs)
        selected.append(random_subinterval(interval, duration))

    return selected


# =============================================
# Slicing & Resampling
# =============================================


def slice_window(signal: np.ndarray, interval: ConditionInterval, hz: int) -> np.ndarray:
    """
    Slice the `signal` (sampled at `hz`) into a segment of duration `interval.duration`,
    synced with `interval`'s start timestamp.
    """

    start = round(interval.start_timestamp * hz)
    duration = round(interval.duration * hz)
    selected = signal[start : start + duration]

    if selected.shape[0] != duration:
        logger.error(f"Duration exceeded range for condition id {interval.condition_id}")
        raise Exception("Mismatched")

    return selected


def resample(source: np.ndarray, original_rate: int, target_rate: int) -> np.ndarray:
    """
    Resample a signal along dimension 0.
    """
    import math
    from scipy.signal import resample_poly

    source = np.asarray(source)
    divisor = math.gcd(original_rate, target_rate)
    return np.array(
        resample_poly(
            source,
            up=target_rate // divisor,
            down=original_rate // divisor,
            axis=0,
        )
    )
