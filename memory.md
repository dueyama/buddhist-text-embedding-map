# Local Project Memory

This file records local project changes for the Okyou experiments. Times are JST.

## 2026-06-01 17:33 JST

- Summary: Initialized local project governance files for git-managed research work.
- Files:
  - `AGENTS.md`
  - `.gitignore`
  - `memory.md`
- Verification:
  - Confirmed this directory was not previously a git repository.
  - Confirmed `.env` exists and must remain untracked.
  - Confirmed legacy notebooks/scripts contain hardcoded API keys and must not be staged.
- Commit: `183a5f88e30101fc28a63aee37895715876eb02d`

## 2026-06-01 17:35 JST

- Summary: Added planning documents for the Japanese Kanbun style map and sect-based sutra map.
- Files:
  - `docs/kanbun-style-map-plan.md`
  - `docs/sect-sutra-map-plan.md`
- Verification:
  - Checked planned commit files for hardcoded API key patterns.
  - Confirmed staged files before committing.
- Commit: `f37b02dda979138c8ba821916543de4b8f03a914`

## 2026-06-01 17:35 JST

- Summary: Added the initial results note for the Amitabha Sutra two-translation comparison.
- Files:
  - `docs/results.md`
- Verification:
  - Read `experiments/amida_compare/outputs/summary.json` and copied the key metrics into the results note.
  - Checked planned commit files for hardcoded API key patterns.
  - Confirmed staged files before committing.
- Commit: `6c0a0439df63b8753bc5d2c45ed56ff64fd43fec`

## 2026-06-01 17:36 JST

- Summary: Recorded the actual commit hash for the initial results-note commit.
- Files:
  - `memory.md`
- Verification:
  - Read `git rev-parse HEAD` after the results-note commit.
- Commit: this entry is committed by the next memory-only commit; its hash is reported in the assistant summary to avoid an infinite self-reference.

## 2026-06-01 17:43 JST

- Summary: Added the v0 manifest for the sect-based sutra map.
- Files:
  - `experiments/sect_sutra_map/manifest.json`
- Verification:
  - Ran `python3 -m json.tool experiments/sect_sutra_map/manifest.json`.
  - Checked the planned commit file for hardcoded API key patterns.
- Commit: `8fb832eef7106d828ad92fa39a62dcc816b5c4ec`

## 2026-06-01 17:45 JST

- Summary: Added the corpus builder and shared helpers for SAT/local text processing.
- Files:
  - `experiments/sect_sutra_map/common.py`
  - `experiments/sect_sutra_map/build_corpus.py`
- Verification:
  - Ran `python3 -m py_compile experiments/sect_sutra_map/common.py experiments/sect_sutra_map/build_corpus.py`.
  - Checked planned commit files for hardcoded API key patterns.
- Commit: `af741f7b9d4a19a25c055cc3c4cb54458532e29f`

## 2026-06-01 17:47 JST

- Summary: Added the OpenAI embedding pipeline with chunk-level cache support.
- Files:
  - `experiments/sect_sutra_map/embed_texts.py`
- Verification:
  - Ran `python3 -m py_compile experiments/sect_sutra_map/embed_texts.py`.
  - Checked the planned commit file for hardcoded API key patterns.
- Commit: `93ad4b31d1947cfbe1f9445e9f0d818c16a99ba2`

## 2026-06-01 17:49 JST

- Summary: Added viewer-data export for coordinates, sect centroids, similarities, and nearest neighbors.
- Files:
  - `experiments/sect_sutra_map/make_viewer_data.py`
- Verification:
  - Ran `python3 -m py_compile experiments/sect_sutra_map/make_viewer_data.py`.
  - Checked the planned commit file for hardcoded API key patterns.
- Commit: `4b6d8722ff089c168f5e18dcef913d077bf2ac40`

## 2026-06-01 17:51 JST

- Summary: Added the static web viewer for the sect-based sutra map.
- Files:
  - `experiments/sect_sutra_map/viewer/index.html`
- Verification:
  - Read the beginning of the HTML file for sanity.
  - Checked the planned commit file for hardcoded API key patterns.
