# Appendix A. Code Artefacts and Reproduction Record

*Thesis:* Verifiable Crypto-Erasure for Cross-Border Health Data Audit Trails under the European Health Data Space
*Author:* Arshad Akhtar Abbasia, MSc Sustainable Energy Logistics, Høgskolen i Molde
*Supervisor:* Prof. João Ferreira
*Artefact date:* 18 September 2026; revised 3–4 October 2026

This appendix contains every piece of code written for the thesis, the exact commands used to produce every reported result, and the provenance of all data. Nothing reported in Chapters 4 or 5 was produced by code not listed here.

---

## A.1 Availability

The artefact is publicly available in two forms.

| Form | Location |
|---|---|
| Source repository | https://github.com/Astheno-sphere/TRF |
| Live demonstration | https://trfhimolde.streamlit.app/ |

The repository is the citable artefact. It contains seven Python modules, the eight-bundle Synthea subset the realism layer reads, a recorded console run for every command, and this appendix. The live application is a convenience for readers who prefer not to clone and run: it executes the same unmodified source, and its Thesis run page asserts that the run reproduces the figures reported in Chapter 5, displaying a failure notice rather than results if it does not.

The demonstration has eight pages. *Witness a record* draws one record of the thesis population through its months, showing where Semantics I contradicts itself and where Semantics II holds, and lights the components of Figure 4.1 that act in each month. *How it is built* embeds Figures 4.1 and 5.1 as interactive diagrams. *Thesis run* reproduces Tables 5.3 and 5.6 and shows the audit-log integrity check and both tamper tests of Section 5.7. *Where the ceiling is anchored* evaluates the condition of Proposition 3 for any floor and ceiling, with Article 68(12) and politiregisterloven § 17 as presets. *Robustness and cross-checks* runs the independent exhaustive cross-check of Section 5.5, the erasure-response-period witness of Section 5.6 and the optional envelope-encryption module of Section 5.8. *Synthea realism* reproduces Table 5.7. *Norwegian context* runs the illustrative Norwegian modules, and *Explore* varies population parameters as a teaching aid; neither reports a thesis figure.

A note on durability. Hosted applications are not archival objects: the live demonstration may be withdrawn or may sleep after inactivity, and no claim in this thesis depends on its availability. Every result reported here is reproducible from the code listed below by executing a single command on any machine with Python installed, which is the form in which the artefact should be assessed.

## A.2 Contents

| File | Purpose | Lines |
|---|---|---|
| `trf_checker.py` | Feasibility checker — executable witness for Propositions 1 and 2, including the independent exhaustive cross-check and the audit-log integrity check | 533 |
| `synthea_layer.py` | Realism layer — substitutes Synthea-generated FHIR R4 payloads and compares every reported figure against the constructed-payload run | 152 |
| `norwegian_layer.py` | Three Norwegian record classes, parallel to the thesis and reporting no thesis figure | 135 |
| `cross_sector_check.py` | Cross-sector instance drawn from politiregisterloven § 17 | 110 |
| `app.py`, `ui.py` | Eight-page demonstration viewer with live architecture diagrams (Figures 4.1 and 5.1), never a source of results | 804 + 133 |
| `crypto_envelope.py` | Optional: the same lifecycle with real AES-256-GCM envelope encryption; needs the `cryptography` package and reports no thesis figure | 118 |
| `z3_check.py` | Optional: bounded SMT check of Propositions 1–3 with the Z3 solver; needs the `z3-solver` package | 153 |
| `data/synthea_subset/` | Eight untrimmed Synthea bundles from the reported cohort, so a reader can run the realism layer without regenerating it | 8 files, 40 MB |
| `docs/expected_trf_output.txt` | Recorded console run of the checker | — |
| `docs/expected_delta_witness_output.txt` | Recorded run at δ = 1 and δ = 3 | — |
| `docs/expected_synthea_subset_output.txt` | Recorded realism-layer run against the committed subset | — |
| `docs/expected_norwegian_output.txt` | Recorded Norwegian-layer run | — |
| `docs/expected_cross_sector_output.txt` | Recorded politiregisterloven § 17 run | — |
| `docs/Data_Provenance_Statement.md` | Where the synthetic data came from, the six Synthea markers a reader can check for, and the cohort-size comparison | — |
| `requirements.txt` | `streamlit>=1.50`, `cryptography>=42`; the checker itself needs nothing | 2 |
| `build_substrate_patch1.py`, `build_substrate_patch2.py` | Generators for the research-substrate patch workbooks; no thesis result depends on them | — |

Every command has a recorded run committed beside it. A reader who executes a command and diffs the result against its recorded file can distinguish a changed file from a changed result, which is the distinction that matters when a figure disagrees with the text.

Two files are *not* included and the reason is stated rather than omitted: the full 98-bundle Synthea cohort (314 MB) and the Synthea jar (197 MB). Both are regenerable from the commands in A.5, deterministically, under the seeds given. The eight-bundle subset that is included is drawn from that cohort and is sufficient to run the realism layer; Chapter 5, Section 5.8 reports the comparison at both cohort sizes and finds every figure identical.

## A.3 Environment and generation provenance

The synthetic cohort was generated by the official Synthea release jar, downloaded from the project's own GitHub releases and executed with the command in Section A.5. Generation was carried out in a Linux environment with OpenJDK 21 rather than under Windows PowerShell, which does not affect the output: Synthea is deterministic under fixed population and clinician seeds, and produces byte-identical bundles in any environment with a compatible JVM. The bundles carry Synthea's own resource-identifier namespace, its `disability-adjusted-life-years` Patient extension, US Core profile conformance and its default Massachusetts demographics, all of which are verifiable by inspecting any bundle.

## A.4 Software environment

```text
OS            Ubuntu 24.04
Python        3.x, standard library only (hashlib, random, itertools, glob, json, os)
Java          OpenJDK 21.0.10 (required for Synthea only)
Dependencies  none for the checker; openpyxl for the substrate patch generators
```

The checker has no third-party dependencies. This is deliberate: a reader should be able to run it on any machine with Python installed, without a package manager, and confirm the thesis's central results for themselves.

---

## A.5 Exact commands

*1. Run the feasibility checker (produces every figure in Chapter 5, Sections 5.3–5.7):*

```bash
python3 trf_checker.py
```

Deterministic. Seed 20260915 is set in the module header. Output is byte-identical across runs and across machines. Runtime measured at 0.019 s.

*2. Obtain Synthea (required only for the realism layer):*

```bash
curl -sL -o synthea.jar \
  https://github.com/synthetichealth/synthea/releases/download/master-branch-latest/synthea-with-dependencies.jar
```

*3. Generate the synthetic cohort:*

```bash
mkdir -p synthea_run && cd synthea_run
java -jar ../synthea.jar \
  -s 20260915 -cs 20260915 -p 100 \
  --exporter.fhir.export=true \
  --exporter.hospital.fhir.export=false \
  --exporter.practitioner.fhir.export=false \
  --generate.only_alive_patients=true
```

`-s` sets the population seed and `-cs` the clinician seed; both are fixed to the thesis seed so the cohort is reproducible. The run yields 98 usable patient bundles from 100 requested. Output lands in `synthea_run/output/fhir/`.

*4. Run the realism layer and the payload-provenance comparison (produces Table 5.7):*

```bash
python3 synthea_layer.py
```

Looks for bundles in `./synthea_run/output/fhir/` first and falls back to `./data/synthea_subset/`, so it runs against either the regenerated cohort or the subset shipped with the artefact. Reports both runs side by side and flags any divergence.

*5. Run the erasure-response-period witness (produces Table 5.5):*

```bash
python3 trf_checker.py --delta-witness
```

Re-runs the population at δ = 1 and δ = 3, the extension Article 12(3) GDPR permits for complex requests, and prints both rows for comparison.

*6. Run the Norwegian context modules (illustrative; no thesis figure depends on them):*

```bash
python3 norwegian_layer.py
python3 cross_sector_check.py
```

The first builds the NO-XB, NO-SPE and NO-JOURNAL classes and walks through one case per class. The second builds the politiregisterloven § 17 instance discussed in Chapter 6, Section 6.10.

*7. Run the demonstration viewer locally:*

```bash
pip install -r requirements.txt
streamlit run app.py
```

*8. Verify any run against its recorded output:*

```bash
python3 trf_checker.py | diff - docs/expected_trf_output.txt && echo identical
```

The same form applies to each of the five recorded runs listed in A.2. A difference means a file changed, not that the result changed.

---

## A.6 What the code does

### `trf_checker.py`

Implements the TRF Model of Chapter 4 directly. Records are the seven-element tuples of Section 4.3, with the metadata split into accessor fields and subject fields. A Secure Processing Environment record carries a researcher and a permit rather than a clinician and a contact point, and its payload stands for the logged activity; a cross-border record's payload stands for the demographic query that the IHE patient-discovery transaction puts into the audit message. Two record classes are generated: cross-border audit records with a 120-month floor, and Secure Processing Environment access-log records with a 12-month floor and the Article 68(12) ceiling. Generation parameters are listed in full in Chapter 5, Table 5.2.

Four components matter for the thesis's claims:

