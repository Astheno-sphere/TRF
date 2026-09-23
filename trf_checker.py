"""
TRF feasibility checker
=======================
Executable witness for Theorem 1 (infeasibility under plaintext-verifiability
semantics) and Theorem 2 (feasibility under accountability-preserving semantics)
of the Tri-Lateral Retention Feasibility Model.

Thesis: Verifiable Crypto-Erasure for Cross-Border Health Data Audit Trails
        under the European Health Data Space.
Author: Arshad Akhtar Abbasia, HiMolde.

Model reference: Chapter 4, Sections 4.3-4.7.
  Record a = (m, p, c, k, t_a, F, sigma)
  C1 retention floor : V(a,t) = 1 for t in [t_a, t_a + F]
  C2 erasure right   : alpha(a,t) = 0 for t >= t_r + delta
  C3 deletion ceiling: alpha(a,t) = 0 for t >= t_pi + 6   (secondary pathway)

Run:  python trf_checker.py
Deterministic: fixed seed, identical output on every run.
"""

import hashlib
import os
import random
from itertools import product

SEED = 20260915
DELTA = 1          # GDPR Art 12(3) baseline response period, months
CEILING = 6        # EHDS Art 68(12), months after permit expiry
FLOOR_XBORDER = 120  # eHDSI deployment baseline, months
FLOOR_SPE = 12       # EHDS Art 73(1)(e), months
INF = float("inf")


# ----------------------------------------------------------------------
# Cryptographic primitives (hiding commitment + simulated key destruction)
# ----------------------------------------------------------------------

def commit(payload: bytes, salt: bytes) -> str:
    """Hiding, binding commitment. Salt is REQUIRED (Chapter 4, Section 4.9):
    an unsalted hash of a low-entropy clinical payload is guessable and would
    itself remain personal data."""
    return hashlib.sha256(salt + payload).hexdigest()


class Record:
    """One audit record and its lifecycle state."""

    def __init__(self, rid, t_a, floor, sigma, payload, t_r=INF, t_pi=INF):
        self.rid = rid
        self.t_a = t_a
        self.floor = floor
        self.sigma = sigma
        self.t_r = t_r
        self.t_pi = t_pi
        # metadata m(a): accountability content, no clinical payload
        self.m = {"rid": rid, "actor": f"HP-{rid % 37:03d}",
                  "ncp": ["NO", "PT", "CZ", "FI"][rid % 4],
                  "patient_pseudonym": f"PSN-{rid % 100:04d}",
                  "doc_category": "PatientSummary" if sigma == "primary" else "SPE-AccessLog",
                  "legal_basis": "Art9(2)(h)" if sigma == "primary" else "DataPermit",
                  "outcome": "success"}
        self.salt = os.urandom(16) if False else bytes([(rid * 7 + i) % 256 for i in range(16)])
        self.payload = payload
        self.c = commit(payload, self.salt)   # survives invalidation
        self.k = f"KEY-{rid:06d}"             # destroyed at invalidation
        self.iota = None                      # invalidation entry

    # -- model quantities ------------------------------------------------
    def window(self):
        return range(self.t_a, self.t_a + self.floor + 1)

    def erasure_deadline(self):
        return self.t_r + DELTA if self.t_r < INF else INF

    def ceiling_deadline(self):
        if self.sigma != "secondary" or self.t_pi == INF:
            return INF
        return self.t_pi + CEILING

    def t_invalidation(self):
        return min(self.erasure_deadline(), self.ceiling_deadline())


# ----------------------------------------------------------------------
# Semantics I - plaintext verifiability:  V_I(a,t) = alpha(a,t)
# ----------------------------------------------------------------------

