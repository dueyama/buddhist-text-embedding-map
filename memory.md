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

## 2026-06-01 18:43 JST

- Summary: Installed a lightweight local TeX engine and generated the figure-included Japanese paper PDF.
- Files:
  - `experiments/sect_sutra_map/make_paper_figures.py`
  - `docs/figures/sect-sutra-semantic-map.png`
  - `docs/figures/sect-sutra-similarity-heatmap.png`
  - `docs/figures/amida-two-translation-comparison.png`
  - `docs/paper/sect-sutra-map-paper.tex`
  - `docs/paper/sect-sutra-map-paper.pdf`
- Verification:
  - Tried `brew install --cask basictex`; download succeeded but installation required an administrator password, so it was not completed by Codex.
  - Installed `tectonic` with Homebrew and verified `Tectonic 0.16.9`.
  - Compiled a minimal Japanese TeX smoke test to PDF.
  - Ran `python3 experiments/sect_sutra_map/make_paper_figures.py`.
  - Ran `python3 -m py_compile experiments/sect_sutra_map/make_paper_figures.py`.
  - Ran `tectonic sect-sutra-map-paper.tex --outdir .`.
  - Rendered the PDF first-page Quick Look thumbnail and confirmed Japanese text and the `要旨` heading.
  - Checked the planned commit files for hardcoded API key patterns.
- Commit: `eed853b552a8a728c31741c10830074ce648f285`

## 2026-06-01 19:22 JST

- Summary: Rebuilt the paper PDF with BasicTeX using upLaTeX and dvipdfmx instead of the earlier XeLaTeX/Tectonic route.
- Files:
  - `.gitignore`
  - `docs/paper/sect-sutra-map-paper.tex`
  - `docs/paper/sect-sutra-map-paper.pdf`
- Verification:
  - Confirmed `uplatex`, `dvipdfmx`, `latexmk`, and `tlmgr` under `/Library/TeX/texbin`.
  - Compiled a minimal `jsarticle` Japanese smoke test with `uplatex` and `dvipdfmx`.
  - Ran `uplatex -interaction=nonstopmode sect-sutra-map-paper.tex` twice.
  - Ran `dvipdfmx sect-sutra-map-paper.dvi`.
  - Rendered the PDF first-page Quick Look thumbnail and confirmed Japanese text.
  - Added LaTeX intermediate patterns to `.gitignore` and removed generated `aux`, `dvi`, `log`, and `out` files.
  - Checked the planned commit files for hardcoded API key patterns.
- Commit: `1cf10f30bacfdf16a82b960875407d2c26b87db9`

## 2026-06-01 19:35 JST

- Summary: Added the J-SOKEN source credit for the local Kyogyoshinsho text and moved the Figure 1 legend below the semantic map so it does not hide plotted labels.
- Files:
  - `experiments/sect_sutra_map/manifest.json`
  - `experiments/sect_sutra_map/build_corpus.py`
  - `experiments/sect_sutra_map/make_paper_figures.py`
  - `docs/results.md`
  - `docs/sect-sutra-map-paper-draft.md`
  - `docs/figures/sect-sutra-semantic-map.png`
  - `docs/paper/sect-sutra-map-paper.tex`
  - `docs/paper/sect-sutra-map-paper.pdf`
- Verification:
  - Ran `python3 -m json.tool experiments/sect_sutra_map/manifest.json`.
  - Ran `python3 -m py_compile experiments/sect_sutra_map/build_corpus.py experiments/sect_sutra_map/common.py experiments/sect_sutra_map/embed_texts.py experiments/sect_sutra_map/make_viewer_data.py experiments/sect_sutra_map/make_paper_figures.py`.
  - Ran `python3 experiments/sect_sutra_map/build_corpus.py` and confirmed `15` non-empty texts.
  - Ran `python3 experiments/sect_sutra_map/embed_texts.py --no-api` and confirmed `433` cache hits, `0` misses, and `0` API tokens.
  - Ran `python3 experiments/sect_sutra_map/make_viewer_data.py` and confirmed `15` texts, `433` chunks, `11` sect centroids, and `3` translator centroids.
  - Ran `python3 experiments/sect_sutra_map/make_paper_figures.py` and visually checked `docs/figures/sect-sutra-semantic-map.png`.
  - Ran `uplatex -interaction=nonstopmode sect-sutra-map-paper.tex` twice and `dvipdfmx sect-sutra-map-paper.dvi`.
  - Rendered the PDF first-page Quick Look thumbnail and confirmed Japanese text.
  - Checked the planned commit files for hardcoded API key patterns.