- `check_semantics_I()` evaluates the constraint system under plaintext verifiability, reporting for each record the first month at which C1 and C2, or C1 and C3, are simultaneously required. These are the witnesses for Proposition 1.
- `check_semantics_II()` applies the constructive trajectory from the proof of Proposition 2 (destroy the payload key and the commitment salt and delete the payload at `min(t_r + δ, t_π + 6)`; remove the subject fields of a Secure Processing Environment record at `t_π + 6`; append a grounded entry for each; retain the accessor fields and the commitment) and then verifies all three constraints, including C3 over the subject link.
- `integrity()` and the `MerkleLog` class give condition (i) of Semantics II real content. Every access event, invalidation and subject-link removal is appended to an append-only Merkle log using RFC 6962 hashing, and `V_II` checks each of a record's entries against the current root with an inclusion proof. The run includes two tamper tests, an altered accessor field and an altered invalidation ground, under which `V_II` fails, and a restore after which it holds.
- `brute_force_semantics_I()` is written independently of the first function, taking the constraint definitions directly and enumerating all 2¹⁴ assignments of the accessibility variable over a fourteen-month horizon. It exists so that the infeasibility results do not rest on the correctness of a single implementation. The control case, in which neither C2 nor C3 is active, returns feasible: confirming the search can succeed when it should.

Cryptographic operations use `hashlib` only. Commitments are salted (`SHA-256(salt ‖ payload)`) because Chapter 4, Section 4.9 establishes that an unsalted hash of a low-entropy clinical payload would itself remain personal data. By default `make_salt()` derives each salt from the record identifier so that runs reproduce exactly; `--random-salts` draws them from `os.urandom` instead and gives the same results. The derivation is for reproducibility only: a production deployment must draw each salt from a cryptographically secure random source, since a salt derivable from the record identifier offers no hiding against an adversary who knows the derivation.

Key destruction is modelled as setting the key reference to `None`, and deletion of the ciphertext as setting the payload to `None`. This demonstrates the mechanism's logic and demonstrates nothing about deployment assurance: a limitation stated in Chapter 5, Section 5.8 and treated in Chapter 6.

### `synthea_layer.py`

Replaces the constructed payload strings with real FHIR R4 resources drawn from Synthea bundles (one clinical resource per bundle, from `Condition`, `Observation`, `MedicationRequest`, `AllergyIntolerance`, `Immunization`, or `Procedure`), recomputes each commitment over the real payload, and leaves every timing quantity untouched. It then runs both populations through the same checks and prints them side by side.

The expected result, and the observed one, is that every reported figure is identical while all 200 commitments differ. Mean payload size rises from 43 bytes to 891 with the committed subset (to 1,006 with the full cohort, recorded on 28 September when the constructed payloads averaged 35 bytes; see A.17). The model reads timing and accessibility, never payload content; running the comparison rather than asserting the invariance lets a reader see the claim tested against inputs that demonstrably changed.

---

## A.7 Data provenance

All data used anywhere in this thesis is synthetic. No real patient data was requested, obtained, or processed at any point.

The cohort is generated by Synthea (Walonoski et al., 2018), an open-source synthetic patient generator. Synthea's default export conforms to the *US Core* implementation guide with United States demographic, geographic, and care-pattern parameters. The FHIR version is *R4*, which matches the version the Norwegian basisprofiler constrain; the *profiles* are not Norwegian, and no claim of Norwegian clinical representativeness is made for these records. The invariance result of Table 5.7 establishes that this mismatch cannot affect any reported figure. The thesis's Norwegian grounding rests on the infrastructure analysis of Chapter 4, Section 4.11.

The eight bundles in `data/synthea_subset/` are untrimmed output from that cohort. With the subset the mean payload is 891 bytes rather than the 1,006 bytes of the full cohort, because a different set of clinical resources is drawn; Chapter 5, Section 5.8 reports both and every other figure is identical.

---

## A.8 Integrity record

Results reported in Chapters 4 and 5 and confirmed by execution:

| Result | Value | Where reported |
|---|---|---|
| Semantics I — records with ≥1 violation | 90 / 200 | Table 5.3 |
| Semantics I — total violations | 95 | §5.3 |
| Violation decomposition | 41 C2-only, 44 C3-only, 5 both | §5.3 |
| Corollary 1.2 witnesses (no erasure request) | 39 | §5.4 |
| Exhaustive cross-check, three conflict cases | no satisfying assignment | Table 5.4 |
| Exhaustive cross-check, control case | satisfying assignment exists | Table 5.4 |
| Semantics II — records invalidated | 138 (52 Art 17, 86 Art 68(12)) | Table 5.6 |
| Semantics II — total violations | 0 | Table 5.6 |
| Synthea comparison — figures changed | none | Table 5.7 |
| Synthea comparison — commitments changed | 200 / 200 | Table 5.7 |
| Audit-log integrity | 200 / 200 records verify; both tamper tests fail V_II | §5.7 |
| Reference commitment, record 100 | `678ade47c1e6dc03…` | §5.7 |

The reference commitment is included so that a reader re-running the checker can confirm in one glance that their run matches the one reported. It changed once, on 3 October 2026, when the Secure Processing Environment payload was redefined as the logged activity (Chapter 4, Section 4.3). Under `--random-salts` it differs on every run, by design.

---

## A.9 Known limitations of the artefact

Stated here so that they are not inferred from silence:

1. The demonstration checks the propositions on the instances generated under one seed. The general claims rest on the proofs in Chapter 4, not on this code.
2. The exhaustive cross-check covers four small cases at a fourteen-month horizon. The cross-border floor is scaled from 120 months to 12 for that check because 2¹²⁰ assignments are not enumerable; Proposition 1's argument depends on the deadline falling inside the window, not on the window's length.
3. No performance measurement is offered as a result. The runtime figure in Chapter 5 indicates only that reproduction is cheap.
4. Key destruction is simulated in program state. The artefact demonstrates the mechanism's logic and says nothing about whether destruction can be assured in deployment.
5. The checker does not connect to any National Contact Point, implement the OpenNCP transmission flow, evaluate consent policies, or implement any zero-knowledge proof system. None of these is claimed anywhere in the thesis.


---

## A.10 Source listing: `trf_checker.py`

The complete source of the feasibility checker, reproduced as executed. It depends on the Python standard library only. Line count: 534.

