# How to run the artefact

Python 3.8 or later. The checker and the Norwegian modules use the standard
library only. Streamlit is needed for the app and nothing else.

```bash
git clone https://github.com/Astheno-sphere/TRF
cd TRF
```

## 1. The thesis result

```bash
python3 trf_checker.py
```

Diff it against the recorded run. Any difference means the file changed:

```bash
python3 trf_checker.py | diff - docs/expected_trf_output.txt && echo "identical"
```

What to look for:

| Measure | Value |
|---|---|
| Semantics I, records with at least one violation | 90 / 200 |
| Semantics I, total violations | 95 |
| Corollary 1.2 witnesses, no erasure request | 39 |
| Records invalidated | 138 (52 GDPR Art 17(1), 86 EHDS Art 68(12)) |
| Semantics II, total violations | 0 |
| Reference commitment, record 100 | `11087780fd192c8f…` |

The extended erasure response period of Chapter 5 §5.5a:

```bash
python3 trf_checker.py --delta-witness
```

## 2. Payload independence

```bash
python3 synthea_layer.py
```

It reads `synthea_run/output/fhir/` if the full cohort has been regenerated,
and otherwise the eight bundles committed at `data/synthea_subset/`. Expect six
identical measures, 200 of 200 commitments differing, and a mean payload of 891
bytes for the eight-bundle subset or 1,006 for the full cohort.

## 3. Norwegian context modules

Illustrative and parallel to the thesis. They import `trf_checker.py`
unmodified and change nothing it reports.

```bash
python3 norwegian_layer.py
```

Three record classes, 160 records: NO-XB at a 120-month floor, NO-SPE at the
EHDS Art 73(1)(e) floor of 12 months with the Art 68(12) ceiling, and
NO-JOURNAL under pasientjournalloven § 25, which sets a purpose-based period
with no fixed term. Expect 68 records carrying 72 Semantics I violations, 95
invalidations, and zero Semantics II violations, followed by one walkthrough per
class showing the collision and the auditor's view after invalidation.

```bash
python3 cross_sector_check.py
```

The politiregisterloven § 17 instance, floor 12 and ceiling 36. Expect 7 records
with Semantics I violations and, of those, none without an erasure request. That
zero is the point: § 17 fixes both limbs from the same origin, so it bounds a
retention window rather than contradicting itself. Collisions appear only when
the ceiling is anchored to an external event, as EHDS Art 68(12) anchors it to
permit expiry.

## 4. The app

```bash
pip install -r requirements.txt
streamlit run app.py
```

Four tabs: the thesis run, exploration that is explicitly not a thesis claim,
the payload-independence comparison, and the Norwegian context. The app is a
viewer over the modules and is never a source of results. The deployed copy is
at <https://trfhimolde.streamlit.app/>.

## If a number differs

Stop and find out why before reporting anything. The seed is fixed at 20260915
in the module header, the checker is deterministic, and `docs/expected_trf_output.txt`
records what it produced. A changed figure means a changed file, not a changed
result.

## Scope

Nothing in the Norwegian modules is empirical. No Norwegian permit-duration
statistics were used and no Norwegian patient data exists anywhere in this
repository. Synthea ships no Norwegian module; its export is US Core with United
States demographics. The payload-independence result in step 2 is the reason
that does not affect any figure the thesis reports.
