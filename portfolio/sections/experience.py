"""Experience: a Plotly timeline above a detailed role-by-role list."""

from __future__ import annotations

import dash_mantine_components as dmc
from dash import dcc

from portfolio.charts import experience_timeline
from portfolio.config import PRIMARY
from portfolio.data import CV, Entry
from portfolio.ui import section


def _timeline_item(entry: Entry) -> dmc.TimelineItem:
    tech_badges = [
        dmc.Badge(t.strip(), variant="outline", color="gray", size="xs")
        for t in entry.tech.split(",")
        if t.strip()
    ]
    return dmc.TimelineItem(
        title=dmc.Group(
            [
                dmc.Text(entry.title, fw=600),
                dmc.Badge(entry.date_range, variant="light", color=PRIMARY, size="sm"),
            ],
            gap="sm",
        ),
        children=[
            dmc.Text(
                f"{entry.subtitle} · {entry.location} · {entry.duration}",
                size="sm",
                c="dimmed",
                mb=6,
            ),
            dmc.List(
                [dmc.ListItem(dmc.Text(b, size="sm")) for b in entry.bullets],
                spacing=4,
                size="sm",
            ),
            dmc.Group(tech_badges, gap=6, mt=8) if tech_badges else None,
        ],
    )


def render() -> dmc.Container:
    items = [_timeline_item(e) for e in CV.experience]
    return section(
        "experience",
        "Experience",
        dmc.Paper(
            [
                dcc.Graph(figure=experience_timeline(), config={"displayModeBar": False}),
                dmc.Timeline(
                    children=items,
                    active=len(items),
                    bulletSize=18,
                    lineWidth=2,
                    color=PRIMARY,
                    mt="xl",
                ),
            ],
            className="glass",
            radius="lg",
            p={"base": "md", "sm": "xl"},
        ),
    )