```python
"""
TRF feasibility checker
=======================
Executable witness for Proposition 1 (infeasibility under plaintext-verifiability
semantics) and Proposition 2 (feasibility under accountability-preserving semantics)
of the Tri-Lateral Retention Feasibility Model.

Thesis: Verifiable Crypto-Erasure for Cross-Border Health Data Audit Trails
        under the European Health Data Space.
Author: Arshad Akhtar Abbasia, HiMolde.

Model reference: Chapter 4, Sections 4.3-4.7.
  Record a = (m, p, c, k, t_a, F, sigma)
  C1 retention floor : V(a,t) = 1 for t in [t_a, t_a + F]
  C2 erasure right   : alpha(a,t) = 0 for t >= t_r + delta
  C3 deletion ceiling: alpha(a,t) = 0 for t >= t_pi + 6   (secondary pathway)

Run:  python trf_checker.py            (reproducible: salts derived from the record id)
      python trf_checker.py --random-salts   (salts from os.urandom, as a deployment must)
Deterministic by default: fixed seed, identical output on every run.

Beyond the constraint check itself:
  - metadata split into accessor fields and subject fields (Ch4 s4.3); the subject link is
    removed at the deletion ceiling and the removal is logged (Ch4 s4.7, step 4)
  - payload ciphertext deleted with key and salt at invalidation (Ch4 s4.8)
  - payloads modelled per record class: the ITI-55 patient-discovery query for cross-border
    records, the logged activity for SPE records (Ch4 s4.3)
  - each log leaf also holds a salted commitment to the patient link, so a changed link no longer
    opens it, while the leaf still never holds the subject fields themselves
  - V_II tests integrity against an append-only Merkle log (RFC 6962 hashing), with a tamper
    test, instead of checking only that fields are present
  - make_salt() derives salts from the record id for reproducibility; --random-salts draws them
    from os.urandom, as a deployment must
"""

import hashlib
import json
import os
import random
import sys
from itertools import product

SEED = 20260915
DELTA = 1          # GDPR Art 12(3) baseline response period, months
CEILING = 6        # EHDS Art 68(12), months after permit expiry
FLOOR_XBORDER = 120  # eHDSI baseline as reported; illustrative (Ch4 s4.3)
FLOOR_SPE = 12       # EHDS Art 73(1)(e), months
INF = float("inf")
RANDOM_SALTS = "--random-salts" in sys.argv
SUBJECT_FIELDS = ("patient_pseudonym",)   # m_subj(a); every other metadata field is m_acc(a)


# ----------------------------------------------------------------------
# Cryptographic primitives (hiding commitment + simulated key destruction)
# ----------------------------------------------------------------------

def make_salt(rid: int) -> bytes:
    """Per-record 16-byte salt. By default derived from the record id so that every run
    reproduces exactly; that derivation is for reproducibility only and gives no hiding
    against an adversary who knows it. --random-salts draws each salt from os.urandom,
    which is what a deployment must do (Appendix A, A.6)."""
    if RANDOM_SALTS:
        return os.urandom(16)
    return bytes([(rid * 7 + i) % 256 for i in range(16)])


# ----------------------------------------------------------------------
# Append-only audit log: Merkle tree with RFC 6962 hashing
# leaf = H(0x00 || data), node = H(0x01 || left || right)
# ----------------------------------------------------------------------

def _h(b: bytes) -> bytes:
    return hashlib.sha256(b).digest()


class MerkleLog:
    """Append-only log of audit events. An auditor holding the current root can check that
    a given event is in the log, unaltered, with an inclusion proof of log2(n) hashes."""

    def __init__(self):
        self.leaves = []                       # leaf hashes

    def append(self, data: bytes) -> int:
        self.leaves.append(_h(b"\x00" + data))
        return len(self.leaves) - 1

    @staticmethod
    def _mth(leaves):
        if len(leaves) == 1:
            return leaves[0]
        k = 1 << ((len(leaves) - 1).bit_length() - 1)     # largest power of 2 < n
        return _h(b"\x01" + MerkleLog._mth(leaves[:k]) + MerkleLog._mth(leaves[k:]))

    def root(self) -> bytes:
        return self._mth(self.leaves) if self.leaves else _h(b"")

    def proof(self, m: int, leaves=None):
        leaves = self.leaves if leaves is None else leaves
        if len(leaves) == 1:
            return []
        k = 1 << ((len(leaves) - 1).bit_length() - 1)
        if m < k:
            return self.proof(m, leaves[:k]) + [("R", self._mth(leaves[k:]))]
        return self.proof(m - k, leaves[k:]) + [("L", self._mth(leaves[:k]))]

    @staticmethod
    def verify(data: bytes, proof, root: bytes) -> bool:
        node = _h(b"\x00" + data)
        for side, sib in proof:
            node = _h(b"\x01" + (sib + node if side == "L" else node + sib))
        return node == root


AUDIT_LOG = MerkleLog()


def _creation_entry(rec) -> bytes:
    """What the floor protects: accessor fields, commitment, creation month (not m_subj)."""
    m_acc = {k: v for k, v in rec.m.items() if k not in SUBJECT_FIELDS}
    return json.dumps({"event": "access", "rid": rec.rid, "t_a": rec.t_a,
                       "m_acc": m_acc, "c": rec.c, "c_subj": rec.c_subj},
                      sort_keys=True).encode()


def _entry(obj) -> bytes:
    return json.dumps(obj, sort_keys=True).encode()


def log_creation(rec):
    if getattr(rec, "log_idx", None) is None:
        rec.log_idx = {"access": AUDIT_LOG.append(_creation_entry(rec))}


def integrity(rec):
    """(ok, reason): every logged event of the record verifies against the current root."""
    idx = getattr(rec, "log_idx", None)
    if not idx:
        return False, "record not in the audit log"
    if any(f in rec.m for f in SUBJECT_FIELDS):                # the link, while it is held
        link = _entry({f: rec.m.get(f) for f in SUBJECT_FIELDS})
        if rec.subj_salt is None or commit(link, rec.subj_salt) != rec.c_subj:
            return False, "patient link does not open its logged commitment (altered)"
    root = AUDIT_LOG.root()
    checks = [("access", _creation_entry(rec))]
    if rec.iota is not None:
        checks.append(("invalidation", _entry(rec.iota)))
    if rec.iota_subj is not None:
        checks.append(("subject_link", _entry(rec.iota_subj)))
    for name, data in checks:
        if name not in idx:
            return False, f"{name} event not logged"
        if not MerkleLog.verify(data, AUDIT_LOG.proof(idx[name]), root):
            return False, f"{name} entry fails its inclusion proof (altered)"
    return True, ""


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
        # metadata m(a) = m_acc(a) + m_subj(a); no clinical content (Ch4 s4.3)
        if sigma == "primary":                # cross-border: clinician, contact point
            self.m = {"rid": rid, "actor": f"HP-{rid % 37:03d}",
                      "ncp": ["NO", "PT", "CZ", "FI"][rid % 4],
                      "patient_pseudonym": f"PSN-{rid % 100:04d}",
                      "doc_category": "PatientSummary", "legal_basis": "Art9(2)(h)",
                      "outcome": "success"}
        else:                                 # SPE: researcher named in the permit
            self.m = {"rid": rid, "actor": f"R-{rid % 23:03d}",
                      "permit": f"DP-{rid % 17:03d}",
                      "patient_pseudonym": f"PSN-{rid % 100:04d}",
                      "doc_category": "SPE-AccessLog", "legal_basis": "DataPermit",
                      "outcome": "success"}
        self.salt = make_salt(rid)
        self.payload = payload                # stands for the ciphertext of p(a)
        self.c = commit(payload, self.salt)   # survives invalidation
        # salted commitment to the patient link, logged with the accessor fields (Ch4 s4.8)
        self.subj_salt = make_salt(rid + 100000)
        self.c_subj = commit(_entry({f: self.m[f] for f in SUBJECT_FIELDS}), self.subj_salt)
        self.k = f"KEY-{rid:06d}"             # destroyed at invalidation
        self.iota = None                      # invalidation entry
        self.iota_subj = None                 # subject-link removal entry (SPE, ceiling)
        self.log_idx = None

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

    def subject_removal(self):
        """Month from which m_subj is gone: the ceiling, where C3 reaches the subject fields."""
        return self.ceiling_deadline()


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
# Trajectory from the constructive proof of Proposition 2.
# ----------------------------------------------------------------------

def apply_invalidation(rec):
    log_creation(rec)                     # the access event enters the log first
    t_I = rec.t_invalidation()
    if t_I < INF:
        ground = ("GDPR Art 17(1)" if rec.erasure_deadline() <= rec.ceiling_deadline()
                  else "EHDS Art 68(12)")
        rec.k = None                      # irreversible key destruction
        rec.salt = None                   # salt destroyed with the key (Ch4 s4.8)
        rec.payload = None                # ciphertext deleted with the key (Ch4 s4.8, D-17)
        rec.iota = {"rid": rec.rid, "month": t_I, "ground": ground,
                    "authorised_by": "DPO", "key_id_commitment":
                        hashlib.sha256(f"KEY-{rec.rid:06d}".encode()).hexdigest()[:16]}
        rec.log_idx["invalidation"] = AUDIT_LOG.append(_entry(rec.iota))
    t_S = rec.subject_removal()
    if t_S < INF and any(f in rec.m for f in SUBJECT_FIELDS):
        for f in SUBJECT_FIELDS:          # beta = 0 from the ceiling (Ch4 s4.7, steps 2 and 4)
            rec.m.pop(f, None)
        rec.subj_salt = None              # the link's salt goes with the link
        rec.iota_subj = {"rid": rec.rid, "month": t_S, "removed": list(SUBJECT_FIELDS),
                         "ground": "EHDS Art 68(12)", "authorised_by": "DPO"}
        rec.log_idx["subject_link"] = AUDIT_LOG.append(_entry(rec.iota_subj))
    return rec


def alpha(rec, t):
    return 1 if t < rec.t_invalidation() else 0


def beta(rec, t):
    """Subject-link variable: 0 from the month the subject fields were removed."""
    return 0 if rec.iota_subj is not None and t >= rec.iota_subj["month"] else 1


def V_II(rec, t, integrity_result=None):
    """(i) m_acc intact and unmodified, checked against the audit log;
       (ii) commitment present and logged; (iii) every loss of accessibility,
       of the payload or of the subject link, is itself a logged entry."""
    ok, why = integrity_result if integrity_result is not None else integrity(rec)
    if not ok:
        return False, why
    if not rec.c:
        return False, "commitment missing"
    if alpha(rec, t) == 0 and t >= rec.t_a and rec.iota is None:
        return False, "payload inaccessible but no invalidation entry"
    if not any(f in rec.m for f in SUBJECT_FIELDS) and rec.iota_subj is None:
        return False, "subject fields removed without a logged entry"
    return True, ""


def check_semantics_II(rec):
    violations = []
    integ = integrity(rec)                                   # one proof check per record
    for t in rec.window():                                   # C1
        ok, why = V_II(rec, t, integ)
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
        for t in range(int(d), horizon + 1):                 # C3 over the subject link
            if beta(rec, t) != 0:
                violations.append({"rid": rec.rid, "month": t, "constraint": "C3",
                                   "detail": "subject link still present after deletion ceiling"})
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
        payload = (f"<ITI-55 QBP name=N{rid:03d} birthTime=19{40 + rid % 60:02d} "
                   f"rid={rid}>").encode()       # demographic query (Ch4 s4.3)
        records.append(Record(rid, t_a, FLOOR_XBORDER, "primary", payload, t_r=t_r))
        rid += 1
    # Class 2: SPE access-log records, floor 12 months, ceiling applies
    for _ in range(n_secondary):
        t_a = rng.randint(0, 11)
        permit_len = rng.randint(1, 12)
        t_pi = t_a + permit_len
        t_r = t_a + rng.randint(1, 18) if rng.random() < 0.25 else INF
        payload = f"<SPE-activity query=cohort-extract rid={rid}>".encode()
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
    print("SEMANTICS I  (plaintext verifiability:  V = alpha)   -> Proposition 1")
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
    print("SEMANTICS II (accountability preservation)          -> Proposition 2")
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
    print(f"  accessor fields      : {integrity(demo)[0]}  actor={demo.m['actor']} "
          f"permit={demo.m.get('permit', '-')} outcome={demo.m['outcome']}")
    print(f"  subject link         : "
          f"{'removed month ' + str(demo.iota_subj['month']) if demo.iota_subj else 'present'}")
    print(f"  commitment c(a)      : {demo.c[:32]}...")
    print(f"  payload key k(a)     : {demo.k}   <- destroyed")
    print(f"  salt, ciphertext     : {demo.salt}, {demo.payload}   <- destroyed, deleted")
    print(f"  invalidation iota(a) : month={demo.iota['month']} "
          f"ground={demo.iota['ground']}")
    print(f"  payload readable?    : {bool(alpha(demo, demo.t_a + demo.floor))}")

    # ---------------- Integrity of the audit log ----------------
    print("\n" + "-" * 74)
    print("AUDIT-LOG INTEGRITY (Merkle log, RFC 6962 hashing)     -> V_II condition (i)")
    print("-" * 74)
    n_ok = sum(1 for r in records if integrity(r)[0])
    print(f"log entries                : {len(AUDIT_LOG.leaves)}")
    print(f"log root                   : {AUDIT_LOG.root().hex()[:32]}...")
    print(f"records verifying          : {n_ok}/{len(records)}")
    saved = demo.m["actor"]
    demo.m["actor"] = "R-999"                                  # tamper with one accessor field
    ok_t, why_t = V_II(demo, demo.t_a)
    demo.m["actor"] = saved
    print(f"tamper test, rid={demo.rid} actor altered : V_II={ok_t}  ({why_t})")
    saved_g = demo.iota["ground"]
    demo.iota["ground"] = "none"                               # tamper with the invalidation entry
    ok_g, why_g = V_II(demo, demo.t_a)
    demo.iota["ground"] = saved_g
    print(f"tamper test, rid={demo.rid} ground altered: V_II={ok_g}  ({why_g})")
    xb = next(r for r in prim if r.iota is not None)          # a cross-border record keeps its link
    saved_p = xb.m["patient_pseudonym"]
    xb.m["patient_pseudonym"] = "PSN-9999"                    # tamper with the patient link
    ok_p, why_p = V_II(xb, xb.t_a)
    xb.m["patient_pseudonym"] = saved_p
    print(f"tamper test, rid={xb.rid} link altered  : V_II={ok_p}  ({why_p})")
    print(f"after restoring all three  : V_II={V_II(demo, demo.t_a)[0] and V_II(xb, xb.t_a)[0]}")

    print("\n" + "=" * 74)
    print(f"RESULT  Semantics I : {total_v} violations across {n_bad} records  "
          f"-> INFEASIBLE")
    print(f"RESULT  Semantics II: {total_v2} violations across {n_bad2} records  "
          f"-> FEASIBLE")
    print("=" * 74)


if __name__ == "__main__":
    main()


# ----------------------------------------------------------------------
# Extended response period witness (Chapter 5, Section 5.6)
# GDPR Art 12(3) permits extension of the one-month response period by a
# further two months. The propositions are stated for arbitrary finite delta;
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
```

