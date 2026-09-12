"""Colours, asset paths, icon maps and the Mantine theme."""

PRIMARY = "blue"
ACCENT = "#1c4587"
EDUCATION_ACCENT = "#2f9e8f"
EDUCATION_COLOR = "teal"  # Mantine palette name matching EDUCATION_ACCENT, for dmc components

PDF_HREF = "/assets/Abdelrahman_Ali_CV.pdf"
PDF_DOWNLOAD_NAME = "Abdelrahman_Ali_CV.pdf"

# Applied to every glass card: translucent panel + hover lift (see assets/style.css).
GLASS = "glass hover-card"

NAV_LINKS = [
    ("Experience", "#experience"),
    ("Skills", "#skills"),
    ("Education", "#education"),
    ("Beyond work", "#interests"),
    ("Contact", "#contact"),
]

SKILL_ICONS = {
    "Languages": "tabler:code",
    "Tools & Practices": "tabler:tools",
    "Data & APIs": "tabler:database",
    "BI & Automation": "tabler:chart-histogram",
    "Domain": "tabler:target-arrow",
}

INTEREST_ICONS = {
    "Photography": "tabler:camera",
    "Gym": "tabler:barbell",
    "DJing & music production": "tabler:music",
}

THEME = {
    "primaryColor": PRIMARY,
    "fontFamily": "Inter, system-ui, -apple-system, sans-serif",
    "headings": {"fontFamily": "Inter, system-ui, sans-serif"},
}
