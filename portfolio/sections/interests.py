"""Beyond work: personal interests as icon cards."""

from __future__ import annotations

import dash_mantine_components as dmc
from dash_iconify import DashIconify

from portfolio.config import GLASS, INTEREST_ICONS, PRIMARY
from portfolio.data import INTERESTS
from portfolio.ui import section


def _card(name: str, detail: str) -> dmc.Card:
    return dmc.Card(
        [
            dmc.ThemeIcon(
                DashIconify(icon=INTEREST_ICONS.get(name, "tabler:star"), width=22),
                size=44,
                radius="md",
                variant="light",
                color=PRIMARY,
            ),
            dmc.Text(name, fw=600, mt="sm"),
            dmc.Text(detail, size="sm", c="dimmed"),
        ],
        withBorder=True,
        radius="md",
        p="lg",
        className=GLASS,
    )


def render() -> dmc.Container:
    return section(
        "interests",
        "Beyond work",
        dmc.SimpleGrid(
            cols={"base": 1, "sm": 3},
            spacing="md",
            children=[_card(name, detail) for name, detail in INTERESTS],
        ),
    )
