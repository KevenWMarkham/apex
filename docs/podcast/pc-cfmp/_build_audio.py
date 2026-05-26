"""
Build podcast audio from markdown scripts (pc-cfmp variant).

Parses **KEVEN:** / **REID:** dialogue lines, generates per-segment audio via
edge-tts (Microsoft neural voices), then concatenates with ffmpeg.

Voices:
  KEVEN = en-US-AndrewNeural             (male, warm, Trilogy continuity host —
                                          Microsoft platform practitioner, 22+ yr)
  REID  = en-US-AndrewMultilingualNeural (male, same tier as Andrew Neural —
                                          cross-cloud principal architect with
                                          MS + AWS + GCP buildout experience.
                                          Rate/pitch tuning differentiates the
                                          two voices since both are Andrew variants.)

This is the eighth distinct voice pairing in the APEX podcast family:
  - Sellers:  Andrew + Brian (boardroom)
  - Services: Andrew + Emma (delivery team)
  - Deploy:   Andrew + Ava (war room)
  - Disney:   Andrew + Emma Multilingual (Disney account team)
  - Studios:  Andrew + Ava Multilingual (Studios account team)
  - DTNA:     Andrew + Brian Multilingual (DTNA account team)
  - Toyota:   Andrew + Michelle (Toyota Zero Day Warranty)
  - X-Cloud:  Andrew + Andrew Multilingual (Cross-Cloud Agentic)
  - CFMP:     Andrew + Andrew Multilingual (CFMP Podcast)  <-- this podcast (same pair for host continuity)

Note on the two-Andrew pairing: both voices are Andrew variants, distinguished
by (a) rate/pitch tuning (Reid runs at -3% rate, -2Hz pitch for the principal-
architect-deliberate register), (b) different vocabulary in the scripts
(Keven references Microsoft platform tenure; Reid references "I have built
this on Bedrock and Vertex AI..."), and (c) different sentence shapes
(Keven uses framing prompts; Reid uses direct architectural pushback).

Output: one MP3 per episode at podcast quality (24kHz mono, 48kbps).

Usage:
    python _build_audio.py 01-the-agentic-stack-and-five-principles.md
    python _build_audio.py --all
"""

from __future__ import annotations
import argparse
import asyncio
import re
import shutil
import subprocess
import sys
from pathlib import Path

import edge_tts

# ---------------------------------------------------------------- voices ----

VOICE_KEVEN = "en-US-AndrewNeural"              # Trilogy continuity host
VOICE_REID  = "en-US-AndrewMultilingualNeural"  # Cross-cloud principal architect

# Rate / pitch tuning. Reid runs slightly slower and lower than Keven to
# differentiate the two Andrew-variant voices.
RATE_KEVEN  = "+0%"
RATE_REID   = "-3%"
PITCH_KEVEN = "+0Hz"
PITCH_REID  = "-2Hz"

# Pause inserted between speaker turns (milliseconds -> silence file via ffmpeg)
TURN_PAUSE_MS = 350

# ---------------------------------------------------------------- parser ---

# Match speaker line: **KEVEN:** or **REID:** at start, content until next
# speaker, heading, or section break.
DIALOGUE_RE = re.compile(
    r"^\*\*(KEVEN|REID):\*\*\s*([\s\S]*?)"
    r"(?=^\*\*(?:KEVEN|REID):\*\*|^##|^---|\Z)",
    re.MULTILINE,
)

# Strip stage directions: [pause], [reading], [Sound: ...], etc.
STAGE_DIR_RE = re.compile(r"\[[^\]]*\]")
# Strip markdown emphasis (* or _ wrapping)
MD_EMPH_RE = re.compile(r"(\*\*|\*|__|_)(.+?)\1")


def clean_text(text: str) -> str:
    """Strip stage directions, markdown, and collapse whitespace."""
    text = STAGE_DIR_RE.sub("", text)
    text = MD_EMPH_RE.sub(r"\2", text)
    text = re.sub(r"\s+", " ", text).strip()
    text = text.replace("…", "...").replace("—", " — ")
    return text


def parse_script(md_text: str) -> list[tuple[str, str]]:
    """Return list of (speaker, cleaned_text) tuples."""
    segments = []
    for match in DIALOGUE_RE.finditer(md_text):
        speaker = match.group(1)
        text = clean_text(match.group(2))
        if text:
            segments.append((speaker, text))
    return segments


# --------------------------------------------------------------- synth -----

