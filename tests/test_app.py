"""Success criteria for the artefact and its viewer.

Run: python3 -m pytest -q tests/
1. Every recorded console run in docs/ reproduces byte for byte.
2. Every page of the app renders without an exception.
3. The claim ledger shows no figure differing from the thesis.
4. Proposition statements and quoted limits appear verbatim in Chapter 4
   (only when the thesis repository is present beside this one; skipped otherwise).
"""
import os
import pathlib
import re
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
RUNS = [
    (["trf_checker.py"], "expected_trf_output.txt"),
    (["trf_checker.py", "--delta-witness"], "expected_delta_witness_output.txt"),
    (["cross_sector_check.py"], "expected_cross_sector_output.txt"),
    (["norwegian_layer.py"], "expected_norwegian_output.txt"),
    (["synthea_layer.py"], "expected_synthea_subset_output.txt"),
    (["crypto_envelope.py"], "expected_crypto_envelope_output.txt"),
    (["z3_check.py"], "expected_z3_check_output.txt"),
]


@pytest.mark.parametrize("cmd,expected", RUNS, ids=[" ".join(c) for c, _ in RUNS])
def test_recorded_output_reproduces(cmd, expected):
    out = subprocess.run([sys.executable, *cmd], cwd=ROOT, capture_output=True, text=True).stdout
    assert out == (ROOT / "docs" / expected).read_text(encoding="utf-8")


def _app():
    from streamlit.testing.v1 import AppTest
    return AppTest.from_file(str(ROOT / "app.py"), default_timeout=120)


PAGES = ["Start here", "Witness a record", "The four propositions", "How it is built", "Thesis run",
         "Claim ledger", "Where the ceiling is anchored", "Robustness and cross-checks",
         "Synthea realism", "Norwegian context (illustrative)", "Explore (not a thesis claim)"]


@pytest.mark.parametrize("page", PAGES)
def test_page_renders(page):
    at = _app()
    at.session_state["page"] = page
    at.run()
    assert not at.exception, [e.value for e in at.exception]


def test_ledger_matches_thesis():
    at = _app()
    at.session_state["page"] = "Claim ledger"
    at.run()
    df = at.dataframe[0].value
    assert (df[""] == "✗").sum() == 0, df[df[""] != "✓"]
    assert (df[""] == "✓").sum() == len(df) == 27


def test_thesis_run_matches_on_load():
    at = _app()
    at.session_state["page"] = "Thesis run"
    at.run()
    assert any("Matches the thesis" in s.value for s in at.success)


CH4 = pathlib.Path(os.environ.get("TRF_THESIS", ROOT.parent / "trf-thesis")) / "Chapter4_TRF_Model_v1.md"


@pytest.mark.skipif(not CH4.exists(), reason="thesis repository not present")
def test_propositions_verbatim():
    sys.path.insert(0, str(ROOT))
    src = (ROOT / "app.py").read_text(encoding="utf-8")
    ns = {}
    block = src[src.index("PROPOSITIONS = ["):src.index("\n]\n", src.index("PROPOSITIONS = [")) + 3]
    exec(block, ns)
    chapter = re.sub(r"(?m)^> ?", "", CH4.read_text(encoding="utf-8"))
    for name, _, _, statement, limits in ns["PROPOSITIONS"]:
        assert statement in chapter, name
        for q in limits:
            assert q in chapter, (name, q[:60])


def test_walk_next_buttons_chain():
    order = ["Start here", "Witness a record", "The four propositions", "Where the ceiling is anchored",
             "How it is built", "Claim ledger", "Robustness and cross-checks"]
    at = _app()
    at.session_state["page"] = order[0]
    at.run()
    for nxt in order[1:]:
        at.button(key="walk_next").click().run()
        assert at.session_state["page"] == nxt and not at.exception


FM = CH4.parent / "Front_Matter_v1.md"


@pytest.mark.skipif(not FM.exists(), reason="thesis repository not present")
def test_not_claimed_quote_verbatim():
    quote = re.search(r"\*What is not claimed\.\* (.*)", FM.read_text(encoding="utf-8")).group(1).strip()
    src = re.sub(r'"\s*\n\s*"', "", (ROOT / "app.py").read_text(encoding="utf-8"))
    assert quote in src
