"""
Defines constants, denoting sampling rate, labels, etc.
"""

LABEL_HZ = 700
"""Sampling rate of the synchronized protocol labels."""

CHEST_SAMPLE_RATES: int = 700
"""Sampling rate of chest related signals."""

WRIST_SAMPLE_RATES: dict[str, int] = {
    "ACC": 32,
    "BVP": 64,
    "EDA": 4,
    "Temp": 4,
}
"""Sampling rate of wrist related signals."""

CONDITIONS: dict[int, str] = {
    1: "baseline",
    2: "stress",
    3: "amusement",
    4: "meditation",
}