## A.11 Source listing: `synthea_layer.py`

The realism layer, reproduced as executed.

```python
"""
Synthea realism layer for the TRF feasibility checker
=====================================================
Chapter 3, Section 3.6 specifies two layers: the feasibility checker (the
load-bearing component) and a realism layer feeding it FHIR-structured
records generated by Synthea.

This module is the realism layer. It replaces the synthetic byte-string
payloads of trf_checker.generate() with real FHIR R4 resources drawn from
Synthea-generated patient bundles, leaving every timing quantity
(t_a, t_r, t_pi, F, sigma, delta) untouched.

The purpose is to establish, by execution rather than assertion, that the
model's results are functions of timing and accessibility alone and do not
depend on payload provenance. If any reported figure changes, the model
reads something it should not.

Cohort: synthea -s 20260915 -cs 20260915 -p 100, FHIR R4 export.
Run:    python synthea_layer.py
"""

import glob
import json
import os

import trf_checker as trf

_HERE = os.path.dirname(os.path.abspath(__file__))
# Search order: the full regenerated cohort first, then the 8-bundle subset
# shipped in the repository. The first directory that contains bundles wins.
SYNTHEA_DIRS = [os.path.join(_HERE, "synthea_run", "output", "fhir"),
                os.path.join(_HERE, "data", "synthea_subset"),
                os.path.join(_HERE, "synthea_subset")]


def _resolve_dir():
    for d in SYNTHEA_DIRS:
        if glob.glob(os.path.join(d, "*.json")):
            return d
    return SYNTHEA_DIRS[0]


SYNTHEA_DIR = _resolve_dir()
CLINICAL_TYPES = ("Condition", "Observation", "MedicationRequest",
                  "AllergyIntolerance", "Immunization", "Procedure")


def load_payloads(limit=400, seed=trf.SEED):
    """Extract clinically meaningful resources from Synthea bundles and
    serialise each as a payload. These stand in for the content of an
    exchanged patient summary or the subject of an SPE access."""
    files = sorted(glob.glob(os.path.join(_resolve_dir(), "*.json")))
    if not files:
        raise FileNotFoundError(
            "No Synthea bundles found. Looked in:\n  "
            + "\n  ".join(SYNTHEA_DIRS)
            + "\nRegenerate the full cohort with:\n"
              "  java -jar synthea.jar -s 20260915 -cs 20260915 -p 100")
    payloads, meta = [], []
    for path in files:
        with open(path) as fh:
            bundle = json.load(fh)
        for entry in bundle.get("entry", []):
            res = entry.get("resource", {})
            if res.get("resourceType") in CLINICAL_TYPES:
                payloads.append(json.dumps(res, sort_keys=True).encode())
                meta.append((os.path.basename(path).split("_")[0],
                             res["resourceType"]))
                break          # one resource per bundle keeps the mapping 1:1
        if len(payloads) >= limit:
            break
    return payloads, meta, len(files)


def generate_with_synthea(n_primary=100, n_secondary=100, seed=trf.SEED):
    """Identical to trf_checker.generate() in every timing respect; only the
    payload bytes differ."""
    records = trf.generate(n_primary, n_secondary, seed)
    payloads, meta, n_files = load_payloads()
    for rec in records:
        p = payloads[rec.rid % len(payloads)]
        rec.payload = p
        rec.c = trf.commit(p, rec.salt)     # recompute commitment over real payload
        rec.m["doc_category"] = (
            f"PatientSummary/{meta[rec.rid % len(meta)][1]}"
            if rec.sigma == "primary"
            else f"SPE-AccessLog/{meta[rec.rid % len(meta)][1]}")
    return records, n_files, len(payloads)


def main():
    print("=" * 74)
    print("SYNTHEA REALISM LAYER — comparison against constructed payloads".center(74))
    print("=" * 74)

    base = trf.generate()
    real, n_files, n_payloads = generate_with_synthea()
    print(f"\nSynthea bundles read : {n_files}")
    print(f"clinical payloads    : {n_payloads}")
    print(f"records              : {len(real)}")
    print(f"payload bytes (mean) : constructed={sum(len(r.payload) for r in base)//len(base)}"
          f"  synthea={sum(len(r.payload) for r in real)//len(real)}")

    results = {}
    for label, recs in (("constructed", base), ("synthea", real)):
        v1 = {r.rid: trf.check_semantics_I(r) for r in recs}
        n_bad = sum(1 for k in v1 if v1[k])
        tot = sum(len(x) for x in v1.values())
        sec = [r for r in recs if r.sigma == "secondary"]
        cor12 = sum(1 for r in sec if r.t_r == trf.INF and v1[r.rid])
        for r in recs:
            trf.apply_invalidation(r)
        v2 = {r.rid: trf.check_semantics_II(r) for r in recs}
        n_bad2 = sum(1 for k in v2 if v2[k])
        tot2 = sum(len(x) for x in v2.values())
        n_inv = sum(1 for r in recs if r.iota is not None)
        results[label] = (n_bad, tot, cor12, n_inv, n_bad2, tot2)

    print("\n" + "-" * 74)
    hdr = f"{'measure':<42}{'constructed':>15}{'synthea':>15}"
    print(hdr); print("-" * 74)
    names = ["Semantics I: records with violation",
             "Semantics I: total violations",
             "Corollary 1.2 witnesses (no request)",
             "Records invalidated",
             "Semantics II: records with violation",
             "Semantics II: total violations"]
    identical = True
    for i, nm in enumerate(names):
        a, b = results["constructed"][i], results["synthea"][i]
        flag = "" if a == b else "   <-- DIFFERS"
        if a != b:
            identical = False
        print(f"{nm:<42}{a:>15}{b:>15}{flag}")
    print("-" * 74)

    # commitments must differ - different payloads, same salts
    diff_c = sum(1 for x, y in zip(base, real) if x.c != y.c)
    print(f"\ncommitments differing between the two runs: {diff_c}/{len(base)}"
          f"   (expected {len(base)} — same salt, different payload)")

    print("\n" + "=" * 74)
    if identical and diff_c == len(base):
        print("RESULT: every reported figure is IDENTICAL under real FHIR payloads,".center(74))
        print("while every commitment differs. The model reads timing, not content.".center(74))
    else:
        print("RESULT: DIVERGENCE DETECTED — investigate before reporting.".center(74))
    print("=" * 74)


if __name__ == "__main__":
    main()
```

