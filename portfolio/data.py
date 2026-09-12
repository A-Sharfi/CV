"""Load and normalise the RenderCV YAML so the Dash app and the PDF share one source.

``CV`` is the parsed résumé, ready for the sections to render.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
YAML_PATH = ROOT / "Abdelrahman_Ali_CV.yaml"

_MONTHS = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]


def _parse_date(value: str | None, *, end: bool = False) -> dt.date | None:
    """'2024-05' -> date(2024, 5, 1); 'present' / None -> today (for end) or None."""
    if value in (None, "", "present"):
        return dt.date.today() if end else None
    parts = str(value).split("-")
    year = int(parts[0])
    month = int(parts[1]) if len(parts) > 1 else (12 if end else 1)
    return dt.date(year, month, 1)


def _fmt(value: str | None) -> str:
    if value in (None, "", "present"):
        return "Present"
    parts = str(value).split("-")
    if len(parts) == 1:
        return parts[0]
    return f"{_MONTHS[int(parts[1]) - 1]} {parts[0]}"


def _duration(start: dt.date | None, end: dt.date | None) -> str:
    if not start or not end:
        return ""
    months = (end.year - start.year) * 12 + (end.month - start.month)
    years, rem = divmod(max(months, 1), 12)
    bits = []
    if years:
        bits.append(f"{years} yr" + ("s" if years > 1 else ""))
    if rem:
        bits.append(f"{rem} mo" + ("s" if rem > 1 else ""))
    return " ".join(bits) or "1 mo"


@dataclass
class Entry:
    """One experience or education item."""

    title: str
    subtitle: str
    location: str
    start_raw: str | None
    end_raw: str | None
    highlights: list[str] = field(default_factory=list)

    @property
    def start(self) -> dt.date | None:
        return _parse_date(self.start_raw)

    @property
    def end(self) -> dt.date | None:
        return _parse_date(self.end_raw, end=True)

    @property
    def is_current(self) -> bool:
        return self.end_raw in (None, "", "present")

    @property
    def date_range(self) -> str:
        return f"{_fmt(self.start_raw)} – {_fmt(self.end_raw)}"

    @property
    def duration(self) -> str:
        return _duration(self.start, self.end)

    @property
    def tech(self) -> str:
        """The trailing 'Technologies: ...' highlight, if present."""
        for h in self.highlights:
            if h.lower().startswith("technologies:"):
                return h.split(":", 1)[1].strip().rstrip(".")
        return ""

    @property
    def bullets(self) -> list[str]:
        return [h for h in self.highlights if not h.lower().startswith("technologies:")]


@dataclass
class Resume:
    name: str
    location: str
    email: str
    github: str
    summary: list[str]
    experience: list[Entry]
    education: list[Entry]
    skills: list[tuple[str, str]]
    languages: list[tuple[str, str]]


def _entry(item: dict, *, title: str) -> Entry:
    return Entry(
        title=title,
        subtitle=item["institution"] if "institution" in item else item["company"],
        location=item.get("location", ""),
        start_raw=item.get("start_date"),
        end_raw=item.get("end_date"),
        highlights=item.get("highlights", []),
    )


def load(path: Path = YAML_PATH) -> Resume:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    cv = raw["cv"]
    sections = cv["sections"]

    github = ""
    for net in cv.get("social_networks", []):
        if net.get("network", "").lower() == "github":
            github = net["username"]

    experience = [
        _entry(item, title=item["position"]) for item in sections.get("experience", [])
    ]
    education = [
        _entry(item, title=f"{item.get('degree', '')} {item.get('area', '')}".strip())
        for item in sections.get("education", [])
    ]

    return Resume(
        name=cv["name"],
        location=cv.get("location", ""),
        email=cv.get("email", ""),
        github=github,
        summary=sections.get("profile_summary", []),
        experience=experience,
        education=education,
        skills=[(s["label"], s["details"]) for s in sections.get("skills", [])],
        languages=[(s["label"], s["details"]) for s in sections.get("languages", [])],
    )


CV: Resume = load()

INTERESTS: list[tuple[str, str]] = [
    ("Photography", "Shooting and editing."),
    ("Gym", "Strength training; a consistent part of my week."),
    ("DJing & music production", "Mixing and producing electronic music in my own time."),
]