def check_semantics_I(rec):
    """C1 demands alpha=1 across the window; C2/C3 demand alpha=0 from their
    deadlines. Report every month where both are demanded at once."""
    violations = []
    for deadline, constraint in ((rec.erasure_deadline(), "C2"),
                                 (rec.ceiling_deadline(), "C3")):
        if deadline == INF:
            continue
        for t in rec.window():
            if t >= deadline:
                violations.append({
                    "rid": rec.rid, "month": t, "constraint": constraint,
                    "detail": (f"C1 requires V=1 (=> alpha=1) at t={t} within "
                               f"[{rec.t_a},{rec.t_a + rec.floor}]; {constraint} "
                               f"requires alpha=0 from t={deadline}")})
                break   # first collision month is the witness
    return violations


# ----------------------------------------------------------------------
# Semantics II - accountability-preserving verifiability
# Trajectory from the constructive proof of Theorem 2.
# ----------------------------------------------------------------------

def apply_invalidation(rec):
    t_I = rec.t_invalidation()
    if t_I < INF:
        ground = ("GDPR Art 17(1)" if rec.erasure_deadline() <= rec.ceiling_deadline()
                  else "EHDS Art 68(12)")
        rec.k = None                      # irreversible key destruction
        rec.salt = None                   # salt destroyed with the key (Ch4 §4.8)
        rec.iota = {"rid": rec.rid, "month": t_I, "ground": ground,
                    "authorised_by": "DPO", "key_id_commitment":
                        hashlib.sha256(f"KEY-{rec.rid:06d}".encode()).hexdigest()[:16]}
    return rec


def alpha(rec, t):
    return 1 if t < rec.t_invalidation() else 0


def V_II(rec, t):
    """(i) metadata intact, (ii) commitment present,
       (iii) any loss of accessibility is itself logged."""
    if not rec.m:
        return False, "metadata missing"
    if not rec.c:
        return False, "commitment missing"
    if alpha(rec, t) == 0 and t >= rec.t_a:
        if rec.iota is None:
            return False, "payload inaccessible but no invalidation entry"
    return True, ""


def check_semantics_II(rec):
    violations = []
    for t in rec.window():                                   # C1
        ok, why = V_II(rec, t)
        if not ok:
            violations.append({"rid": rec.rid, "month": t,
                               "constraint": "C1", "detail": why})
            break
    d = rec.erasure_deadline()                               # C2
    if d < INF:
        horizon = int(min(rec.t_a + rec.floor, d + 24))
        for t in range(int(d), horizon + 1):
            if alpha(rec, t) != 0:
                violations.append({"rid": rec.rid, "month": t, "constraint": "C2",
                                   "detail": "payload still accessible after erasure deadline"})
                break
    d = rec.ceiling_deadline()                               # C3
    if d < INF:
        horizon = int(min(rec.t_a + rec.floor, d + 24))
        for t in range(int(d), horizon + 1):
            if alpha(rec, t) != 0:
                violations.append({"rid": rec.rid, "month": t, "constraint": "C3",
                                   "detail": "payload still accessible after deletion ceiling"})
                break
    return violations


# ----------------------------------------------------------------------
# Independent cross-check: exhaustive search over alpha assignments.
# Confirms Semantics I infeasibility is a property of the constraints and
# not an artefact of how check_semantics_I is written.
# ----------------------------------------------------------------------

def brute_force_semantics_I(t_a, floor, t_r, t_pi, sigma, horizon):
    """Enumerate every alpha in {0,1}^horizon; return True if any satisfies
    C1 (under V_I = alpha), C2 and C3 simultaneously."""
    e_dl = t_r + DELTA if t_r < INF else INF
    c_dl = t_pi + CEILING if (sigma == "secondary" and t_pi < INF) else INF
    for assign in product([0, 1], repeat=horizon):
        ok = True
        for t in range(horizon):
            if t_a <= t <= t_a + floor and assign[t] != 1:
                ok = False; break                      # C1 under Semantics I
            if t >= e_dl and assign[t] != 0:
                ok = False; break                      # C2
            if t >= c_dl and assign[t] != 0:
                ok = False; break                      # C3
        if ok:
            return True
    return False


# ----------------------------------------------------------------------
# Record generation
# ----------------------------------------------------------------------

