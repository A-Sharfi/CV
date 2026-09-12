"""Dash server entry point.

Run locally:   python app.py
Production:    gunicorn app:server
"""

import dash_mantine_components as dmc
from dash import Dash, _dash_renderer

_dash_renderer._set_react_version("18.2.0")

from portfolio.config import OG_IMAGE_HREF, SITE_DESCRIPTION, SITE_URL
from portfolio.data import CV
from portfolio.layout import build_layout

_PAGE_TITLE = f"{CV.name} | {CV.experience[0].title}"

app = Dash(
    __name__,
    external_stylesheets=dmc.styles.ALL,
    title=_PAGE_TITLE,
    update_title=None,
)
server = app.server
app.layout = build_layout()

_OG_IMAGE_URL = SITE_URL + OG_IMAGE_HREF
app.index_string = app.index_string.replace(
    "{%metas%}",
    "{%metas%}\n"
    f'        <meta name="description" content="{SITE_DESCRIPTION}">\n'
    f'        <meta property="og:type" content="website">\n'
    f'        <meta property="og:url" content="{SITE_URL}">\n'
    f'        <meta property="og:title" content="{_PAGE_TITLE}">\n'
    f'        <meta property="og:description" content="{SITE_DESCRIPTION}">\n'
    f'        <meta property="og:image" content="{_OG_IMAGE_URL}">\n'
    '        <meta property="og:image:width" content="1200">\n'
    '        <meta property="og:image:height" content="630">\n'
    '        <meta name="twitter:card" content="summary_large_image">\n'
    f'        <meta name="twitter:title" content="{_PAGE_TITLE}">\n'
    f'        <meta name="twitter:description" content="{SITE_DESCRIPTION}">\n'
    f'        <meta name="twitter:image" content="{_OG_IMAGE_URL}">',
)

if __name__ == "__main__":
    app.run(debug=True, port=8050)
