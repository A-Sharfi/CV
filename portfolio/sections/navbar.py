"""Sticky glass navigation bar (hidden on small screens)."""

import dash_mantine_components as dmc
from dash import html

from portfolio.config import NAV_LINKS

_STYLE = {
    "position": "sticky",
    "top": 0,
    "zIndex": 100,
    "background": "rgba(255,255,255,0.5)",
    "backdropFilter": "blur(14px) saturate(160%)",
    "WebkitBackdropFilter": "blur(14px) saturate(160%)",
    "borderBottom": "1px solid rgba(255,255,255,0.55)",
}


def render() -> dmc.Box:
    return dmc.Box(
        visibleFrom="sm",
        style=_STYLE,
        children=dmc.Container(
            size="md",
            px="md",
            py="sm",
            children=dmc.Group(
                [
                    html.A(label, href=href, className="nav-link")
                    for label, href in NAV_LINKS
                ],
                gap="xl",
                justify="center",
            ),
        ),
    )
