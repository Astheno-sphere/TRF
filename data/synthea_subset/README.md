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

Synthea is deterministic, so the same command under the same seeds reproduces
the same bundles on any platform.

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
