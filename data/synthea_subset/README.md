# Synthea subset — eight untrimmed patient bundles

This directory holds the dataset `synthea_layer.py` reads when the full cohort
is absent. The bundles are genuine Synthea output, untrimmed and unmodified.

## How they were generated

```bash
curl -sL -o synthea.jar \
  https://github.com/synthetichealth/synthea/releases/download/master-branch-latest/synthea-with-dependencies.jar

java -jar synthea.jar \
  -s 20260915 -cs 20260915 -p 100 \
  --exporter.fhir.export=true \
  --exporter.hospital.fhir.export=false \
  --exporter.practitioner.fhir.export=false \
  --generate.only_alive_patients=true
```

The run produced 98 usable bundles totalling 314 MB. Two of the hundred
requested patients did not survive to the end of their simulated lifetime and
were therefore not exported, which is what `only_alive_patients` does. The
eight bundles here are the first eight in file order, copied without
modification. The full cohort is not committed because of its size.

## Version pin and what a regeneration reproduces

Every bundle records the generator that wrote it: `Version identifier: d9d07a6`,
i.e. Synthea commit `d9d07a6eef91ee5144293b42ab64224d84d124f8`
(https://github.com/synthetichealth/synthea/commit/d9d07a6eef91ee5144293b42ab64224d84d124f8).
`master-branch-latest` is a moving release; use that commit, or check `version.txt`
inside the jar (`unzip -p synthea.jar version.txt`) before regenerating.

Synthea's simulation is seeded, but it anchors the simulated timeline to the clock
time of the run. Regenerated on 6 October 2026 with the pinned jar, the seeds above
and reference date `-r 20260916`, the cohort had the same 98 patients except one,
the same clinical events, and timestamps shifted by a constant time-of-day offset; no
bundle was byte-identical. The thesis figures do not depend on this: re-running
`synthea_layer.py` on that regenerated cohort with the final code gives the same six
measures and 200/200 differing commitments, with a mean payload of 1,002 bytes
against 1,006 for the September cohort (`docs/expected_synthea_full_cohort_rerun_2026-10-06.txt`).

## Provenance markers, checkable by opening any file

| Marker | Value present |
|---|---|
| Identifier namespace | `synthetichealth` / `synthea` URLs |
| Synthea-specific extension | `disability-adjusted-life-years` on Patient |
| Profile conformance | `http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient` |
| Demographics | Massachusetts addresses, Synthea's default population |
| Name convention | Synthea's name-plus-numeral pattern, e.g. `Adelle43_Jalisa590_Schmitt836` |
| Bundle type | `transaction` |

These are US Core profiles, not Norwegian basisprofiler. Synthea ships no
Norwegian module. The payloads stand in for the content of an exchanged patient
summary; they are not claimed to be Norwegian records, and Chapter 5 states this.

## What this subset changes, and what it does not

Running `python3 synthea_layer.py` against these eight bundles reproduces every
reported figure of the constructed-payload run:

| Measure | Constructed | Synthea (8 bundles) |
|---|---|---|
| Semantics I, records with violation | 90 | 90 |
| Semantics I, total violations | 95 | 95 |
| Corollary 1.2 witnesses, no erasure request | 39 | 39 |
| Records invalidated | 138 | 138 |
| Semantics II, records with violation | 0 | 0 |
| Semantics II, total violations | 0 | 0 |

All 200 commitments differ between the two runs, because the salts are the same
and the payloads are not.

One figure does change with cohort size, and Chapter 5 reports both. The mean
payload is **891 bytes** across this eight-bundle subset and **1,006 bytes**
across the full 98-bundle cohort, because a different set of clinical resources
is drawn and each payload is reused roughly twenty-five times across the two
hundred records rather than twice. The six measures above are unchanged under
both, which is the stronger result: payload independence holds across cohort
size and across payload repetition frequency, not merely across one substitution.