## A.12 Source listing: `norwegian_layer.py`

The Norwegian context module, reproduced as executed. It imports `trf_checker.py` without modifying it and changes nothing the thesis reports: it varies only the retention floor, the pathway, and the arrival of erasure requests and permit expiries. Line count: 135.

```python
"""
Norwegian context layer for the TRF feasibility checker
=======================================================
PLUG-AND-PLAY. This module imports trf_checker unmodified and adds record
classes shaped by the Norwegian implementation context. It changes nothing the
thesis depends on: `python3 trf_checker.py` still reproduces 95/90/39/0/138.

What it varies is what the model actually reads: the retention floor F(a), the
pathway, and the arrival of erasure requests and permit expiries. It does NOT
claim that Norwegian payloads change any result — Chapter 5 shows the results
are invariant to payload content, and that invariance is why the illustrative
payloads below are safe to use.

Classes
  NO-XB      Cross-border audit record at the Norwegian NCPeH. Inbound patient
             summary from PT/CZ/FI to a legevakt (Bodo, Stjordal).
             F = 120 months (eHDSI deployment baseline).
  NO-SPE     Secure Processing Environment access log, Helsedataservice permit,
             processing in a NORTRE node. F = 12 (Art 73(1)(e)),
             ceiling 6 months after permit expiry (Art 68(12)).
  NO-JOURNAL Audit record tied to a patient record held under Norwegian law.
             Floor is INDEFINITE: pasientjournalloven s 25 and journalforskriften
             s 14 require retention until, given the character of the health care,
             the record is no longer assumed to be needed; archive law may then
             preserve it. There is no number in the primary sources, so none is
             invented here. For computation the indefinite floor is truncated at
             HORIZON_INDEFINITE months and labelled as a truncation.

Run:  python3 norwegian_layer.py
"""

import random
import trf_checker as trf

HORIZON_INDEFINITE = 600          # 50 years; a computation bound, NOT a legal period
SEED = trf.SEED

NCPS = ["PT", "CZ", "FI"]
SITES = ["Bodo legevakt", "Stjordal legevakt"]
NODES = ["TSD (UiO)", "SAFE (UiB)", "HUNT Cloud (NTNU)", "controller-provided server"]


def _xb_payload(rid, rng):
    """Stands for the ITI-55 QueryByParameter segment an ATNA record carries:
    the demographics typed into patient discovery. Constructed, not real."""
    return (f"<ITI-55 QueryByParameter base64> name=SYN-{rid:04d} "
            f"birthTime=19{rng.randint(40,99)}{rng.randint(10,12)}{rng.randint(10,28)} "
            f"gender={rng.choice('MF')} addr=NO-{rng.randint(1000,9999)}").encode()


def _spe_payload(rid, rng):
    return (f"<SPE activity log> query=SELECT diagnosis,birthyear FROM permit-"
            f"{rng.randint(2026,2031)}-{rid:04d} rows={rng.randint(50,5000)}").encode()


def build(n_xb=60, n_spe=60, n_journal=40, seed=SEED):
    rng = random.Random(seed)
    recs, rid = [], 0
    for _ in range(n_xb):                                   # NO-XB
        t_a = rng.randint(0, 11)
        t_r = t_a + rng.randint(1, 130) if rng.random() < 0.40 else trf.INF
        r = trf.Record(rid, t_a, trf.FLOOR_XBORDER, "primary", _xb_payload(rid, rng), t_r=t_r)
        r.m.update({"klasse": "NO-XB", "site": rng.choice(SITES),
                    "ncp": rng.choice(NCPS), "doc_category": "PatientSummary (inbound)",
                    "legal_basis": "Art9(2)(h)"})
        recs.append(r); rid += 1
    for _ in range(n_spe):                                  # NO-SPE
        t_a = rng.randint(0, 11)
        t_pi = t_a + rng.randint(1, 12)
        t_r = t_a + rng.randint(1, 18) if rng.random() < 0.25 else trf.INF
        r = trf.Record(rid, t_a, trf.FLOOR_SPE, "secondary", _spe_payload(rid, rng),
                       t_r=t_r, t_pi=t_pi)
        r.m.update({"klasse": "NO-SPE", "node": rng.choice(NODES),
                    "doc_category": "SPE-ActivityLog", "legal_basis": "DataPermit (Helsedataservice)"})
        recs.append(r); rid += 1
    for _ in range(n_journal):                              # NO-JOURNAL
        t_a = rng.randint(0, 11)
        t_r = t_a + rng.randint(1, 240) if rng.random() < 0.40 else trf.INF
        r = trf.Record(rid, t_a, HORIZON_INDEFINITE, "primary", _xb_payload(rid, rng), t_r=t_r)
        r.m.update({"klasse": "NO-JOURNAL", "doc_category": "JournalAccess",
                    "legal_basis": "pasientjournalloven s 25 (purpose-based, indefinite)"})
        recs.append(r); rid += 1
    return recs


def run(recs, label="NORWEGIAN LAYER"):
    klasser = sorted({r.m["klasse"] for r in recs})
    v1 = {r.rid: trf.check_semantics_I(r) for r in recs}
    for r in recs:
        trf.apply_invalidation(r)
    v2 = {r.rid: trf.check_semantics_II(r) for r in recs}
    print("=" * 74); print(label.center(74)); print("=" * 74)
    print(f"\n{'class':<12}{'n':>5}{'SemI recs':>11}{'SemI viol':>11}"
          f"{'invalidated':>13}{'SemII viol':>12}")
    for k in klasser:
        sub = [r for r in recs if r.m["klasse"] == k]
        print(f"{k:<12}{len(sub):>5}"
              f"{sum(1 for r in sub if v1[r.rid]):>11}"
              f"{sum(len(v1[r.rid]) for r in sub):>11}"
              f"{sum(1 for r in sub if r.iota):>13}"
              f"{sum(len(v2[r.rid]) for r in sub):>12}")
    print(f"\n{'TOTAL':<12}{len(recs):>5}"
          f"{sum(1 for r in recs if v1[r.rid]):>11}"
          f"{sum(len(x) for x in v1.values()):>11}"
          f"{sum(1 for r in recs if r.iota):>13}"
          f"{sum(len(x) for x in v2.values()):>12}")
    return v1, v2


def walkthrough(recs, v1):
    """One record per class, shown end to end: which obligation binds, where it
    collides, and what an auditor is left with after invalidation."""
    print("\n" + "-" * 74); print("CASE WALKTHROUGHS"); print("-" * 74)
    for k in sorted({r.m["klasse"] for r in recs}):
        cand = [r for r in recs if r.m["klasse"] == k and v1[r.rid]]
        if not cand:
            print(f"\n{k}: no infeasible record under Semantics I in this draw."); continue
        r = cand[0]
        print(f"\n{k}  rid={r.rid}  ({r.m.get('site') or r.m.get('node') or r.m['legal_basis']})")
        print(f"  floor    : t={r.t_a} .. {r.t_a + r.floor}"
              + ("   [indefinite, truncated]" if k == "NO-JOURNAL" else ""))
        print(f"  erasure  : {'none' if r.t_r == trf.INF else 't_r=' + str(r.t_r) + ' -> deadline ' + str(int(r.erasure_deadline()))}")
        print(f"  ceiling  : {'n/a' if r.ceiling_deadline() == trf.INF else 't_pi=' + str(r.t_pi) + ' -> ' + str(int(r.ceiling_deadline()))}")
        print(f"  collision: {v1[r.rid][0]['constraint']} at t={v1[r.rid][0]['month']}")
        print(f"  after invalidation -> metadata intact={bool(r.m)}, commitment={r.c[:16]}..., "
              f"key={r.k}, salt={r.salt}, ground={r.iota['ground'] if r.iota else None}")


if __name__ == "__main__":
    recs = build()
    v1, _ = run(recs)
    walkthrough(recs, v1)
    print("\nNote: figures above are illustrative of the Norwegian setting, not")
    print("empirical. The canonical result of the thesis is unchanged and is")
    print("reproduced by running trf_checker.py on its own.")
```

---

## A.13 Source listing: `cross_sector_check.py`

The cross-sector instance discussed in Chapter 6, Section 6.10. It takes the floor and ceiling of politiregisterloven § 17 and runs them through the same unmodified model. Line count: 110.

