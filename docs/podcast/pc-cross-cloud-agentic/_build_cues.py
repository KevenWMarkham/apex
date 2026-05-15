"""
Generate per-episode timeline cue data for the Cross-Cloud Agentic study guide.

Parses each episode script, splits into sections, estimates per-section start
timestamps by word-count proportion of the episode's known MP3 duration
(offset for the 5-second opening sting), and prints a JS object literal.

Usage:
    python _build_cues.py            # prints JS to stdout
    python _build_cues.py > cues.js  # capture
"""
from __future__ import annotations
import re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent

# episode id -> (md filename, final mp3 duration in seconds)
EPISODES = {
    "e1": ("01-the-agentic-stack-and-five-principles.md", 2048),
    "e2": ("02-data-foundation-and-no-replication.md", 2356),
    "e3": ("03-agent-runtime-talking-to-gold.md", 2240),
    "e4": ("04-governance-identity-and-safety.md", 2736),
    "e5": ("05-audit-ledger-and-replay.md", 2537),
    "e6": ("06-finops-for-agentic-ai.md", 2282),
    "e7": ("07-multi-cloud-and-portability.md", 2497),
    "e8": ("08-the-sellers-playbook.md", 2222),
}
OPEN_STING = 5.3   # opening sting + sting-to-voice silence
CLOSE_STING = 6.6  # closing sting + silence

STAGE = re.compile(r"\[[^\]]*\]")
EMPH = re.compile(r"(\*\*|\*|__|_)(.+?)\1")
SPEAKER = re.compile(r"^\*\*(KEVEN|REID):\*\*", re.MULTILINE)


def sections(md: str):
    """Return list of (title, body_text) for the episode's spoken sections."""
    start = md.find("## Cold Open")
    end = md.find("## Further reading")
    region = md[start:end] if start >= 0 and end >= 0 else md
    out = []
    cur_title, cur_buf = None, []
    for line in region.splitlines():
        h2 = re.match(r"^## (.+)", line)
        h3 = re.match(r"^### (.+)", line)
        if h2 and "Cold Open" in line:
            cur_title, cur_buf = "Cold Open", []
        elif h2 and "The conversation" in line:
            continue  # the conversation wrapper heading — not a section
        elif h3:
            if cur_title:
                out.append((cur_title, "\n".join(cur_buf)))
            cur_title, cur_buf = h3.group(1).strip(), []
        else:
            if cur_title is not None:
                cur_buf.append(line)
    if cur_title:
        out.append((cur_title, "\n".join(cur_buf)))
    return out


def wordcount(text: str) -> int:
    t = STAGE.sub("", text)
    t = EMPH.sub(r"\2", t)
    t = SPEAKER.sub("", t)
    return len(t.split())


def js_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def main():
    print("const EP_CUES = {")
    for ep, (fn, dur) in EPISODES.items():
        md = (HERE / fn).read_text(encoding="utf-8")
        secs = sections(md)
        counts = [wordcount(b) for _, b in secs]
        total = sum(counts) or 1
        window = dur - OPEN_STING - CLOSE_STING
        cues = []
        cum = 0
        for (title, _), c in zip(secs, counts):
            t = int(OPEN_STING + (cum / total) * window)
            cues.append((t, title))
            cum += c
        print(f'  "{ep}": [')
        for t, title in cues:
            print(f'    {{t:{t}, title:"{js_escape(title)}", point:"{js_escape(title)}"}},')
        print("  ],")
    print("};")


if __name__ == "__main__":
    main()
