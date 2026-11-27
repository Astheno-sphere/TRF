"""Secondary-use (SPE) subset sensitivity checks for the fixed 200-record cohort (seed 20260915).

Reuses trf_checker (generate, check_semantics_I, apply_invalidation, check_semantics_II).
Prints claims 1-5 and the baseline re-confirmation. Deterministic; standard library only.

    python3 sensitivity_secondary.py
"""
from collections import defaultdict

import trf_checker as t

INF = t.INF


def population(floor_xborder=120, floor_spe=12, ceiling_applies=True, delta=1):
    """Fresh cohort under the given parameters; constants restored by the caller via _params."""
    saved = (t.FLOOR_XBORDER, t.FLOOR_SPE, t.DELTA)
    t.FLOOR_XBORDER, t.FLOOR_SPE, t.DELTA = floor_xborder, floor_spe, delta
    try:
        recs = t.generate()
    finally:
        t.FLOOR_XBORDER, t.FLOOR_SPE, t.DELTA = saved
    if not ceiling_applies:
        for r in recs:
            if r.sigma == "secondary":
                r.t_pi = INF
    return recs


def sem1(recs, strict=False, delta=1):
    """Semantics I violations per record, via t.check_semantics_I. strict = half-open endpoint:
    conflict only if deadline < t_a + F, obtained by shortening the window by one month."""
    saved = t.DELTA
    t.DELTA = delta
    try:
        out = {}
        for r in recs:
            if strict:
                f = r.floor
                r.floor = f - 1
                try:
                    out[r.rid] = t.check_semantics_I(r)
                finally:
                    r.floor = f
            else:
                out[r.rid] = t.check_semantics_I(r)
        return out
    finally:
        t.DELTA = saved


def secondary_stats(floor_spe, ceiling_applies):
    recs = population(floor_spe=floor_spe, ceiling_applies=ceiling_applies)
    sec = [r for r in recs if r.sigma == "secondary"]
    v = sem1(sec)
    req = sum(1 for r in sec for x in v[r.rid] if x["constraint"] == "C2")
    ceil_ = sum(1 for r in sec for x in v[r.rid] if x["constraint"] == "C3")
    both = sum(1 for r in sec if {x["constraint"] for x in v[r.rid]} == {"C2", "C3"})
    return {"n": len(sec), "request": req, "ceiling": ceil_, "both": both,
            "records": sum(1 for r in sec if v[r.rid]),
            "pairs": sum(len(v[r.rid]) for r in sec)}


def baseline(floor=120, ceiling_applies=True, strict=False, delta=1):
    recs = population(floor_xborder=floor, ceiling_applies=ceiling_applies, delta=delta)
    v1 = sem1(recs, strict=strict, delta=delta)
    prim = [r for r in recs if r.sigma == "primary"]
    sec = [r for r in recs if r.sigma == "secondary"]
    allv = [x for r in recs for x in v1[r.rid]]
    c2 = {r.rid for r in recs if any(x["constraint"] == "C2" for x in v1[r.rid])}
    c3 = {r.rid for r in recs if any(x["constraint"] == "C3" for x in v1[r.rid])}
    saved = t.DELTA
    t.DELTA = delta
    try:
        for r in recs:
            t.apply_invalidation(r)
        v2 = sum(len(t.check_semantics_II(r)) for r in recs)
    finally:
        t.DELTA = saved
    return {"records": sum(1 for r in recs if v1[r.rid]), "viol": len(allv),
            "xb": sum(1 for r in prim if v1[r.rid]), "spe": sum(1 for r in sec if v1[r.rid]),
            "req_only": len(c2 - c3), "ceil_only": len(c3 - c2), "both": len(c2 & c3),
            "no_req": sum(1 for r in sec if r.t_r == INF and v1[r.rid]),
            "c2_pairs": sum(1 for x in allv if x["constraint"] == "C2"),
            "c3_pairs": sum(1 for x in allv if x["constraint"] == "C3"),
            "inv": sum(1 for r in recs if r.iota is not None),
            "inv_request": sum(1 for r in recs if r.iota and "Art 17" in r.iota["ground"]),
            "inv_ceiling": sum(1 for r in recs if r.iota and "68(12)" in r.iota["ground"]),
            "sem2": v2}