- Commit: `9592ef602f02e7c7e17d9a117e543d264d485637`

## 2026-06-01 19:41 JST

- Summary: Added a v0 plan for cross-lingual sutra comparison, focusing first on whether parallel Chinese, Tibetan-derived English, and later Tibetan texts cluster by meaning across languages.
- Files:
  - `docs/multilingual-sutra-map-plan.md`
- Verification:
  - Reviewed the document with `sed`.
  - Checked the planned commit file for hardcoded API key patterns.
- Commit: `cbda8ea94c2ab11c2585ed02c4bc229e08c2e6ba`

## 2026-06-01 19:55 JST

- Summary: Implemented and ran a cross-language sutra pilot using SAT `T0676` and 84000 `Toh 106` English translation against Chinese controls; the 84000 English text's nearest Chinese text was the matching `T0676`.
- Files:
  - `docs/multilingual-sutra-map-plan.md`
  - `docs/results.md`
  - `experiments/multilingual_sutra_map/manifest.json`
  - `experiments/multilingual_sutra_map/run_pilot.py`
- Verification:
  - Downloaded the 84000 `Toh 106` HTML into ignored raw cache.
  - Ran `python3 -m json.tool experiments/multilingual_sutra_map/manifest.json`.
  - Ran `python3 -m py_compile experiments/multilingual_sutra_map/run_pilot.py`.
  - Ran `python3 experiments/multilingual_sutra_map/run_pilot.py`, embedding `105` chunks with `71630` API tokens.
  - Ran `python3 experiments/multilingual_sutra_map/run_pilot.py --no-api` and confirmed `105` cache hits, `0` misses, and `0` API tokens.
  - Validated `experiments/multilingual_sutra_map/outputs/pilot_results.json` with `python3 -m json.tool`.
  - Checked the planned commit files for hardcoded API key patterns.
- Commit: `cb2aa95efb8b74bb6b47834e9d64a2fa6c60b59c`

## 2026-06-01 20:34 JST

- Summary: Updated the paper PDF to include the multilingual sutra pilot result for SAT `T0676` and 84000 `Toh 106`.
- Files:
  - `docs/paper/sect-sutra-map-paper.tex`
  - `docs/paper/sect-sutra-map-paper.pdf`
- Verification:
  - Ran `uplatex -interaction=nonstopmode sect-sutra-map-paper.tex` twice.
  - Ran `dvipdfmx sect-sutra-map-paper.dvi`.
  - Rendered the PDF first-page Quick Look thumbnail and confirmed Japanese text and the updated multilingual title.
  - Checked the planned commit files for hardcoded API key patterns.
- Commit: `e3770e0ce094b23de6e62af16cf0ef29fda62db7`

## 2026-06-01 21:15 JST

- Summary: Removed user-facing `local` source labels for Kyogyoshinsho, treating it as J-SOKEN Seikyo DB sourced text, and regenerated the corpus metadata, viewer data, and paper PDF.
- Files:
  - `experiments/sect_sutra_map/build_corpus.py`
  - `experiments/sect_sutra_map/manifest.json`
  - `docs/paper/sect-sutra-map-paper.tex`
  - `docs/paper/sect-sutra-map-paper.pdf`
  - `docs/sect-sutra-map-paper-draft.md`
  - `docs/results.md`
- Verification:
  - Ran `python3 -m json.tool experiments/sect_sutra_map/manifest.json`.
  - Ran `python3 -m py_compile experiments/sect_sutra_map/build_corpus.py experiments/sect_sutra_map/common.py experiments/sect_sutra_map/embed_texts.py experiments/sect_sutra_map/make_viewer_data.py`.
  - Ran `python3 experiments/sect_sutra_map/build_corpus.py` and confirmed `15` texts.
  - Ran `python3 experiments/sect_sutra_map/embed_texts.py --no-api` and confirmed `433` cache hits, `0` misses, and `0` API tokens.
  - Ran `python3 experiments/sect_sutra_map/make_viewer_data.py`.
  - Ran `uplatex -interaction=nonstopmode sect-sutra-map-paper.tex` twice and `dvipdfmx sect-sutra-map-paper.dvi`.
  - Rendered the PDF first-page Quick Look thumbnail and confirmed Japanese text.
  - Checked the planned commit files for hardcoded API key patterns.
- Commit: `ebb920150384cede81a38608f04f1bc68da5ee69`

## 2026-06-01 22:43 JST

