"""
Norwegian context layer for the TRF feasibility checker
=======================================================
PLUG-AND-PLAY. This module imports trf_checker unmodified and adds record
classes shaped by the Norwegian implementation context. It changes nothing the
thesis depends on: `python3 trf_checker.py` still reproduces 95/90/39/0/138.

What it varies is what the model actually reads: the retention floor F(a), the
pathway, and the arrival of erasure requests and permit expiries. It does NOT
claim that Norwegian payloads change any result — Chapter 5 shows the results
are invariant to payload content, and that invariance is why the illustrative
payloads below are safe to use.

Classes
  NO-XB      Cross-border audit record at the Norwegian NCPeH. Inbound patient
             summary from PT/CZ/FI to a legevakt (Bodo, Stjordal).
             F = 120 months (eHDSI deployment baseline).
  NO-SPE     Secure Processing Environment access log, Helsedataservice permit,
             processing in a NORTRE node. F = 12 (Art 73(1)(e)),
             ceiling 6 months after permit expiry (Art 68(12)).
  NO-JOURNAL Audit record tied to a patient record held under Norwegian law.
             Floor is INDEFINITE: pasientjournalloven s 25 and journalforskriften
             s 14 require retention until, given the character of the health care,
             the record is no longer assumed to be needed; archive law may then
             preserve it. There is no number in the primary sources, so none is
             invented here. For computation the indefinite floor is truncated at
             HORIZON_INDEFINITE months and labelled as a truncation.

Run:  python3 norwegian_layer.py
"""

import random
import trf_checker as trf

HORIZON_INDEFINITE = 600          # 50 years; a computation bound, NOT a legal period
SEED = trf.SEED

NCPS = ["PT", "CZ", "FI"]
SITES = ["Bodo legevakt", "Stjordal legevakt"]
NODES = ["TSD (UiO)", "SAFE (UiB)", "HUNT Cloud (NTNU)", "controller-provided server"]


def _xb_payload(rid, rng):
    """Stands for the ITI-55 QueryByParameter segment an ATNA record carries:
    the demographics typed into patient discovery. Constructed, not real."""
    return (f"<ITI-55 QueryByParameter base64> name=SYN-{rid:04d} "
            f"birthTime=19{rng.randint(40,99)}{rng.randint(10,12)}{rng.randint(10,28)} "
            f"gender={rng.choice('MF')} addr=NO-{rng.randint(1000,9999)}").encode()


def _spe_payload(rid, rng):
    return (f"<SPE activity log> query=SELECT diagnosis,birthyear FROM permit-"
            f"{rng.randint(2026,2031)}-{rid:04d} rows={rng.randint(50,5000)}").encode()


def build(n_xb=60, n_spe=60, n_journal=40, seed=SEED):
    rng = random.Random(seed)
    recs, rid = [], 0
    for _ in range(n_xb):                                   # NO-XB
        t_a = rng.randint(0, 11)
        t_r = t_a + rng.randint(1, 130) if rng.random() < 0.40 else trf.INF
        r = trf.Record(rid, t_a, trf.FLOOR_XBORDER, "primary", _xb_payload(rid, rng), t_r=t_r)
        r.m.update({"klasse": "NO-XB", "site": rng.choice(SITES),
                    "ncp": rng.choice(NCPS), "doc_category": "PatientSummary (inbound)",
                    "legal_basis": "Art9(2)(h)"})
        recs.append(r); rid += 1
    for _ in range(n_spe):                                  # NO-SPE
        t_a = rng.randint(0, 11)
        t_pi = t_a + rng.randint(1, 12)
        t_r = t_a + rng.randint(1, 18) if rng.random() < 0.25 else trf.INF
        r = trf.Record(rid, t_a, trf.FLOOR_SPE, "secondary", _spe_payload(rid, rng),
                       t_r=t_r, t_pi=t_pi)
        r.m.update({"klasse": "NO-SPE", "node": rng.choice(NODES),
                    "doc_category": "SPE-ActivityLog", "legal_basis": "DataPermit (Helsedataservice)"})
        recs.append(r); rid += 1
    for _ in range(n_journal):                              # NO-JOURNAL
        t_a = rng.randint(0, 11)
        t_r = t_a + rng.randint(1, 240) if rng.random() < 0.40 else trf.INF
        r = trf.Record(rid, t_a, HORIZON_INDEFINITE, "primary", _xb_payload(rid, rng), t_r=t_r)
        r.m.update({"klasse": "NO-JOURNAL", "doc_category": "JournalAccess",
                    "legal_basis": "pasientjournalloven s 25 (purpose-based, indefinite)"})
        recs.append(r); rid += 1
    return recs


