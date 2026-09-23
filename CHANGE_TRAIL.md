# Change trail

Every change to a canonical file, with the chapters it affects. Newest session first.
Columns: ID · file · section · chapters affected · change · reason and source · inspector verdict.
A REJECT is acceptable only when every *lost* item is the intended removal; each is listed.

## Session 22 September 2026, pass 8 — Datatilsynet enquiry finalised for a single sender

| ID | File | Affects | Change | Reason | Status |
|---|---|---|---|---|---|
| P8-01 | Datatilsynet_Enquiry_DRAFT.md | none (not thesis text) | Rewritten from "we" to "jeg"/"I" throughout; supervisor's signature line removed; institution, programme, supervisor's name and institutional email carried in the body instead, so the enquiry still shows its provenance | Tiger's decision, 22 Sept: send from the author alone | Ready to send. Prof. Ferreira to be informed before it goes, not after |
| P8-03 | Datatilsynet_Enquiry_DRAFT.md | none (not thesis text) | Short version added at the top and marked "send this one": provisions quoted inline, two numbered questions, stated submission date, explicit permission to answer informally or to say the point is unsettled. Long version kept below for the record | Tiger's request for a version more likely to be answered. Nothing overstated: no invented urgency, no flattery, same two questions | Ready to send |
| P8-02 | same | Ch7 §7.4 (pending) | Note added: once sent, §7.4 changes from "decidable by asking" to a record that the enquiry was made, by whom and on what date. Not written yet, because it is not true yet | Trail rule: nothing reported as done before it is done | Waiting on the send date |

No chapter changed in this pass. Checker untouched.

## Session 22 September 2026, pass 8 — repository fix, Norwegian tab, Appendix A aligned to the repo

Context: the first upload to github.com/Astheno-sphere/TRF landed `trf_checker.py` (363 lines, correct), `app.py`, `synthea_layer.py` and a placeholder README. The data subset, the Norwegian modules and the docs did not land, so Tab 3 was still broken. Verified by fetching the repository.

| ID | File | Affects | Change | Reason | Verification |
|---|---|---|---|---|---|
| P8-01 | demo_app/synthea_layer.py (+ repro_package/src, code_artefacts copies) | code, App A §A.9 | Bundle directory resolved from a search list: the regenerated cohort first, then `data/synthea_subset/`, then `./synthea_subset/`. Error message lists all three | The repo ships the 8-bundle subset, not a `synthea_run` tree, so Tab 3 could never find bundles | Ran from the new path: 8 bundles, mean 891 bytes, all six measures identical, 200/200 commitments differ. 132 → 152 lines. Three copies identical |
| P8-02 | demo_app/app.py | app only, no thesis text | New Tab 4, Norwegian context: the three classes with their floors and sources, a per-class results table, one case walkthrough per class, and the politiregisterloven cross-sector run with its no-structural-collision finding. Footer updated | Tiger's request for a plug-and-play exploring scenario in the app | Parses; tab logic smoke-tested outside Streamlit (160 records, 68 Sem I, 0 Sem II; cross-sector 7 violations, 0 structural). 275 → 404 lines |
| P8-03 | code_artefacts/README_Appendix_A.md | App A §A.1b, §A.2 note, §A.3, §A.5 | Contents table now lists `data/synthea_subset/` (8 untrimmed bundles) and the two Norwegian modules instead of three trimmed bundles; synthea_layer line count 132 → 152; §A.3 records the fallback path; §A.5 replaces the trimming note with the 891 vs 1,006 byte comparison | The appendix described files the repository does not contain | REJECT, intended: lost 132 and the two 25s, gained the new counts. §A.9 listing re-synced and verified identical to the file |
| P8-04 | 10_GitHub_Push/ | delivery | Rebuilt flat: every Python file at the root, because Streamlit Cloud runs `app.py` from there. README and push instructions rewritten for that layout; CHECKSUMS.md carries md5 and line counts | First upload showed the folder layout was not used | — |
| A-13 | Submission, bibliography | all | Rebuilt | — | Appendix A present verbatim; checker byte-identical |

The app's Tab 4 is explicitly labelled illustrative and not a thesis claim, in the tab text and in the footer.

## Session 22 September 2026, pass 7 — D7.2 read in full; Datatilsynet enquiry drafted

Source: TEHDAS2 D7.2, final version accepted 24 March 2026, DOI 10.5281/zenodo.20269109. Four findings bear on the thesis; all four are now in the text or acted on.

