"""
TRF Feasibility Checker — online demonstration (viewer over the verified artefact).

THESIS INTEGRITY NOTE
  "Thesis run" executes trf_checker.py UNMODIFIED under seed 20260915. Every figure it
  shows is the figure reported in Chapter 5. "Synthea realism" executes the realism
  layer unmodified and reproduces Table 5.7. "Explore" varies population parameters and
  is NOT part of any thesis claim. "Witness a record" draws one record of the thesis
  population through its life using the checker's own functions; ui.py only draws.

  The app is a viewer over the artefact, never a source of results. If a number
  here disagrees with the thesis, either the thesis text is wrong or the app is
  wrong — the app never becomes the authority.

Run locally:  streamlit run app.py
"""

import json

import streamlit as st

import trf_checker as trf
import ui

st.set_page_config(page_title="TRF Feasibility Checker", layout="wide", page_icon="🔏")
ui.theme()


# ----------------------------------------------------------------------
# Shared measurement, used by the thesis run and the realism layer
# ----------------------------------------------------------------------

def measure(records):
    """Run both semantics over a population and return the reported figures."""
    v1 = {r.rid: trf.check_semantics_I(r) for r in records}
    primary = [r for r in records if r.sigma == "primary"]
    secondary = [r for r in records if r.sigma == "secondary"]

    out = {
        "records": len(records),
        "sem1_records": sum(1 for k in v1 if v1[k]),
        "sem1_total": sum(len(x) for x in v1.values()),
        "sem1_primary": sum(1 for r in primary if v1[r.rid]),
        "sem1_secondary": sum(1 for r in secondary if v1[r.rid]),
        "cor12": sum(1 for r in secondary if r.t_r == trf.INF and v1[r.rid]),
        "witnesses": [v1[r.rid][0] for r in secondary
                      if r.t_r == trf.INF and v1[r.rid]][:3],
    }

    for r in records:
        trf.apply_invalidation(r)
    v2 = {r.rid: trf.check_semantics_II(r) for r in records}
    out["sem2_records"] = sum(1 for k in v2 if v2[k])
    out["sem2_total"] = sum(len(x) for x in v2.values())
    out["invalidated"] = sum(1 for r in records if r.iota is not None)
    out["ground_art17"] = sum(1 for r in records
                              if r.iota and "Art 17" in r.iota["ground"])
    out["ground_art68"] = sum(1 for r in records
                              if r.iota and "68(12)" in r.iota["ground"])
    return out, records


@st.cache_resource
def thesis_population():
    """The seed-20260915 population, checked under Semantics I before invalidation and
    under Semantics II after it, exactly as trf_checker.main() does."""
    recs = trf.generate()
    v1 = {r.rid: trf.check_semantics_I(r) for r in recs}
    plan = {r.rid: (r.t_invalidation(), r.erasure_deadline(), r.ceiling_deadline()) for r in recs}
    for r in recs:
        trf.apply_invalidation(r)
    v2 = {r.rid: trf.check_semantics_II(r) for r in recs}
    return recs, v1, v2, plan


# ----------------------------------------------------------------------
# Witness a record: the life strip and the live mechanism diagram
# ----------------------------------------------------------------------

