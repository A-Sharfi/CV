"""Page footer."""

from __future__ import annotations

import datetime as dt

import dash_mantine_components as dmc

from portfolio.data import CV


def render() -> dmc.Box:
    return dmc.Box(
        style={"borderTop": "1px solid #e9ecef"},
        children=dmc.Container(
            size="md",
            px="md",
            py="xl",
            children=dmc.Group(
                [
                    dmc.Text(f"© {dt.date.today().year} {CV.name}", size="sm", c="dimmed"),
                    dmc.Text("Built with Python, Dash & Plotly", size="sm", c="dimmed"),
                ],
                justify="space-between",
            ),
        ),
    )