| ID | File | Section | Affects | Change | Source passage | Inspector |
|---|---|---|---|---|---|---|
| P7-01 | Chapter2 | §2.6 | Ch2 | D7.2 treats archival of pseudonymised data in an SPE as subject to Art 68(12), time-limited to permit validity and not open-ended: the obligation applied by location to data sitting in the environment, though to the permitted dataset rather than the logs. Also records that D7.2 expressly excludes the Digital Omnibus proposal of 19 Nov 2025 as undetermined, and that this thesis takes the same course | D7.2 §4.3 finalisation phase; §2.1 scope note | REJECT, gains only |
| P7-03 | Chapter4 | §4.9 | Ch4 | New paragraph: D7.2 holds that an unsalted hash of direct identifiers does not qualify as pseudonymisation, and requires the salt to be kept separate and secure as part of the pseudonymisation secrets. These are the same two requirements §4.8 places on the commitment and its salt. D7.2 also holds that irreversible pseudonymisation does not automatically meet the Recital 26 anonymisation threshold, which is this section's own conclusion by another route | D7.2 §4.4; §4.4 closing | REJECT, gains only |
| P7-04 | Chapter4 | §4.6 | Ch4 | D7.2's archival provision added as further evidence on the location reading, with its limit stated | D7.2 §4.3 | gains |
| P7-02, P7-05 | Chapter2, Chapter4 | References | Ch2, Ch4, bibliography | TEHDAS2 (2026c) added | — | reference list |
| P7-06 | Datatilsynet_Enquiry_DRAFT.md | new | — | Enquiry drafted in Norwegian and English: Q1 on accountability-preserving verifiability, Q2 on whether Art 68(12) reaches health data in the environment's own logs. States it is not an Art 36 prior consultation, sets expectations that any answer is an administrative view, and tabulates what changes in the thesis for each outcome | Ch6 §6.2, Ch7 §7.4 | not thesis text; needs João's approval before sending |
| A-11 | Submission, bibliography | all | all | Rebuilt | 73 entries, 51 with DOI/URL; all bodies present; 177 equations; both figures embedded; checker byte-identical | verified |
| A-12 | 07_Highlighted/PASS7_* | new | — | Highlighted copies of the two changed chapters plus combined HTML | — | not canonical |

Still unread: D7.1. Its deletion-at-closure content is partly visible through D7.2's citation of it on archival, and the thesis no longer attributes that claim to it.

## Session 22 September 2026, pass 6 — Rak, D6.3 final, two figures

| ID | File | Section | Affects | Change | Verified against | Inspector |
|---|---|---|---|---|---|---|
| P6-01 | Chapter1, Chapter2, Chapter4, Chapter6 | References and all in-text cites | Ch1, Ch2, Ch4, Ch6, bibliography | D6.3 cited as the final version: TEHDAS2 (2026a), DOI 10.5281/zenodo.20199187. D7.4 becomes TEHDAS2 (2026b). All six in-text citations renumbered | Zenodo record 20199187 and tehdas.eu results pages; the 2025 text was the draft that went to public consultation Oct–Nov 2025 | REJECT, intended: lost "TEHDAS2, 2025" and "TEHDAS2, 2026" throughout, gained 2026a and 2026b |
| P6-02 | Chapter2 | §2.3 | Ch2, bibliography | Rak (2024) cited: the Regulation is ambiguously drafted and its definition of electronic health data is singled out, which is the term on which the reach of Art 68(12) turns | EJRR 15(4), 928–938, DOI 10.1017/err.2024.67 | gains |
| P6-03 | Chapter4 | §4.6 | Ch4, bibliography | Rak (2024) added to the interpretive block: the peer-reviewed literature independently expects this ambiguity, which is a reason to put the question to a supervisory authority rather than settle it by argument | Same | gains |
| P6-04 | figures/figure1_regulatory_timeline.(svg\|png) + Chapter6 §6.8 | §6.8 | Ch6 | Figure 1, the implementation window: in force 26 Mar 2025, general application and Art 73(5) acts 26 Mar 2027, Chapter IV and Group One 26 Mar 2029, Group Two 2031, with the submission date marked | Regulation (EU) 2025/327 Arts 73(5), 105 | gains (figure reference) |
| P6-05 | figures/figure2_record_states.(svg\|png) + Chapter4 §4.8 | §4.8 | Ch4 | Figure 2, the three record states: LIVE, INVALIDATED (key and salt destroyed, commitment surviving, entry logged), TERMINAL at floor expiry | Ch4 §§4.7–4.9 as written | gains |
| A-10 | Submission, bibliography | all | all | Rebuilt | 72 entries, 50 with DOI/URL; 177 equations; both figures embed as PNG in the Word conversion (SVG needs rsvg-convert, which the build box lacks, so PNG is the referenced form and SVG ships as the source) | verified |