def page_witness():
    recs, v1, v2, plan = thesis_population()
    by = {r.rid: r for r in recs}
    st.title("Watch one audit record live through its retention window")
    st.markdown(
        '<p class="lede">Three rules act on every record below. A floor says it must stay '
        'verifiable. An erasure request, or the end of a research permit, says its payload '
        'must go. Read <i>verifiable</i> as <i>readable</i> and the rules contradict each '
        'other inside the floor. Read it as <i>accountable</i> and they do not. Pick a record, '
        'move through its months, and watch which part of the mechanism acts.</p>',
        unsafe_allow_html=True)

    cor12 = next(r.rid for r in recs if r.sigma == "secondary" and r.t_r == trf.INF and v1[r.rid])
    xb = next(r.rid for r in recs if r.sigma == "primary" and r.t_r < trf.INF and v1[r.rid])
    spe_req = next(r.rid for r in recs if r.sigma == "secondary" and r.t_r < trf.INF and v1[r.rid])
    quiet = next(r.rid for r in recs if r.sigma == "primary" and r.t_r == trf.INF)
    presets = {
        f"Research log, no erasure request (Corollary 1.2), record {cor12}": cor12,
        f"Cross-border record with an erasure request, record {xb}": xb,
        f"Research log with an erasure request, record {spe_req}": spe_req,
        f"Cross-border record nobody asks to erase, record {quiet}": quiet,
    }
    c1, c2 = st.columns([3, 1])
    choice = c1.selectbox("Record", list(presets) + ["Any record by number"])
    rid = presets.get(choice) if choice in presets else c2.number_input("Record number", 0, len(recs) - 1, 100)
    r = by[int(rid)]
    t_I, d_er, d_ceil = plan[r.rid]
    deadline = min(d_er, d_ceil)
    end = r.t_a + r.floor
    horizon = int(min(max(end, deadline if deadline < trf.INF else 0) + 3, 130))
    focus = int(t_I) if t_I < trf.INF else r.t_a
    now = st.slider("Month", 0, horizon, focus, help="Move through the record's life")

    pathway = "cross-border" if r.sigma == "primary" else "research log"
    ui.facts([
        (("NCPeH audit repository" if r.sigma == "primary" else "SPE access log"), pathway),
        ("created", f"month {r.t_a}"),
        ("floor runs to", f"month {end}"),
        ("erasure deadline", "none" if d_er == trf.INF else f"month {int(d_er)}"),
        ("deletion ceiling", "none" if d_ceil == trf.INF else f"month {int(d_ceil)}"),
    ])
    st.altair_chart(ui.life_strip(r, t_I, deadline, horizon, now), width="stretch", height=300, theme=None)

    if v1[r.rid]:
        w = v1[r.rid][0]
        ui.verdict(f"<b>Semantics I fails.</b> {w['detail']}. No assignment of readability "
                   "satisfies both (Proposition 1).", ui.REVOKE)
    else:
        ui.verdict("<b>Semantics I holds for this record:</b> no deadline falls inside its floor.", ui.FLOOR)
    ui.verdict("<b>Semantics II holds.</b> " + (
        "0 violations: the payload goes at the deadline, the invalidation entry is logged, "
        "and the record stays verifiable through the floor (Proposition 2)."
        if not v2[r.rid] else f"{len(v2[r.rid])} violation(s): investigate before citing."),
        ui.SEAL if not v2[r.rid] else ui.REVOKE)

    trigger = "erasure" if d_er <= d_ceil else "permit"
    if now < r.t_a:
        active, msg = (), "Before the access event: nothing exists yet."
    elif now == r.t_a:
        active = ("access", "writer", "commit", "kms", "store", "merkle")
        msg = ("Access event. The writer splits accessor and subject fields, encrypts the payload "
               "under its own key, commits to it, and appends the accessor fields and commitment "
               "to the Merkle log.")
    elif t_I == trf.INF or now < t_I:
        active = ("store", "kms", "merkle", "auditor")
        msg = "Retained. The payload is readable under its key; the auditor can open the commitment."
    elif now == t_I:
        active = (trigger, "scheduler", "kms", "store", "registry", "merkle")
        msg = (f"Invalidation at month {int(t_I)} on the ground {r.iota['ground']}: key, salt and "
               "ciphertext destroyed, the entry appended to the registry and the log.")
    else:
        active = ("auditor", "merkle", "registry", "commit")
        msg = ("After invalidation. The auditor sees who acted, when, the commitment and the "
               "invalidation entry, each proved against the log root, and cannot read the payload.")
    if now > end:
        msg += " The floor has run out; the terminal transition is specified (§4.8) but not implemented."
    st.subheader("Which part of the mechanism acts this month")
    st.write(msg)
    ui.diagram("cei-mechanism.html", active, ui.REVOKE if now == t_I else ui.SEAL, height=720)

    with st.expander("What the auditor holds for this record now"):
        ok, why = trf.integrity(r)
        idx = r.log_idx["access"]
        proof = trf.AUDIT_LOG.proof(idx)
        st.code(
            f"accessor fields   : actor={r.m['actor']}  "
            f"{'permit=' + r.m['permit'] if 'permit' in r.m else 'ncp=' + r.m.get('ncp', '-')}  outcome={r.m['outcome']}\n"
            f"subject link      : {'removed month ' + str(r.iota_subj['month']) if r.iota_subj else 'present'}\n"
            f"commitment c(a)   : {r.c[:40]}...\n"
            f"key, salt, payload: {'destroyed at month ' + str(int(t_I)) if r.iota else 'held'}\n"
            f"invalidation entry: {r.iota['ground'] + ', month ' + str(r.iota['month']) if r.iota else 'none'}\n"
            f"inclusion proof   : {len(proof)} hashes to root {trf.AUDIT_LOG.root().hex()[:24]}...  "
            f"verifies={ok} {why}",
            language="text")


