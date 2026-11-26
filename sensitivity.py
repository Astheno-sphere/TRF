"""Sensitivity analysis for the fixed 200-record cohort (seed 20260915).

Varies only two inputs: the cross-border (primary-use) retention floor, and whether
the Art 68(12) ceiling reaches the SPE audit entries. Request times, permit expiries
and the SPE floor stay as generated. Prints one row per scenario, then the
extended-response-period check. Deterministic; standard library only.

    python3 sensitivity.py
"""
import trf_checker as t

INF = t.INF


def run(floor, ceiling_applies, delta=1):
    old_floor, old_delta = t.FLOOR_XBORDER, t.DELTA
    t.FLOOR_XBORDER, t.DELTA = floor, delta
    try:
        recs = t.generate()
        if not ceiling_applies:
            for r in recs:
                if r.sigma == "secondary":
                    r.t_pi = INF          # ceiling deadline becomes infinite
        v1 = {r.rid: t.check_semantics_I(r) for r in recs}
        for r in recs:
            t.apply_invalidation(r)
        v2 = {r.rid: t.check_semantics_II(r) for r in recs}
        return {"recs": sum(1 for k in v1 if v1[k]),
                "viol": sum(len(x) for x in v1.values()),
                "sem2": sum(len(x) for x in v2.values()),
                "inv": sum(1 for r in recs if r.iota is not None)}
    finally:
        t.FLOOR_XBORDER, t.DELTA = old_floor, old_delta


if __name__ == "__main__":
    print(f"seed={t.SEED}  SPE floor={t.FLOOR_SPE}  ceiling={t.CEILING} months")
    print(f"{'floor':>6} {'ceiling':>9} {'records':>8} {'plaintext viol':>15} "
          f"{'accountability viol':>20} {'invalidated':>12}")
    for floor in (120, 72, 36):
        for applies in (True, False):
            r = run(floor, applies)
            print(f"{floor:>6} {'applies' if applies else 'excluded':>9} {r['recs']:>8} "
                  f"{r['viol']:>15} {r['sem2']:>20} {r['inv']:>12}")
    r3 = run(120, True, delta=3)
    print(f"\nresponse period 3 months, floor 120, ceiling applies: "
          f"{r3['recs']} records, {r3['viol']} violations, accountability {r3['sem2']}")