def permit_labels():
    recs = population()
    sec = [r for r in recs if r.sigma == "secondary"]
    by = defaultdict(list)
    for r in sec:
        by[r.m["permit"]].append(r)
    reused = {k: v for k, v in by.items() if len(v) > 1}
    multi = {k: v for k, v in reused.items() if len({r.t_pi for r in v}) > 1}
    return {"secondary": len(sec), "distinct": len(by), "reused": len(reused),
            "singleton": len(by) - len(reused), "multi_expiry": len(multi),
            "same_expiry": sorted(set(reused) - set(multi)),
            "min_group": min(len(v) for v in by.values()),
            "max_group": max(len(v) for v in by.values()),
            "expiry_counts": {k: len({r.t_pi for r in v}) for k, v in sorted(reused.items())}}


def main():
    print(f"seed={t.SEED}  delta={t.DELTA}  ceiling={t.CEILING}  SPE floor={t.FLOOR_SPE}  "
          f"xborder floor={t.FLOOR_XBORDER}")

    print("\n[1] Secondary-use subset, 12-month floor")
    for ceil_ in (True, False):
        s = secondary_stats(12, ceil_)
        print(f"  ceiling {'applies ' if ceil_ else 'excluded'}: n={s['n']} request-related={s['request']} "
              f"ceiling={s['ceiling']} both={s['both']} affected_records={s['records']} "
              f"record_constraint_pairs={s['pairs']}")

    print("\n[2] Secondary-use subset, 60-month floor")
    for ceil_ in (True, False):
        s = secondary_stats(60, ceil_)
        print(f"  ceiling {'applies ' if ceil_ else 'excluded'}: affected_records={s['records']} "
              f"record_constraint_pairs={s['pairs']} (request={s['request']} ceiling={s['ceiling']})")
    print("  Arithmetic: ceiling deadline = t_a + offset + 6 <= t_a + 18 (offset in 1..12, 6-month ceiling).")
    print("  The window ends at t_a + 60 > t_a + 18, so C3 collides in every one of the 100 records (100/100).")
    print("  Pairs = 100 ceiling + 22 request: a request deadline t_a + (1..18) + 1 <= t_a + 19 < t_a + 60 also always collides.")

    print("\n[3] Strict (half-open) endpoint, baseline 120-month primary floor, ceiling applies")
    for strict in (False, True):
        b = baseline(strict=strict)
        print(f"  {'strict  ' if strict else 'closed  '}: pairs={b['viol']} records={b['records']} "
              f"SPE ceiling(C3) pairs={b['c3_pairs']} request(C2) pairs={b['c2_pairs']}")

    print("\n[4] GDPR response parameter delta=3, reference scenario")
    for d in (1, 3):
        b = baseline(delta=d)
        print(f"  delta={d}: violations={b['viol']} records={b['records']} "
              f"no_request_ceiling_witnesses={b['no_req']} semantics_II={b['sem2']}")

    print("\n[5] Permit labels in the 100 secondary-use records")
    p = permit_labels()
    print("  label rule: permit = f'DP-{rid % 17:03d}' (rid 100..199)")
    print(f"  secondary records={p['secondary']} distinct labels={p['distinct']} reused (>1 record)={p['reused']} "
          f"singletons={p['singleton']}")
    print(f"  group size min={p['min_group']} max={p['max_group']}")
    print(f"  reused labels with >1 distinct expiry month={p['multi_expiry']}; "
          f"reused labels with one expiry={p['same_expiry']}")
    print(f"  distinct expiry months per label: {p['expiry_counts']}")

    print("\n[6] Baseline re-confirmation")
    b = baseline()
    print(f"  violations={b['viol']} records={b['records']} cross-border={b['xb']} SPE={b['spe']}")
    print(f"  request-only={b['req_only']} ceiling-only={b['ceil_only']} both={b['both']} "
          f"no-request witnesses={b['no_req']}")
    print(f"  invalidations={b['inv']} (request {b['inv_request']}, ceiling {b['inv_ceiling']}) "
          f"semantics II violations={b['sem2']}")
    print("  Table 2 (records/violations):")
    for floor in (120, 72, 36):
        row = [baseline(floor=floor, ceiling_applies=c) for c in (True, False)]
        print(f"    floor {floor:>3}: applies {row[0]['records']}/{row[0]['viol']}  "
              f"excluded {row[1]['records']}/{row[1]['viol']}")


if __name__ == "__main__":
    main()