def page_architecture():
    st.title("How the artefact is built")
    st.markdown(
        '<p class="lede">Two drawings, both interactive: drag to pan, scroll to zoom, click a '
        'component to trace its connections. The first is the mechanism of Chapter 4 at the audit '
        'boundary (Figure 4.1). The second is the code you are running (Figure 5.1).</p>',
        unsafe_allow_html=True)
    st.subheader("The mechanism at the audit boundary")
    ui.diagram("cei-mechanism.html", height=640)
    st.subheader("The modules behind this app")
    ui.diagram("trf-artefact.html", height=660)
    st.caption("Drawn with Archify from candidate JSON kept in the repository; each passed "
               "Archify's validation, layout and browser checks.")


# ----------------------------------------------------------------------
# Tab 1 — the thesis run
# ----------------------------------------------------------------------

def page_thesis_run():
    st.subheader("Thesis configuration — seed 20260915, n = 200")
    st.info(
        "Executes the checker exactly as reported in Chapter 5, Tables 5.3 and 5.6, "
        "and the audit-log integrity check of Section 5.7. "
        "Deterministic: this run is byte-identical to the one in the thesis."
    )

    if st.button("Run thesis configuration", key="run_thesis"):
        with st.spinner("Executing trf_checker.py ..."):
            M, records = measure(trf.generate())

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Violations — Semantics I", M["sem1_total"])
        c2.metric("Records infeasible", f"{M['sem1_records']}/{M['records']}")
        c3.metric("Corollary 1.2 witnesses", M["cor12"])
        c4.metric("Violations — Semantics II", M["sem2_total"])

        st.markdown("**Table 5.3 — violations under Semantics I**")
        st.table({
            "Record class": ["Cross-border audit (F = 120)",
                             "SPE access log (F = 12)", "Total"],
            "Records": [100, 100, 200],
            "With ≥1 violation": [M["sem1_primary"], M["sem1_secondary"],
                                  M["sem1_records"]],
        })

        st.markdown(
            "**Corollary 1.2 — infeasible with no erasure request whatsoever.** "
            "These records received no Article 17 request. The collision is between "
            "Article 73(1)(e) and Article 68(12) alone, on the broad reading of "
            "Article 68(12) and for logs kept at patient-record granularity "
            "(Chapter 4, Section 4.6). On the narrow reading these witnesses lapse."
        )
        for w in M["witnesses"]:
            st.code(w["detail"], language="text")

        st.markdown("**Table 5.6 — Semantics II**")
        st.table({
            "Measure": ["Records invalidated", "— ground: GDPR Art. 17(1)",
                        "— ground: EHDS Art. 68(12)", "Records with violation",
                        "Total violations"],
            "Value": [M["invalidated"], M["ground_art17"], M["ground_art68"],
                      M["sem2_records"], M["sem2_total"]],
        })

        demo = next(r for r in records if r.rid == 100)
        st.markdown("**Auditor's view of record 100 after invalidation**")
        st.code(
            f"accessor fields      : {trf.integrity(demo)[0]}   actor={demo.m['actor']}  "
            f"permit={demo.m.get('permit', '-')}  outcome={demo.m['outcome']}\n"
            f"subject link         : "
            f"{'removed month ' + str(demo.iota_subj['month']) if demo.iota_subj else 'present'}\n"
            f"commitment c(a)      : {demo.c[:32]}...\n"
            f"payload key k(a)     : {demo.k}   <- destroyed\n"
            f"salt, ciphertext     : {demo.salt}, {demo.payload}   <- destroyed, deleted\n"
            f"invalidation iota(a) : month={demo.iota['month']}  "
            f"ground={demo.iota['ground']}\n"
            f"payload readable     : {bool(trf.alpha(demo, demo.t_a + demo.floor))}",
            language="text",
        )

        st.markdown("**Audit-log integrity — Chapter 5, Section 5.7**")
        st.write(
            "Every access, invalidation and subject-link removal is a leaf of an "
            "append-only Merkle log (RFC 6962 hashing). A record counts as verifiable "
            "under Semantics II only if each of its entries passes an inclusion proof "
            "against the log root. Leaves hold the accessor fields and the commitment, "
            "never the payload or the patient link, so the log never needs erasing."
        )
        n_ok = sum(1 for r in records if trf.integrity(r)[0])
        saved = demo.m["actor"]
        demo.m["actor"] = "R-999"
        ok_t, why_t = trf.V_II(demo, demo.t_a)
        demo.m["actor"] = saved
        saved_g = demo.iota["ground"]
        demo.iota["ground"] = "none"
        ok_g, why_g = trf.V_II(demo, demo.t_a)
        demo.iota["ground"] = saved_g
        ok_r = trf.V_II(demo, demo.t_a)[0]
        i1, i2, i3 = st.columns(3)
        i1.metric("Records verifying", f"{n_ok}/{len(records)}")
        i2.metric("Tamper: actor altered", "fails" if not ok_t else "PASSES")
        i3.metric("Tamper: ground altered", "fails" if not ok_g else "PASSES")
        st.code(
            f"rid={demo.rid} actor R-008 -> R-999 : V_II={ok_t}  ({why_t})\n"
            f"rid={demo.rid} ground -> 'none'    : V_II={ok_g}  ({why_g})\n"
            f"after restoring both          : V_II={ok_r}",
            language="text",
        )

        if (M["sem1_total"] == 95 and M["sem2_total"] == 0 and M["cor12"] == 39
                and n_ok == len(records) and not ok_t and not ok_g and ok_r):
            st.success(
                "Matches the thesis: 95 violations across 90 records under "
                "Semantics I, 39 Corollary 1.2 witnesses, 0 violations under "
                "Semantics II, 200/200 records verifying, both tamper tests failing."
            )
        else:
            st.error(
                "This run does NOT match the figures reported in Chapter 5. "
                "Do not present these numbers — investigate the discrepancy first."
            )