def generate(n_primary=100, n_secondary=100, seed=SEED):
    rng = random.Random(seed)
    records = []
    rid = 0
    # Class 1: cross-border audit records, floor 120 months
    for _ in range(n_primary):
        t_a = rng.randint(0, 11)
        t_r = t_a + rng.randint(1, 130) if rng.random() < 0.40 else INF
        payload = f"<FHIR:Bundle patient-summary rid={rid}>".encode()
        records.append(Record(rid, t_a, FLOOR_XBORDER, "primary", payload, t_r=t_r))
        rid += 1
    # Class 2: SPE access-log records, floor 12 months, ceiling applies
    for _ in range(n_secondary):
        t_a = rng.randint(0, 11)
        permit_len = rng.randint(1, 12)
        t_pi = t_a + permit_len
        t_r = t_a + rng.randint(1, 18) if rng.random() < 0.25 else INF
        payload = f"<FHIR:AuditEvent spe-access rid={rid}>".encode()
        records.append(Record(rid, t_a, FLOOR_SPE, "secondary", payload,
                              t_r=t_r, t_pi=t_pi))
        rid += 1
    return records


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main():
    print("=" * 74)
    print("TRF FEASIBILITY CHECKER".center(74))
    print(f"seed={SEED}  delta={DELTA}  ceiling={CEILING}  "
          f"floors: cross-border={FLOOR_XBORDER}, SPE={FLOOR_SPE}".center(74))
    print("=" * 74)

    records = generate()
    prim = [r for r in records if r.sigma == "primary"]
    sec = [r for r in records if r.sigma == "secondary"]
    print(f"\nGenerated {len(records)} records "
          f"({len(prim)} cross-border, {len(sec)} SPE access-log)")

    # ---------------- Semantics I ----------------
    print("\n" + "-" * 74)
    print("SEMANTICS I  (plaintext verifiability:  V = alpha)   -> Theorem 1")
    print("-" * 74)
    v1 = {r.rid: check_semantics_I(r) for r in records}
    n_bad = sum(1 for k in v1 if v1[k])
    n_bad_p = sum(1 for r in prim if v1[r.rid])
    n_bad_s = sum(1 for r in sec if v1[r.rid])
    total_v = sum(len(x) for x in v1.values())
    print(f"records with >=1 violation : {n_bad}/{len(records)}")
    print(f"  cross-border (F=120)     : {n_bad_p}/{len(prim)}")
    print(f"  SPE access-log (F=12)    : {n_bad_s}/{len(sec)}")
    print(f"total constraint violations: {total_v}")

    # SPE records violating WITHOUT any erasure request -> Corollary 1.2
    no_req = [r for r in sec if r.t_r == INF and v1[r.rid]]
    print(f"\nCorollary 1.2 witnesses (SPE, NO erasure request, still infeasible):"
          f" {len(no_req)}")
    for r in no_req[:3]:
        d = v1[r.rid][0]
        print(f"  rid={r.rid}: t_a={r.t_a} permit expires t_pi={r.t_pi} "
              f"-> C3 from t={int(r.ceiling_deadline())}, "
              f"C1 to t={r.t_a + r.floor}  | collision at t={d['month']}")

    print("\nSample violation witnesses (cross-border):")
    shown = 0
    for r in prim:
        if v1[r.rid] and shown < 3:
            print(f"  {v1[r.rid][0]['detail']}")
            shown += 1

    # ---------------- Independent cross-check ----------------
    print("\n" + "-" * 74)
    print("INDEPENDENT CROSS-CHECK: exhaustive search over alpha assignments")
    print("-" * 74)
    cases = [
        ("SPE, no erasure request, permit 3mo", 0, 12, INF, 3, "secondary"),
        ("SPE, erasure at t=2",                 0, 12, 2,   9, "secondary"),
        ("cross-border scaled (F=12), erasure at t=4", 0, 12, 4, INF, "primary"),
        ("control: no request, no expiry",      0, 12, INF, INF, "primary"),
    ]
    for label, t_a, floor, t_r, t_pi, sigma in cases:
        feasible = brute_force_semantics_I(t_a, floor, t_r, t_pi, sigma, horizon=14)
        print(f"  {label:<46} feasible={feasible}")

    # ---------------- Semantics II ----------------
    print("\n" + "-" * 74)
    print("SEMANTICS II (accountability preservation)          -> Theorem 2")
    print("-" * 74)
    for r in records:
        apply_invalidation(r)
    v2 = {r.rid: check_semantics_II(r) for r in records}
    n_bad2 = sum(1 for k in v2 if v2[k])
    total_v2 = sum(len(x) for x in v2.values())
    n_inv = sum(1 for r in records if r.iota is not None)
    print(f"records invalidated        : {n_inv}/{len(records)}")
    print(f"  ground = GDPR Art 17(1)  : "
          f"{sum(1 for r in records if r.iota and 'Art 17' in r.iota['ground'])}")
    print(f"  ground = EHDS Art 68(12) : "
          f"{sum(1 for r in records if r.iota and '68(12)' in r.iota['ground'])}")
    print(f"records with >=1 violation : {n_bad2}/{len(records)}")
    print(f"total constraint violations: {total_v2}")

    # auditor view on a previously-violating record
    demo = no_req[0] if no_req else sec[0]
    print(f"\nAuditor view of rid={demo.rid} after invalidation:")
    print(f"  metadata intact      : {bool(demo.m)}  actor={demo.m['actor']} "
          f"ncp={demo.m['ncp']} outcome={demo.m['outcome']}")
    print(f"  commitment c(a)      : {demo.c[:32]}...")
    print(f"  payload key k(a)     : {demo.k}   <- destroyed")
    print(f"  invalidation iota(a) : month={demo.iota['month']} "
          f"ground={demo.iota['ground']}")
    print(f"  payload readable?    : {bool(alpha(demo, demo.t_a + demo.floor))}")

    print("\n" + "=" * 74)
    print(f"RESULT  Semantics I : {total_v} violations across {n_bad} records  "
          f"-> INFEASIBLE")
    print(f"RESULT  Semantics II: {total_v2} violations across {n_bad2} records  "
          f"-> FEASIBLE")
    print("=" * 74)


