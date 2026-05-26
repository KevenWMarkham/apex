"""
Build royalty-free music stings for the Disney Studios Account Podcast.

The Studios podcast is a sibling brand to the Disney Account podcast, so the
musical character stays in the same bell-tree register — but in F major
instead of C major. The brighter key gives the Studios stings a distinct
sonic identity from the Account podcast while staying within the Disney
brand family.

  opening_sting.mp3 (~5 sec)  ascending F-A-C-F major arpeggio · bell timbre · light reverb
  closing_sting.mp3 (~6 sec)  descending F-C-A-F resolving into sustained F-A-C chord

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

# F major — brighter / more cinematic register than Account podcast (C major)
F4 = 349.23
A4 = 440.00
C5 = 523.25
F5 = 698.46
A5 = 880.00
C6 = 1046.50
F6 = 1396.91

SAMPLE_RATE = 24000
BITRATE = "48k"


def build_opening_sting() -> None:
    """Ascending F-A-C-F arpeggio. Studios-bright sparkle."""
    print(f"Building {OPENING_PATH.name} ...")

    notes = [
        (F5, 0.00, 3.5),
        (A5, 0.35, 3.2),
        (C6, 0.70, 3.0),
        (F6, 1.05, 4.0),
    ]

    filter_parts = []
    bell_labels = []
    for i, (freq, start, dur) in enumerate(notes):
        f1 = freq
        f2 = freq * 2.0
        f3 = freq * 3.0
        delay_ms = int(start * 1000)
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
    """Descending F-C-A-F arpeggio resolving to sustained F major chord."""
    print(f"Building {CLOSING_PATH.name} ...")

    notes = [
        (F6, 0.00, 2.5),
        (C6, 0.35, 2.5),
        (A5, 0.70, 2.8),
        (F5, 1.05, 4.5),
        # Sustained F major chord
        (F5, 1.80, 4.2),
        (A5, 1.80, 4.2),
        (C6, 1.80, 4.2),
    ]

    filter_parts = []
    bell_labels = []
    for i, (freq, start, dur) in enumerate(notes):
        f1 = freq
        f2 = freq * 2.0
        delay_ms = int(start * 1000)
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