# ----------------------------------------------------------------------
# Tab 2 — parameter exploration, explicitly outside the thesis
# ----------------------------------------------------------------------

def page_explore():
    st.subheader("Exploration — how the violation rate responds to parameters")
    st.warning(
        "Not a thesis claim. The thesis reports the seed-20260915 configuration "
        "only. This tab exists to show that the collision is not an artefact of "
        "the chosen parameters: Proposition 1 holds for any parameters under which a "
        "deadline falls inside a retention window."
    )

    p_primary = st.slider("Erasure-request probability — cross-border",
                          0.0, 1.0, 0.40, 0.05)
    p_spe = st.slider("Erasure-request probability — SPE", 0.0, 1.0, 0.25, 0.05)
    pi_max = st.slider("Permit horizon, months — SPE", 1, 60, 12)

    if st.button("Run exploration", key="run_explore"):
        import random

        rng = random.Random(trf.SEED)
        records, rid = [], 0
        for _ in range(100):
            t_a = rng.randint(0, 11)
            t_r = t_a + rng.randint(1, 130) if rng.random() < p_primary else trf.INF
            records.append(trf.Record(rid, t_a, trf.FLOOR_XBORDER, "primary",
                                      f"<payload {rid}>".encode(), t_r=t_r))
            rid += 1
        for _ in range(100):
            t_a = rng.randint(0, 11)
            t_pi = t_a + rng.randint(1, pi_max)
            t_r = t_a + rng.randint(1, 18) if rng.random() < p_spe else trf.INF
            records.append(trf.Record(rid, t_a, trf.FLOOR_SPE, "secondary",
                                      f"<payload {rid}>".encode(),
                                      t_r=t_r, t_pi=t_pi))
            rid += 1

        M, _ = measure(records)
        c1, c2, c3 = st.columns(3)
        c1.metric("Records infeasible — Semantics I",
                  f"{M['sem1_records']}/{M['records']}")
        c2.metric("Corollary 1.2 witnesses", M["cor12"])
        c3.metric("Violations — Semantics II", M["sem2_total"])
        st.caption(
            f"Structural SPE collision rate at this horizon is approximately "
            f"6/{pi_max} = {6 / pi_max:.0%}, as Chapter 5, Section 5.4 states. "
            f"Semantics II yields {M['sem2_total']} violations at every setting."
        )


# ----------------------------------------------------------------------
# Tab 3 — Synthea realism layer
# ----------------------------------------------------------------------

