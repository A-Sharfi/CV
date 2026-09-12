"""Dash server entry point.

Run locally:   python app.py
Production:    gunicorn app:server
"""

import dash_mantine_components as dmc
from dash import Dash, _dash_renderer

_dash_renderer._set_react_version("18.2.0")

from portfolio.data import CV
from portfolio.layout import build_layout

app = Dash(
    __name__,
    external_stylesheets=dmc.styles.ALL,
    title=f"{CV.name}'s CV",
    update_title=None,
)
server = app.server
app.layout = build_layout()

if __name__ == "__main__":
    app.run(debug=True, port=8050)