- Summary: Added chunk distribution figures and high-dimensional chunk neighbor mixing to the paper so the final PDF shows both mean points and text-internal spread/overlap.
- Files:
  - `experiments/sect_sutra_map/make_paper_figures.py`
  - `docs/figures/sect-sutra-semantic-map.png`
  - `docs/figures/sect-sutra-chunk-distribution-overview.png`
  - `docs/figures/sect-sutra-chunk-distribution-focus.png`
  - `docs/figures/sect-sutra-chunk-overlap-heatmap.png`
  - `docs/figures/sect-sutra-similarity-heatmap.png`
  - `docs/figures/amida-two-translation-comparison.png`
  - `docs/paper/sect-sutra-map-paper.tex`
  - `docs/paper/sect-sutra-map-paper.pdf`
  - `docs/results.md`
- Verification:
  - Ran `python3 -m py_compile experiments/sect_sutra_map/make_paper_figures.py`.
  - Ran `python3 experiments/sect_sutra_map/make_paper_figures.py` and visually checked the three new chunk distribution figures.
  - Ran `uplatex -interaction=nonstopmode sect-sutra-map-paper.tex` twice and `dvipdfmx sect-sutra-map-paper.dvi`.
  - Rendered the PDF first-page Quick Look thumbnail and confirmed Japanese text.
  - Checked the planned commit files for hardcoded API key patterns.
- Commit: `f3eefacfaff5a454287e018a6c4d7c84eb563f75`

## 2026-06-01 23:00 JST

- Summary: Added an overlap-vs-centroid scatter plot and bridge chunk table, with explicit interpretation of Kyogyoshinsho's partial overlap with the Pure Land three sutras.
- Files:
  - `experiments/sect_sutra_map/make_paper_figures.py`
  - `docs/figures/sect-sutra-chunk-overlap-heatmap.png`
  - `docs/figures/sect-sutra-overlap-vs-centroid.png`
  - `docs/paper/sect-sutra-map-paper.tex`
  - `docs/paper/sect-sutra-map-paper.pdf`
  - `docs/results.md`
  - `memory.md`
- Verification:
  - Ran `python3 -m py_compile experiments/sect_sutra_map/make_paper_figures.py`.
  - Ran `python3 experiments/sect_sutra_map/make_paper_figures.py` and checked the new scatter figure visually.
  - Ran `uplatex -interaction=nonstopmode sect-sutra-map-paper.tex` twice and `dvipdfmx sect-sutra-map-paper.dvi`.
  - Checked the LaTeX log for overfull boxes and undefined references.
  - Rendered the PDF first-page Quick Look thumbnail and confirmed Japanese text.
  - Checked the planned commit files for hardcoded API key patterns.
- Commit: `9b3a8951fb8629f581df3af497fa6f7eed123354`

## 2026-06-02 00:19 JST

- Summary: Added a Shinran-side Amida source attribution pilot, separating explicit citation labels, translation-specific markers, and semantic chunk affinity for `T0366` / `T0367`.
- Files:
  - `experiments/shinran_amida_sources/manifest.json`
  - `experiments/shinran_amida_sources/run_analysis.py`
  - `docs/shinran-amida-source-analysis.md`
  - `docs/figures/shinran-amida-source-markers.png`
  - `docs/figures/shinran-kyogyoshinsho-amida-chunk-affinity.png`
  - `docs/paper/sect-sutra-map-paper.tex`
  - `docs/paper/sect-sutra-map-paper.pdf`
  - `docs/results.md`
  - `memory.md`
- Verification:
  - Ran `python3 -m py_compile experiments/shinran_amida_sources/run_analysis.py`.
  - Ran `python3 -m json.tool experiments/shinran_amida_sources/manifest.json`.
  - Ran `python3 experiments/shinran_amida_sources/run_analysis.py` and confirmed marker summary, text-level similarities, chunk affinities, and generated figures.
  - Validated `experiments/shinran_amida_sources/outputs/analysis_results.json` with `python3 -m json.tool`.
  - Ran `uplatex -interaction=nonstopmode sect-sutra-map-paper.tex` twice and `dvipdfmx sect-sutra-map-paper.dvi`.
  - Checked the LaTeX log for overfull boxes and undefined references.
  - Rendered Quick Look thumbnails for PDF pages 1, 9, and 10 and confirmed Japanese text plus the new Shinran figures.
  - Checked the planned commit files for hardcoded API key patterns.
- Commit: `92926a51437154e86aa59ffc0078e2aee7b81250`