def page_synthea():
    st.subheader("Synthea realism layer — payload-provenance invariance")
    st.write(
        "Replaces constructed payloads with committed Synthea FHIR R4 resources "
        "and reruns both checkers with every timing quantity untouched. Java is "
        "needed only for the offline generation step, never at runtime. Expected "
        "result: every figure identical, every commitment different."
    )

    if st.button("Run realism comparison", key="run_synthea"):
        try:
            import synthea_layer as sl

            with st.spinner("Loading bundles and rerunning both checkers ..."):
                base = trf.generate()
                real, n_files, n_payloads = sl.generate_with_synthea()
                sample_payload = real[0].payload      # read before invalidation deletes it
                mean_base = sum(len(r.payload) for r in base) // len(base)
                mean_real = sum(len(r.payload) for r in real) // len(real)
                diff_c = sum(1 for x, y in zip(base, real) if x.c != y.c)
                Mb, _ = measure(base)
                Mr, _ = measure(real)

            st.write(
                f"Bundles read: {n_files}  |  clinical payloads: {n_payloads}  |  "
                f"records: {len(real)}"
            )
            st.write(
                f"Mean payload size: constructed {mean_base} bytes, "
                f"Synthea {mean_real} bytes"
            )

            keys = [("sem1_records", "Semantics I — records with violation"),
                    ("sem1_total", "Semantics I — total violations"),
                    ("cor12", "Corollary 1.2 witnesses"),
                    ("invalidated", "Records invalidated"),
                    ("sem2_records", "Semantics II — records with violation"),
                    ("sem2_total", "Semantics II — total violations")]
            st.markdown("**Table 5.7 — constructed against Synthea payloads**")
            st.table({
                "Measure": [label for _, label in keys],
                "Constructed": [Mb[k] for k, _ in keys],
                "Synthea": [Mr[k] for k, _ in keys],
            })

            identical = all(Mb[k] == Mr[k] for k, _ in keys)
            if identical and diff_c == len(base):
                st.success(
                    f"Invariance holds: every figure identical, {diff_c}/"
                    f"{len(base)} commitments differ. The model reads timing "
                    f"and accessibility, never payload content."
                )
            else:
                st.error(
                    "Divergence detected. Do not report these figures — the "
                    "model is reading something it should not."
                )

            with st.expander("Inspect one Synthea payload"):
                st.json(json.loads(sample_payload))

        except FileNotFoundError:
            import glob as _glob
            import os as _os

            import synthea_layer as _sl

            searched = "\n".join(
                f"- `{d}` — {len(_glob.glob(_os.path.join(d, '*.json')))} bundles"
                for d in _sl.SYNTHEA_DIRS
            )
            st.info(
                "No committed bundles found in this deployment. Directories "
                f"searched:\n\n{searched}\n\n"
                "Fix: commit the eight-bundle subset to `data/synthea_subset/` "
                "in the repository root. Alternatively regenerate the full "
                "cohort offline, which needs Java 17+:\n\n"
                "`java -jar synthea.jar -s 20260915 -cs 20260915 -p 100 "
                "--exporter.fhir.export=true`\n\n"
                "and commit `synthea_run/output/fhir/`."
            )


# ----------------------------------------------------------------------
# Tab 4 — Norwegian context modules (parallel to the thesis, illustrative)
# ----------------------------------------------------------------------

