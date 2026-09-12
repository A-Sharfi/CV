"""Experience: a Plotly timeline above a detailed role-by-role list."""

from __future__ import annotations

import dash_mantine_components as dmc
from dash import dcc
from dash_iconify import DashIconify

from portfolio.charts import career_timeline
from portfolio.config import EDUCATION_COLOR, PRIMARY
from portfolio.data import CV, Entry
from portfolio.ui import section

_KIND_STYLE = {
    "Experience": {"color": PRIMARY, "icon": "tabler:briefcase"},
    "Education": {"color": EDUCATION_COLOR, "icon": "tabler:school"},
}


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


def _compact_timeline_item(entry: Entry, kind: str) -> dmc.TimelineItem:
    style = _KIND_STYLE[kind]
    return dmc.TimelineItem(
        bullet=dmc.ThemeIcon(
            DashIconify(icon=style["icon"], width=12),
            size=22,
            radius="xl",
            color=style["color"],
        ),
        title=dmc.Group(
            [
                dmc.Text(entry.title, fw=600, size="sm"),
                dmc.Badge(entry.date_range, variant="light", color=style["color"], size="xs"),
            ],
            gap=6,
            wrap="wrap",
        ),
        children=dmc.Text(f"{entry.subtitle} · {entry.location}", size="xs", c="dimmed"),
    )


def _mobile_chart() -> dmc.Box:
    """A compact vertical timeline for phone widths.

    The Plotly Gantt chart needs real horizontal room to plot ~15 years of
    history; below that it degrades into unreadable stacked tick labels. A
    simple chronological timeline reads fine at any width instead.
    """
    combined = [(e, "Experience") for e in CV.experience] + [
        (e, "Education") for e in CV.education
    ]
    combined.sort(key=lambda pair: pair[0].start, reverse=True)
    items = [_compact_timeline_item(e, kind) for e, kind in combined]
    return dmc.Box(
        dmc.Paper(
            [
                dmc.Group(
                    [
                        dmc.Group(
                            [dmc.ThemeIcon(DashIconify(icon="tabler:briefcase", width=12), size=18, radius="xl", color=PRIMARY),
                             dmc.Text("Experience", size="xs", c="dimmed")],
                            gap=4,
                        ),
                        dmc.Group(
                            [dmc.ThemeIcon(DashIconify(icon="tabler:school", width=12), size=18, radius="xl", color=EDUCATION_COLOR),
                             dmc.Text("Education", size="xs", c="dimmed")],
                            gap=4,
                        ),
                    ],
                    gap="lg",
                    mb="sm",
                ),
                dmc.Timeline(children=items, bulletSize=22, lineWidth=2),
            ],
            className="glass",
            radius="lg",
            p="md",
        ),
        hiddenFrom="sm",
        mb="lg",
    )


def render() -> dmc.Container:
    items = [_timeline_item(e) for e in CV.experience]
    desktop_chart = dmc.Box(
        dmc.Paper(
            dcc.Graph(
                figure=career_timeline(),
                config={"displayModeBar": False, "responsive": True},
                style={"width": "100%"},
            ),
            className="glass",
            radius="lg",
            p={"base": "md", "sm": "xl"},
        ),
        visibleFrom="sm",
        mb="lg",
    )
    chart = dmc.Box([desktop_chart, _mobile_chart()])
    timeline = dmc.Paper(
        dmc.Timeline(
            children=items, active=len(items), bulletSize=18, lineWidth=2, color=PRIMARY
        ),
        className="glass",
        radius="lg",
        p={"base": "md", "sm": "xl"},
    )
    return section("experience", "Experience", timeline, before=chart)
