"""
Cross-sector instance: Norwegian police register logs
=====================================================
PLUG-AND-PLAY. Imports trf_checker unmodified.

Why this exists. Chapter 6 s 6.9 and Chapter 7 s 7.5 say the structure the TRF
Model captures — a retention floor, a subject-triggered erasure right, and a
deletion ceiling — is probably not specific to health, and flag the question as
uninvestigated. Norwegian law supplies a genuine instance outside health.

  Politiregisterloven (LOV-2010-05-28-16) s 17, kravet til sporbarhet:
    information about use of the system shall be registered and stored for at
    least 1 year and deleted at the latest after 3 years.
  Politiregisterforskriften (FOR-2013-09-20-1097) ch. 40 mirrors this:
    deleted at the earliest after 1 year and at the latest after 3 years.
  Politiregisterloven s 50-51 give the registered person rights to correction,
    blocking and deletion of information no longer necessary for the purpose.

That is a floor of 12 months and a ceiling of 36 months on the SAME log, plus a
subject-triggered right: the tri-lateral structure, in another sector, in
national law.

THE RESULT IS NOT THE ONE EXPECTED, AND IT IS THE MORE USEFUL ONE. Running the
model on this instance produces NO structural collision at all: the floor ends
at t_a + 12 and the ceiling bites at t_a + 36, so the provision defines a
bounded retention window rather than a contradiction. The Norwegian legislator
ordered the two limbs. Collisions appear only where an erasure request lands
inside the window.

That isolates what is defective about the EHDS pair. There the ceiling is
anchored to an EXTERNAL event, the expiry of the data permit, which can fall
before the floor on a log written late in the permit. A floor and a ceiling on
the same record are compatible when the instrument orders them from the same
origin, and collide when one is anchored elsewhere. The contribution of the
thesis is therefore not that floors and ceilings conflict in general; it is that
they conflict when their origins differ, which is the EHDS case.

Two further differences from the EHDS case are stated rather than hidden:
  1. The ceiling here runs from the log's own creation, not from the expiry of a
     permit. It is modelled by setting t_pi so that the ceiling lands at
     t_a + 36 (the checker computes ceiling = t_pi + 6).
  2. The ceiling attaches to the whole record, not only to a payload inside it.
     Under Semantics II the metadata cannot survive it, so the terminal
     transition of Chapter 4 s 4.8 is what discharges the ceiling here, at
     t_a + 36 rather than at floor expiry. This module reports the collision;
     it does not claim the mechanism transfers unchanged.

Run:  python3 cross_sector_check.py
"""

import random
import trf_checker as trf

FLOOR_POLITI = 12      # politiregisterloven s 17: at least 1 year
CEILING_POLITI = 36    # politiregisterloven s 17: deleted at the latest after 3 years


def build(n=60, seed=trf.SEED):
    rng = random.Random(seed)
    recs = []
    for rid in range(900, 900 + n):
        t_a = rng.randint(0, 11)
        # ceiling lands at t_a + 36; checker computes t_pi + 6
        t_pi = t_a + CEILING_POLITI - trf.CEILING
        t_r = t_a + rng.randint(1, 40) if rng.random() < 0.30 else trf.INF
        payload = f"<politiloggpost> bruker=POL-{rid % 97:03d} oppslag=register".encode()
        r = trf.Record(rid, t_a, FLOOR_POLITI, "secondary", payload, t_r=t_r, t_pi=t_pi)
        r.m.update({"klasse": "POLITI-LOG", "doc_category": "SystemUseLog",
                    "legal_basis": "politiregisterloven s 17"})
        recs.append(r)
    return recs


def main():
    recs = build()
    v1 = {r.rid: trf.check_semantics_I(r) for r in recs}
    n_bad = sum(1 for k in v1 if v1[k])
    structural = sum(1 for r in recs if r.t_r == trf.INF and v1[r.rid])
    for r in recs:
        trf.apply_invalidation(r)
    v2 = {r.rid: trf.check_semantics_II(r) for r in recs}
    print("=" * 74)
    print("CROSS-SECTOR INSTANCE: politiregisterloven s 17 (floor 12, ceiling 36)".center(74))
    print("=" * 74)
    print(f"\nrecords                              : {len(recs)}")
    print(f"Semantics I, records with violation  : {n_bad}")
    print(f"  of which with NO erasure request   : {structural}  <- floor vs ceiling alone")
    print(f"Semantics II, total violations       : {sum(len(x) for x in v2.values())}")
    print(f"records invalidated                  : {sum(1 for r in recs if r.iota)}")
    if structural == 0:
        print("\nNo structural collision: s 17 orders its two limbs from one origin")
        print("(floor at t_a + 12, ceiling at t_a + 36), so the provision defines a")
        print("bounded retention window rather than a contradiction. Every collision")
        print("found is erasure-driven.")
    cand = [r for r in recs if v1[r.rid]]
    if cand:
        r = cand[0]; d = v1[r.rid][0]
        print(f"\nwitness rid={r.rid}: log written t={r.t_a}; floor to t={r.t_a + r.floor}; "
              f"ceiling at t={int(r.ceiling_deadline())}; erasure deadline "
              f"{int(r.erasure_deadline())}; collision {d['constraint']} at t={d['month']}")
    print("\nThe floor parameter F(a) took a third value with no change to the model.")
    print("The finding: floors and ceilings coexist when one instrument fixes both from")
    print("the same origin, and collide when the ceiling is anchored to an external")
    print("event, as Art 68(12) anchors it to permit expiry. Scope: a structural")
    print("parallel. Whether the mechanism transfers to a record-level ceiling is a")
    print("design question this module does not answer.")


if __name__ == "__main__":
    main()