def page_norway():
    st.subheader("Norwegian context — plug-and-play modules")
    st.write(
        "These modules import `trf_checker.py` unmodified and change nothing the "
        "thesis reports. They vary what the model actually reads: the retention "
        "floor F(a), the pathway, and the arrival of erasure requests and permit "
        "expiries. Payload content cannot change any figure, which Tab 3 "
        "demonstrates, so the Norwegian payloads here are for legibility only."
    )
    st.info(
        "Illustrative, not empirical. No Norwegian permit-duration statistics were "
        "used, and no Norwegian patient data exists here: Synthea has no Norwegian "
        "module. Nothing on this tab is a thesis claim.",
        icon="ℹ️",
    )

    st.markdown(
        "| Class | Floor | Ceiling | Source |\n|---|---|---|---|\n"
        "| NO-XB | 120 months | — | eHDSI deployment baseline; inbound patient "
        "summary at Bodø / Stjørdal legevakt from PT, CZ, FI |\n"
        "| NO-SPE | 12 months | 6 months after permit expiry | EHDS Art 73(1)(e); "
        "Art 68(12); Helsedataservice permit into a NORTRE node |\n"
        "| NO-JOURNAL | indefinite | — | pasientjournalloven § 25, "
        "journalforskriften § 14: purpose-based, no fixed period in law |"
    )

    if st.button("Run Norwegian layer", key="run_no"):
        try:
            import norwegian_layer as nl

            with st.spinner("Building Norwegian record classes ..."):
                recs = nl.build()
                v1 = {r.rid: trf.check_semantics_I(r) for r in recs}
                for r in recs:
                    trf.apply_invalidation(r)
                v2 = {r.rid: trf.check_semantics_II(r) for r in recs}

            rows = []
            for k in sorted({r.m["klasse"] for r in recs}):
                sub = [r for r in recs if r.m["klasse"] == k]
                rows.append({
                    "class": k,
                    "records": len(sub),
                    "Sem I records with violation": sum(1 for r in sub if v1[r.rid]),
                    "Sem I violations": sum(len(v1[r.rid]) for r in sub),
                    "invalidated": sum(1 for r in sub if r.iota),
                    "Sem II violations": sum(len(v2[r.rid]) for r in sub),
                })
            st.dataframe(rows, width="stretch", hide_index=True)

            st.markdown("**One case per class**")
            for k in sorted({r.m["klasse"] for r in recs}):
                cand = [r for r in recs if r.m["klasse"] == k and v1[r.rid]]
                if not cand:
                    st.write(f"{k}: no infeasible record in this draw.")
                    continue
                r = cand[0]
                d = v1[r.rid][0]
                where = r.m.get("site") or r.m.get("node") or r.m["legal_basis"]
                st.code(
                    f"{k}  rid={r.rid}  ({where})\n"
                    f"  floor     : t={r.t_a} .. {r.t_a + r.floor}"
                    + ("   [indefinite, truncated for computation]"
                       if k == "NO-JOURNAL" else "") + "\n"
                    f"  erasure   : "
                    + ("none" if r.t_r == trf.INF
                       else f"t_r={r.t_r} -> deadline {int(r.erasure_deadline())}") + "\n"
                    f"  ceiling   : "
                    + ("n/a" if r.ceiling_deadline() == trf.INF
                       else f"t_pi={r.t_pi} -> {int(r.ceiling_deadline())}") + "\n"
                    f"  collision : {d['constraint']} at t={d['month']}\n"
                    f"  after invalidation: metadata intact, commitment "
                    f"{r.c[:16]}..., key={r.k}, salt={r.salt}, "
                    f"ground={r.iota['ground'] if r.iota else None}",
                    language="text",
                )
        except ModuleNotFoundError:
            st.error("norwegian_layer.py is not beside app.py in this deployment.")

    st.divider()
    st.markdown("**Cross-sector instance: politiregisterloven § 17**")
    st.write(
        "Norwegian police register law requires information about use of the "
        "system to be stored for at least one year and deleted at the latest "
        "after three: a floor, a ceiling and a subject right on one log, outside "
        "health. Running it through the same model gives the result we did not "
        "expect, and the more informative one."
    )

    if st.button("Run cross-sector check", key="run_cs"):
        try:
            import cross_sector_check as cs

            recs = cs.build()
            v1 = {r.rid: trf.check_semantics_I(r) for r in recs}
            structural = sum(1 for r in recs if r.t_r == trf.INF and v1[r.rid])
            for r in recs:
                trf.apply_invalidation(r)
            v2 = {r.rid: trf.check_semantics_II(r) for r in recs}
            c1, c2, c3 = st.columns(3)
            c1.metric("records", len(recs))
            c2.metric("Sem I violations", sum(1 for k in v1 if v1[k]))
            c3.metric("structural (no erasure request)", structural)
            if structural == 0:
                st.success(
                    "No structural collision. The floor ends at t_a + 12 and the "
                    "ceiling bites at t_a + 36, both measured from the same "
                    "origin, so § 17 defines a bounded retention window rather "
                    "than a contradiction. Every collision found is "
                    "erasure-driven. Article 68(12) collides instead because it "
                    "anchors its ceiling to an external event, the expiry of the "
                    "data permit, which can fall before the floor has run.",
                    icon="✅",
                )
            else:
                st.warning(f"{structural} structural collisions in this draw.")
            st.caption(
                f"Semantics II violations: {sum(len(x) for x in v2.values())}"
            )
        except ModuleNotFoundError:
            st.error("cross_sector_check.py is not beside app.py in this deployment.")


# ----------------------------------------------------------------------
# Tab 5 — Robustness and cross-checks (Chapter 5 §5.5, §5.6 and §5.8)
# ----------------------------------------------------------------------

