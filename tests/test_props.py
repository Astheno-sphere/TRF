"""The exhaustive cross-check agrees with the checker, including at the window boundaries.

brute_force_semantics_I enumerates every validity trajectory; check_semantics_I applies the
closed-form condition. They are separate functions sharing only the constants DELTA and CEILING,
so a boundary error in either one shows up here as a disagreement.
"""
import pytest
from trf_checker import INF, Record, brute_force_semantics_I, check_semantics_I

CASES = (
    [("primary", 0, 12, t_r, INF) for t_r in range(0, 15)]          # erasure before, at, after the floor's end
    + [("secondary", 0, 12, INF, t_pi) for t_pi in range(0, 10)]    # ceiling only
    + [("secondary", 0, 12, t_r, 3) for t_r in (0, 5, 11, 12, 13)]  # both
    + [("primary", 2, 4, INF, INF)]                                 # nothing pulls toward removal
)


@pytest.mark.parametrize("sigma,t_a,floor,t_r,t_pi", CASES)
def test_brute_force_matches_checker(sigma, t_a, floor, t_r, t_pi):
    horizon = t_a + floor + 3
    rec = Record(0, t_a, floor, sigma, b"x", t_r=t_r, t_pi=t_pi)
    assert brute_force_semantics_I(t_a, floor, t_r, t_pi, sigma, horizon) == (check_semantics_I(rec) == [])
