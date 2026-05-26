"""
Build royalty-free music stings for the Disney Account Podcast.

Two stings — opening and closing — synthesised entirely via ffmpeg from
sine-wave additive synthesis. The goal is to evoke the "magical / sparkle /
bell-tree" register often associated with media-and-entertainment company
brand stings, without being any specific copyrighted melody.

  opening_sting.mp3 (~5 sec)  ascending C-E-G-C major arpeggio · bell timbre · slight reverb
  closing_sting.mp3 (~6 sec)  descending C-G-E-C resolving into a sustained C-major chord

Both files are 24kHz mono MP3 at 48 kbps — matching the podcast's encoding
parameters so they concat cleanly with the episode tracks.

NOTE: this is royalty-free synthesised audio. It is not, and is not derived
from, any copyrighted Disney composition. The Account Team should be
explicit about this in any external use of these files.

Usage:
    python _build_music.py
"""

from __future__ import annotations
import subprocess
import sys
from pathlib import Path

OUT_DIR = Path(__file__).parent
OPENING_PATH = OUT_DIR / "opening_sting.mp3"
CLOSING_PATH = OUT_DIR / "closing_sting.mp3"

# Musical notes (frequencies in Hz) — C major scale
C5 = 523.25
E5 = 659.25
G5 = 783.99
C6 = 1046.50
G4 = 392.00
E4 = 329.63
C4 = 261.63

SAMPLE_RATE = 24000
BITRATE = "48k"


def _bell_note(freq: float, start_s: float, duration_s: float,
               amplitude: float = 0.4) -> str:
    """Build a filter-chain string for one bell note via additive synthesis.

    Each "bell" is the sum of 3 sines (fundamental, 2nd, 3rd harmonic) with
    decreasing amplitudes, modulated by an exponential decay envelope.
    Returns a string suitable for embedding inside a filter_complex graph.
    """
    f1 = freq
    f2 = freq * 2.0
    f3 = freq * 3.0
    # Amplitude weights — fundamental loudest, harmonics softer for bell timbre
    a1 = amplitude * 0.60
    a2 = amplitude * 0.25
    a3 = amplitude * 0.10
    delay_ms = int(start_s * 1000)

    # Build filter ops. Each tone:
    #   sine generator → adjust volume → fade out (exponential-like decay) → delay
    # Then mix the three into one bell note via amix.
    chain = (
        f"sine=f={f1}:d={duration_s},volume={a1},afade=t=out:st=0.02:d={duration_s - 0.02:.3f}:curve=exp,adelay={delay_ms}|{delay_ms}[n{int(freq)}_1];"
        f"sine=f={f2}:d={duration_s},volume={a2},afade=t=out:st=0.02:d={duration_s - 0.02:.3f}:curve=exp,adelay={delay_ms}|{delay_ms}[n{int(freq)}_2];"
        f"sine=f={f3}:d={duration_s},volume={a3},afade=t=out:st=0.02:d={duration_s - 0.02:.3f}:curve=exp,adelay={delay_ms}|{delay_ms}[n{int(freq)}_3];"
    )
    return chain


