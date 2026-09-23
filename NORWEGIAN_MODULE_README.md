# Norwegian context module (pass 4) — plug and play, not part of the thesis

Two modules that import `trf_checker.py` **unmodified**. Nothing in the thesis changes.
`python3 trf_checker.py` still reproduces 95 violations across 90 records, 39 Corollary 1.2
witnesses, 138 invalidated, 0 under Semantics II — verified byte-identical after this pass.

```
python3 norwegian_layer.py       # Norwegian record classes + case walkthroughs
python3 cross_sector_check.py    # politiregisterloven s 17 instance
```

## What is varied, and what is not

Varied: the floor F(a), the pathway, and the arrival of erasure requests and permit expiries.
Those are what the model reads.

Not varied in any way that could change a figure: payload content. Chapter 5 proves the
results are invariant to it. The Norwegian payloads here make the demonstration legible;
they are **constructed, not real**, and they are not evidence of anything.

## The three Norwegian classes (`norwegian_layer.py`)

| Class | Floor | Ceiling | Source |
|---|---|---|---|
| NO-XB | 120 months | — | eHDSI deployment baseline, inbound patient summary at Bodo / Stjordal legevakt from PT, CZ, FI |
| NO-SPE | 12 months | 6 months after permit expiry | EHDS Art 73(1)(e); Art 68(12); Helsedataservice permit, NORTRE node or controller server |
| NO-JOURNAL | **indefinite** | — | pasientjournalloven s 25, journalforskriften s 14 |

**Why NO-JOURNAL has no number.** Norwegian law sets no fixed retention period for patient
records: they are kept until, given the character of the health care, they are no longer
assumed to be needed, and are then deleted unless archive law preserves them. A government
consultation paper states that the frequently quoted ten years is indicative only and as a
rule cannot be applied. No number was invented. The indefinite floor is truncated at 600
months for computation, and the truncation is labelled in the output.

Run of 2026-09-22 (seed 20260915), illustrative:

| class | n | Sem I records with violation | Sem I violations | invalidated | Sem II violations |
|---|---|---|---|---|---|
| NO-JOURNAL | 40 | 12 | 12 | 12 | 0 |
| NO-SPE | 60 | 36 | 40 | 60 | 0 |
| NO-XB | 60 | 20 | 20 | 23 | 0 |
| **total** | **160** | **68** | **72** | **95** | **0** |

## The cross-sector instance (`cross_sector_check.py`) — and the finding it produced

Politiregisterloven (LOV-2010-05-28-16) s 17 requires that information about use of the
system be registered and stored **for at least 1 year and deleted at the latest after 3
years**; politiregisterforskriften ch. 40 mirrors it; ss 50-51 give the registered person
rights of correction, blocking and deletion. A floor, a ceiling and a subject right on one
log, in Norwegian law, outside health.

**It produces no structural collision, and that is the useful result.** The floor ends at
t_a + 12 and the ceiling bites at t_a + 36, both measured from the same origin, so the
provision defines a bounded retention window. Only erasure requests inside the window
collide (7 of 60 in this draw).

The contrast isolates what is defective in the EHDS pair. Article 68(12) anchors its ceiling
to an **external** event, the expiry of the data permit, which can fall before the floor on a
log written late in that permit. So the thesis's claim should not be that floors and ceilings
conflict in general. It is that they conflict **when their origins differ** — and that is
worth carrying into Chapter 6 s 6.9, where the generalisation question is currently open and
rests on an uninvestigated guess about MiFID II.

## Limits, stated

- Illustrative, not empirical. No Norwegian permit-duration statistics were used; none were found.
- No Norwegian patient data exists here. Synthea has no Norwegian module, and re-labelling US
  demographics as Norwegian would be invented realism.
- The police ceiling attaches to the whole record, not to a payload inside it, so the terminal
  transition of Chapter 4 s 4.8 would have to discharge it. Whether the mechanism transfers to
  a record-level ceiling is not answered here.
- Nothing in this module has entered the thesis text. If it survives review with the supervisor,
  it becomes a Chapter 5 section and a Chapter 6 paragraph in a later pass, with trail rows.

## Sources

- Politiregisterloven s 17, ss 50-51 — lovdata.no/lov/2010-05-28-16
- Politiregisterforskriften ch. 40 — lovdata.no/dokument/SF/forskrift/2013-09-20-1097
- Pasientjournalforskriften s 14 — lovdata.no/forskrift/2000-12-21-1385
- Pasientjournalloven s 25; consultation paper on retention, regjeringen.no