Checker byte-identical after the pass.

## Session 22 September 2026, pass 5 — adopted after verification (items 1, 2, 5)

Provenance note. These chapter edits were produced by an interrupted run earlier in the session and were found in the working copies without trail rows, while the delivered folder still held the clean pass-3 state. Tiger confirmed the run was his. Every addition was therefore verified against its source before being adopted, and each file was then gated through the inspector against the delivered pass-3 baseline. Nothing was adopted on the strength of it already being there.

| ID | File | Section | Affects | Change | Verified against | Inspector |
|---|---|---|---|---|---|---|
| P5-01 | Chapter6_Discussion_v1.md | §6.9 | Ch6, bibliography | MiFID II guess replaced by the politiregisterloven instance and the origin-anchoring finding: floor at 12 months, ceiling at 36, both from one origin, so no structural collision; the EHDS pair collides because Art 68(12) anchors its ceiling to permit expiry. Claim restated as "conflict when their origins differ" | Lovdata LOV-2010-05-28-16 § 17, §§ 50–51; the pass-4 run (0 of 60 structural, 7 erasure-driven) | REJECT, intended: lost hedge "candidate" with the removed MiFID guess, which a verified instance replaces |
| P5-02 | Chapter7_Conclusion_v1.md | §7.5 | Ch7, bibliography | Generalisation paragraph rewritten to the sharper question: which sectors anchor floor and ceiling differently, and whether a record-level ceiling can be discharged at all | Same | REJECT, intended: "is not obviously specific" → "is not specific", justified by the instance; lost "or that it does not" with the superseded sentence |
| P5-03 | Chapter2, Chapter3, Chapter4, Chapter5 | §2.1, §3.1, §4.1, §5.1 | Ch2–Ch5 | Opening hooks applied from `Opening_Hooks_Proposals.md`: the renumbering (Arts 46 and 50 → 68 and 73), the abandoned draft (28 citations, ~14 unverifiable), the supervisory-authority example, and record 100 | Each hook restates a claim already sourced in the thesis | gains only |
| P5-04 | Chapter2, Chapter4 | References | Ch2, Ch4, bibliography | Finck (2019): Study PE 634.445 added, and DOI 10.2861/535 | Publications Office record: ISBN 978-92-846-5044-6, DOI 10.2861/535, PE 634.445, July 2019 | reference list |
| P5-05 | Chapter2 | References | Ch2, bibliography | Staffa et al. (2018) DOI 10.1007/978-3-319-95189-8_2 | Springer chapter record, CCIS 821, pp. 11–27 | reference list |
| P5-06 | Chapter2, Chapter4 | References | Ch2, Ch4, bibliography | Scope et al. JDI (2022): pages 149–168 and DOI 10.26421/JDI3.1-4 | Rinton Press issue and NSF-PAR record | reference list |
| P5-07 | — | — | verification register | Scope & Rasin patent: no DOI exists for a US patent; the USPTO number 12,425,209 is the identifier. Item closed as not applicable | — | — |
| A-08 | Submission, bibliography (.md, .Rmd) | all | all | Rebuilt | 71 entries, 48 with DOI/URL (up from 70 and 44); all bodies present verbatim; 177 equations; checker byte-identical | verified |
| A-09 | 07_Highlighted/PASS5_* | new | — | Highlighted copies of the six changed files plus combined HTML, 14 marked blocks | — | not canonical |

Still open from the same request: D7.2 and D7.1 unread; the two figures not built; Zenodo DOI needs Tiger's account. Rak (2024) verified as EJRR 15(4), 928–938, DOI 10.1017/err.2024.67, and not yet cited: it argues the EHDS definition of "electronic health data" is drafted ambiguously, which is peer-reviewed support for the §4.6 hinge and should go in next.

## Session 22 September 2026, pass 4 — Norwegian context module (parallel, not in the thesis)

Canonical checker untouched and verified byte-identical afterwards. Both modules import `trf_checker.py` unmodified; no chapter changed in this pass.

