"""
TRF Feasibility Checker — online demonstration (viewer over the verified artefact).

THESIS INTEGRITY NOTE
  Tab 1 executes trf_checker.py UNMODIFIED under seed 20260915. Every figure it
  shows is the figure reported in Chapter 5. Tab 3 executes the Synthea realism
  layer unmodified and reproduces Table 5.4. Tab 2 is a teaching aid that varies
  population parameters and is NOT part of any thesis claim.

  The app is a viewer over the artefact, never a source of results. If a number
  here disagrees with the thesis, either the thesis text is wrong or the app is
  wrong — the app never becomes the authority.

Run locally:  streamlit run app.py
"""

import json

import streamlit as st

import trf_checker as trf

st.set_page_config(page_title="TRF Feasibility Checker", layout="wide")

st.title("Tri-Lateral Retention Feasibility Model")
st.caption(
    "Live demonstration of the executable witness for Theorems 1 and 2. "
    "Abbasia, MSc Sustainable Energy Logistics, Høgskolen i Molde, 2026. "
    "Seed 20260915 throughout the thesis run."
)

tab1, tab2, tab3 = st.tabs(
    ["Thesis run", "Exploration — not thesis claims", "Synthea realism layer"]
)


# ----------------------------------------------------------------------
# Shared measurement, used by tabs 1 and 3 so both report identically
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


# ----------------------------------------------------------------------
# Tab 1 — the thesis run
# ----------------------------------------------------------------------

with tab1:
    st.subheader("Thesis configuration — seed 20260915, n = 200")
    st.info(
        "Executes the checker exactly as reported in Chapter 5, Tables 5.1 to 5.3. "
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

        st.markdown("**Table 5.1 — violations under Semantics I**")
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
            "Article 73(1)(e) and Article 68(12) alone, conditional on the reading "
            "of Article 68(12) defended in Chapter 4, Section 4.6."
        )
        for w in M["witnesses"]:
            st.code(w["detail"], language="text")

        st.markdown("**Table 5.3 — Semantics II**")
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
            f"metadata intact      : True   actor={demo.m['actor']}  "
            f"ncp={demo.m['ncp']}  outcome={demo.m['outcome']}\n"
            f"commitment c(a)      : {demo.c[:32]}...\n"
            f"payload key k(a)     : {demo.k}   <- destroyed\n"
            f"invalidation iota(a) : month={demo.iota['month']}  "
            f"ground={demo.iota['ground']}\n"
            f"payload readable     : {bool(trf.alpha(demo, demo.t_a + demo.floor))}",
            language="text",
        )

        if M["sem1_total"] == 95 and M["sem2_total"] == 0 and M["cor12"] == 39:
            st.success(
                "Matches the thesis: 95 violations across 90 records under "
                "Semantics I, 39 Corollary 1.2 witnesses, 0 violations under "
                "Semantics II."
            )
        else:
            st.error(
                "This run does NOT match the figures reported in Chapter 5. "
                "Do not present these numbers — investigate the discrepancy first."
            )


# ----------------------------------------------------------------------
# Tab 2 — parameter exploration, explicitly outside the thesis
# ----------------------------------------------------------------------

with tab2:
    st.subheader("Exploration — how the violation rate responds to parameters")
    st.warning(
        "Not a thesis claim. The thesis reports the seed-20260915 configuration "
        "only. This tab exists to show that the collision is not an artefact of "
        "the chosen parameters: Theorem 1 holds for any parameters under which a "
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

with tab3:
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
            st.markdown("**Table 5.4 — constructed against Synthea payloads**")
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
                st.json(json.loads(real[0].payload))

        except FileNotFoundError:
            st.info(
                "No committed bundles found. Offline step, requires Java 17+:\n\n"
                "`java -jar synthea.jar -s 20260915 -cs 20260915 -p 100 "
                "--exporter.fhir.export=true`\n\n"
                "then commit `synthea_run/output/fhir/` to the repository."
            )


st.divider()
st.caption(
    "This application is a viewer over the verified artefact. It is not a source "
    "of results. Tab 1 and Tab 3 reproduce figures reported in Chapter 5; Tab 2 "
    "is outside the thesis claims. Source: trf_checker.py and synthea_layer.py, "
    "both unmodified."
)