def run(recs, label="NORWEGIAN LAYER"):
    klasser = sorted({r.m["klasse"] for r in recs})
    v1 = {r.rid: trf.check_semantics_I(r) for r in recs}
    for r in recs:
        trf.apply_invalidation(r)
    v2 = {r.rid: trf.check_semantics_II(r) for r in recs}
    print("=" * 74); print(label.center(74)); print("=" * 74)
    print(f"\n{'class':<12}{'n':>5}{'SemI recs':>11}{'SemI viol':>11}"
          f"{'invalidated':>13}{'SemII viol':>12}")
    for k in klasser:
        sub = [r for r in recs if r.m["klasse"] == k]
        print(f"{k:<12}{len(sub):>5}"
              f"{sum(1 for r in sub if v1[r.rid]):>11}"
              f"{sum(len(v1[r.rid]) for r in sub):>11}"
              f"{sum(1 for r in sub if r.iota):>13}"
              f"{sum(len(v2[r.rid]) for r in sub):>12}")
    print(f"\n{'TOTAL':<12}{len(recs):>5}"
          f"{sum(1 for r in recs if v1[r.rid]):>11}"
          f"{sum(len(x) for x in v1.values()):>11}"
          f"{sum(1 for r in recs if r.iota):>13}"
          f"{sum(len(x) for x in v2.values()):>12}")
    return v1, v2


def walkthrough(recs, v1):
    """One record per class, shown end to end: which obligation binds, where it
    collides, and what an auditor is left with after invalidation."""
    print("\n" + "-" * 74); print("CASE WALKTHROUGHS"); print("-" * 74)
    for k in sorted({r.m["klasse"] for r in recs}):
        cand = [r for r in recs if r.m["klasse"] == k and v1[r.rid]]
        if not cand:
            print(f"\n{k}: no infeasible record under Semantics I in this draw."); continue
        r = cand[0]
        print(f"\n{k}  rid={r.rid}  ({r.m.get('site') or r.m.get('node') or r.m['legal_basis']})")
        print(f"  floor    : t={r.t_a} .. {r.t_a + r.floor}"
              + ("   [indefinite, truncated]" if k == "NO-JOURNAL" else ""))
        print(f"  erasure  : {'none' if r.t_r == trf.INF else 't_r=' + str(r.t_r) + ' -> deadline ' + str(int(r.erasure_deadline()))}")
        print(f"  ceiling  : {'n/a' if r.ceiling_deadline() == trf.INF else 't_pi=' + str(r.t_pi) + ' -> ' + str(int(r.ceiling_deadline()))}")
        print(f"  collision: {v1[r.rid][0]['constraint']} at t={v1[r.rid][0]['month']}")
        print(f"  after invalidation -> metadata intact={bool(r.m)}, commitment={r.c[:16]}..., "
              f"key={r.k}, salt={r.salt}, ground={r.iota['ground'] if r.iota else None}")


if __name__ == "__main__":
    recs = build()
    v1, _ = run(recs)
    walkthrough(recs, v1)
    print("\nNote: figures above are illustrative of the Norwegian setting, not")
    print("empirical. The canonical result of the thesis is unchanged and is")
    print("reproduced by running trf_checker.py on its own.")
