"""
Bounded SMT check of Propositions 1-3 (optional module)
========================================================
An independent check of the TRF Model's propositions in a different formalism from the
checker. trf_checker.py evaluates 200 generated records; this module asks the Z3 SMT solver
whether ANY record, with ANY parameter values inside the stated bounds, contradicts a
proposition. Every check is posed as "find a counterexample"; the expected answer is
"unsat" (no counterexample exists within the bounds).

Model (Chapter 4, Sections 4.3-4.6), one record, months t = 0..H:
  alpha_t        payload accessible at month t (free Boolean per month)
  C1 floor       alpha_t for t in [t_a, t_a + F]                       (Semantics I: V = alpha)
  C2 right       not alpha_t for t >= t_r + delta, if a request arrives
  C3 ceiling     not alpha_t for t >= e + L, if a ceiling applies (e: its anchor event)
Semantics II (Proposition 2) adds the accountability state per month: m_acc kept, c kept,
an invalidation entry iota present, the subject link beta readable, and a subject-link
entry iota_subj present. V_II = m_acc and c and (alpha or iota) and (beta or iota_subj),
and C3 also requires beta = 0 from the ceiling where it reaches the subject fields.

Bounds: t_a in [0, 12], F in [1, 120] (so the 120-month cross-border floor is covered),
delta in [1, 3], request month and anchor event in [t_a, H], L in [1, 120], H = 140.
This is a bounded check: it covers every combination within the bounds, not all integers.
It checks that the propositions follow from the constraints as encoded here; like the
checker, it does not check that the constraints translate the law (Section 4.2 does that).

Run:  pip install z3-solver   then   python3 z3_check.py
"""

from z3 import And, Bool, If, Implies, Int, Not, Or, Solver, sat, unsat

H = 140
T = range(H + 1)


def record():
    """Symbolic parameters and constraints common to every check."""
    ta, F, d = Int("t_a"), Int("F"), Int("delta")
    tr, e, L = Int("t_r"), Int("e"), Int("L")
    req, ceil = Bool("request"), Bool("ceiling")
    alpha = [Bool(f"alpha_{t}") for t in T]
    bounds = And(ta >= 0, ta <= 12, F >= 1, F <= 120, d >= 1, d <= 3,
                 tr >= ta, tr <= H, e >= ta, e <= H, L >= 1, L <= 120)
    return ta, F, d, tr, e, L, req, ceil, alpha, bounds


def C1(alpha, ta, F):
    return And([Implies(And(ta <= t, t <= ta + F), alpha[t]) for t in T])


def C2(alpha, req, tr, d):
    return And([Implies(And(req, t >= tr + d), Not(alpha[t])) for t in T])


def C3(alpha, ceil, e, L):
    return And([Implies(And(ceil, t >= e + L), Not(alpha[t])) for t in T])


def check(name, formula):
    s = Solver()
    s.add(formula)
    r = s.check()
    print(f"{name:<74} {'unsat (no counterexample)' if r == unsat else 'SAT: ' + str(s.model())}")
    return r == unsat


