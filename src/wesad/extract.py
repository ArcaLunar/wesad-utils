"""Condition-window selection on the WESAD label clock."""

import numpy as np
import random
from loguru import logger
from .metadata import LABEL_HZ
from .derived_classes import ConditionInterval, CONDITION_ID_TYPE

# =============================================
# Label Processing
# =============================================


def find_condition(labels: np.ndarray, condition_id: CONDITION_ID_TYPE):
    """
    Return contiguous run for a condition.
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
    return results[0]


def random_sample(cond: ConditionInterval, duration: float) -> ConditionInterval:
    """
    Sample a segment of interval of length `duration` from interval `cond`
    """
    assert cond.duration >= duration

    start_timestamp = random.uniform(
        cond.start_timestamp, cond.end_timestamp - duration
    )
    return ConditionInterval(
        condition_id=cond.condition_id,
        start_timestamp=start_timestamp,
        end_timestamp=start_timestamp + duration,
    )


def select_windows(
    labels: np.ndarray,
    condition_ids: tuple[CONDITION_ID_TYPE, ...],
    duration: float,
) -> list[ConditionInterval]:
    """
    For each condition, select the window from the labels.
    """

    selected: list[ConditionInterval] = []

    for cond_id in condition_ids:
        interval = find_condition(labels, cond_id)
        selected.append(random_sample(interval, duration))

    return selected


# =============================================
# NOTE: Extract features corresponding to labels
# =============================================


def slice_segment(source: np.ndarray, cond: ConditionInterval, rate: int, name: str):
    """
    Slice the `source` into a segment of (synced) duration `cond.duration` under sampling rate `rate`
    """

    start = round(cond.start_timestamp * rate)
    duration = round(cond.duration * rate)
    selected = source[start : start + duration]

    if selected.shape[0] != duration:
        logger.error(f"Duration exceeded range for {name}")
        raise Exception("Mismatched")

    return selected


def resample(source: np.ndarray, original_rate: int, target_rate: int):
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
