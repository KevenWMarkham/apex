"""
Generate short audition samples of candidate male voices for REID.

REID is the cross-cloud principal architect co-host opposite Keven. The voice
should match Andrew (KEVEN) in naturalness — Davis is the planned default;
two alternates are auditioned in case Davis reads as synthetic (Aria-lesson).

Candidates — the three viable male voices in edge-tts en-US that match
Andrew's natural quality (the older Christopher/Eric/Guy/Roger voices are
Aria-era synthetic):
  - AndrewMultilingualNeural (same tier as Andrew/Keven; risk: too similar)
  - BrianMultilingualNeural  (reuse from DTNA Marcus; known natural)
  - SteffanNeural            (unknown character; worth auditioning)

Each candidate reads the same ~30s passage. Output:
  audio/_auditions/reid-andrew-multi.mp3
  audio/_auditions/reid-brian-multi.mp3
  audio/_auditions/reid-steffan.mp3

Usage:
    python _voice_audition.py
"""

from __future__ import annotations
import asyncio
from pathlib import Path
import edge_tts

HERE = Path(__file__).parent
OUT_DIR = HERE / "audio" / "_auditions"
OUT_DIR.mkdir(exist_ok=True, parents=True)

# Reid's register — technical/architectural pushback. ~30 seconds.
PASSAGE = (
    "I want to push back on something. The phrase 'agent' is overloaded. "
    "Most of what gets called agentic AI in production today is a pipeline — "
    "a deterministic sequence of model calls and tool invocations. That's "
    "useful, but it's not what we mean when we talk about the agentic stack. "
    "The agentic stack requires reasoning, tool use, state, and an audit "
    "substrate that an external reviewer can replay. If those four aren't "
    "all present, you're shipping a pipeline. And pipelines are fine — but "
    "they don't earn the governance posture the agentic stack does."
)

CANDIDATES = [
    ("reid-andrew-multi.mp3", "en-US-AndrewMultilingualNeural"),
    ("reid-brian-multi.mp3",  "en-US-BrianMultilingualNeural"),
    ("reid-steffan.mp3",      "en-US-SteffanNeural"),
]

RATE = "-2%"   # slightly slower than Keven, matches the contemplative-architect register
PITCH = "+0Hz"


async def synth(text: str, voice: str, out_path: Path) -> None:
    communicate = edge_tts.Communicate(text, voice, rate=RATE, pitch=PITCH)
    await communicate.save(str(out_path))


async def main_async() -> None:
    for filename, voice in CANDIDATES:
        path = OUT_DIR / filename
        print(f"Generating {filename} ({voice})...")
        await synth(PASSAGE, voice, path)
        size_kb = path.stat().st_size // 1024
        print(f"  -> {path.name} ({size_kb} KB)")


def main() -> None:
    asyncio.run(main_async())
    print(f"\nAudition samples in: {OUT_DIR}")


if __name__ == "__main__":
    main()
