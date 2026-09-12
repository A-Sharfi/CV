"""Plotly figures used in the portfolio."""

from __future__ import annotations

import datetime as dt

import plotly.graph_objects as go

from portfolio.config import ACCENT
from portfolio.data import CV


def experience_timeline() -> go.Figure:
    """A horizontal timeline of roles, newest at the top."""
    entries = list(reversed(CV.experience))
    fig = go.Figure()
    for i, e in enumerate(entries):
        fig.add_trace(
            go.Scatter(
                x=[e.start, e.end],
                y=[i, i],
                mode="lines",
                line=dict(color=ACCENT, width=16),
                hovertemplate=(
                    f"<b>{e.title}</b><br>{e.subtitle}<br>"
                    f"{e.date_range} ({e.duration})<extra></extra>"
                ),
                showlegend=False,
            )
        )
    fig.update_layout(
        height=70 + 46 * len(entries),
        margin=dict(l=150, r=20, t=10, b=30),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(28,69,135,0.12)",
            tickformat="%Y",
            dtick="M12",
            range=[dt.date(2017, 6, 1), dt.date.today() + dt.timedelta(days=120)],
        ),
        yaxis=dict(
            tickmode="array",
            tickvals=list(range(len(entries))),
            ticktext=[e.title for e in entries],
            showgrid=False,
            range=[-0.6, len(entries) - 0.4],
        ),
        font=dict(family="Inter, system-ui, sans-serif", size=12),
        hoverlabel=dict(font_size=13),
    )
    return fig