def main():
    print("=" * 100)
    print("BOUNDED SMT CHECK OF PROPOSITIONS 1-3 (Z3)".center(100))
    print("=" * 100)
    print(f"bounds: t_a 0..12, F 1..120, delta 1..3, t_r and e in [t_a, {H}], L 1..120, horizon {H}")
    ok = []
    ta, F, d, tr, e, L, req, ceil, alpha, B = record()

    # Proposition 1, infeasibility direction: if a deadline falls inside the window,
    # no accessibility trajectory satisfies C1, C2 and C3 under Semantics I.
    inside = Or(And(req, tr + d <= ta + F), And(ceil, e + L <= ta + F))
    ok.append(check("P1  deadline inside window => no trajectory satisfies C1-C3 (Sem I)",
                    And(B, inside, C1(alpha, ta, F), C2(alpha, req, tr, d), C3(alpha, ceil, e, L))))

    # Proposition 1, boundary: if no deadline falls inside the window, the trajectory
    # "accessible until the earliest deadline" satisfies all three. Counterexample = it fails.
    dl = If(req, If(ceil, If(tr + d < e + L, tr + d, e + L), tr + d), If(ceil, e + L, H + 1))
    witness = [t < dl for t in T]
    ok.append(check("P1  no deadline inside window => witness trajectory satisfies C1-C3",
                    And(B, Not(inside),
                        Not(And(C1(witness, ta, F), C2(witness, req, tr, d), C3(witness, ceil, e, L))))))

    # Proposition 2: under Semantics II the constructive trajectory satisfies C1, C2 and C3
    # for every arrival pattern and floor. The construction keeps m_acc and c, sets alpha = 0
    # and logs iota from t_I = earliest deadline, and, where a ceiling applies (SPE records
    # whose subject fields it reaches), sets beta = 0 and logs iota_subj from the ceiling.
    tI = dl
    traj = [t < tI for t in T]

    def sem2(macc, c, iota, beta, iota_s):
        V2 = [And(macc[t], c[t], Or(traj[t], iota[t]), Or(beta[t], iota_s[t])) for t in T]
        c1 = And([Implies(And(ta <= t, t <= ta + F), V2[t]) for t in T])
        c3b = And([Implies(And(ceil, t >= e + L), Not(beta[t])) for t in T])
        return And(c1, C2(traj, req, tr, d), C3(traj, ceil, e, L), c3b)

    keep = [True for t in T]
    iota = [t >= tI for t in T]
    beta = [Or(Not(ceil), t < e + L) for t in T]
    iota_s = [And(ceil, t >= e + L) for t in T]
    ok.append(check("P2  constructive trajectory satisfies C1 (Sem II), C2, C3 for all inputs",
                    And(B, Not(sem2(keep, keep, iota, beta, iota_s)))))
    # Mutations of the construction must be refuted (sat): no invalidation entry; the
    # commitment removed at t_I; the subject link removed without its entry.
    mut2 = [Solver() for _ in range(3)]
    mut2[0].add(B, Not(sem2(keep, keep, [False for t in T], beta, iota_s)))
    mut2[1].add(B, Not(sem2(keep, [t < tI for t in T], iota, beta, iota_s)))
    mut2[2].add(B, Not(sem2(keep, keep, iota, beta, [False for t in T])))
    m2ok = all(m.check() == sat for m in mut2)
    print(f"{'mutation: construction without iota / without c / without iota_subj refuted':<74} {'sat, counterexamples found (as expected)' if m2ok else 'UNSAT: check insensitive'}")

    # Proposition 3: floor F from t_a, ceiling L from e >= t_a, Semantics I.
    # (a) collision whenever e + L <= t_a + F: no trajectory satisfies floor and ceiling.
    both = And(C1(alpha, ta, F), C3(alpha, True, e, L))
    ok.append(check("P3  e + L <= t_a + F => floor and ceiling not jointly satisfiable",
                    And(B, e + L <= ta + F, both)))
    # (b) no collision whenever e + L > t_a + F: accessible-until-(e+L) satisfies both.
    w3 = [t < e + L for t in T]
    ok.append(check("P3  e + L > t_a + F => witness satisfies floor and ceiling",
                    And(B, e + L > ta + F, Not(And(C1(w3, ta, F), C3(w3, True, e, L))))))
    # (i) same anchor (e = t_a): satisfiable for the record iff L > F.
    ok.append(check("P3(i)  e = t_a: jointly satisfiable only if L > F",
                    And(B, e == ta, L <= F, both)))
    ok.append(check("P3(i)  e = t_a and L > F: witness satisfies floor and ceiling",
                    And(B, e == ta, L > F, Not(And(C1(w3, ta, F), C3(w3, True, e, L))))))
    # (ii) external anchor with L <= F: collision exactly when e - t_a <= F - L.
    ok.append(check("P3(ii) L <= F, e - t_a <= F - L => collision",
                    And(B, L <= F, e - ta <= F - L, both)))
    ok.append(check("P3(ii) L <= F, e - t_a >  F - L => witness satisfies both",
                    And(B, L <= F, e - ta > F - L, Not(And(C1(w3, ta, F), C3(w3, True, e, L))))))

    # Sanity: the encoding can return sat, so unsat above is not an artefact of a broken model.
    s = Solver(); s.add(B, Not(req), Not(ceil), C1(alpha, ta, F))
    sanity = s.check() == sat
    print(f"{'sanity: no request, no ceiling => some trajectory satisfies C1':<74} {'sat (as expected)' if sanity else 'UNSAT: encoding broken'}")
    # Mutation checks: deliberately wrong versions of Proposition 3 must be refuted (sat),
    # showing the checks are sensitive to an off-by-one in the condition.
    m1 = Solver(); m1.add(B, e + L <= ta + F + 1, both)       # claims collision one month too late
    m2 = Solver(); m2.add(B, e + L > ta + F - 1, Not(And(C1(w3, ta, F), C3(w3, True, e, L))))
    mut = m1.check() == sat and m2.check() == sat
    print(f"{'mutation: Proposition 3 with an off-by-one condition is refuted':<74} {'sat, counterexample found (as expected)' if mut else 'UNSAT: checks insensitive'}")
    sanity = sanity and mut and m2ok
    print("=" * 100)
    print(f"RESULT: {sum(ok)}/{len(ok)} checks found no counterexample; sanity and mutation checks {'passed' if sanity else 'FAILED'}")
    print("=" * 100)


if __name__ == "__main__":
    main()
