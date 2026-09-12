"""Self-contained canned Q&A for the portfolio chatbot.

No external API. Matching is keyword overlap + difflib fuzzy ratio against the
question bank below. Edit ``QA`` freely — each entry is (list of phrasings, answer).
"""

from __future__ import annotations

import difflib
import re

QA: list[tuple[list[str], str]] = [
    (
        ["who are you", "tell me about yourself", "introduce yourself", "your background", "about"],
        "I'm Abdelrahman Ali, a Financial Applications Developer at the European "
        "Stability Mechanism in Luxembourg. I have 3+ years building financial "
        "software (ETL pipelines, database design and maintenance, dashboards and market-data "
        "integrations). I hold a M.Sc. in Economics & Data Analysis and a B.Eng. "
        "in Electrical Engineering.",
    ),
    (
        ["what do you do", "current role", "current job", "what is your job", "where do you work"],
        "I'm a Fullstack Developer at the European Stability Mechanism "
        "(ESM) in Luxembourg (since May 2024). I build and deploy applications, "
        "write unit tests, run UAT, build ETL processes for market data, and "
        "integrate financial data APIs like Bloomberg and Refinitiv.",
    ),
    (
        ["day to day", "typical day", "your day to day", "average day", "day in the life",
         "daily routine", "daily tasks", "normal day look like"],
        "Depends on the day, but usually some mix of: building or refactoring features "
        "for our internal apps, writing unit tests, running through UAT with whoever "
        "owns the business side, and keeping the ETL jobs that pull in market data "
        "actually working. I also write up docs so the next person (often "
        "future me) isn't stuck guessing how something works.",
    ),
    (
        ["what languages", "programming languages", "which languages do you code", "tech stack", "what technologies"],
        "Main languages: Python, C, C++ and SQL, plus basic JavaScript and CSS. "
        "Day to day I use Python Dash, Pandas, SQLAlchemy, MS SQL Server, Jenkins, "
        "Git, Selenium, SonarQube and Pylint.",
    ),
    (
        ["python", "do you know python", "how good is your python", "python experience"],
        "Python is my primary language — I use it for full-stack app development "
        "(Dash), ETL pipelines, data analysis, unit testing and automation. This "
        "site is built with Python and Dash.",
    ),
    (
        ["data", "data analysis", "data science", "machine learning", "ml", "nlp"],
        "My M.Sc. covered Machine Learning, NLP, Big Data Management, Statistics and "
        "R. My thesis was 'Predicting Inflation in the European Union Using Machine "
        "Learning'. Professionally, I design and build ETL data pipelines and analytics. "
        "I would like to expand my scope to include ML and deep learning model building "
        "and their CI/CD pipelines.",
    ),
    (
        ["next goal", "future goal", "next mission", "career goal", "future plans",
         "what's next for you", "long term goal", "what are you working towards",
         "next accomplishment", "biggest goal", "where do you see yourself"],
        "Moving from applying ML in coursework and side projects to actually shipping "
        "AI software for a living: deep learning and LLM-based systems, not just "
        "dashboards and ETL. I'm already putting in the work outside my day job with "
        "FastAPI, Docker, retrieval-augmented generation, and LLM agents, building on "
        "the ML and NLP I studied in my M.Sc. and the inflation-forecasting thesis I "
        "wrote. The goal is a role where that's the actual job, not the side project.",
    ),
    (
        ["experience", "work history", "previous jobs", "career", "past roles"],
        "ESM: Financial Applications Developer  and IT Officer (2023–now) "
        "(2023–2024); DAL Group in Sudan: Project Manager & Business Analyst "
        "(2020–2021) and a two-year Graduate Development Program (2018–2020).",
    ),
    (
        ["education", "study", "studies", "studied", "degree", "masters", "bachelor", "university", "qualifications", "academic"],
        "M.Sc. in Economics and Data Analysis: a double degree from the University "
        "of Trier and the University of Bergamo (2021–2023). B.Eng. (Hons) in "
        "Electrical Engineering (Control) from Sudan University of Science and "
        "Technology (2012–2017).",
    ),
    (
        ["power bi", "tableau", "dashboards", "bi", "business intelligence", "visualization"],
        "As IT Officer at ESM I led a project migrating market data and dashboards "
        "from Tableau to Power BI, and built Power Platform automations. I also "
        "build interactive dashboards in Python Dash.",
    ),
    (
        ["etl", "pipelines", "data engineering"],
        "I build ETL processes for the scheduled update of market data at ESM — "
        "retrieving from financial data APIs (Bloomberg, Refinitiv), processing "
        "with Pandas / SQLAlchemy, and loading into MS SQL Server.",
    ),
    (
        ["languages you speak", "spoken languages", "do you speak french", "english level", "arabic", "german"],
        "Arabic (native), English C1 (IELTS Academic), French A2 (ongoing at INL), "
        "German A1.",
    ),
    (
        ["location", "where are you based", "where do you live", "luxembourg", "relocate", "work permit", "visa"],
        "I'm based in Luxembourg and hold a European Blue Card.",
    ),
    (
        ["hobbies", "interests", "outside work", "free time", "beyond work"],
        "Photography, weight lifting, DJing and music production.",
    ),
    (
        ["music", "dj", "djing", "production", "electronic music"],
        "I DJ and produce music in my spare time.",
    ),
    (
        ["contact", "email", "get in touch", "reach you", "hire", "available"],
        "Email me at abdu96sharfi@gmail.com or find me on GitHub at github.com/"
        "A-Sharfi. There's a Download CV button at the top of the page.",
    ),
    (
        ["cv", "resume", "download"],
        "Use the 'Download CV (PDF)' button in the header. It's a polished PDF "
        "generated from the same data as this site.",
    ),
    (
        ["this site", "how was this built", "what is this made with", "portfolio tech"],
        "This portfolio is a Python Dash app with Dash Mantine Components and "
        "Plotly, deployed on a host. The PDF CV is generated with RenderCV "
        "from a single YAML file that also feeds this page.",
    ),
]

_GREETINGS = {"hi", "hello", "hey"}
_STOPWORDS = {
    "a", "an", "the", "is", "are", "do", "does", "you", "your", "what", "who",
    "how", "tell", "me", "about", "of", "to", "in", "on", "and", "with", "have",
    "has", "can", "i", "my",
}

_FALLBACK = (
    "Sorry, I am designed to only answer questions about Abdelrahman's CV."
    "Ask be about his experience, Python/data skills, education, languages, hobbies, or "
    "how to get in touch."
)


def _tokens(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9+#]+", text.lower())} - _STOPWORDS


def answer(query: str) -> str:
    q = query.strip().lower()
    if not q:
        return "Ask me about my experience, skills, education or how to get in touch."
    if q.rstrip("!.") in _GREETINGS:
        return "Hi! Ask me anything about Abdelrahman's experience, skills or background."

    q_tokens = _tokens(q)
    best_score = 0.0
    best_answer = ""
    for phrasings, ans in QA:
        score = 0.0
        for phrase in phrasings:
            overlap = len(q_tokens & _tokens(phrase))
            ratio = difflib.SequenceMatcher(None, q, phrase).ratio()
            score = max(score, overlap + ratio)
        if score > best_score:
            best_score, best_answer = score, ans

    return best_answer if best_score >= 0.6 else _FALLBACK


SUGGESTIONS = [
    "What do you do?",
    "What's your tech stack?",
    "Tell me about your experience",
    "What's next for you?",
    "How can I contact you?",
]
