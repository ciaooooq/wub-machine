from dataclasses import FrozenInstanceError

import pytest

from wubmachine.analysis import Beat, Section, SongAnalysis
from wubmachine.pitch import (
    compatible_pitch_classes,
    normalize_pitch_class,
    pitch_class_name,
)


def test_empty_analysis_has_safe_defaults():
    analysis = SongAnalysis.empty(duration=123.5)

    assert analysis.duration == 123.5
    assert analysis.sample_rate == 44_100
    assert analysis.channels == 2
    assert analysis.bpm is None
    assert analysis.key is None
    assert analysis.beats == ()
    assert analysis.key_name is None


def test_analysis_exposes_key_name():
    analysis = SongAnalysis(
        duration=10,
        sample_rate=48_000,
        channels=2,
        bpm=140,
        key=10,
    )

    assert analysis.key_name == "Bb"


def test_analysis_rejects_invalid_values():
    with pytest.raises(ValueError):
        SongAnalysis(duration=-1, sample_rate=44_100, channels=2)

    with pytest.raises(ValueError):
        SongAnalysis(duration=1, sample_rate=44_100, channels=2, bpm=0)

    with pytest.raises(ValueError):
        SongAnalysis(duration=1, sample_rate=44_100, channels=2, key=12)


def test_analysis_is_immutable():
    analysis = SongAnalysis.empty(10)

    with pytest.raises(FrozenInstanceError):
        analysis.duration = 20


def test_beat_and_section_end_times():
    beat = Beat(start=1.25, duration=0.5)
    section = Section(start=4, duration=8, label="drop")

    assert beat.end == 1.75
    assert section.end == 12
    assert section.label == "drop"


def test_pitch_classes_wrap_chromatically():
    assert normalize_pitch_class(-1) == 11
    assert normalize_pitch_class(13) == 1
    assert pitch_class_name(11) == "B"


def test_compatible_pitch_classes_are_unique_and_normalized():
    assert compatible_pitch_classes(11, (0, 3, 7, 12)) == (11, 2, 6)


def test_analysis_collections_are_tuples():
    analysis = SongAnalysis(
        duration=2,
        sample_rate=44_100,
        channels=2,
        beats=(Beat(0),),
    )

    assert isinstance(analysis.beats, tuple)
