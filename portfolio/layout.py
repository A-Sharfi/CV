"""Assemble the full page layout from the sections and the chatbot widget."""

from __future__ import annotations

import dash_mantine_components as dmc

from portfolio import chatbot
from portfolio.config import THEME
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

# Sections rendered in order, with a divider between each.
_SECTIONS = [experience, skills, education, interests, contact]


def build_layout() -> dmc.MantineProvider:
    body: list = [navbar.render(), hero.render()]
    for i, module in enumerate(_SECTIONS):
        if i:
            body.append(dmc.Divider())
        body.append(module.render())
    body.append(footer.render())
    body.append(chatbot.widget())

    return dmc.MantineProvider(
        forceColorScheme="light",
        theme=THEME,
        children=dmc.Box(body),
    )
