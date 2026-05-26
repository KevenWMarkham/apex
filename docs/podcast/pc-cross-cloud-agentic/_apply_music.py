"""
Apply the opening and closing music stings to every Cross-Cloud Agentic episode MP3.

For each episode MP3 in audio/:
  output = opening_sting (5s) + 0.3s silence + episode + 0.3s silence + closing_sting (6s)

The stings crossfade lightly into / out of the silence around the spoken
audio so the transition feels musical rather than abrupt.

Run *after* the episode audio has been generated (via _build_audio.py),
and *after* the stings have been built (via _build_music.py).

Usage:
    python _apply_music.py        # apply to all episodes in audio/
"""

from __future__ import annotations
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
AUDIO_DIR = HERE / "audio"
ORIG_DIR = AUDIO_DIR / "_originals"   # backups of stingless versions
OPENING = HERE / "opening_sting.mp3"
CLOSING = HERE / "closing_sting.mp3"
SILENCE_BETWEEN_MS = 300              # gap between sting and voice

EPISODES = [
    "01-the-agentic-stack-and-five-principles.mp3",
    "02-data-foundation-and-no-replication.mp3",
    "03-agent-runtime-talking-to-gold.mp3",
    "04-governance-identity-and-safety.mp3",
    "05-audit-ledger-and-replay.mp3",
    "06-finops-for-agentic-ai.mp3",
    "07-multi-cloud-and-portability.mp3",
    "08-the-sellers-playbook.mp3",
]


def apply_stings(episode_mp3: Path) -> None:
    """Concat opening + silence + episode + silence + closing into a new MP3.

    Backs up the original to _originals/ first so the apply is idempotent.
    """
    backup = ORIG_DIR / episode_mp3.name
    if not backup.exists():
        shutil.copy2(episode_mp3, backup)
        source = backup
    else:
        # Already wrapped at least once — re-wrap from the backup
        source = backup

    # Build a concat list. ffmpeg's concat demuxer requires file paths only,
    # so we generate small silence files on demand for the inter-clip gaps.
    silence_path = AUDIO_DIR / "_silence_gap.mp3"
    if not silence_path.exists():
        subprocess.run(
            [
                "ffmpeg", "-y", "-loglevel", "error",
                "-f", "lavfi",
                "-i", "anullsrc=channel_layout=mono:sample_rate=24000",
                "-t", f"{SILENCE_BETWEEN_MS / 1000:.3f}",
                "-c:a", "libmp3lame", "-b:a", "48k",
                str(silence_path),
            ],
            check=True,
        )

    concat_txt = AUDIO_DIR / f"_concat_{episode_mp3.stem}.txt"
    concat_txt.write_text(
        f"file '{OPENING.as_posix()}'\n"
        f"file '{silence_path.as_posix()}'\n"
        f"file '{source.as_posix()}'\n"
        f"file '{silence_path.as_posix()}'\n"
        f"file '{CLOSING.as_posix()}'\n",
        encoding="utf-8",
    )

    # Concat — re-encode rather than copy to ensure clean timestamps + uniform
    # format across the joined segments.
    tmp_out = AUDIO_DIR / f"_wrap_{episode_mp3.stem}.mp3"
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-f", "concat", "-safe", "0",
            "-i", str(concat_txt),
            "-c:a", "libmp3lame", "-b:a", "48k",
            "-ar", "24000", "-ac", "1",
            str(tmp_out),
        ],
        check=True,
    )
    concat_txt.unlink()

    # Replace the in-place episode with the wrapped one
    shutil.move(str(tmp_out), str(episode_mp3))

    dur_proc = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(episode_mp3),
        ],
        capture_output=True, text=True,
    )
    duration_s = float(dur_proc.stdout.strip())
    mins, secs = divmod(int(duration_s), 60)
    print(f"  -> {episode_mp3.name}  |  {mins:02d}:{secs:02d}  (stings applied)")


def main() -> None:
    if not OPENING.exists() or not CLOSING.exists():
        print("Missing sting files. Run _build_music.py first.", file=sys.stderr)
        sys.exit(1)
    if not AUDIO_DIR.exists():
        print(f"Missing audio dir: {AUDIO_DIR}", file=sys.stderr)
        sys.exit(1)
    ORIG_DIR.mkdir(exist_ok=True)

    for name in EPISODES:
        ep = AUDIO_DIR / name
        if not ep.exists():
            print(f"  !! skipping {name} (not generated yet)")
            continue
        apply_stings(ep)

    # Tidy the silence helper file
    silence_path = AUDIO_DIR / "_silence_gap.mp3"
    if silence_path.exists():
        silence_path.unlink()

    print("Done.")


if __name__ == "__main__":
    main()