```python
"""
Cross-sector instance: Norwegian police register logs
=====================================================
PLUG-AND-PLAY. Imports trf_checker unmodified.

Why this exists. Chapter 6 s 6.9 and Chapter 7 s 7.5 say the structure the TRF
Model captures — a retention floor, a subject-triggered erasure right, and a
deletion ceiling — is probably not specific to health, and flag the question as
uninvestigated. Norwegian law supplies a genuine instance outside health.

  Politiregisterloven (LOV-2010-05-28-16) s 17, kravet til sporbarhet:
    information about use of the system shall be registered and stored for at
    least 1 year and deleted at the latest after 3 years.
  Politiregisterforskriften (FOR-2013-09-20-1097) ch. 40 mirrors this:
    deleted at the earliest after 1 year and at the latest after 3 years.
  Politiregisterloven s 50-51 give the registered person rights to correction,
    blocking and deletion of information no longer necessary for the purpose.

That is a floor of 12 months and a ceiling of 36 months on the SAME log, plus a
subject-triggered right: the tri-lateral structure, in another sector, in
national law.

THE RESULT IS NOT THE ONE EXPECTED, AND IT IS THE MORE USEFUL ONE. Running the
model on this instance produces NO structural collision at all: the floor ends
at t_a + 12 and the ceiling bites at t_a + 36, so the provision defines a
bounded retention window rather than a contradiction. The Norwegian legislator
ordered the two limbs. Collisions appear only where an erasure request lands
inside the window.

That isolates what is defective about the EHDS pair. There the ceiling is
anchored to an EXTERNAL event, the expiry of the data permit, which can fall
before the floor on a log written late in the permit. A floor and a ceiling on
the same record are compatible when the instrument orders them from the same
origin, and collide when one is anchored elsewhere. The contribution of the
thesis is therefore not that floors and ceilings conflict in general; it is that
they conflict when their origins differ, which is the EHDS case.

Two further differences from the EHDS case are stated rather than hidden:
  1. The ceiling here runs from the log's own creation, not from the expiry of a
     permit. It is modelled by setting t_pi so that the ceiling lands at
     t_a + 36 (the checker computes ceiling = t_pi + 6).
  2. The ceiling attaches to the whole record, not only to a payload inside it.
     Under Semantics II the metadata cannot survive it, so the terminal
     transition of Chapter 4 s 4.8 is what discharges the ceiling here, at
     t_a + 36 rather than at floor expiry. This module reports the collision;
     it does not claim the mechanism transfers unchanged.

Run:  python3 cross_sector_check.py
"""

import random
import trf_checker as trf

FLOOR_POLITI = 12      # politiregisterloven s 17: at least 1 year
CEILING_POLITI = 36    # politiregisterloven s 17: deleted at the latest after 3 years


def build(n=60, seed=trf.SEED):
    rng = random.Random(seed)
    recs = []
    for rid in range(900, 900 + n):
        t_a = rng.randint(0, 11)
        # ceiling lands at t_a + 36; checker computes t_pi + 6
        t_pi = t_a + CEILING_POLITI - trf.CEILING
        t_r = t_a + rng.randint(1, 40) if rng.random() < 0.30 else trf.INF
        payload = f"<politiloggpost> bruker=POL-{rid % 97:03d} oppslag=register".encode()
        r = trf.Record(rid, t_a, FLOOR_POLITI, "secondary", payload, t_r=t_r, t_pi=t_pi)
        r.m.update({"klasse": "POLITI-LOG", "doc_category": "SystemUseLog",
                    "legal_basis": "politiregisterloven s 17"})
        recs.append(r)
    return recs


def main():
    recs = build()
    v1 = {r.rid: trf.check_semantics_I(r) for r in recs}
    n_bad = sum(1 for k in v1 if v1[k])
    structural = sum(1 for r in recs if r.t_r == trf.INF and v1[r.rid])
    for r in recs:
        trf.apply_invalidation(r)
    v2 = {r.rid: trf.check_semantics_II(r) for r in recs}
    print("=" * 74)
    print("CROSS-SECTOR INSTANCE: politiregisterloven s 17 (floor 12, ceiling 36)".center(74))
    print("=" * 74)
    print(f"\nrecords                              : {len(recs)}")
    print(f"Semantics I, records with violation  : {n_bad}")
    print(f"  of which with NO erasure request   : {structural}  <- floor vs ceiling alone")
    print(f"Semantics II, total violations       : {sum(len(x) for x in v2.values())}")
    print(f"records invalidated                  : {sum(1 for r in recs if r.iota)}")
    if structural == 0:
        print("\nNo structural collision: s 17 orders its two limbs from one origin")
        print("(floor at t_a + 12, ceiling at t_a + 36), so the provision defines a")
        print("bounded retention window rather than a contradiction. Every collision")
        print("found is erasure-driven.")
    cand = [r for r in recs if v1[r.rid]]
    if cand:
        r = cand[0]; d = v1[r.rid][0]
        print(f"\nwitness rid={r.rid}: log written t={r.t_a}; floor to t={r.t_a + r.floor}; "
              f"ceiling at t={int(r.ceiling_deadline())}; erasure deadline "
              f"{int(r.erasure_deadline())}; collision {d['constraint']} at t={d['month']}")
    print("\nThe floor parameter F(a) took a third value with no change to the model.")
    print("The finding: floors and ceilings coexist when one instrument fixes both from")
    print("the same origin, and collide when the ceiling is anchored to an external")
    print("event, as Art 68(12) anchors it to permit expiry. Scope: a structural")
    print("parallel. Whether the mechanism transfers to a record-level ceiling is a")
    print("design question this module does not answer.")


if __name__ == "__main__":
    main()
```

---

## A.14 The demonstration viewer: `app.py` and `ui.py`