def page_robustness():
    st.subheader("Robustness and cross-checks")
    st.write(
        "Two results the thesis reports that the other tabs do not show. Both "
        "answer the same objection: that the infeasibility rests on one "
        "implementation, or on one arbitrary parameter."
    )

    st.markdown("**Independent exhaustive cross-check — Chapter 5 §5.5**")
    st.write(
        "`brute_force_semantics_I()` is written separately from "
        "`check_semantics_I()`. It takes the constraint definitions directly and "
        "enumerates all 2¹⁴ assignments of the accessibility variable over a "
        "fourteen-month horizon. Agreement between two independent "
        "implementations is worth more than confidence in either one. The "
        "control case, where neither the erasure right nor the ceiling is "
        "active, must come back feasible: a search that never succeeds proves "
        "nothing."
    )

    if st.button("Run exhaustive cross-check", key="run_bf"):
        # Parameters copied verbatim from trf_checker.main(); the expected
        # column is what docs/expected_trf_output.txt records for each case.
        cases = [
            ("SPE, no erasure request, permit 3mo",
             (0, 12, trf.INF, 3, "secondary", 14), False),
            ("SPE, erasure at t=2",
             (0, 12, 2, 9, "secondary", 14), False),
            ("cross-border scaled (F=12), erasure at t=4",
             (0, 12, 4, trf.INF, "primary", 14), False),
            ("control: no request, no expiry",
             (0, 12, trf.INF, trf.INF, "primary", 14), True),
        ]
        rows, ok = [], True
        with st.spinner("Enumerating 2^14 assignments per case ..."):
            for label, args, expected in cases:
                got = trf.brute_force_semantics_I(*args)
                rows.append({"case": label, "feasible": got,
                             "expected": expected,
                             "agrees": "yes" if got == expected else "NO"})
                ok = ok and got == expected
        st.dataframe(rows, width="stretch", hide_index=True)
        if ok:
            st.success(
                "Both implementations agree on every case, and the control "
                "returns feasible, so the search can succeed when it should.",
                icon="✅",
            )
        else:
            st.error(
                "DISAGREEMENT. Do not present any figure from this artefact "
                "until the discrepancy is explained.",
                icon="🚨",
            )

    st.divider()
    st.markdown("**Erasure response period — Chapter 5 §5.6**")
    st.write(
        "The model sets δ, the controller's response period for an erasure "
        "request, to one month. GDPR Article 12(3) allows an extension to three "
        "where the request is complex. If the infeasibility were an artefact of "
        "the tighter period, a longer one would dissolve it. This runs the "
        "population at both values rather than asserting the answer."
    )

    if st.button("Run δ witness", key="run_delta"):
        with st.spinner("Re-running the population at δ = 1 and δ = 3 ..."):
            rows = trf.delta_witness()
        st.dataframe(
            [{"δ (months)": r["delta"],
              "Sem I records": r["sem1_records"],
              "Sem I violations": r["sem1_total"],
              "Corollary 1.2 witnesses": r["cor12"],
              "invalidated": r["invalidated"],
              "Sem II violations": r["sem2_total"]} for r in rows],
            width="stretch", hide_index=True,
        )
        if all(r["sem2_total"] == 0 for r in rows) and all(
                r["sem1_total"] > 0 for r in rows):
            st.success(
                "Infeasibility under Semantics I survives the longer response "
                "period, and Semantics II remains satisfiable at both values. "
                "The collision is structural, not a consequence of δ = 1.",
                icon="✅",
            )
        else:
            st.warning(
                "The pattern differs from what Chapter 5 §5.6 reports. Check "
                "the module before citing this.",
                icon="⚠️",
            )

    st.divider()
    st.markdown("**Real envelope encryption — optional module, Chapter 5 §5.8**")
    st.write(
        "The checker models key destruction as removing a reference. This module "
        "repeats the lifecycle with real AES-256-GCM: each record under its own data "
        "key, each data key wrapped under a key-encrypting key, and the wrapped key "
        "destroyed at the record's invalidation month. Keys are random on every run; "
        "the counts are not."
    )
    if st.button("Run envelope encryption", key="run_crypto"):
        try:
            import crypto_envelope as ce

            with st.spinner("Encrypting 200 records, destroying keys, decrypting ..."):
                recs = trf.generate()
                custody = ce.Custody()
                store = {r.rid: ce.encrypt(custody, r.rid, r.payload) for r in recs}
                inval = [r for r in recs if r.t_invalidation() < trf.INF]
                for r in inval:
                    custody.destroy(r.rid)
                readable = refused = 0
                for r in recs:
                    try:
                        ce.decrypt(custody, r.rid, *store[r.rid])
                        readable += 1
                    except KeyError:
                        refused += 1
            e1, e2, e3 = st.columns(3)
            e1.metric("Records encrypted", len(recs))
            e2.metric("Refused after key destruction", refused)
            e3.metric("Still readable", readable)
            if refused == len(inval) == 138 and readable == 62:
                st.success(
                    "Exactly the 138 invalidated records refuse to decrypt and the "
                    "other 62 read, as Appendix A.22 records. Unreadability follows "
                    "from destruction; that destruction happened in hardware is still "
                    "an attestation (Chapter 6, Section 6.3).",
                    icon="✅",
                )
            else:
                st.error("Counts differ from Appendix A.22. Investigate before citing.")
        except ImportError:
            st.info("The `cryptography` package is not installed in this deployment.")

    st.divider()
    st.markdown("**What this artefact does not do**")
    st.write(
        "It does not connect to any National Contact Point, implement the "
        "OpenNCP transmission flow, evaluate consent policies, or implement any "
        "zero-knowledge proof system, and it does not implement the terminal "
        "transition at floor expiry. Key destruction is simulated by removing a "
        "reference in program state, or in the optional module by discarding a "
        "wrapped key in memory: either demonstrates the mechanism's logic and "
        "says nothing about whether destruction can be assured in deployment. "
        "Chapter 5 §5.8 and Chapter 6 state these limits in full."
    )



