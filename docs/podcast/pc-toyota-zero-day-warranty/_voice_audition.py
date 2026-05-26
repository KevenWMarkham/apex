"""
Generate short audition samples of candidate female voices for Mia.

The current Toyota Zero Day Warranty podcast uses Aria, which the user
reports reads as synthetic / news-anchor. The goal is a female voice
that matches Andrew (KEVEN) in naturalness.

Candidates — all newer-generation natural-quality voices in edge-tts:
  - MichelleNeural           (newer Neural, natural, unused in APEX family)
  - AvaMultilingualNeural    (Multilingual tier, same as Andrew, natural)
  - EmmaMultilingualNeural   (Multilingual tier, same as Andrew, natural)

Each candidate reads the same ~30s passage. Output:
  audio/_auditions/mia-michelle.mp3
  audio/_auditions/mia-ava.mp3
  audio/_auditions/mia-emma.mp3

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

# Same passage Mia delivers in the Ep 1 cold open — chosen because it has
# conversational rhythm, technical content (Toyota production context), and
# the warm-but-credible register the character requires.
PASSAGE = (
    "I want to start at eleven PM on a Tuesday at a Toyota plant in Kentucky. "
    "A quality engineer is staring at a monitor. The connected-vehicle data "
    "team just sent her a warranty cluster — a transmission fault pattern on "
    "Camry builds from a specific six-week production window. Three plants "
    "involved. Three suppliers in scope. Six teams about to be pulled into "
    "the investigation. And what she knows, right now, is that it's going to "
    "take 8 to 12 weeks to trace this back to the factory minute."
)

CANDIDATES = [
    ("mia-michelle.mp3", "en-US-MichelleNeural"),
    ("mia-ava.mp3",      "en-US-AvaMultilingualNeural"),
    ("mia-emma.mp3",     "en-US-EmmaMultilingualNeural"),
]

# Same rate / pitch tuning we use for Mia in the production build
RATE = "-2%"
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
