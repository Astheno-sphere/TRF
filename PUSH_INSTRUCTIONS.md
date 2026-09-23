# Pushing to github.com/Astheno-sphere/TRF — second upload

The first upload landed `trf_checker.py` (363 lines, correct), `app.py`, `synthea_layer.py` and a placeholder README. This upload adds what is missing and fixes Tab 3.

## Important: the layout is now flat

Streamlit Cloud runs `app.py` from the repository root and imports modules beside it. So every Python file sits at the root, not in `src/`. Do not move them into folders or the app will fail on import.

```
trf_checker.py            # unchanged from your first upload
synthea_layer.py          # UPDATED: now also looks in data/synthea_subset/
app.py                    # UPDATED: new Tab 4, Norwegian context
norwegian_layer.py        # new
cross_sector_check.py     # new
requirements.txt
data/synthea_subset/      # new, 8 bundles, this is what fixes Tab 3
docs/Appendix_A.md
docs/expected_trf_output.txt
norwegian_docs/           # module README and the run-and-demo guide
README.md
```

## Steps

```bash
cd /path/to/local/TRF
git pull

# copy everything from this bundle into the repository root
cp -r /path/to/10_GitHub_Push/* .
rm -f PUSH_INSTRUCTIONS.md CHECKSUMS.md      # these two are for you, not the repo

# verify before committing
python3 trf_checker.py > /tmp/run.txt
diff /tmp/run.txt docs/expected_trf_output.txt && echo MATCHES
python3 synthea_layer.py | grep "bundles read"      # expect 8

git add -A
git commit -m "Add Synthea subset, Norwegian modules and Tab 4; layer now finds the subset"
git push
```

If the diff does not print MATCHES, stop and tell me.

## After pushing

1. Open the Streamlit app. Tab 3 should now report 8 bundles and a mean payload of 891 bytes. Tab 4 is new.
2. In the repository About panel, add a description and topics. It currently says none are provided.
3. Add a licence: MIT for the code, CC BY 4.0 for the documents.
4. Mint the Zenodo DOI and send it to me for Appendix A §A.1.
