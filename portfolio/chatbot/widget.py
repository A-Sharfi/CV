"""Floating 'ask me anything' widget backed by canned Q&A (no external API).

Importing this module registers its callbacks, so ``portfolio.layout`` just
imports it and drops ``widget()`` into the layout.
"""

from __future__ import annotations

import dash_mantine_components as dmc
from dash import ALL, Input, Output, State, callback, clientside_callback, ctx, dcc, html
from dash_iconify import DashIconify

from portfolio.chatbot import qa
from portfolio.config import PRIMARY

_GREETING = (
    "Hi — I'm a small canned bot. Ask about experience, skills, education, "
    "languages or contact."
)
_PANEL_STYLE = {"width": 340, "maxWidth": "90vw"}


def _suggestions() -> dmc.Group:
    return dmc.Group(
        [
            dmc.Button(
                text,
                id={"type": "sugg", "i": i},
                variant="light",
                color=PRIMARY,
                size="compact-xs",
                radius="xl",
            )
            for i, text in enumerate(qa.SUGGESTIONS)
        ],
        gap=6,
        mt=8,
    )


def _panel() -> dmc.Paper:
    return dmc.Paper(
        id="chat-panel",
        withBorder=True,
        shadow="lg",
        radius="md",
        p="sm",
        className="glass-strong",
        style={**_PANEL_STYLE, "display": "none"},
        children=[
            dmc.Group(
                [
                    dmc.Text("Ask me about Abdelrahman", fw=600, size="sm"),
                    dmc.ActionIcon(
                        DashIconify(icon="tabler:x", width=16),
                        id="chat-close",
                        variant="subtle",
                        color="gray",
                        size="sm",
                    ),
                ],
                justify="space-between",
            ),
            dmc.ScrollArea(h=260, mt=8, children=dmc.Stack(id="chat-window", gap=8, px=4)),
            _suggestions(),
            dmc.Group(
                [
                    dmc.TextInput(
                        id="chat-input",
                        placeholder="Type a question…",
                        style={"flex": 1},
                        size="sm",
                    ),
                    dmc.ActionIcon(
                        DashIconify(icon="tabler:send", width=16),
                        id="chat-send",
                        variant="filled",
                        color=PRIMARY,
                        size="lg",
                    ),
                ],
                gap=6,
                mt=8,
                align="flex-end",
            ),
            dmc.Text(
                "Canned answers only — no data leaves this page.", size="xs", c="dimmed", mt=6
            ),
        ],
    )


def widget() -> html.Div:
    return html.Div(
        [
            dcc.Store(id="chat-open", data=False),
            dcc.Store(id="chat-history", data=[]),
            dmc.Affix(
                dmc.Stack(
                    [
                        _panel(),
                        dmc.Group(
                            dmc.Button(
                                "Ask me anything",
                                id="chat-fab",
                                leftSection=DashIconify(icon="tabler:message-chatbot", width=18),
                                radius="xl",
                                size="sm",
                                style={"boxShadow": "0 4px 16px rgba(28,69,135,0.35)"},
                            ),
                            justify="flex-end",
                        ),
                    ],
                    gap=10,
                    align="flex-end",
                ),
                position={"bottom": 20, "right": 20},
            ),
        ]
    )


clientside_callback(
    """
    function(openClicks, closeClicks, isOpen) {
        const t = window.dash_clientside.callback_context.triggered;
        if (!t || !t.length) return window.dash_clientside.no_update;
        const id = t[0].prop_id.split(".")[0];
        const next = id === "chat-close" ? false : !isOpen;
        return [next, {width: 340, maxWidth: "90vw", display: next ? "block" : "none"}];
    }
    """,
    [Output("chat-open", "data"), Output("chat-panel", "style")],
    [Input("chat-fab", "n_clicks"), Input("chat-close", "n_clicks")],
    State("chat-open", "data"),
    prevent_initial_call=True,
)


@callback(
    Output("chat-history", "data"),
    Output("chat-input", "value"),
    Input("chat-send", "n_clicks"),
    Input("chat-input", "n_submit"),
    Input({"type": "sugg", "i": ALL}, "n_clicks"),
    State("chat-input", "value"),
    State("chat-history", "data"),
    prevent_initial_call=True,
)
def _on_message(_send, _submit, _sugg, value, history):
    trigger = ctx.triggered_id
    if isinstance(trigger, dict) and trigger.get("type") == "sugg":
        if not _sugg or all(not clicks for clicks in _sugg):
            return history, value or ""
        query = qa.SUGGESTIONS[trigger["i"]]
    else:
        query = (value or "").strip()

    if not query:
        return history, ""

    history = (history or []) + [
        {"role": "user", "text": query},
        {"role": "bot", "text": qa.answer(query)},
    ]
    return history, ""


@callback(Output("chat-window", "children"), Input("chat-history", "data"))
def _render_history(history):
    if not history:
        return [dmc.Text(_GREETING, className="chat-bubble-bot", size="sm")]
    return [
        dmc.Text(
            msg["text"],
            className="chat-bubble-user" if msg["role"] == "user" else "chat-bubble-bot",
            size="sm",
        )
        for msg in history
    ]
