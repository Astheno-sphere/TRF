"""
Presentation layer for app.py: theme, the record life-strip chart and the live
architecture diagram. Nothing here computes a result; every number shown in the app
comes from trf_checker.py or the optional modules, unmodified.
"""

import pathlib

import altair as alt
import streamlit as st
import streamlit.components.v1 as components

ASSETS = pathlib.Path(__file__).resolve().parent / "assets"

# Palette: named for what each colour means in the model, and matched to the
# semantic colours of the Archify diagrams (Figures 4.1 and 5.1).
INK = "#10263A"        # text
LEDGER = "#EEF2F1"     # page
SEAL = "#0F7C6B"       # accountable: Semantics II holds
FLOOR = "#C98A12"      # retention floor: must stay verifiable
TRIGGER = "#6B4FBB"    # erasure request / permit expiry and the deadlines they set
REVOKE = "#B4233C"     # contradiction under Semantics I; key destruction
MUTED = "#8A9AA6"
FONT = "Atkinson Hyperlegible, Helvetica, Arial, sans-serif"

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Atkinson+Hyperlegible:wght@400;700&family=JetBrains+Mono:wght@400;600&display=swap');
html, body, .stMarkdown, p, li, label, input, textarea {{ font-family: 'Atkinson Hyperlegible', sans-serif; }}
h1, h2, h3, h4 {{ font-family: 'Bricolage Grotesque', sans-serif !important; color: {INK}; letter-spacing: -0.01em; }}
h1 {{ font-size: 2.6rem !important; line-height: 1.08 !important; font-weight: 700 !important; max-width: 22ch; }}
code, pre, .stCode {{ font-family: 'JetBrains Mono', monospace !important; }}
.block-container {{ max-width: 1180px; padding-top: 2.2rem; }}
.lede {{ font-size: 1.15rem; line-height: 1.6; max-width: 68ch; color: #2C4255; }}
.verdict {{ border-left: 4px solid var(--c); padding: .7rem 1rem; margin: .4rem 0 1rem;
           background: white; border-radius: 0 6px 6px 0; max-width: 72ch; }}
.verdict b {{ color: var(--c); }}
.facts {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: .6rem; margin: .6rem 0 1.2rem; }}
.fact {{ background: white; border: 1px solid #D5DEDB; border-radius: 6px; padding: .6rem .8rem; }}
.fact .v {{ font-family: 'Bricolage Grotesque', sans-serif; font-size: 1.6rem; font-weight: 700; color: {INK}; }}
.fact .k {{ font-size: .86rem; color: #4A5E6E; }}
.legend span {{ display: inline-block; margin-right: 1rem; font-size: .88rem; }}
.legend i {{ display: inline-block; width: .8rem; height: .8rem; border-radius: 2px; margin-right: .3rem; vertical-align: -1px; }}
section[data-testid="stSidebar"] {{ background: #E2E9E7; }}
section[data-testid="stSidebar"] .stRadio label {{ font-size: 1rem; }}
</style>
"""


def theme():
    st.markdown(CSS, unsafe_allow_html=True)


def verdict(text, colour=SEAL):
    st.markdown(f'<div class="verdict" style="--c:{colour}">{text}</div>', unsafe_allow_html=True)


def facts(pairs):
    cells = "".join(f'<div class="fact"><div class="v">{v}</div><div class="k">{k}</div></div>'
                    for k, v in pairs)
    st.markdown(f'<div class="facts">{cells}</div>', unsafe_allow_html=True)


# ----------------------------------------------------------------------
# The record life strip: one row per demand or semantics, one cell per month
# ----------------------------------------------------------------------

ROWS = ["C1 floor: must stay verifiable",
        "C2 / C3: payload must be gone",
        "Semantics I: verifiable = readable",
        "Semantics II: payload readable",
        "Semantics II: record verifiable"]

STATES = {
    "required": FLOOR, "must be gone": TRIGGER, "contradiction": REVOKE,
    "readable": "#7FC4B6", "destroyed, entry logged": "#2F5D73", "verifiable": SEAL,
    "not required": "#DCE3E1",
}


def life_strip(rec, inv_month, deadline, horizon, now):
    """rec is a trf_checker.Record; inv_month and deadline are its t_I and earliest
    deadline (equal in the model); the strip is drawn from the model's quantities only."""
    t_a, end = rec.t_a, rec.t_a + rec.floor
    cells = []
    for t in range(0, horizon + 1):
        in_floor = t_a <= t <= end
        gone = t >= deadline
        cells.append((ROWS[0], t, "required" if in_floor else "not required"))
        cells.append((ROWS[1], t, "must be gone" if gone else "not required"))
        if in_floor and gone:
            s1 = "contradiction"
        elif t >= t_a and not gone:
            s1 = "readable"
        else:
            s1 = "not required"
        cells.append((ROWS[2], t, s1))
        cells.append((ROWS[3], t, "readable" if t_a <= t < inv_month else
                      ("destroyed, entry logged" if t >= inv_month else "not required")))
        cells.append((ROWS[4], t, "verifiable" if in_floor else "not required"))
    data = alt.Data(values=[{"row": r, "t": t, "t2": t + 1, "state": s} for r, t, s in cells])
    scale = alt.Scale(domain=list(STATES), range=list(STATES.values()))
    base = alt.Chart(data).mark_rect(stroke="white", strokeWidth=0.6 if horizon < 60 else 0).encode(
        x=alt.X("t:Q", title="month", scale=alt.Scale(domain=[0, horizon + 1])), x2="t2:Q",
        y=alt.Y("row:N", sort=ROWS, title=None, axis=alt.Axis(labelLimit=260, labelFontSize=12)),
        color=alt.Color("state:N", scale=scale, legend=alt.Legend(orient="bottom", title=None, columns=4)),
        tooltip=[alt.Tooltip("row:N", title="row"), alt.Tooltip("t:Q", title="month"),
                 alt.Tooltip("state:N", title="state")])
    marker = alt.Chart(alt.Data(values=[{"t": now + 0.5}])).mark_rule(color=INK, strokeWidth=2).encode(x="t:Q")
    return (base + marker).properties(height=220).configure_view(stroke=None).configure_axis(
        labelFont=FONT, titleFont=FONT, labelColor=INK, titleColor=INK
    ).configure_legend(labelFont=FONT, labelFontSize=12)


# ----------------------------------------------------------------------
# Live architecture diagram: the Archify figure with the active components lit
# ----------------------------------------------------------------------

def diagram(name, active=(), glow=SEAL, height=640):
    html = (ASSETS / name).read_text(encoding="utf-8")
    if active:
        sel = ",".join(f'[data-node-id="{n}"]' for n in active)
        html = html.replace("</head>", (
            "<style>[data-node-id]{opacity:.22;transition:opacity .35s ease}"
            f"{sel}{{opacity:1!important;filter:drop-shadow(0 0 7px {glow})}}"
            "@media (prefers-reduced-motion: reduce){[data-node-id]{transition:none}}</style></head>"), 1)
    components.html(html, height=height, scrolling=True)


def legend(items):
    st.markdown('<div class="legend">' + "".join(
        f'<span><i style="background:{c}"></i>{t}</span>' for t, c in items) + "</div>",
        unsafe_allow_html=True)