| ID | File | Affects | Change | Reason / source | Verification |
|---|---|---|---|---|---|
| NO-01 | norwegian_module/norwegian_layer.py | none (parallel) | Three Norwegian record classes: NO-XB (F=120, Bodo/Stjordal inbound from PT/CZ/FI), NO-SPE (F=12, ceiling 6, Helsedataservice permit, NORTRE node or controller server), NO-JOURNAL (indefinite floor) | Tiger's request for a demo in Norwegian context; floors from eHDSI baseline, Art 73(1)(e), Art 68(12), pasientjournalloven s 25 | Runs; 160 records, 68 infeasible under Sem I, 0 under Sem II |
| NO-02 | same | none | NO-JOURNAL floor left INDEFINITE rather than numeric, truncated at 600 months for computation and labelled as such | Norwegian law sets no fixed period: journalforskriften s 14 and pasientjournalloven s 25 are purpose-based, and the government consultation paper states the ten-year figure is indicative only and as a rule cannot be applied | No number invented |
| NO-03 | norwegian_module/cross_sector_check.py | none | Cross-sector instance: politiregisterloven s 17, floor 12 months and ceiling 36 months on the same log, with ss 50-51 subject rights | Chapter 6 s 6.9 flags generalisation as uninvestigated | Verified at Lovdata (LOV-2010-05-28-16 s 17; FOR-2013-09-20-1097 ch. 40) |
| NO-04 | same | **candidate for Ch6 s 6.9, Ch7 s 7.5** | FINDING, contrary to expectation: the police provision produces NO structural collision. Floor and ceiling run from the same origin (t_a + 12, t_a + 36), defining a bounded window; only erasure requests inside it collide. The EHDS pair collides because Art 68(12) anchors its ceiling to an external event, permit expiry, which can precede the floor | Executed, not assumed | 0 of 60 structural, 7 of 60 erasure-driven |
| NO-05 | norwegian_module/NORWEGIAN_MODULE_README.md | none | Module documentation: what varies, what does not, run outputs, limits, sources | Demo for João | — |
| NO-06 | 08_Norwegian_Module/ | delivery | Modules plus captured run outputs | — | Canonical `trf_checker.py` byte-identical to the recorded run after the pass |

Correction made during the pass: my first version of the cross-sector module asserted a structural collision and crashed selecting a witness for one that does not exist. Both the code and its framing were rewritten around the actual result.

Stated limits carried with the module: illustrative not empirical; no Norwegian patient data, since Synthea has no Norwegian module; the police ceiling attaches to the whole record rather than a payload, so whether the mechanism transfers is unanswered.

## Session 22 September 2026, pass 3 — Article 68(12) primary text, D7.4 full text, case-law currency

Sources read this pass: TEHDAS2 D7.4 in full (24 Feb 2026, DOI 10.5281/zenodo.20266473) — requirements EHDSR-8 (all SPE logs kept at least one year), OPR-6 (electronic health data deleted **or rendered unrecoverable** within six months of permit expiry, backups included, subject to applicable legal obligations and traceability), §5.5 (termination and deletion balanced against logging and auditability), SPER-8 and OPR-17 (logging proportionate, no unnecessary user-behaviour detail). Article 68(12) primary text. CJEU, *EDPS v SRB*, C-413/23 P, 4 September 2025.

**The correction that drove the pass.** Six places quoted Article 68(12) as governing "the data within the secure processing environment". The text reads "the electronic health data within the secure processing environment". The broad reading survives on the location framing, but its object is electronic health data, so Corollary 1.2 is now stated for log records that carry such data, not for access logs at large. The division this forces — Art 73(1)(e) over the metadata, Art 68(12) over the health-data payload — coincides with the model's own decomposition, which strengthens §4.6 rather than weakening it.