# ----------------------------------------------------------------------
# Tab 6 — Proposition 3: where the ceiling is anchored (Chapter 4, Section 4.6)
# ----------------------------------------------------------------------

def page_anchor():
    st.subheader("Where the ceiling is anchored — Proposition 3")
    st.write(
        "A retention floor of F months runs from the record's creation t(a). A deletion "
        "ceiling of L months runs from an event e(a) at or after creation. Under plaintext "
        "verifiability the two collide for a record exactly when e(a) + L <= t(a) + F. "
        "A collision therefore needs L <= F; where the ceiling is anchored decides "
        "whether the collision can be read from the text or only from each record's history."
    )
    preset = st.radio(
        "Preset",
        ["EHDS Art 73(1)(e) floor, Art 68(12) ceiling", "politiregisterloven § 17",
         "Free"], horizontal=True)
    if preset.startswith("EHDS"):
        F0, L0, same0 = 12, 6, False
    elif preset.startswith("politi"):
        F0, L0, same0 = 12, 36, True
    else:
        F0, L0, same0 = 24, 12, False
    F = st.slider("Floor F (months, from creation)", 1, 120, F0, key=f"F_{preset}")
    L = st.slider("Ceiling L (months, from its anchor)", 1, 120, L0, key=f"L_{preset}")
    same = st.checkbox("Ceiling anchored to creation, the same event as the floor",
                       value=same0, key=f"same_{preset}")
    if same:
        if L > F:
            st.success(f"L = {L} > F = {F}: no record collides. The two limits bound one "
                       "retention window, readable from the text alone.", icon="✅")
        else:
            st.error(f"L = {L} <= F = {F}: every record collides, and the text "
                     "contradicts itself on its face.", icon="🚨")
    else:
        if L > F:
            st.success(f"L = {L} > F = {F}: no record collides, wherever its anchor "
                       "event falls.", icon="✅")
        else:
            gap = F - L
            st.warning(
                f"L = {L} <= F = {F}: a record collides exactly when its anchor event "
                f"falls within {gap} month(s) of creation (e(a) - t(a) <= {gap}). "
                "Nothing in the text says which records those are; each record's "
                "history does.", icon="⚠️")
            offsets = list(range(0, F + 1))
            st.bar_chart(
                {"months of collision": [max(0, (t0 + F) - (t0 + d + L) + 1)
                                         for t0, d in [(0, d) for d in offsets]]},
                x_label="anchor event, months after creation",
                y_label="months in which both apply")
    st.caption(
        "Article 68(12) is of the external-anchor kind: six months from permit expiry "
        "against twelve from the log entry, so logs whose permit expires within six "
        "months of the entry collide (Corollary 1.2). Section 17 of politiregisterloven "
        "measures both limbs from the log entry with the ceiling longer, so it bounds a "
        "window instead (Chapter 6, Section 6.10).")



# ----------------------------------------------------------------------
# Navigation
# ----------------------------------------------------------------------

PAGES = {
    "Witness a record": page_witness,
    "How it is built": page_architecture,
    "Thesis run": page_thesis_run,
    "Where the ceiling is anchored": page_anchor,
    "Robustness and cross-checks": page_robustness,
    "Synthea realism": page_synthea,
    "Norwegian context (illustrative)": page_norway,
    "Explore (not a thesis claim)": page_explore,
}

with st.sidebar:
    st.markdown("### Tri-Lateral Retention Feasibility")
    page = st.radio("Go to", list(PAGES), label_visibility="collapsed")
    st.caption("Abbasia, MSc Sustainable Energy Logistics, Høgskolen i Molde, 2026. "
               "Seed 20260915 throughout the thesis run.")
    st.caption("A viewer over the verified artefact, never a source of results. Thesis run, "
               "Synthea realism and Robustness reproduce Chapter 5; Explore and Norwegian "
               "context are not thesis claims.")

PAGES[page]()
