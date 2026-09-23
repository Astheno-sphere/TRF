# Pushing this to github.com/Astheno-sphere/TRF

The repository currently holds an older checker, so Appendix A's listing and the live demo no longer match it. This bundle is the version after the pass-2 salt change and all later patching.

## What changed since the repo was last updated

- `trf_checker.py` is 363 lines. `apply_invalidation` now destroys the commitment salt along with the key: `rec.salt = None`. That is the only code change, and the run output is unchanged.
- The Synthea subset is included, so the demo's Tab 3 will work.
- The Norwegian modules and their documentation are new.

## Steps

```bash
cd /path/to/your/local/TRF
git pull

# copy the bundle over the working tree
cp -r 10_GitHub_Push/src/* .
mkdir -p norwegian data/synthea_subset docs
cp -r 10_GitHub_Push/norwegian/* norwegian/
cp -r 10_GitHub_Push/data/synthea_subset/* data/synthea_subset/
cp -r 10_GitHub_Push/docs/* docs/
cp 10_GitHub_Push/README.md .

# verify BEFORE committing
python3 trf_checker.py > /tmp/run.txt
diff /tmp/run.txt docs/expected_trf_output.txt && echo MATCHES

git add -A
git commit -m "Checker v2: destroy commitment salt at invalidation; add Norwegian modules and Synthea subset"
git push
```

If the diff does not print MATCHES, stop and tell me. Do not push a checker whose output disagrees with Chapter 5.

## After pushing

1. Check that the Streamlit demo reloads and that Tab 3 finds the bundles.
2. Mint the Zenodo DOI from the repository, then send me the DOI so Appendix A §A.1 can cite it.
3. The subset is about 40 MB. That is fine for GitHub, but if you would rather keep the repository light, trim each bundle to its first 25 entries and note the trimming in Appendix A §A.5. The payload-independence result holds either way.

## One caveat to keep honest

Appendix A §A.1b and §A.5 currently describe three bundles trimmed to 25 entries, which is what `code_artefacts/synthea_sample/` holds. Once you push 8 untrimmed bundles, those two passages need a one-line update. Tell me when the push is done and I will patch them with a trail row.
