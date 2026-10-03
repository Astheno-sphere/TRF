# Version and Change Record

This thesis and its artefact are versioned together. The table records what changed, when, and what verified it, so that a reader comparing the document against the published repository can tell which of the two moved if a figure disagrees. The full trail, with an identifier for every individual change, is maintained alongside the artefact.

*Table F.1. Document and artefact versions*

| Date | Document | Artefact | What changed | Verification |
|---|---|---|---|---|
| 16 Sept 2026 | Chapters 1–7 assembled | `trf_checker.py`, `synthea_layer.py` | First complete draft; the checker and the realism layer written and run | Checker output recorded |
| 18 Sept 2026 | Appendix A written | — | Provenance of the synthetic cohort established by inspecting the bundles rather than by recollection | Six Synthea markers confirmed in every bundle |
| 19 Sept 2026 | §5.5a added | `--delta-witness` added | The erasure response period tested at δ = 3 rather than asserted | Table 5.2a produced by execution |
| 21 Sept 2026 | §4.8 terminal transition; mathematics to LaTeX | Salt destroyed with the key | A reviewer-found gap at the end of the record's life closed; 159 equations converted | Checker output unchanged, byte for byte |
| 23 Sept 2026 | — | Repository published | Code and documents pushed to GitHub; demonstration deployed | — |
| 28 Sept 2026 | §5.2 line counts corrected; §6.9a added; Appendix A extended | Eight-bundle subset committed; Tab 5 added; five recorded runs committed | The dataset the thesis reports on made obtainable; the two robustness results given a viewer; the cross-sector instance carried into the discussion | Verified from a fresh clone: checker byte-identical to its recorded run, realism layer 891 bytes and six identical measures |
| 28 Sept 2026 | Bibliography linked | — | Every entry given a DOI or URL that was fetched; two entries removed as documents that do not exist as cited; six citations corrected on year, title or author | 67 of 67 entries carry a locator |

*Table F.2. The artefact at the date of submission*

| Module | Lines | Reports a thesis figure? |
|---|---|---|
| `trf_checker.py` | 533 | Yes — Tables 5.1, 5.2a, 5.3 |
| `synthea_layer.py` | 152 | Yes — Table 5.4 |
| `norwegian_layer.py` | 135 | No — illustrative |
| `cross_sector_check.py` | 110 | No — illustrative, discussed at §6.9a |
| `app.py` | 526 | No — a viewer, never a source |

Repository: https://github.com/Astheno-sphere/TRF · Demonstration: https://trfhimolde.streamlit.app/

Published commits, most recent first:

```text
  0d855a7  28 Sep 2026  Add Tab 5 robustness checks and a recorded run per command
  88840a6  28 Sep 2026  Record R-09 to R-11 and refresh checksums
  cc0d7f3  28 Sep 2026  Appendix A: drop the norwegian/ path prefix
  d79b96f  28 Sep 2026  Ship the Synthea subset and repair the flattened upload
  03048f2  23 Sep 2026  Add files via upload
```

Two corrections are recorded here because they were made against the thesis's own earlier claims rather than in response to a reviewer. An inference dating a source from the age of its web page was withdrawn, the page being updated in place and its age therefore saying nothing about its contents. And a statement that the artefact's code carried a comment recommending a cryptographically secure random source was removed, no such comment existing; the salt's reproducibility-only status is now stated directly instead.

*Moved here from the thesis front matter on 3 October 2026 at the supervisor's request (review of 30
September: "move the Version and Change Record to the repository"). Entries after 29 September are in
`CHANGE_TRAIL.md` (R- identifiers) and in the thesis's own change trail. Table F.2 was last updated on
3 October; current line counts are in `README.md` and `CHECKSUMS.md`.*
