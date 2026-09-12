"""Landing section: name, contact chips, summary, CTAs and a stats strip."""

from __future__ import annotations

import datetime as dt

import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

from portfolio.config import ACCENT, PDF_DOWNLOAD_NAME, PDF_HREF
from portfolio.data import CV
from portfolio.ui import contact_chip, stat

COUNTRIES_WORKED_IN = "3"


def _contact() -> dmc.Group:
    return dmc.Group(
        [
            contact_chip("tabler:map-pin", CV.location, "#contact"),
            contact_chip("tabler:mail", CV.email, f"mailto:{CV.email}"),
            contact_chip(
                "tabler:brand-github",
                f"github.com/{CV.github}",
                f"https://github.com/{CV.github}",
            ),
        ],
        gap="lg",
        mt="xs",
    )


def _ctas() -> dmc.Group:
    return dmc.Group(
        [
            html.A(
                dmc.Button(
                    "Download CV (PDF)",
                    leftSection=DashIconify(icon="tabler:download", width=18),
                    size="md",
                ),
                href=PDF_HREF,
                download=PDF_DOWNLOAD_NAME,
                style={"textDecoration": "none"},
            ),
            html.A(
                dmc.Button(
                    "Get in touch",
                    variant="outline",
                    size="md",
                    leftSection=DashIconify(icon="tabler:send", width=18),
                ),
                href="#contact",
                style={"textDecoration": "none"},
            ),
        ],
        mt="lg",
    )


def _stats() -> dmc.Paper:
    years = (dt.date.today() - CV.experience[-1].start).days // 365
    return dmc.Paper(
        dmc.Group(
            [
                stat(f"{years}+", "years in software"),
                stat(str(len(CV.experience)), "roles"),
                stat(str(len(CV.education)), "degrees"),
                stat(COUNTRIES_WORKED_IN, "countries worked in"),
            ],
            gap={"base": 26, "sm": 50},
            justify="center",
        ),
        className="glass",
        radius="lg",
        p="lg",
        mt=32,
    )


def render() -> dmc.Box:
    return dmc.Box(
        dmc.Container(
            size="md",
            px="md",
            pt={"base": 56, "sm": 84},
            pb={"base": 10, "sm": 14},
            children=dmc.Stack(
                [
                    dmc.Title(CV.name, order=1, fz={"base": 34, "sm": 46}, c=ACCENT),
                    _contact(),
                    dmc.Text(CV.summary[0], mt="md", maw=680, c="dark"),
                    _ctas(),
                    _stats(),
                ],
                gap="xs",
            ),
        )
    )
