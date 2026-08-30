#!/usr/bin/env python3
"""Build Google-proof query chips HTML."""

import urllib.parse


def g(q: str) -> str:
    return (
        "https://www.google.com/search?q="
        + urllib.parse.quote_plus(q)
        + "&hl=bg&gl=bg"
    )


def chips(queries: list[str]) -> str:
    return "\n".join(
        f'                <a class="search-chip" href="{g(q)}" target="_blank" rel="noopener noreferrer">{q}</a>'
        for q in queries
    )


def google_proof(queries: list[str], note: str = "") -> str:
    note_html = f'\n              <p class="google-proof__note">{note}</p>' if note else ""
    return f"""            <div class="google-proof">
              <p class="google-proof__lead">Провери сам в Google</p>{note_html}
              <div class="google-proof__queries">
{chips(queries)}
              </div>
            </div>"""