def build_opening_sting() -> None:
    """Ascending C-E-G-C arpeggio. Magical / sparkle feel."""
    print(f"Building {OPENING_PATH.name} ...")

    # Notes: (frequency, start_time_seconds, duration_seconds)
    notes = [
        (C5, 0.00, 3.5),
        (E5, 0.35, 3.2),
        (G5, 0.70, 3.0),
        (C6, 1.05, 4.0),
    ]

    # Build the filter graph
    filter_parts = []
    bell_labels = []
    for i, (freq, start, dur) in enumerate(notes):
        # Three sines per bell
        f1 = freq
        f2 = freq * 2.0
        f3 = freq * 3.0
        delay_ms = int(start * 1000)
        # Inline note synthesis — fundamental + 2 harmonics, exp-decay, then delayed
        filter_parts.append(
            f"sine=f={f1}:d={dur}:sample_rate={SAMPLE_RATE},"
            f"volume=0.24,afade=t=out:st=0.05:d={dur - 0.1:.3f}:curve=exp,"
            f"adelay={delay_ms}|{delay_ms}[a{i}_f]"
        )
        filter_parts.append(
            f"sine=f={f2}:d={dur}:sample_rate={SAMPLE_RATE},"
            f"volume=0.10,afade=t=out:st=0.05:d={dur - 0.1:.3f}:curve=exp,"
            f"adelay={delay_ms}|{delay_ms}[a{i}_h2]"
        )
        filter_parts.append(
            f"sine=f={f3}:d={dur}:sample_rate={SAMPLE_RATE},"
            f"volume=0.04,afade=t=out:st=0.05:d={dur - 0.1:.3f}:curve=exp,"
            f"adelay={delay_ms}|{delay_ms}[a{i}_h3]"
        )
        bell_labels.extend([f"[a{i}_f]", f"[a{i}_h2]", f"[a{i}_h3]"])

    # Mix all 12 streams (4 bells × 3 harmonics) — sum them
    n = len(bell_labels)
    mix = "".join(bell_labels) + f"amix=inputs={n}:duration=longest:normalize=0,volume=4,aecho=0.7:0.7:60|180:0.35|0.2,afade=t=in:d=0.05,afade=t=out:st=4.0:d=1.0[out]"

    full_filter = ";".join(filter_parts) + ";" + mix

    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-filter_complex", full_filter,
        "-map", "[out]",
        "-c:a", "libmp3lame", "-b:a", BITRATE,
        "-ar", str(SAMPLE_RATE), "-ac", "1",
        "-t", "5.0",
        str(OPENING_PATH),
    ]
    subprocess.run(cmd, check=True)
    size_kb = OPENING_PATH.stat().st_size // 1024
    print(f"  -> {OPENING_PATH.name} ({size_kb} KB)")


def build_closing_sting() -> None:
    """Descending C-G-E-C arpeggio resolving to sustained C major chord. Warm."""
    print(f"Building {CLOSING_PATH.name} ...")

    # Descending arpeggio: C6, G5, E5, C5  (bright down to warm)
    # Then a sustained chord: C5, E5, G5  (resolves with held C major)
    notes = [
        # (freq, start, duration)
        (C6, 0.00, 2.5),
        (G5, 0.35, 2.5),
        (E5, 0.70, 2.8),
        (C5, 1.05, 4.5),
        # Sustained chord — held in
        (C5, 1.80, 4.2),
        (E5, 1.80, 4.2),
        (G5, 1.80, 4.2),
    ]

    filter_parts = []
    bell_labels = []
    for i, (freq, start, dur) in enumerate(notes):
        f1 = freq
        f2 = freq * 2.0
        delay_ms = int(start * 1000)
        # Lower harmonic content for warmer closing tone
        filter_parts.append(
            f"sine=f={f1}:d={dur}:sample_rate={SAMPLE_RATE},"
            f"volume=0.20,afade=t=out:st=0.08:d={dur - 0.15:.3f}:curve=exp,"
            f"adelay={delay_ms}|{delay_ms}[c{i}_f]"
        )
        filter_parts.append(
            f"sine=f={f2}:d={dur}:sample_rate={SAMPLE_RATE},"
            f"volume=0.07,afade=t=out:st=0.08:d={dur - 0.15:.3f}:curve=exp,"
            f"adelay={delay_ms}|{delay_ms}[c{i}_h2]"
        )
        bell_labels.extend([f"[c{i}_f]", f"[c{i}_h2]"])

    n = len(bell_labels)
    mix = "".join(bell_labels) + f"amix=inputs={n}:duration=longest:normalize=0,volume=3.5,aecho=0.7:0.7:80|220:0.35|0.2,afade=t=in:d=0.05,afade=t=out:st=5.0:d=1.0[out]"

    full_filter = ";".join(filter_parts) + ";" + mix

    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-filter_complex", full_filter,
        "-map", "[out]",
        "-c:a", "libmp3lame", "-b:a", BITRATE,
        "-ar", str(SAMPLE_RATE), "-ac", "1",
        "-t", "6.0",
        str(CLOSING_PATH),
    ]
    subprocess.run(cmd, check=True)
    size_kb = CLOSING_PATH.stat().st_size // 1024
    print(f"  -> {CLOSING_PATH.name} ({size_kb} KB)")


def main():
    if not (OUT_DIR.exists() and OUT_DIR.is_dir()):
        print(f"Output directory missing: {OUT_DIR}", file=sys.stderr)
        sys.exit(1)
    build_opening_sting()
    build_closing_sting()
    print("Done.")


if __name__ == "__main__":
    main()
