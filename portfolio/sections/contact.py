"""Contact: links only (email, GitHub, PDF) — no form, no backend."""

from __future__ import annotations

import dash_mantine_components as dmc

from portfolio.config import PDF_HREF
from portfolio.data import CV
from portfolio.ui import link_button, section


def render() -> dmc.Container:
    return section(
        "contact",
        "Get in touch",
        dmc.Paper(
            [
                dmc.Text(
                    "Open to conversations about financial-applications and data "
                    "engineering roles.",
                    c="dark",
                    mb="md",
                ),
                dmc.Group(
                    [
                        link_button("Email", "tabler:mail", f"mailto:{CV.email}"),
                        link_button(
                            "GitHub",
                            "tabler:brand-github",
                            f"https://github.com/{CV.github}",
                            variant="outline",
                        ),
                        link_button(
                            "Download CV", "tabler:download", PDF_HREF, variant="outline"
                        ),
                    ]
                ),
            ],
            className="glass",
            radius="lg",
            p={"base": "md", "sm": "xl"},
        ),
    )
