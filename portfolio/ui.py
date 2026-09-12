"""Presentational helpers shared across sections."""

from __future__ import annotations

import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

from portfolio.config import ACCENT


def reveal(*children) -> html.Div:
    """Wrap content so it fades in when scrolled into view (assets/portfolio.js)."""
    return html.Div(className="reveal", children=list(children))


def section(section_id: str, title: str, *children) -> dmc.Container:
    """A titled page section; every child is wrapped in a scroll-reveal."""
    return dmc.Container(
        id=section_id,
        className="scroll-target",
        size="md",
        px="md",
        py={"base": 36, "sm": 48},
        children=[
            reveal(dmc.Title(title, order=2, mb="lg", c=ACCENT)),
            *[reveal(child) for child in children],
        ],
    )


def stat(value: str, label: str) -> dmc.Stack:
    return dmc.Stack(
        [
            dmc.Text(value, fw=700, fz={"base": 24, "sm": 30}, c=ACCENT),
            dmc.Text(label, size="sm", c="dimmed"),
        ],
        gap=0,
        align="center",
    )


def contact_chip(icon: str, label: str, href: str) -> html.A:
    # Plain <a>, not dmc.Anchor: dmc.Anchor does SPA navigation and swallows
    # in-page "#section" jumps.
    return html.A(
        dmc.Group(
            [DashIconify(icon=icon, width=18), dmc.Text(label, size="sm")],
            gap=6,
            wrap="nowrap",
        ),
        href=href,
        target="_blank" if href.startswith("http") else None,
        style={"textDecoration": "none", "color": "var(--mantine-color-dimmed)"},
    )


def link_button(label: str, icon: str, href: str, **button_kwargs) -> html.A:
    return html.A(
        dmc.Button(
            label, leftSection=DashIconify(icon=icon, width=18), size="md", **button_kwargs
        ),
        href=href,
        target="_blank" if href.startswith("http") else None,
        style={"textDecoration": "none"},
    )
