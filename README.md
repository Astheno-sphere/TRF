# TRF — Tri-Lateral Retention Feasibility Model

Executable artefact for the MSc thesis *Verifiable Crypto-Erasure for Cross-Border Health Data Audit Trails under the European Health Data Space* (Arshad Akhtar Abbasia, Høgskolen i Molde, 2026). Supervisor: Prof. João Ferreira.

Python 3, standard library only for the checker and the Norwegian modules. No packages needed to reproduce the thesis result.

## Reproduce the thesis result

```bash
python3 trf_checker.py
```

Expected output, which must match `docs/expected_trf_output.txt` byte for byte:

| Measure | Value |
|---|---|
| Semantics I, records with at least one violation | 90 / 200 |
| Semantics I, total violations | 95 |
| Corollary 1.2 witnesses, no erasure request | 39 |
| Records invalidated | 138 (52 under GDPR Art 17(1), 86 under EHDS Art 68(12)) |
| Semantics II, total violations | 0 |
| Reference commitment, record 100 | `11087780fd192c8f…` |

Seed 20260915 is fixed in the module header. If a number differs, the file has changed.

Extended erasure response period, Chapter 5 §5.5a:

```bash
python3 trf_checker.py --delta-witness
```

Reproduces Table 5.2a: 90 records and 95 violations at δ = 1, against 89 and 94 at δ = 3, with 39 Corollary 1.2 witnesses and zero Semantics II violations at both. The infeasibility is structural, not a consequence of the one-month response period.

Every recorded run lives in `docs/`, one file per command, for diffing:

| Command | Recorded output |
|---|---|
| `python3 trf_checker.py` | `docs/expected_trf_output.txt` |
| `python3 trf_checker.py --delta-witness` | `docs/expected_delta_witness_output.txt` |
| `python3 synthea_layer.py` | `docs/expected_synthea_subset_output.txt` |
| `python3 norwegian_layer.py` | `docs/expected_norwegian_output.txt` |
| `python3 cross_sector_check.py` | `docs/expected_cross_sector_output.txt` |

## Payload independence

```bash
python3 synthea_layer.py
```

It reads `synthea_run/output/fhir/` if you have regenerated the full cohort, and otherwise falls back to the eight bundles in `data/synthea_subset/`.

Every reported figure is identical to the constructed-payload run while all 200 commitments differ. Mean payload rises from 43 bytes to 891 with this 8-bundle subset, and to 1,006 with the full 98-bundle cohort (that run was recorded on 28 September, before the constructed payloads were revised, and shows 35 bytes on the constructed side). The model reads timing and accessibility, never payload content.

## Norwegian context modules

Parallel to the thesis result. They import `trf_checker.py` unmodified and change nothing it reports.

```bash
python3 norwegian_layer.py       # NO-XB, NO-SPE, NO-JOURNAL classes with case walkthroughs
python3 cross_sector_check.py    # politiregisterloven § 17: floor 12 months, ceiling 36
```

The same two modules drive Tab 4 of the app. See `norwegian_docs/NORWEGIAN_MODULE_README.md` for what is varied, what is not, and the limits, and `norwegian_docs/HOW_TO_RUN.md` for a step-by-step guide and a demonstration script.

All Python files sit at the repository root, because Streamlit Cloud runs `app.py` from there and imports its neighbours.

## Contents

| Path | What it is | Lines |
|---|---|---|
| `trf_checker.py` | Feasibility checker: executable witness for Propositions 1 and 2, with an independently written exhaustive cross-check and an audit-log integrity check (Merkle log, tamper test) | 533 |
| `synthea_layer.py` | Realism layer and payload-provenance comparison | 152 |
| `app.py` | Streamlit viewer over the artefact, never a source of results. Tab 1 the thesis run, Tab 2 exploration, Tab 3 payload independence, Tab 4 Norwegian context, Tab 5 robustness and cross-checks | 530 |
| `norwegian_layer.py` | Three Norwegian record classes | 135 |
| `cross_sector_check.py` | Cross-sector instance from Norwegian police register law | 110 |
| `data/synthea_subset/` | 8 untrimmed Synthea FHIR R4 bundles, seed 20260915 | 8 files |
| `docs/Appendix_A.md` | Appendix A: provenance, commands, full source listings, console output | — |
| `docs/expected_trf_output.txt` | The recorded checker run, to diff against | — |
| `docs/expected_delta_witness_output.txt` | Recorded δ = 1 against δ = 3 run, Chapter 5 §5.5a | — |
| `docs/expected_synthea_subset_output.txt` | Recorded realism-layer run against the committed subset | — |
| `docs/expected_norwegian_output.txt` | Recorded Norwegian-layer run | — |
| `docs/expected_cross_sector_output.txt` | Recorded politiregisterloven § 17 run | — |
| `docs/Data_Provenance_Statement.md` | Where the synthetic data came from, and how to check it yourself | — |

## Regenerating the full cohort

```bash
java -jar synthea.jar -s 20260915 -cs 20260915 -p 100 \
  --exporter.fhir.export=true --exporter.hospital.fhir.export=false \
  --exporter.practitioner.fhir.export=false --generate.only_alive_patients=true
```

Yields 98 usable bundles from 100 requested. Synthea's default export is US Core with United States demographics, not Norwegian basisprofiler. The FHIR version, R4, matches the version the Norwegian profiles constrain. No claim of Norwegian clinical representativeness is made, and the payload-independence result is why that does not affect any figure.

## Robustness

Tab 5 of the app runs two checks the thesis reports and the other tabs do not show.

The **exhaustive cross-check** enumerates all 2¹⁴ assignments of the accessibility variable over a fourteen-month horizon using `brute_force_semantics_I()`, which is written independently of `check_semantics_I()`. Agreement between two separate implementations is worth more than confidence in either. The control case, where neither the erasure right nor the ceiling is active, returns feasible, so the search can succeed when it should.

The **δ witness** re-runs the population at δ = 1 and δ = 3, the extension Article 12(3) GDPR allows for complex requests, and shows the infeasibility surviving the longer period.

## What this artefact does not do

It does not connect to any National Contact Point, implement the OpenNCP transmission flow, evaluate consent policies, or implement any zero-knowledge proof system. Key destruction is simulated by removing a reference in program state: it demonstrates the mechanism's logic and says nothing about whether destruction can be assured in deployment.

## Data

All data is synthetic, generated by Synthea. No real patient data was requested, obtained or processed at any point.

## Licence

Add one before making the repository public. MIT for the code and CC BY 4.0 for the documents is the usual pairing for an artefact of this kind.

## Revision of 3 October 2026

Made in answer to the supervisor's review of 30 September. No reported figure changes: Semantics I
90/200 records and 95 violations, 39 Corollary 1.2 witnesses, 138 invalidations, Semantics II 0.

- Metadata is split into accessor fields (who accessed, when, under which permit or basis) and
  subject fields (the patient pseudonym). A Secure Processing Environment record now names a
  researcher and a permit, not a clinician and a contact point, and its subject link is removed at
  the deletion ceiling with a logged entry.
- Payloads are modelled per record class: the ITI-55 demographic query for cross-border records,
  the logged activity for SPE records. The constructed mean payload is therefore 43 bytes.
- At invalidation the key, the salt and the payload ciphertext all go.
- `V_II` checks each record against an append-only Merkle log (RFC 6962 hashing) instead of only
  checking that fields exist. The run prints two tamper tests under which `V_II` fails.
- The dead `os.urandom(16) if False` branch is replaced by `make_salt()`; run with
  `--random-salts` to draw salts from `os.urandom`. Results are the same.

