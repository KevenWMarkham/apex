"""
Build royalty-free music stings for the Cross-Cloud Agentic Podcast.

Two stings — opening and closing — synthesised entirely via ffmpeg from
sine-wave additive synthesis. C-major boardroom register — clean, professional,
distinct from the DTNA/Toyota industrial G-major and the Disney bell-tree
registers. Fits a Microsoft sellers audience (think corporate executive
briefing room, not factory floor or theme park).

  opening_sting.mp3 (~5 sec)  ascending C3-G3-C4 fanfare with major-third warmth
  closing_sting.mp3 (~6 sec)  sustained C-major chord with low fundamental + high-fifth sparkle

Distinct sonic register from the prior seven podcasts in the family — each
podcast has its own sting key and register so listeners can identify the
podcast from the sting alone.

Both files are 24kHz mono MP3 at 48 kbps — matching the podcast's encoding
parameters so they concat cleanly with the episode tracks.

NOTE: this is royalty-free synthesised audio. It is not, and is not derived
from, any copyrighted composition. The Account Team should be explicit about
this in any external use of these files.

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

# Musical notes (frequencies in Hz) — C major / G major boardroom register
C3 = 130.81
G3 = 196.00
C4 = 261.63
E4 = 329.63
G4 = 392.00
C5 = 523.25
E5 = 659.25
G5 = 783.99

SAMPLE_RATE = 24000
BITRATE = "48k"


def build_opening_sting() -> None:
    """Ascending C-G-C fanfare with major-third warmth. Boardroom executive briefing feel."""
    print(f"Building {OPENING_PATH.name} ...")

    # Notes: (frequency, start_time_seconds, duration_seconds)
    # Ascending root-fifth-octave-third in C — clean professional fanfare
    notes = [
        (C3, 0.00, 4.5),   # low root — grounded
        (G3, 0.40, 4.0),   # fifth above
        (C4, 0.80, 4.0),   # octave
        (E4, 1.30, 3.5),   # major third — adds warmth (now C major chord)
    ]

    # Build the filter graph
    filter_parts = []
    bell_labels = []
    for i, (freq, start, dur) in enumerate(notes):
        # Warm horn timbre — heavier on fundamental + even harmonics (octave + 2-octave)
        # Less odd-harmonic content for a smoother sound
        f1 = freq
        f2 = freq * 2.0
        f4 = freq * 4.0
        delay_ms = int(start * 1000)
        # Slow attack-and-sustain envelope rather than bell-decay
        filter_parts.append(
            f"sine=f={f1}:d={dur}:sample_rate={SAMPLE_RATE},"
            f"volume=0.30,afade=t=in:d=0.20,afade=t=out:st={dur - 0.8:.3f}:d=0.8,"
            f"adelay={delay_ms}|{delay_ms}[a{i}_f]"
        )
        filter_parts.append(
            f"sine=f={f2}:d={dur}:sample_rate={SAMPLE_RATE},"
            f"volume=0.12,afade=t=in:d=0.20,afade=t=out:st={dur - 0.8:.3f}:d=0.8,"
            f"adelay={delay_ms}|{delay_ms}[a{i}_h2]"
        )
        filter_parts.append(
            f"sine=f={f4}:d={dur}:sample_rate={SAMPLE_RATE},"
            f"volume=0.05,afade=t=in:d=0.20,afade=t=out:st={dur - 0.8:.3f}:d=0.8,"
            f"adelay={delay_ms}|{delay_ms}[a{i}_h4]"
        )
        bell_labels.extend([f"[a{i}_f]", f"[a{i}_h2]", f"[a{i}_h4]"])

    n = len(bell_labels)
    mix = ("".join(bell_labels) +
           f"amix=inputs={n}:duration=longest:normalize=0,"
           f"volume=4,"
           f"aecho=0.6:0.5:90|180:0.3|0.18,"
           f"afade=t=in:d=0.08,afade=t=out:st=4.2:d=0.8[out]")

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
    """Sustained C major chord with low fundamental + high-fifth sparkle. Boardroom resolution."""
    print(f"Building {CLOSING_PATH.name} ...")

    # All notes start near-together for a chord, sustain through, fade
    # Lower-register C major triad with strong root presence + high-fifth sparkle
    notes = [
        (C3, 0.00, 5.5),   # low root — grounded
        (G3, 0.10, 5.5),   # fifth
        (C4, 0.20, 5.5),   # octave
        (E4, 0.50, 5.3),   # major third (chord builds)
        (G5, 1.20, 4.5),   # higher fifth (sparkle on top)
    ]

    filter_parts = []
    bell_labels = []
    for i, (freq, start, dur) in enumerate(notes):
        f1 = freq
        f2 = freq * 2.0
        delay_ms = int(start * 1000)
        # Warmer envelope — long attack/sustain, gradual fade
        filter_parts.append(
            f"sine=f={f1}:d={dur}:sample_rate={SAMPLE_RATE},"
            f"volume=0.25,afade=t=in:d=0.30,afade=t=out:st={dur - 1.5:.3f}:d=1.5,"
            f"adelay={delay_ms}|{delay_ms}[c{i}_f]"
        )
        filter_parts.append(
            f"sine=f={f2}:d={dur}:sample_rate={SAMPLE_RATE},"
            f"volume=0.08,afade=t=in:d=0.30,afade=t=out:st={dur - 1.5:.3f}:d=1.5,"
            f"adelay={delay_ms}|{delay_ms}[c{i}_h2]"
        )
        bell_labels.extend([f"[c{i}_f]", f"[c{i}_h2]"])

    n = len(bell_labels)
    mix = ("".join(bell_labels) +
           f"amix=inputs={n}:duration=longest:normalize=0,"
           f"volume=3.8,"
           f"aecho=0.7:0.6:120|240:0.35|0.22,"
           f"afade=t=in:d=0.10,afade=t=out:st=4.8:d=1.2[out]")

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