- Commit: `c45805776141df9c8231035e0b4c93a2ae80feb3`

## 2026-06-01 17:53 JST

- Summary: Fixed SAT row parsing for direct SAT pages where refs and body text are split across span/a tags.
- Files:
  - `experiments/sect_sutra_map/common.py`
- Verification:
  - Ran `python3 -m py_compile experiments/sect_sutra_map/common.py experiments/sect_sutra_map/build_corpus.py`.
  - Parsed cached `t0360_larger_sukhavati.html` and confirmed 638 SAT rows with body text.
  - Checked the planned commit file for hardcoded API key patterns.
- Commit: `d407ab19c0592b3cb22fca89f81179daee1d4be5`

## 2026-06-01 17:57 JST

- Summary: Generated the sect map v0 corpus, embeddings, viewer data, and documented the initial results.
- Files:
  - `docs/results.md`
- Verification:
  - Ran `python3 experiments/sect_sutra_map/build_corpus.py`.
  - Ran `python3 experiments/sect_sutra_map/embed_texts.py`.
  - Ran `python3 experiments/sect_sutra_map/embed_texts.py --no-api` and confirmed `403` cache hits, `0` misses.
  - Ran `python3 experiments/sect_sutra_map/make_viewer_data.py`.
  - Ran `python3 -m json.tool experiments/sect_sutra_map/outputs/viewer_data.json`.
  - Served the viewer locally and captured `/private/tmp/okyou-sect-map.png` with headless Chrome.
- Commit: `d015b7cbe9f5a951284b53357d0714a86e905a4b`

## 2026-06-01 17:58 JST

- Summary: Recorded the actual commit hash for the sect map v0 results commit.
- Files:
  - `memory.md`
- Verification:
  - Read `git rev-parse HEAD` after the results commit.
- Commit: this entry is committed by the next memory-only commit; its hash is reported in the assistant summary to avoid an infinite self-reference.

## 2026-06-01 18:12 JST

- Summary: Added translator comparison support with additional Xuanzang texts and translator centroids in the viewer data.
- Files:
  - `experiments/sect_sutra_map/manifest.json`
  - `experiments/sect_sutra_map/make_viewer_data.py`
  - `experiments/sect_sutra_map/viewer/index.html`
- Verification:
  - Ran `python3 -m json.tool experiments/sect_sutra_map/manifest.json`.
  - Ran `python3 -m py_compile experiments/sect_sutra_map/*.py`.
  - Checked the planned commit files for hardcoded API key patterns.
- Commit: `0d2bb76ac3599b96ba6710b41e2ed991722d0400`

## 2026-06-01 18:15 JST

- Summary: Generated the translator comparison corpus, embeddings, viewer data, and documented the v0.1 result.
- Files:
  - `docs/results.md`
- Verification:
  - Ran `python3 experiments/sect_sutra_map/build_corpus.py` and confirmed `15` texts.
  - Ran `python3 experiments/sect_sutra_map/embed_texts.py` and embedded `30` new chunks with `20869` API tokens.
  - Ran `python3 experiments/sect_sutra_map/embed_texts.py --no-api` and confirmed `433` cache hits, `0` misses.
  - Ran `python3 experiments/sect_sutra_map/make_viewer_data.py` and confirmed `3` translator centroids.
  - Validated `experiments/sect_sutra_map/outputs/viewer_data.json` with `python3 -m json.tool`.
  - Captured `/private/tmp/okyou-translator-map.png` with headless Chrome.
- Commit: `433e5e75974581d0e9e2a6f8665781a1ce1c1368`

## 2026-06-01 18:23 JST

- Summary: Added a Japanese paper-style draft summarizing the sect sutra map and translator comparison results.
- Files:
  - `docs/sect-sutra-map-paper-draft.md`
- Verification:
  - Read the draft with `sed` to check structure and wording.
  - Checked for leftover English section headings and common placeholder markers.
  - Checked the planned commit files for hardcoded API key patterns.
- Commit: `69008a4a13c4da6ea775725a853d03e7e2b2ae0d`
