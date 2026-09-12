"""Skills: one glass card per category, each a row of technology badges."""

from __future__ import annotations

import dash_mantine_components as dmc
from dash_iconify import DashIconify

from portfolio.config import GLASS, PRIMARY, SKILL_ICONS
from portfolio.data import CV
from portfolio.ui import section


def _card(label: str, details: str) -> dmc.Card:
    techs = [p.strip() for p in details.split(",") if p.strip()]
    return dmc.Card(
        [
            dmc.Group(
                [
                    dmc.ThemeIcon(
                        DashIconify(icon=SKILL_ICONS.get(label, "tabler:point"), width=20),
                        size=38,
                        radius="md",
                        variant="light",
                        color=PRIMARY,
                    ),
                    dmc.Text(label, fw=600),
                ],
                gap="sm",
                mb="sm",
            ),
            dmc.Group(
                [dmc.Badge(t, variant="light", color=PRIMARY, size="sm") for t in techs],
                gap=6,
            ),
        ],
        withBorder=True,
        radius="md",
        p="md",
        className=GLASS,
    )


def render() -> dmc.Container:
    return section(
        "skills",
        "Skills",
        dmc.SimpleGrid(
            cols={"base": 1, "sm": 2},
            spacing="md",
            children=[_card(label, details) for label, details in CV.skills],
        ),
    )
