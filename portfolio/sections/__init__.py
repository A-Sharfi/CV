"""Page sections in vertical order. Each module exposes ``render()``."""

from portfolio.sections import (
    contact,
    education,
    experience,
    footer,
    hero,
    interests,
    navbar,
    skills,
)

__all__ = [
    "navbar",
    "hero",
    "experience",
    "skills",
    "education",
    "interests",
    "contact",
    "footer",
]