| ID | File | Section | Affects | Change | Reason / source | Inspector |
|---|---|---|---|---|---|---|
| T-01 | Front_Matter_v1.md | Abstract | Front | Corollary 1.2 result scoped to log records carrying electronic health data | Art 68(12) text | ADMIT (with T-34) |
| T-02 | Chapter1 | §1.1 hook | Ch1 | Hook's second provision restated with the correct object | Art 68(12) text | ADMIT |
| T-03 | Chapter1 | §1.1 | Ch1 | Provision quoted verbatim; reading restated as location-based over electronic health data | Art 68(12) text | ADMIT |
| T-04, T-05 | Chapter1 | §1.2 | Ch1 | "personal data" → "electronic health data"; the emptying sentence scoped to log content | Art 68(12) text | ADMIT |
| T-06 | Chapter2 | §2.3 | Ch2 | Same correction, with the counter-argument (a bare log identifies the health data user, not the patient) stated | Art 68(12) text | REJECT, gains only |
| T-07, T-07b | Chapter2 | §2.6 | Ch2 | "Neither connects that deletion obligation …" replaced: D7.4 states both obligations and defers to legal exceptions without a mechanism; its "rendered unrecoverable" wording and its logging-minimisation caution recorded as support. Misattributed guideline name corrected to D6.3 | D7.4 read in full | REJECT: lost the sentence "has not addressed their interaction" and one Art 73(1)(e) reference — both the overclaim being removed |
| T-08 | Chapter2 | §2.9 | Ch2 | Absence claim narrowed to absence of a resolution, not of awareness | D7.4 | gains |
| T-09, T-10 | Chapter4 | §4.4 C3, §4.6 | Ch4 | Constraint C3 and Corollary 1.2 restated over electronic health data | Art 68(12) text | gains |
| T-11 | Chapter4 | §4.6 | Ch4 | Interpretive block rewritten: verbatim provision, the two features of its wording, the narrower claim, and the mapping of the two provisions onto m(a) and p(a) | Art 68(12) text | gains (+2 native equations) |
| T-12 | Chapter4 | §4.6 | Ch4 | D7.4's handling added as evidence of practice, consistent with either reading | D7.4 | gains |
| T-13 | Chapter4 | §4.9 | Ch4 | New paragraph: *EDPS v SRB* relative test (asymmetric, modest consequence) and D7.4's "deleted or rendered unrecoverable" | CJEU C-413/23 P; D7.4 | gains |
| T-14 | Chapter4 | §4.11 | Ch4 | D7.4's permissive deletion wording noted at the integration analysis | D7.4 | gains |
| T-15 | Chapter4 | References | Ch4, bibliography | CJEU judgment added (ECLI:EU:C:2025:645) | For T-13 | reference list |
| T-16, T-17, T-18 | Chapter5 | §5.2, §5.4 | Ch5 | SPE record class described as payload = health-data content, metadata = identifiable element; witnesses scoped | Art 68(12) text | gains |
| T-19, T-20, T-21 | Chapter6 | §6.1, §6.4 | Ch6 | Headline claim and the access-control rebuttal restated over electronic health data; scope of the claim stated | Art 68(12) text | gains |
| T-22 | Chapter6 | §6.8 | Ch6 | TEHDAS2 implication rewritten: both obligations stated, modes of discharge accepted, the health-data-in-logs case left unspecified | D7.4 | gains |
| T-23, T-24 | Chapter7 | §7.4 | Ch7 | Second authority question restated with the correct text and narrower scope; the Datatilsynet question reworded to match | Art 68(12) text | ADMIT |
| T-25, T-26 | Appendix_C | §C.5 Q7, §C.6 R3 | App C | Interview question and questionnaire item quote the provision correctly and ask about health-data content of logs | Art 68(12) text | ADMIT |
| T-27 to T-35 | Appendix_B, Chapter2, Front_Matter | App B, §2.1.1, §2.1.4, §2.1.7, §2.9, TOC | App B, Ch2, Front | Round 6 logged (7 queries, including the ITI-55 retrieval used in pass 2); 63 → 70 queries; five → six rounds; round purpose recorded | Queries run must be in the log | REJECT, intended: 63 → 70 |
| A-06 | Submission, bibliography (.md, .Rmd) | all | all | Rebuilt | 70 entries, 44 with DOI/URL; all bodies present verbatim; 177 native equations (up 2 from the new m(a)/p(a) spans in §4.6), no LaTeX leak; checker byte-identical | verified |
| A-07 | 07_Highlighted/ | new | — | Highlighted copies of the nine changed files plus one combined HTML; 35 marked spans, one per edit | Tiger's visual check | not canonical |

Cross-verification against the pass-2 state: Front 2 hunks, Ch1 3, Ch2 10, Ch4 7, Ch5 2, Ch6 4, Ch7 2, App B 1, App C 2. Every hunk carries an ID; the misquote now appears nowhere in the assembly (0 occurrences), and "electronic health data within the secure processing environment" appears 6 times. Ch3, Appendix A and the code are untouched in this pass.

## Session 22 September 2026, pass 2 — attack-and-strengthen (A1–A5)