if __name__ == "__main__":
    main()


# ----------------------------------------------------------------------
# Extended response period witness (Chapter 5, Section 5.5a)
# GDPR Art 12(3) permits extension of the one-month response period by a
# further two months. The theorems are stated for arbitrary finite delta;
# this runs the model at delta = 3 to witness that claim rather than assert it.
# ----------------------------------------------------------------------

def delta_witness(delta_values=(1, 3)):
    """Re-run the population at each delta and report the figures."""
    global DELTA
    original, rows = DELTA, []
    for d in delta_values:
        DELTA = d
        recs = generate()
        v1 = {r.rid: check_semantics_I(r) for r in recs}
        sec = [r for r in recs if r.sigma == "secondary"]
        row = {"delta": d,
               "sem1_records": sum(1 for k in v1 if v1[k]),
               "sem1_total": sum(len(x) for x in v1.values()),
               "cor12": sum(1 for r in sec if r.t_r == INF and v1[r.rid])}
        for r in recs:
            apply_invalidation(r)
        v2 = {r.rid: check_semantics_II(r) for r in recs}
        row["sem2_records"] = sum(1 for k in v2 if v2[k])
        row["sem2_total"] = sum(len(x) for x in v2.values())
        row["invalidated"] = sum(1 for r in recs if r.iota is not None)
        rows.append(row)
    DELTA = original
    return rows


if __name__ == "__main__" and "--delta-witness" in __import__("sys").argv:
    print(f"{'delta':>6}{'SemI recs':>11}{'SemI viol':>11}{'Cor1.2':>9}"
          f"{'SemII recs':>12}{'SemII viol':>12}{'invalidated':>13}")
    for r in delta_witness():
        print(f"{r['delta']:>6}{r['sem1_records']:>11}{r['sem1_total']:>11}"
              f"{r['cor12']:>9}{r['sem2_records']:>12}{r['sem2_total']:>12}"
              f"{r['invalidated']:>13}")
