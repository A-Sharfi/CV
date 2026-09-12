"""Plotly figures used in the portfolio."""

from __future__ import annotations

import datetime as dt

import plotly.graph_objects as go

from portfolio.config import ACCENT, EDUCATION_ACCENT
from portfolio.data import CV

_COLORS = {"Experience": ACCENT, "Education": EDUCATION_ACCENT}

# Shorter y-axis labels so the chart doesn't need a huge left margin on narrow
# (phone-width) screens. Hover text and the detail cards below still use the
# full title.
_SHORT_LABELS = {
    "Financial Applications Developer": "Fin. Apps Developer",
    "Project Manager & Business Analyst": "PM & Business Analyst",
    "Graduate Development Program": "Graduate Program",
    "M.Sc. Economics and Data Analysis": "M.Sc. Econ. & Data Analysis",
    "B.Eng. (Hons) Electrical Engineering (Control)": "B.Eng. Electrical Eng.",
}


def _short_label(title: str, limit: int = 26) -> str:
    if title in _SHORT_LABELS:
        return _SHORT_LABELS[title]
    return title if len(title) <= limit else title[: limit - 1].rstrip() + "…"


def career_timeline() -> go.Figure:
    """Experience and education on one timeline, oldest at the bottom.

    Combining both series (rather than experience alone) fills out the years
    before the first job and makes real overlaps visible: the M.Sc. ending
    right as the IT Officer traineeship begins, for instance.
    """
    items = [(e, "Experience") for e in CV.experience] + [
        (e, "Education") for e in CV.education
    ]
    items.sort(key=lambda pair: pair[0].start)

    fig = go.Figure()
    shown_kinds: set[str] = set()
    for i, (e, kind) in enumerate(items):
        fig.add_trace(
            go.Scatter(
                x=[e.start, e.end],
                y=[i, i],
                mode="lines",
                line=dict(color=_COLORS[kind], width=16),
                name=kind,
                legendgroup=kind,
                showlegend=kind not in shown_kinds,
                hovertemplate=(
                    f"<b>{e.title}</b><br>{e.subtitle}<br>"
                    f"{e.date_range} ({e.duration})<extra></extra>"
                ),
            )
        )
        shown_kinds.add(kind)

    earliest = min(e.start for e, _ in items)
    fig.update_layout(
        height=110 + 46 * len(items),
        margin=dict(l=10, r=20, t=40, b=30),
        autosize=True,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(28,69,135,0.12)",
            tickformat="%Y",
            dtick="M12",
            range=[dt.date(earliest.year, 1, 1), dt.date.today() + dt.timedelta(days=120)],
        ),
        yaxis=dict(
            tickmode="array",
            tickvals=list(range(len(items))),
            ticktext=[_short_label(e.title) for e, _ in items],
            showgrid=False,
            automargin=True,
            range=[-0.6, len(items) - 0.4],
        ),
        font=dict(family="Inter, system-ui, sans-serif", size=12),
        hoverlabel=dict(font_size=13),
    )
    return fig
