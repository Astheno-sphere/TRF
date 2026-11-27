"""Pins the secondary-use sensitivity figures (seed 20260915, 200 records, 100 secondary)."""
import sensitivity_secondary as s


def test_secondary_12_month_floor():
    a = s.secondary_stats(12, True)
    assert (a["request"], a["ceiling"], a["both"], a["records"], a["pairs"]) == (9, 49, 5, 53, 58)
    e = s.secondary_stats(12, False)
    assert (e["records"], e["pairs"]) == (9, 9)


def test_secondary_60_month_floor():
    a = s.secondary_stats(60, True)
    assert (a["records"], a["pairs"], a["ceiling"], a["request"]) == (100, 122, 100, 22)
    e = s.secondary_stats(60, False)
    assert (e["records"], e["pairs"]) == (22, 22)


def test_strict_endpoint():
    b = s.baseline(strict=True)
    assert (b["viol"], b["records"], b["c3_pairs"]) == (86, 83, 41)
    assert s.baseline()["c3_pairs"] == 49


def test_delta_3():
    b = s.baseline(delta=3)
    assert (b["viol"], b["records"], b["no_req"], b["sem2"]) == (94, 89, 39, 0)


def test_permit_labels():
    p = s.permit_labels()
    assert (p["secondary"], p["distinct"], p["reused"], p["multi_expiry"]) == (100, 17, 17, 17)
    assert p["same_expiry"] == []


def test_baseline_and_table2():
    b = s.baseline()
    assert (b["viol"], b["records"], b["xb"], b["spe"]) == (95, 90, 37, 53)
    assert (b["req_only"], b["ceil_only"], b["both"], b["no_req"]) == (41, 44, 5, 39)
    assert (b["inv"], b["inv_request"], b["inv_ceiling"], b["sem2"]) == (138, 52, 86, 0)
    got = [(f, c, s.baseline(floor=f, ceiling_applies=c)) for f in (120, 72, 36) for c in (True, False)]
    assert [(g["records"], g["viol"]) for _, _, g in got] == [
        (90, 95), (46, 46), (78, 83), (34, 34), (61, 66), (17, 17)]


def test_module_constants_restored():
    import trf_checker as t
    s.baseline(floor=36, delta=3)
    assert (t.FLOOR_XBORDER, t.FLOOR_SPE, t.DELTA) == (120, 12, 1)
