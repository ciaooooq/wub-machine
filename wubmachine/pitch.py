"""Small, dependency-free pitch-class utilities."""

from __future__ import annotations

from typing import Iterable, Optional


PITCH_CLASS_NAMES = (
    "C", "C#", "D", "Eb", "E", "F",
    "F#", "G", "G#", "A", "Bb", "B",
)


def normalize_pitch_class(value: int) -> int:
    """Normalize any integer pitch value to the chromatic 0-11 range."""

    return int(value) % 12


def pitch_class_name(value: int) -> str:
    """Return the Wub Machine's canonical name for a pitch class."""

    return PITCH_CLASS_NAMES[normalize_pitch_class(value)]


def compatible_pitch_classes(root: int, intervals: Iterable[int]) -> tuple[int, ...]:
    """Return unique pitch classes formed from a root and relative intervals."""

    return tuple(
        dict.fromkeys(
            normalize_pitch_class(normalize_pitch_class(root) + interval)
            for interval in intervals
        )
    )


def closest_pitch_class(value: float) -> Optional[int]:
    """Round a numeric pitch estimate to the nearest chromatic pitch class."""

    if value is None:
        return None
    return normalize_pitch_class(round(value))
