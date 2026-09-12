"""Education: one glass card per degree, plus a language badge row."""

from __future__ import annotations

import dash_mantine_components as dmc

from portfolio.config import GLASS, PRIMARY
from portfolio.data import CV, Entry
from portfolio.ui import section


def _card(entry: Entry) -> dmc.Card:
    return dmc.Card(
        [
            dmc.Group(
                [
                    dmc.Text(entry.title, fw=600),
                    dmc.Badge(entry.date_range, variant="light", color=PRIMARY, size="sm"),
                ],
                justify="space-between",
            ),
            dmc.Text(f"{entry.subtitle} · {entry.location}", size="sm", c="dimmed", mb=8),
            dmc.List(
                [dmc.ListItem(dmc.Text(b, size="sm")) for b in entry.bullets],
                spacing=4,
                size="sm",
            ),
        ],
        withBorder=True,
        radius="md",
        p="md",
        className=GLASS,
    )


def _languages() -> dmc.Group:
    return dmc.Group(
        [
            dmc.Badge(f"{name}: {detail.rstrip('.')}", variant="outline", color="gray")
            for name, detail in CV.languages
        ],
        gap=8,
    )


def render() -> dmc.Container:
    return section(
        "education",
        "Education",
        dmc.Stack([_card(e) for e in CV.education], gap="md"),
        _languages(),
    )