Source fetched for A1: IHE ITI Technical Framework Vol. 2, rev. 20.1 (12 Dec 2024), §3.55 [ITI-55]: §3.55.4.1.2.1 (required query elements name and birth time; optional address, telecom, mother's maiden name) and §3.55.5.1.1 (audit message must carry ParticipantObjectQuery = QueryByParameter segment, base64-encoded).
Design decision A3 approved by Tiger before the pass.

| ID | File | Section | Affects | Change | Reason / source | Inspector |
|---|---|---|---|---|---|---|
| C-01a/b | Chapter1_Introduction_v2.md | §1.1, References | Ch1, bibliography | IHE International (2024) → (2024a) | Same author and year as the new ITI-55 source | REJECT, intended: label only |
| C-01c/d/e | Chapter2_LitReview_v2_FINAL.md | §2.3, References | Ch2, bibliography | (2024) → (2024a); IHE International (2024b) ITI-55 added | Same. An insertion bug of mine fused the two entries on one line; caught on read-back and repaired; ATNA entry verified identical except its label | REJECT, intended |
| A1-a | Chapter2 | §2.3 | Ch2 | New sentences: an audit record is not the clinical document; ITI-55 audit carries the encoded demographic query | A1 | (in the Ch2 reject above; gains only) |
| A1-b | Chapter4_TRF_Model_v1.md | §4.2 | Ch4 | Medication-list example replaced: what ATNA actually holds, and why accountability does not need the typed demographics | A1: previous example was inaccurate | REJECT, intended |
| A2-a | Chapter4 | §4.2 | Ch4 | New paragraph: the valid ground for erasure of an audit record (17(1)(b) and Art 21(1) unavailable under 6(1)(c); 17(3)(b) shields the required part; 17(1)(d) reaches the excess via 5(1)(c)); marked as carrying the same want of authority as §6.2 | A2 | gains |
| A2-b | Chapter4 | §4.6 Cor 1.1 | Ch4 | "Generic case" claim replaced by conditional statement pointing to §4.2 and §3.7 | A2: overclaim | lost "Article 17" (intended) |
| A1-c | Chapter4 | §4.3 | Ch4 | p(a) redefined as personal data beyond the accountability skeleton (encoded query; SPE activity detail); abstract, never read | A1 | gains |
| A5-a/b | Chapter4 | §4.5, §4.12 | Ch4 | Semantics I no longer "implicit in current practice"; stated as the unattributed default of whole-record retention | A5: no source existed | — |
| A4-a | Chapter4 | §4.7 | Ch4 | "Theorem 1 carries the load" replaced: both theorems immediate; contribution is the translation they make checkable | A4 | lost one "2" (intended) |
| A3-a…i | Chapter4 | §4.8, §4.9, §4.12 | Ch4 | Salt destroyed with the key at invalidation; commitment survives as unopenable chained seal; optional opening to data subject (unspecified); residue list, threat example, response, honest limit, auditor view, terminal transition, summary aligned | A3 design change | hedges "unconditionally" and one "candidate" removed with the retained-salt sentence (intended; the pseudonymisation limit is kept in "The honest limit") |
| C-01f | Chapter4 | References | Ch4, bibliography | ITI-55 entry added | A1 citation | intended |
| A1-d | Chapter5_Demonstration_v1.md | §5.2 | Ch5 | States that clinical resources are not ATNA content and why they are used | A1 | gains |
| A3-j | Chapter5 | §5.6 | Ch5 | Trajectory description: salt destroyed with the key | A3 | — |
| D-07a/b | Chapter5 | §5.2 | Ch5 | 362 → 363 lines; 275 → 276 non-blank non-comment | One code line added | intended |
| D-08a | Chapter3_Methodology_v1.md | §3.6 | Ch3 | "fifty to one hundred lines" → "constraint logic on the order of ninety lines" | Contradicted Ch5 (363 lines) | gains |
| D-08b | Chapter3 | §3.6 | Ch3 | Realism layer: "constructing metadata from encounter events" and "two to four hundred lines" corrected to what the code does (labels document category) and its size (132 lines) | Overclaim found while reading the code | gains |
| A1-e | Chapter3 | §3.6 | Ch3 | Realism layer's function restated as the invariance test only | A1 | gains |
| A3-k | Chapter3 | §3.6 | Ch3 | Simulated destruction covers key and salt | A3 | — |
| A3-l, D-07c/d, A3-m | code_artefacts/README_Appendix_A.md | §A.4, §A.1b, §A.8 | App A | Trajectory text; 362 → 363; source listing gains the salt line | A3 | intended; §A.8 listing verified identical to the file |
| A3-n | demo_app/, repro_package/src/, code_artefacts/ trf_checker.py | apply_invalidation | code | `rec.salt = None` after key destruction (1 line) | A3 | three copies identical; main output byte-identical to recorded run; δ-witness unchanged (90/95/39/0/138; 89/94/39/0/138); realism layer on 8-bundle subset identical, 200/200 commitments differ; 138 invalidated records have key and salt None, 62 live records keep both |
| A-04 | repro_package/docs/Appendix_A.md | all | repro package | Replaced with current App A | Was already stale at session start (16 Sept text) | n/a |
| A-05 | Submission, bibliography (.md, .Rmd) | all | all | Rebuilt | 69 entries (+ITI-55), 43 with DOI/URL; order otherwise unchanged; all bodies present verbatim; 175 equations, 0 LaTeX leak | verified |

Cross-verification against the folder delivered earlier today: Ch1 2 hunks (C-01a, C-01b); Ch2 2 (A1-a+C-01c; C-01d/e); Ch3 3 (D-08a; D-08b+A1-e; A3-k); Ch4 15 (A1-b, A2-a, A1-c, A5-a, A2-b, A4-a, A3-a, A3-b, A3-c, A3-d, A3-e, A3-f, A3-g, A5-b+A3-h+A3-i, C-01f); Ch5 3 (D-07a/b; A1-d; A3-j); App A 4 (A3-l, D-07c, D-07d, A3-m); code 1 line (A3-n). Front matter, Ch6, Ch7, App B, App C unchanged. Every hunk has an ID; every ID has its hunk.

## Session 22 September 2026, pass 1

| ID | File | Section | Affects | Change | Reason / source | Inspector |
|---|---|---|---|---|---|---|
| D-01 | Chapter2_LitReview_v2_FINAL.md | §2.2 | Ch2 (+ bibliography) | "designate a National Digital Health Authority by June 2025 … certify … by January 2026 (Ernst & Young, 2025)" → Art 19(1): inform Commission of digital health authorities by 26 March 2027, cited to the Regulation | Secondary source contradicted the primary text (OJ L 2025/327, Art 19(1), retrieved via EUR-Lex). Certification clause removed: no primary date verified | REJECT, intended: lost EY citation, June 2025, Jan 2026; gained Regulation citation, Art 19(1), 26 March 2027 |
| D-01b | Chapter2 | References | Ch2, bibliography | Ernst & Young (2025) entry removed | No longer cited anywhere | REJECT, intended (reference list) |
| D-02 | Chapter2 | §2.5 | Ch2 | "European Data Protection Board, 2025" → "2026b" | Phantom citation: no 2025 entry exists; Guidelines 02/2025 are 2026b (v2.0) | REJECT, intended |
| D-03a/b | Chapter4_TRF_Model_v1.md | §4.10, §4.12 | Ch4 | "Four are treated here" / "Four rival designs" → "Five" | §4.10 treats five rivals since DePaul (Rival 5) was added | ADMIT on prose; REJECT only for N-05b |
| D-04a | Chapter5_Demonstration_v1.md | §5.2 | Ch5 | 322 lines / 246 → 362 lines / 275 neither blank nor comment | `wc -l` = 362; δ-witness block added after text written | REJECT, intended: 322, 246 → 362, 275 |
| D-04b | code_artefacts/README_Appendix_A.md | §A.1b | App A | 322 → 362 | Matches §A.8 and file | REJECT, intended |
| D-05 | README_Appendix_A.md | §A.4 | App A | False claim "code states in a comment … CSPRNG" replaced by an accurate statement of the salt's reproducibility-only status | No such comment exists (line 63). Text fixed, code untouched, so checksums and outputs unchanged | (same file as D-04b) |
| D-06a/b | Appendix_C_Evaluation_Instrument.md | header, §C.8 | App C | §3.9 ↔ §3.8 cross-references swapped to correct targets | Execution status is §3.8; ethics statement is §3.9 | ADMIT |
| N-01 | Chapter2 | §2.4 | Ch2 | New paragraph: aiAuthZ (Kodathala, 2026) as convergent practice; "verifiability semantics" delta narrowed | Round 5 jeopardy check; paper read in full (arXiv HTML §1.4, §3.4) | REJECT, gains only |
| N-02 | Chapter2 | §2.9 | Ch2 | New paragraph: Borovits, Tamburri & van den Heuvel (2026) SLR as independent academic corroboration of the gap | Round 5; read §1, §3.2, §3.3.12 | REJECT, gains only |
| N-03, N-04 | Chapter2 | References | Ch2, bibliography | Borovits et al. (2026) and Kodathala (2026) added, arXiv DOIs | For N-01, N-02 | REJECT, gains only |
| N-05a/b/c | Chapter2, Chapter4, Chapter6 | References | Ch2, Ch4, Ch6, bibliography | TEHDAS2 (2026) D7.4: date 24 Feb 2026, lead author, DOI 10.5281/zenodo.20266473 | Zenodo record retrieved | REJECT, reference list only |
| N-06a–j | Chapter2, Front_Matter_v1.md, Appendix_B_Search_Log.md | §2.1.1, §2.1.4, §2.1.7, §2.9, TOC, App B | Ch2, Front, App B | Round 5 (22 Sept, 4 queries) logged; 59 → 63 queries; four → five rounds; three adversarial | Queries run this session must be in the log | REJECT, intended: 59 → 63 |
| A-01 | VERA-SNARK_Thesis_SUBMISSION.md, Consolidated_Bibliography.md | all | all | Rebuilt with assemble.py | Bibliography 67 → 68 entries (−EY, +2), 42 with DOI/URL | Verified: 175 native equations, 0 LaTeX leak; checker output byte-identical |
| H-01 | Chapter1_Introduction_v2.md | §1.1, first paragraph | Ch1 (+ assembly) | Unsourced superlative ("most significant data-governance transformation in its history") replaced by a merged Norwegian-context hook: Bodø/Stjørdal gateway live but nearly empty, then the Art 73(1)(e)/68(12) collision, conditional on one reading and on EEA incorporation | Supervisor request; Tiger chose a mix of Options A and B. Sources already in thesis: Helsedirektoratet (2026a), §1.1, §4.6 | REJECT, gains only: +(Helsedirektoratet, 2026a). Assembly diff: 1 paragraph replaced, nothing else changed; 175 equations; checker byte-identical |
| N-05d | Chapter2, Chapter4, Chapter6 | References | Ch2, Ch4, Ch6, bibliography | TEHDAS2 (2026) entry: "(2026, 24 February)" → "(2026)" with "published 24 February 2026" moved inside the bracket | Regression caught in cross-verification: the dated form sorted D7.4 (2026) before D6.3 (2025), breaking APA same-author year order | REJECT, reference list only; order restored (2025 at line 150, 2026 at 152) |
| A-02 | Consolidated_Bibliography.Rmd | all | bibliography (knit copy) | Body re-synced from the .md; YAML header kept | Was already stale at session start (19 Sept vs .md 21 Sept); now 68 = 68 entries | n/a (generated) |
| A-03 | VERA-SNARK_Thesis_SUBMISSION.md, Consolidated_Bibliography.md | all | all | Final rebuild after N-05d | Every current chapter and appendix verified present verbatim in the assembly | 175 equations; checker byte-identical |
| M-01 | HANDOFF_READ_FIRST.md | §0, §6, §8a, §9 | control | Resume step 6 (trail rule); file table (App B 63/5, bibliography 68/42, new files); completed list; open work re-prioritised | Keep handoff truthful | n/a (control file) |
| M-02 | VERSION_REGISTER.md | table, reconciled line, non-canonical list | control | Checksums recomputed after final edit; CHANGE_TRAIL and hooks rows added; stale top-level code copies listed as non-canonical | Register must match files | 0 mismatches |
| M-03 | CHANGE_TRAIL.md, Opening_Hooks_Proposals.md | new | control | Created; hooks file marks Ch1 as applied (H-01) | Tiger's trail rule; supervisor request | n/a |
| P-01 | Opening_Hooks_Proposals.md | new | Ch1–5 (proposed) | Hook drafts for approval; nothing applied | Supervisor request | n/a |

## Cross-verification, 22 September 2026

Every canonical file was diffed against the session-start archive (`files__2_.zip`). Each changed line is mapped to a trail ID; no change exists without one, and no ID exists without its change.

| File | Status | Diff hunks | Trail IDs |
|---|---|---|---|
| Front_Matter_v1.md | patched | 1 | N-06h |
| Chapter1_Introduction_v2.md | patched | 1 | H-01 |
| Chapter2_LitReview_v2_FINAL.md | patched | 14 | N-06b, N-06a, N-06c, N-06d, N-06e, N-06f, D-01, N-01, D-02, N-06g + N-02 (same paragraph), N-03, D-01b + N-04 (adjacent), N-05a/N-05d |
| Chapter3_Methodology_v1.md | unchanged | 0 | — |
| Chapter4_TRF_Model_v1.md | patched | 3 | D-03a, D-03b, N-05b/N-05d |
| Chapter5_Demonstration_v1.md | patched | 1 | D-04a |
| Chapter6_Discussion_v1.md | patched | 1 | N-05c/N-05d |
| Chapter7_Conclusion_v1.md | unchanged | 0 | — |
| Appendix A (README_Appendix_A.md) | patched | 2 | D-04b, D-05 |
| Appendix_B_Search_Log.md | patched | 2 | N-06i, N-06j |
| Appendix_C_Evaluation_Instrument.md | patched | 2 | D-06a, D-06b |
| Consolidated_Bibliography.md / .Rmd | regenerated | — | A-01, A-02, A-03 |
| VERA-SNARK_Thesis_SUBMISSION.md | regenerated | — | A-01, A-03 (every chapter verified present verbatim) |
| trf_checker.py, synthea_layer.py, app.py | unchanged | 0 | — |

Checks after the last edit: checker output byte-identical to the recorded run; 175 native Word equations, no LaTeX leakage; bibliography 68 entries, 42 with DOI/URL, APA order intact.
