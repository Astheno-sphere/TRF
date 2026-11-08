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
INK = "#1B1C20"        # text: charcoal
LEDGER = "#FFFFFF"     # page
SEAL = "#0F7C6B"       # accountable: Semantics II holds
FLOOR = "#C98A12"      # retention floor: must stay verifiable
TRIGGER = "#6B4FBB"    # erasure request / permit expiry and the deadlines they set
REVOKE = "#B4233C"     # contradiction under Semantics I; key destruction
MUTED = "#8A9AA6"
FONT = "IBM Plex Sans, Helvetica, Arial, sans-serif"

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&family=Source+Serif+4:opsz,wght@8..60,400;8..60,500&display=swap');
html, body, .stMarkdown, p, li, label, input, textarea {{ font-family: 'IBM Plex Sans', sans-serif; }}
h1, h2, h3, h4 {{ font-family: 'IBM Plex Sans', sans-serif !important; color: {INK}; letter-spacing: -0.01em; }}
h1 {{ font-size: 2.2rem !important; line-height: 1.12 !important; font-weight: 600 !important; letter-spacing: -0.018em; max-width: 24ch; }}
h2, h3 {{ font-weight: 600 !important; letter-spacing: -0.01em; }}
code, pre, .stCode {{ font-family: 'IBM Plex Mono', monospace !important; }}
.block-container {{ max-width: 1180px; padding-top: 2.2rem; }}
.lede {{ font-family: 'Source Serif 4', Georgia, serif; font-size: 1.18rem; line-height: 1.62; max-width: 66ch; color: #33343A; }}
.verdict {{ border-left: 2px solid var(--c); padding: .2rem 0 .2rem 1rem; margin: .6rem 0 1.1rem;
           max-width: 70ch; }}
.verdict b {{ color: var(--c); }}
.facts {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: .6rem; margin: .6rem 0 1.2rem; }}
.fact {{ background: white; border: 0; border-radius: 0; padding: .55rem .2rem .2rem 0; }}
.fact .v {{ font-family: 'IBM Plex Sans', sans-serif; font-size: 1.45rem; font-weight: 600; color: {INK}; }}
.fact .k {{ font-size: .84rem; color: #6A6B72; }}
.legend span {{ display: inline-block; margin-right: 1rem; font-size: .88rem; }}
.legend i {{ display: inline-block; width: .8rem; height: .8rem; border-radius: 2px; margin-right: .3rem; vertical-align: -1px; }}
section[data-testid="stSidebar"] {{ background: #F5F4F0; border-right: 1px solid #E6E2D8; }}

/* Facts: one card per quantity, its top rule in the colour of what it is in the model */
.fact {{ border-top: 2px solid var(--c, #D9D4C8); }}
.fact .v {{ font-variant-numeric: tabular-nums; line-height: 1.15; }}

/* Brand mark: the three clocks on one record, floor, deadline, accountable */
.brand {{ margin: 0 0 1.1rem; }}
.brand .t {{ font-family: 'IBM Plex Sans', sans-serif; font-weight: 600; font-size: 1.12rem; letter-spacing: -0.01em;
            line-height: 1.15; color: {INK}; }}
.brand .band {{ display: grid; grid-template-columns: 5fr 2fr 3fr; height: 3px; margin: .6rem 0 .5rem; overflow: hidden; }}
.brand .band i:nth-child(1) {{ background: {FLOOR}; }}
.brand .band i:nth-child(2) {{ background: {TRIGGER}; }}
.brand .band i:nth-child(3) {{ background: {SEAL}; }}
.brand .s {{ font-size: .84rem; color: #6A6B72; }}

/* Navigation: rows, not radio buttons; the walk is numbered because it is a sequence */
section[data-testid="stSidebar"] [role="radiogroup"] {{ counter-reset: step; gap: 0; }}
section[data-testid="stSidebar"] [role="radiogroup"] > div {{ width: 100%; }}
section[data-testid="stSidebar"] [data-testid="stRadioOption"] {{
    padding: .36rem .6rem .36rem .7rem; margin: 0; border-left: 3px solid transparent;
    border-radius: 0 5px 5px 0; cursor: pointer; width: 100%; }}
section[data-testid="stSidebar"] [data-testid="stRadioOption"] > div > div:first-child {{ display: none; }}
section[data-testid="stSidebar"] [data-testid="stRadioOption"]:hover {{ background: #ECEAE3; }}
section[data-testid="stSidebar"] [data-testid="stRadioOption"][data-selected="true"] {{
    border-left-color: {INK}; background: #FFFFFF; }}
section[data-testid="stSidebar"] [data-testid="stRadioOption"][data-selected="true"] p {{ font-weight: 700; color: {INK}; }}
section[data-testid="stSidebar"] [data-testid="stRadioOption"]:has(input:focus-visible) {{ outline: 1px dashed {MUTED}; outline-offset: -1px; }}
section[data-testid="stSidebar"] [role="radiogroup"] > div:nth-child(-n+7) p::before {{
    counter-increment: step; content: counter(step); display: inline-block; width: 1.35rem;
    color: {MUTED}; font-variant-numeric: tabular-nums; }}
section[data-testid="stSidebar"] [role="radiogroup"] > div:nth-child(n+8) p {{ padding-left: 1.35rem; }}
section[data-testid="stSidebar"] [role="radiogroup"] > div:nth-child(1)::before,
section[data-testid="stSidebar"] [role="radiogroup"] > div:nth-child(8)::before,
section[data-testid="stSidebar"] [role="radiogroup"] > div:nth-child(10)::before {{
    display: block; font-size: .8rem; color: #6A6B72; margin: 1rem 0 .3rem .1rem; }}
section[data-testid="stSidebar"] [role="radiogroup"] > div:nth-child(1)::before {{ content: "The walk, in the order of the thesis"; margin-top: 0; }}
section[data-testid="stSidebar"] [role="radiogroup"] > div:nth-child(8)::before {{ content: "Full runs"; }}
section[data-testid="stSidebar"] [role="radiogroup"] > div:nth-child(10)::before {{ content: "Context, not thesis claims"; }}

/* Alerts in the palette instead of the framework's blue */
div[data-testid="stAlert"] {{ background: white; border: 0; border-left: 2px solid {SEAL};
    border-radius: 0; color: {INK}; }}
div[data-testid="stAlert"] p {{ color: {INK}; }}
div[data-testid="stAlert"] > div {{ background: transparent !important; color: {INK} !important; }}
div[data-testid="stAlertContentError"], div[data-testid="stAlert"]:has(div[data-testid="stAlertContentError"]) {{ border-left-color: {REVOKE}; }}
div[data-testid="stAlert"]:has(div[data-testid="stAlertContentWarning"]) {{ border-left-color: {FLOOR}; }}

/* Metrics read like the facts */
div[data-testid="stMetricValue"] {{ font-family: 'IBM Plex Sans', sans-serif; font-weight: 700;
    font-variant-numeric: tabular-nums; color: {INK}; }}
div[data-testid="stMetricLabel"] p {{ font-size: .88rem; color: #6A6B72; }}

/* Buttons: quiet until used */
.stButton > button {{ border: 1px solid #CFCAC0; border-radius: 3px; background: white; color: {INK}; font-weight: 500; }}
.stButton > button:hover {{ border-color: {SEAL}; color: {SEAL}; }}
.stButton > button:focus-visible {{ outline: 2px solid {SEAL}; outline-offset: 2px; }}

/* The walk, as a strip of its steps */
.walk {{ display: grid; grid-template-columns: repeat(var(--n), 1fr); gap: 4px; margin: .4rem 0 .5rem; }}
.walk i {{ height: 5px; border-radius: 2px; background: #CBD6D3; }}
.walk i.done {{ background: #8CC2B7; }}
.walk i.now {{ background: {SEAL}; }}
.walkcap {{ font-size: .86rem; color: #6A6B72; }}
@media (prefers-reduced-motion: reduce) {{ * {{ transition: none !important; animation: none !important; }} }}
</style>
"""


def theme():
    st.markdown(CSS, unsafe_allow_html=True)


def brand():
    st.markdown('<div class="brand"><div class="t">Tri-Lateral Retention Feasibility</div>'
                '<div class="band" aria-hidden="true"><i></i><i></i><i></i></div>'
                '<div class="s">One audit record, three legal clocks. MSc thesis, Høgskolen i Molde, 2026.</div></div>',
                unsafe_allow_html=True)


def walk_progress(i, steps):
    marks = "".join(f'<i class="{"now" if k == i else "done" if k < i else ""}" title="{name}"></i>'
                    for k, name in enumerate(steps))
    cap = f"Step {i + 1} of {len(steps)} in the walk" + (f". Next: {steps[i + 1]}" if i + 1 < len(steps) else ". The end of the walk")
    st.markdown(f'<div class="walk" style="--n:{len(steps)}" role="img" aria-label="{cap}">{marks}</div>'
                f'<div class="walkcap">{cap}</div>', unsafe_allow_html=True)


def verdict(text, colour=SEAL):
    st.markdown(f'<div class="verdict" style="--c:{colour}">{text}</div>', unsafe_allow_html=True)


def facts(pairs, colours=None):
    """pairs of (label, value); colours, if given, mark each card with what it is in the model."""
    colours = colours or [None] * len(pairs)
    cells = "".join(f'<div class="fact"{f" style=\"--c:{c}\"" if c else ""}><div class="v">{v}</div>'
                    f'<div class="k">{k}</div></div>' for (k, v), c in zip(pairs, colours))
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
    "not required": "#DCE3E1", "fails its check": "#B0592B",
}


def life_strip(rec, inv_month, deadline, horizon, now):
    """rec is a trf_checker.Record; inv_month and deadline are its t_I and earliest
    deadline (equal in the model); the strip is drawn from the model's quantities only."""
    import trf_checker as trf             # the Semantics II row is computed, not drawn
    t_a, end = rec.t_a, rec.t_a + rec.floor
    integ = trf.integrity(rec) if getattr(rec, "log_idx", None) else (False, "not logged")
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
        cells.append((ROWS[4], t, ("verifiable" if trf.V_II(rec, t, integ)[0] else "fails its check")
                                   if in_floor else "not required"))
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
