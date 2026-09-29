"""Music-analysis data structures used by the modern remix engine.

This module intentionally contains no audio backend. Analysis providers (for example
librosa-based or native DSP implementations) can populate these immutable models.
Keeping the model independent makes the remix algorithms testable without decoding
audio files.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Sequence, Tuple


PITCH_CLASS_NAMES: Tuple[str, ...] = (
    "C", "C#", "D", "Eb", "E", "F",
    "F#", "G", "G#", "A", "Bb", "B",
)


@dataclass(frozen=True)
class Beat:
    """A detected beat in seconds."""

    start: float
    duration: Optional[float] = None

    @property
    def end(self) -> float:
        if self.duration is None:
            raise ValueError("Beat duration is not available")
        return self.start + self.duration


@dataclass(frozen=True)
class Section:
    """A musical section such as an intro, verse, chorus, or drop."""

    start: float
    duration: float
    label: Optional[str] = None
    confidence: Optional[float] = None

    @property
    def end(self) -> float:
        return self.start + self.duration


@dataclass(frozen=True)
class SongAnalysis:
    """Backend-independent analysis of a song.

    Times are expressed in seconds. BPM and key are optional because an analyzer
    may be unable to determine them reliably.
    """

    duration: float
    sample_rate: int
    channels: int
    bpm: Optional[float] = None
    key: Optional[int] = None
    key_confidence: Optional[float] = None
    beats: Tuple[Beat, ...] = field(default_factory=tuple)
    bars: Tuple[Beat, ...] = field(default_factory=tuple)
    sections: Tuple[Section, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if self.duration < 0:
            raise ValueError("duration must be non-negative")
        if self.sample_rate <= 0:
            raise ValueError("sample_rate must be positive")
        if self.channels <= 0:
            raise ValueError("channels must be positive")
        if self.bpm is not None and self.bpm <= 0:
            raise ValueError("bpm must be positive")
        if self.key is not None and not 0 <= self.key <= 11:
            raise ValueError("key must be a pitch class from 0 to 11")

    @property
    def key_name(self) -> Optional[str]:
        """Return the human-readable key name when a key was detected."""

        return None if self.key is None else PITCH_CLASS_NAMES[self.key]

    @classmethod
    def empty(
        cls,
        duration: float,
        sample_rate: int = 44_100,
        channels: int = 2,
    ) -> "SongAnalysis":
        """Create an analysis containing only basic technical metadata."""

        return cls(
            duration=duration,
            sample_rate=sample_rate,
            channels=channels,
        )