Not reproduced here, because the viewer is never a source of results: every figure it displays comes from executing one of the modules listed in this appendix, unmodified. `app.py` (804 lines) holds the pages and the self-checks; `ui.py` (133 lines) holds only presentation: the theme, the record life strip and the embedding of the two Archify diagrams. The Thesis run page asserts the reported figures and shows a failure notice rather than results if the run disagrees with Chapter 5. Both files are in the repository (https://github.com/Astheno-sphere/TRF).

## A.15 Source listing: `crypto_envelope.py`

The optional envelope-encryption module. Each record's payload is encrypted under its own AES-256-GCM data key; the data keys are wrapped under a key-encrypting key held in a custody object standing in for a hardware security module; at each record's invalidation month the wrapped key is destroyed; every record is then decrypted again. It is the only module with a dependency outside the standard library. Line count: 118.

```python
"""
Envelope encryption with real AES-256-GCM (optional module)
===========================================================
The feasibility checker (trf_checker.py) models key destruction as removing a reference and
uses the standard library only. This module shows the same lifecycle with real cryptography,
so that "rendered unrecoverable" (TEHDAS2 D7.4, OPR-6) is executed rather than asserted:

  - each record's payload is encrypted under its own random 256-bit data key (AES-256-GCM,
    record id as associated data);
  - each data key is wrapped under a key-encrypting key held in a custody object standing in
    for a hardware security module (Chapter 4, Section 4.8, key hierarchy);
  - at the record's invalidation month the wrapped data key is destroyed in custody;
  - every record is then decrypted again: invalidated records must fail, the rest must succeed.

It reads its population and invalidation months from trf_checker unchanged and reports no
thesis figure. Destruction here is still destruction in program memory: the module shows that
the ciphertext is unreadable without the key, not that a key was erased from hardware
(Chapter 6, Section 6.3).

Run:  pip install cryptography   then   python3 crypto_envelope.py
Keys are random on every run; the printed counts are deterministic.
"""

import os

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

import trf_checker as trf


class Custody:
    """Stands in for an HSM: holds the key-encrypting key and the wrapped data keys."""

    def __init__(self):
        self._kek = AESGCM(AESGCM.generate_key(bit_length=256))
        self._wrapped = {}                                # rid -> (nonce, wrapped data key)

    def new_data_key(self, rid):
        dek = AESGCM.generate_key(bit_length=256)
        nonce = os.urandom(12)
        self._wrapped[rid] = (nonce, self._kek.encrypt(nonce, dek, f"dek:{rid}".encode()))
        return dek

    def data_key(self, rid):
        if rid not in self._wrapped:
            raise KeyError(f"data key for record {rid} destroyed")
        nonce, wrapped = self._wrapped[rid]
        return self._kek.decrypt(nonce, wrapped, f"dek:{rid}".encode())

    def destroy(self, rid):
        self._wrapped.pop(rid, None)


def encrypt(custody, rid, payload):
    dek = custody.new_data_key(rid)
    nonce = os.urandom(12)
    ct = AESGCM(dek).encrypt(nonce, payload, f"rec:{rid}".encode())
    del dek                                            # only the wrapped copy survives
    return nonce, ct


def decrypt(custody, rid, nonce, ct):
    return AESGCM(custody.data_key(rid)).decrypt(nonce, ct, f"rec:{rid}".encode())


def main():
    print("=" * 74)
    print("ENVELOPE ENCRYPTION (AES-256-GCM, wrapped data keys)".center(74))
    print("=" * 74)
    records = trf.generate()
    custody = Custody()
    store = {r.rid: encrypt(custody, r.rid, r.payload) for r in records}
    ok_before = sum(1 for r in records if decrypt(custody, r.rid, *store[r.rid]) == r.payload)
    print(f"records encrypted                     : {len(records)}")
    print(f"decrypt and match before invalidation : {ok_before}/{len(records)}")

    invalidated = [r for r in records if r.t_invalidation() < trf.INF]
    for r in invalidated:
        custody.destroy(r.rid)                          # key destroyed at t_I (Ch4 s4.7 step 2)
    print(f"data keys destroyed (t_I finite)      : {len(invalidated)}")

    readable, refused = 0, 0
    for r in records:
        try:
            decrypt(custody, r.rid, *store[r.rid])
            readable += 1
        except KeyError:
            refused += 1
    print(f"decryptable after invalidation        : {readable}  (expected {len(records) - len(invalidated)})")
    print(f"refused, key destroyed                : {refused}  (expected {len(invalidated)})")

    # The ciphertext of an invalidated record does not open under any surviving key.
    victim = invalidated[0]
    survivors = [r for r in records if r.t_invalidation() == trf.INF]
    opened = 0
    for s in survivors:
        try:
            AESGCM(custody.data_key(s.rid)).decrypt(store[victim.rid][0], store[victim.rid][1],
                                                    f"rec:{victim.rid}".encode())
            opened += 1
        except InvalidTag:
            pass
    print(f"rid={victim.rid} ciphertext tried under {len(survivors)} surviving keys : opened {opened}")

    for r in invalidated:                               # then the ciphertext is deleted (D-17)
        del store[r.rid]
    print(f"ciphertexts kept after deletion       : {len(store)}")

    ok = (ok_before == len(records) and refused == len(invalidated)
          and readable == len(records) - len(invalidated) and opened == 0)
    print("=" * 74)
    print(f"RESULT: {'every invalidated record is unrecoverable; every other record reads' if ok else 'MISMATCH'}")
    print("=" * 74)


if __name__ == "__main__":
    main()
```

---

## A.16 Console output of the reported run

Verbatim output of `python3 trf_checker.py` under seed 20260915. Every figure in Chapter 5, Tables 5.3, 5.4 and 5.6 appears here, with the δ = 1 row of Table 5.5; its δ = 3 row is in A.18.

```text
==========================================================================
                         TRF FEASIBILITY CHECKER                          
   seed=20260915  delta=1  ceiling=6  floors: cross-border=120, SPE=12    
==========================================================================

Generated 200 records (100 cross-border, 100 SPE access-log)

--------------------------------------------------------------------------
SEMANTICS I  (plaintext verifiability:  V = alpha)   -> Proposition 1
--------------------------------------------------------------------------
records with >=1 violation : 90/200
  cross-border (F=120)     : 37/100
  SPE access-log (F=12)    : 53/100
total constraint violations: 95

Corollary 1.2 witnesses (SPE, NO erasure request, still infeasible): 39
  rid=100: t_a=7 permit expires t_pi=10 -> C3 from t=16, C1 to t=19  | collision at t=16
  rid=103: t_a=7 permit expires t_pi=10 -> C3 from t=16, C1 to t=19  | collision at t=16
  rid=104: t_a=3 permit expires t_pi=4 -> C3 from t=10, C1 to t=15  | collision at t=10

Sample violation witnesses (cross-border):
  C1 requires V=1 (=> alpha=1) at t=116 within [11,131]; C2 requires alpha=0 from t=116
  C1 requires V=1 (=> alpha=1) at t=120 within [4,124]; C2 requires alpha=0 from t=120
  C1 requires V=1 (=> alpha=1) at t=41 within [0,120]; C2 requires alpha=0 from t=41

--------------------------------------------------------------------------
INDEPENDENT CROSS-CHECK: exhaustive search over alpha assignments
--------------------------------------------------------------------------
  SPE, no erasure request, permit 3mo            feasible=False
  SPE, erasure at t=2                            feasible=False
  cross-border scaled (F=12), erasure at t=4     feasible=False
  control: no request, no expiry                 feasible=True

--------------------------------------------------------------------------
SEMANTICS II (accountability preservation)          -> Proposition 2
--------------------------------------------------------------------------
records invalidated        : 138/200
  ground = GDPR Art 17(1)  : 52
  ground = EHDS Art 68(12) : 86
records with >=1 violation : 0/200
total constraint violations: 0

Auditor view of rid=100 after invalidation:
  accessor fields      : True  actor=R-008 permit=DP-015 outcome=success
  subject link         : removed month 16
  commitment c(a)      : 678ade47c1e6dc03296175e056fd8116...
  payload key k(a)     : None   <- destroyed
  salt, ciphertext     : None, None   <- destroyed, deleted
  invalidation iota(a) : month=16 ground=EHDS Art 68(12)
  payload readable?    : False

--------------------------------------------------------------------------
AUDIT-LOG INTEGRITY (Merkle log, RFC 6962 hashing)     -> V_II condition (i)
--------------------------------------------------------------------------
log entries                : 438
log root                   : a91c07936a4eb9752b58c6483ca93d7d...
records verifying          : 200/200
tamper test, rid=100 actor altered : V_II=False  (access entry fails its inclusion proof (altered))
tamper test, rid=100 ground altered: V_II=False  (invalidation entry fails its inclusion proof (altered))
tamper test, rid=3 link altered  : V_II=False  (patient link does not open its logged commitment (altered))
after restoring all three  : V_II=True

==========================================================================
RESULT  Semantics I : 95 violations across 90 records  -> INFEASIBLE
RESULT  Semantics II: 0 violations across 0 records  -> FEASIBLE
==========================================================================
```

## A.17 Console output of the payload-provenance comparison, full cohort

Produced by command 4 against the regenerated 98-bundle cohort. Verbatim output of `python3 synthea_layer.py` against the full 98-bundle cohort, the source of Chapter 5, Table 5.7, which Section 5.8 reports at a mean payload of 1,006 bytes. It was recorded on 28 September 2026, before the code revision of 3 October, and its constructed-payload mean (35 bytes) reflects the earlier constructed strings; no measure in it depends on them, as the subset run in A.21, recorded after the revision, shows. Reproducing it requires regenerating the cohort with command 3, because the full cohort is 314 MB and is not committed.

```text
==========================================================================
     SYNTHEA REALISM LAYER — comparison against constructed payloads      
==========================================================================

Synthea bundles read : 98
clinical payloads    : 98
records              : 200
payload bytes (mean) : constructed=35  synthea=1006

--------------------------------------------------------------------------
measure                                       constructed        synthea
--------------------------------------------------------------------------
Semantics I: records with violation                    90             90
Semantics I: total violations                          95             95
Corollary 1.2 witnesses (no request)                   39             39
Records invalidated                                   138            138
Semantics II: records with violation                    0              0
Semantics II: total violations                          0              0
--------------------------------------------------------------------------

commitments differing between the two runs: 200/200   (expected 200 — same salt, different payload)

==========================================================================
   RESULT: every reported figure is IDENTICAL under real FHIR payloads,   
   while every commitment differs. The model reads timing, not content.   
==========================================================================
```

---

## A.18 Console output of the erasure-response-period witness

Produced by command 5. Reproduces Table 5.5: the infeasibility survives the extension Article 12(3) GDPR permits.

```text
==========================================================================
                         TRF FEASIBILITY CHECKER                          
   seed=20260915  delta=1  ceiling=6  floors: cross-border=120, SPE=12    
==========================================================================

Generated 200 records (100 cross-border, 100 SPE access-log)

--------------------------------------------------------------------------
SEMANTICS I  (plaintext verifiability:  V = alpha)   -> Proposition 1
--------------------------------------------------------------------------
records with >=1 violation : 90/200
  cross-border (F=120)     : 37/100
  SPE access-log (F=12)    : 53/100
total constraint violations: 95

Corollary 1.2 witnesses (SPE, NO erasure request, still infeasible): 39
  rid=100: t_a=7 permit expires t_pi=10 -> C3 from t=16, C1 to t=19  | collision at t=16
  rid=103: t_a=7 permit expires t_pi=10 -> C3 from t=16, C1 to t=19  | collision at t=16
  rid=104: t_a=3 permit expires t_pi=4 -> C3 from t=10, C1 to t=15  | collision at t=10

Sample violation witnesses (cross-border):
  C1 requires V=1 (=> alpha=1) at t=116 within [11,131]; C2 requires alpha=0 from t=116
  C1 requires V=1 (=> alpha=1) at t=120 within [4,124]; C2 requires alpha=0 from t=120
  C1 requires V=1 (=> alpha=1) at t=41 within [0,120]; C2 requires alpha=0 from t=41

--------------------------------------------------------------------------
INDEPENDENT CROSS-CHECK: exhaustive search over alpha assignments
--------------------------------------------------------------------------
  SPE, no erasure request, permit 3mo            feasible=False
  SPE, erasure at t=2                            feasible=False
  cross-border scaled (F=12), erasure at t=4     feasible=False
  control: no request, no expiry                 feasible=True

--------------------------------------------------------------------------
SEMANTICS II (accountability preservation)          -> Proposition 2
--------------------------------------------------------------------------
records invalidated        : 138/200
  ground = GDPR Art 17(1)  : 52
  ground = EHDS Art 68(12) : 86
records with >=1 violation : 0/200
total constraint violations: 0

Auditor view of rid=100 after invalidation:
  accessor fields      : True  actor=R-008 permit=DP-015 outcome=success
  subject link         : removed month 16
  commitment c(a)      : 678ade47c1e6dc03296175e056fd8116...
  payload key k(a)     : None   <- destroyed
  salt, ciphertext     : None, None   <- destroyed, deleted
  invalidation iota(a) : month=16 ground=EHDS Art 68(12)
  payload readable?    : False

--------------------------------------------------------------------------
AUDIT-LOG INTEGRITY (Merkle log, RFC 6962 hashing)     -> V_II condition (i)
--------------------------------------------------------------------------
log entries                : 438
log root                   : a91c07936a4eb9752b58c6483ca93d7d...
records verifying          : 200/200
tamper test, rid=100 actor altered : V_II=False  (access entry fails its inclusion proof (altered))
tamper test, rid=100 ground altered: V_II=False  (invalidation entry fails its inclusion proof (altered))
tamper test, rid=3 link altered  : V_II=False  (patient link does not open its logged commitment (altered))
after restoring all three  : V_II=True

==========================================================================
RESULT  Semantics I : 95 violations across 90 records  -> INFEASIBLE
RESULT  Semantics II: 0 violations across 0 records  -> FEASIBLE
==========================================================================
 delta  SemI recs  SemI viol   Cor1.2  SemII recs  SemII viol  invalidated
     1         90         95       39           0           0          138
     3         89         94       39           0           0          138
```

---

## A.19 Console output of the Norwegian context module

Produced by the first command in 6. Illustrative of the Norwegian setting; no figure here is a thesis claim, and the module states so in its own output.

```text
==========================================================================
                             NORWEGIAN LAYER                              
==========================================================================

class           n  SemI recs  SemI viol  invalidated  SemII viol
NO-JOURNAL     40         12         12           12           0
NO-SPE         60         36         40           60           0
NO-XB          60         20         20           23           0

TOTAL         160         68         72           95           0

--------------------------------------------------------------------------
CASE WALKTHROUGHS
--------------------------------------------------------------------------

NO-JOURNAL  rid=121  (pasientjournalloven s 25 (purpose-based, indefinite))
  floor    : t=0 .. 600   [indefinite, truncated]
  erasure  : t_r=10 -> deadline 11
  ceiling  : n/a
  collision: C2 at t=11
  after invalidation -> metadata intact=True, commitment=c8eb840b7abcb3e4..., key=None, salt=None, ground=GDPR Art 17(1)

NO-SPE  rid=61  (controller-provided server)
  floor    : t=10 .. 22
  erasure  : none
  ceiling  : t_pi=15 -> 21
  collision: C3 at t=21
  after invalidation -> metadata intact=True, commitment=900dc608470b8289..., key=None, salt=None, ground=EHDS Art 68(12)

NO-XB  rid=1  (Bodo legevakt)
  floor    : t=4 .. 124
  erasure  : t_r=119 -> deadline 120
  ceiling  : n/a
  collision: C2 at t=120
  after invalidation -> metadata intact=True, commitment=af06e57b08ba4cf8..., key=None, salt=None, ground=GDPR Art 17(1)

Note: figures above are illustrative of the Norwegian setting, not
empirical. The canonical result of the thesis is unchanged and is
reproduced by running trf_checker.py on its own.
```

---

## A.20 Console output of the cross-sector instance

Produced by the second command in 6, and discussed in Chapter 6, Section 6.10. The zero in the second row is the finding: § 17 fixes both its limbs from the same origin, so it bounds a retention window rather than contradicting itself, and every collision the model finds is erasure-driven.

```text
==========================================================================
  CROSS-SECTOR INSTANCE: politiregisterloven s 17 (floor 12, ceiling 36)  
==========================================================================

records                              : 60
Semantics I, records with violation  : 7
  of which with NO erasure request   : 0  <- floor vs ceiling alone
Semantics II, total violations       : 0
records invalidated                  : 60

No structural collision: s 17 orders its two limbs from one origin
(floor at t_a + 12, ceiling at t_a + 36), so the provision defines a
bounded retention window rather than a contradiction. Every collision
found is erasure-driven.

witness rid=906: log written t=0; floor to t=12; ceiling at t=36; erasure deadline 11; collision C2 at t=11

The floor parameter F(a) took a third value with no change to the model.
The finding: floors and ceilings coexist when one instrument fixes both from
the same origin, and collide when the ceiling is anchored to an external
event, as Art 68(12) anchors it to permit expiry. Scope: a structural
parallel. Whether the mechanism transfers to a record-level ceiling is a
design question this module does not answer.
```

---

## A.21 Console output of the payload-provenance comparison, committed subset

Produced by command 4 against the eight bundles committed at `data/synthea_subset/`, which is what a reader who clones the repository obtains without regenerating anything. Chapter 5, Section 5.8 reports both cohort sizes because one figure changes and the rest do not: the mean payload is 891 bytes here against 1,006 for the full cohort, while all six measures and all 200 differing commitments are identical. That the measures hold across cohort size and across payload repetition frequency is a stronger result than a single substitution would give.

```text
==========================================================================
     SYNTHEA REALISM LAYER — comparison against constructed payloads      
==========================================================================

Synthea bundles read : 8
clinical payloads    : 8
records              : 200
payload bytes (mean) : constructed=43  synthea=891

--------------------------------------------------------------------------
measure                                       constructed        synthea
--------------------------------------------------------------------------
Semantics I: records with violation                    90             90
Semantics I: total violations                          95             95
Corollary 1.2 witnesses (no request)                   39             39
Records invalidated                                   138            138
Semantics II: records with violation                    0              0
Semantics II: total violations                          0              0
--------------------------------------------------------------------------

commitments differing between the two runs: 200/200   (expected 200 — same salt, different payload)

==========================================================================
   RESULT: every reported figure is IDENTICAL under real FHIR payloads,   
   while every commitment differs. The model reads timing, not content.   
==========================================================================
```


---

## A.22 Console output of the envelope-encryption module

Verbatim output of `python3 crypto_envelope.py`. Keys are random on every run; the counts are the same on every run. All 200 records decrypt before invalidation; after the 138 data keys due for destruction are destroyed, those 138 records are refused and the other 62 still read, and the ciphertext of an invalidated record opens under none of the surviving keys.

```text
==========================================================================
           ENVELOPE ENCRYPTION (AES-256-GCM, wrapped data keys)           
==========================================================================
records encrypted                     : 200
decrypt and match before invalidation : 200/200
data keys destroyed (t_I finite)      : 138
decryptable after invalidation        : 62  (expected 62)
refused, key destroyed                : 138  (expected 138)
rid=3 ciphertext tried under 62 surviving keys : opened 0
ciphertexts kept after deletion       : 62
==========================================================================
RESULT: every invalidated record is unrecoverable; every other record reads
==========================================================================
```

## A.23 Source listing: `z3_check.py`

Optional module. It poses each of Propositions 1–3 to the Z3 SMT solver as a request for a counterexample within stated bounds, and checks that deliberately wrong versions of Proposition 3 are refuted (Chapter 5, Section 5.5). It reports no thesis figure from the generated population.

```python
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
```

## A.24 Console output of the bounded SMT check

Verbatim output of `python3 z3_check.py` (Z3 5.1.0). Nine checks find no counterexample; the sanity check finds a satisfying trajectory and the mutation check finds counterexamples, as they must.

```text
====================================================================================================
                             BOUNDED SMT CHECK OF PROPOSITIONS 1-3 (Z3)                             
====================================================================================================
bounds: t_a 0..12, F 1..120, delta 1..3, t_r and e in [t_a, 140], L 1..120, horizon 140
P1  deadline inside window => no trajectory satisfies C1-C3 (Sem I)        unsat (no counterexample)
P1  no deadline inside window => witness trajectory satisfies C1-C3        unsat (no counterexample)
P2  constructive trajectory satisfies C1 (Sem II), C2, C3 for all inputs   unsat (no counterexample)
mutation: construction without iota / without c / without iota_subj refuted sat, counterexamples found (as expected)
P3  e + L <= t_a + F => floor and ceiling not jointly satisfiable          unsat (no counterexample)
P3  e + L > t_a + F => witness satisfies floor and ceiling                 unsat (no counterexample)
P3(i)  e = t_a: jointly satisfiable only if L > F                          unsat (no counterexample)
P3(i)  e = t_a and L > F: witness satisfies floor and ceiling              unsat (no counterexample)
P3(ii) L <= F, e - t_a <= F - L => collision                               unsat (no counterexample)
P3(ii) L <= F, e - t_a >  F - L => witness satisfies both                  unsat (no counterexample)
sanity: no request, no ceiling => some trajectory satisfies C1             sat (as expected)
mutation: Proposition 3 with an off-by-one condition is refuted            sat, counterexample found (as expected)
====================================================================================================
RESULT: 9/9 checks found no counterexample; sanity and mutation checks passed
====================================================================================================
```