async def synth_one(text: str, voice: str, rate: str, pitch: str, out_path: Path):
    """Generate one MP3 segment via edge-tts, retrying on transient 503s."""
    last_err = None
    for attempt in range(5):
        try:
            communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
            await communicate.save(str(out_path))
            return
        except Exception as e:  # noqa: BLE001
            last_err = e
            wait_s = 8 * (2 ** attempt)
            print(f"    !! synth error (attempt {attempt + 1}/5): {type(e).__name__}; backing off {wait_s}s")
            await asyncio.sleep(wait_s)
    raise RuntimeError(f"synth_one failed after 5 retries: {last_err}")


async def synth_episode(md_path: Path, out_dir: Path) -> Path:
    """Synthesize one episode end-to-end. Returns the final MP3 path."""
    md_text = md_path.read_text(encoding="utf-8")
    segments = parse_script(md_text)
    if not segments:
        raise SystemExit(f"No dialogue parsed from {md_path}")

    print(f"  {md_path.name}: {len(segments)} dialogue segments")

    tmp_dir = out_dir / "_tmp" / md_path.stem
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)
    tmp_dir.mkdir(parents=True)

    segment_paths: list[Path] = []
    for i, (speaker, text) in enumerate(segments):
        if speaker == "KEVEN":
            voice, rate, pitch = VOICE_KEVEN, RATE_KEVEN, PITCH_KEVEN
        else:
            voice, rate, pitch = VOICE_REID, RATE_REID, PITCH_REID
        seg_path = tmp_dir / f"{i:04d}_{speaker}.mp3"
        await synth_one(text, voice, rate, pitch, seg_path)
        segment_paths.append(seg_path)
        if (i + 1) % 25 == 0:
            print(f"    ... {i + 1}/{len(segments)} segments synthesized")

    silence_path = tmp_dir / "silence.mp3"
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-f", "lavfi",
            "-i", "anullsrc=channel_layout=mono:sample_rate=24000",
            "-t", f"{TURN_PAUSE_MS / 1000:.3f}",
            "-c:a", "libmp3lame", "-b:a", "48k",
            str(silence_path),
        ],
        check=True,
    )

    concat_list = tmp_dir / "concat.txt"
    with concat_list.open("w", encoding="utf-8") as f:
        for i, seg in enumerate(segment_paths):
            f.write(f"file '{seg.name}'\n")
            if i < len(segment_paths) - 1:
                f.write(f"file '{silence_path.name}'\n")

    final_path = out_dir / f"{md_path.stem}.mp3"
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-f", "concat", "-safe", "0",
            "-i", str(concat_list),
            "-c:a", "libmp3lame", "-b:a", "48k", "-ar", "24000", "-ac", "1",
            str(final_path),
        ],
        check=True,
        cwd=tmp_dir,
    )

    dur_proc = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(final_path)],
        capture_output=True, text=True,
    )
    duration_s = float(dur_proc.stdout.strip()) if dur_proc.stdout.strip() else 0.0
    mins, secs = divmod(int(duration_s), 60)
    size_kb = final_path.stat().st_size // 1024
    print(f"  -> {final_path.name}  |  {mins:02d}:{secs:02d}  |  {size_kb} KB")

    return final_path


# --------------------------------------------------------------- main ------

EPISODES = [
    "01-sarahs-day.md",
    "02-agent-fleet-and-audit-chain.md",
    "03-mobile-scan-and-lot.md",
    "04-mobile-trips-replenish-home.md",
    "05-portal-operator-console-multitenant.md",
    "06-sonos-ambient-voice-channel.md",
    "07-fulfillment-plugin-tier.md",
    "08-identity-consent-hipaa-senior.md",
    "09-sellers-playbook.md",
    "10-flux-household-composition.md",
    "11-recipes-meal-plan-front-door.md",
    "12-privacy-as-the-moat.md",
    "13-phase-1-live-the-honest-demo-map.md",
]


async def main_async(targets: list[str], out_dir: Path, keep_tmp: bool):
    out_dir.mkdir(exist_ok=True, parents=True)
    for t in targets:
        md_path = Path(__file__).parent / t
        if not md_path.exists():
            print(f"!! missing: {md_path}")
            continue
        await synth_episode(md_path, out_dir)
    _ = keep_tmp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("targets", nargs="*", help="Episode markdown files (or --all)")
    ap.add_argument("--all", action="store_true", help="Build all 9 episodes")
    ap.add_argument("--out", default="audio", help="Output dir (default: audio/)")
    ap.add_argument("--keep-tmp", action="store_true", help="Keep _tmp segments")
    args = ap.parse_args()

    targets = EPISODES if args.all else args.targets
    if not targets:
        print("Specify an episode .md or --all")
        sys.exit(1)

    out_dir = Path(__file__).parent / args.out
    asyncio.run(main_async(targets, out_dir, args.keep_tmp))


if __name__ == "__main__":
    main()
