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
  - Confirmed legacy notebooks/scripts may contain secrets and must not be staged.
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
  - Served the viewer locally and captured a headless Chrome screenshot for visual checking.
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
  - Captured a headless Chrome screenshot for visual checking.
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
  - Confirmed `uplatex`, `dvipdfmx`, `latexmk`, and `tlmgr` were available in the local TeX path.
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

## 2026-06-02 01:46 JST

- Summary: Addressed the attached review comments for the sect sutra map paper by softening claims, expanding reproducibility details, adding corpus statistics, PCA variance, top-k sensitivity checks, and a response checklist.
- Files:
  - `docs/paper/sect-sutra-map-paper.tex`
  - `docs/paper/sect-sutra-map-paper.pdf`
  - `docs/results.md`
  - `docs/sect-sutra-map-review-response.md`
  - `experiments/sect_sutra_map/make_paper_figures.py`
  - `experiments/sect_sutra_map/review_stats.py`
  - `docs/figures/sect-sutra-semantic-map.png`
  - `docs/figures/sect-sutra-chunk-distribution-overview.png`
  - `docs/figures/sect-sutra-chunk-distribution-focus.png`
  - `memory.md`
- Verification:
  - Ran `python3 -m py_compile experiments/sect_sutra_map/make_paper_figures.py experiments/sect_sutra_map/review_stats.py`.
  - Ran `python3 experiments/sect_sutra_map/review_stats.py` and confirmed PCA variance, corpus table, and Amida top-k sensitivity output.
  - Ran `python3 experiments/sect_sutra_map/make_paper_figures.py` and regenerated the paper figures.
  - Ran `uplatex -interaction=nonstopmode sect-sutra-map-paper.tex` twice and `dvipdfmx sect-sutra-map-paper.dvi`.
  - Checked the LaTeX log for overfull boxes and undefined references; only known caption and underfull warnings remained.
  - Rendered Quick Look thumbnails for PDF pages 1, 2, 8, and 10 and confirmed the revised Japanese paper, corpus table, sensitivity table, and Amida metric table.
  - Checked the planned commit files for hardcoded API key patterns.
- Commit: `fcc17861a943667608338ceb011894e895f3497d`

## 2026-06-02 02:19 JST

- Summary: Applied the second review report's minor revisions to the sect sutra map paper, including author placeholder replacement, table and figure label fixes, complete-mixing terminology, corpus notes, and final PDF regeneration.
- Files:
  - `docs/paper/sect-sutra-map-paper.tex`
  - `docs/paper/sect-sutra-map-paper.pdf`
  - `docs/figures/amida-two-translation-comparison.png`
  - `docs/results.md`
  - `docs/sect-sutra-map-review-response.md`
  - `experiments/sect_sutra_map/make_paper_figures.py`
  - `memory.md`
- Verification:
  - Checked T0365 and T0279 translator name forms against online catalog/search sources before editing notes.
  - Ran `python3 -m py_compile experiments/sect_sutra_map/make_paper_figures.py experiments/sect_sutra_map/review_stats.py`.
  - Ran `python3 experiments/sect_sutra_map/make_paper_figures.py` and regenerated the Amida comparison figure.
  - Ran `uplatex -interaction=nonstopmode sect-sutra-map-paper.tex` and `dvipdfmx sect-sutra-map-paper.dvi`.
  - Checked the LaTeX log for overfull boxes and undefined references; only known caption and underfull warnings remained.
  - Rendered Quick Look thumbnails for PDF pages 1, 2, 8, 9, 10, 14, and 15 and confirmed the author line, corpus table, complete-mixing table, Figure 7 labels, conclusion, and references.
  - Checked the planned commit files for hardcoded API key patterns.
- Commit: `17739d421a7a3aae0d622d619e5756c241730c97`

## 2026-06-02 02:23 JST

- Summary: Added `-2` suffixed filenames for the second-review paper deliverables while keeping the canonical build filenames in place.
- Files:
  - `docs/paper/sect-sutra-map-paper-2.tex`
  - `docs/paper/sect-sutra-map-paper-2.pdf`
  - `docs/sect-sutra-map-review-response-2.md`
  - `memory.md`
- Verification:
  - Compared each `-2` file with its source file using `cmp -s`.
  - Listed the new `-2` files and confirmed sizes.
  - Checked the planned commit files for hardcoded API key patterns.
- Commit: `11b6fe22ade24caadc17588656ff9e397648bbe5`

## 2026-06-02 02:43 JST

- Summary: Applied the final third-review editorial fixes and created `-3` suffixed paper deliverables.
- Files:
  - `docs/paper/sect-sutra-map-paper.tex`
  - `docs/paper/sect-sutra-map-paper.pdf`
  - `docs/paper/sect-sutra-map-paper-3.tex`
  - `docs/paper/sect-sutra-map-paper-3.pdf`
  - `docs/results.md`
  - `docs/sect-sutra-map-review-response.md`
  - `docs/sect-sutra-map-review-response-3.md`
  - `memory.md`
- Verification:
  - Ran `uplatex -interaction=nonstopmode sect-sutra-map-paper.tex` twice and `dvipdfmx sect-sutra-map-paper.dvi`.
  - Checked the LaTeX log for overfull boxes and undefined references; only known caption and underfull warnings remained.
  - Rendered Quick Look thumbnails for PDF pages 1, 2, and 15 and confirmed the author line, corpus table, and reference page.
  - Compared each `-3` file with its canonical source using `cmp -s`.
  - Checked the planned commit files for hardcoded API key patterns.
- Commit: `055456210500eee9153109fa90e505362afb1565`

## 2026-06-02 06:39 JST

- Summary: Added Buddhist NLP / Buddhist DH prior-work framing and originality positioning, clarifying that the paper's contribution is an integrated exploratory map rather than first application of embeddings to Buddhist texts.
- Files:
  - `docs/paper/sect-sutra-map-paper.tex`
  - `docs/paper/sect-sutra-map-paper.pdf`
  - `docs/paper/sect-sutra-map-paper-4.tex`
  - `docs/paper/sect-sutra-map-paper-4.pdf`
  - `docs/results.md`
  - `docs/sect-sutra-map-review-response.md`
  - `docs/sect-sutra-map-author-report-originality-response.md`
  - `memory.md`
- Verification:
  - Checked and added prior-work references for CBETA, BDRC, Hung et al. 2010, Bingenheimer et al. 2017, Huang and Wang 2023, Nehrdich 2020, Felbur et al. 2022, Lugli et al. 2022, DharmaNexus, and MITRA.
  - Ran `uplatex -interaction=nonstopmode sect-sutra-map-paper.tex` twice and `dvipdfmx sect-sutra-map-paper.dvi`.
  - Checked the LaTeX log for overfull boxes and undefined references; only known caption and underfull warnings remained.
  - Rendered Quick Look thumbnails for PDF pages 1, 2, 14, and 16 and confirmed the abstract, prior-work introduction, discussion, and reference list.
  - Compared `sect-sutra-map-paper-4.tex` and `.pdf` with the canonical source files using `cmp -s`.
  - Checked the planned commit files for hardcoded API key patterns.
- Commit: `c6402f29c36e8e3f3a7951b037d71f4d7c887148`

## 2026-06-02 07:03 JST

- Summary: Applied the literature-review-after-revision report's editorial follow-up to the sect sutra map paper, including introduction subheadings, citation ordering, MITRA preprint wording, and regenerated fifth-version paper deliverables.
- Files:
  - `docs/paper/sect-sutra-map-paper.tex`
  - `docs/paper/sect-sutra-map-paper.pdf`
  - `docs/paper/sect-sutra-map-paper-5.tex`
  - `docs/paper/sect-sutra-map-paper-5.pdf`
  - `docs/results.md`
  - `docs/sect-sutra-map-author-report-literature-review-after-revision-response.md`
  - `memory.md`
- Verification:
  - Ran `uplatex -interaction=nonstopmode sect-sutra-map-paper.tex` twice and `dvipdfmx sect-sutra-map-paper.dvi`.
  - Checked the LaTeX log for overfull boxes and undefined references; only the known caption warning and underfull boxes remained.
  - Rendered Quick Look thumbnails for PDF pages 1, 2, 15, and 16 and confirmed the added introduction subheadings, citation order, reference pages, special characters, and MITRA preprint wording.
  - Compared `sect-sutra-map-paper-5.tex` and `.pdf` with the canonical source files using `cmp -s`.
  - Checked the planned commit files for hardcoded API key patterns.
- Commit: `20d5ff666e4b24b466600410824286bd53c2bf21`

## 2026-06-02 10:26 JST

- Summary: Prepared the sect sutra map repository for GitHub and GitHub Pages publication, including a README, citation metadata, publication checklist, Pages landing page, public viewer, and sanitized public viewer data.
- Files:
  - `.gitignore`
  - `README.md`
  - `CITATION.cff`
  - `docs/.nojekyll`
  - `docs/PUBLICATION.md`
  - `docs/index.html`
  - `docs/results.md`
  - `docs/viewer/index.html`
  - `docs/viewer/viewer_data.json`
  - `experiments/sect_sutra_map/make_public_viewer_data.py`
  - `memory.md`
- Verification:
  - Ran `python3 -m py_compile experiments/sect_sutra_map/*.py experiments/multilingual_sutra_map/*.py experiments/shinran_amida_sources/*.py`.
  - Ran `python3 experiments/sect_sutra_map/make_public_viewer_data.py` and confirmed 15 texts / 433 chunks.
  - Checked public viewer data for missing `source_path`, `body_path`, `line_path`, local `お経/` paths, and non-placeholder chunk previews.
  - Served `docs/` locally with `python3 -m http.server 8766 --directory docs` and verified the Pages landing page and public viewer in the in-app browser.
  - Checked the planned commit files for hardcoded API key patterns.
- Commit: `4b53cbd562bf3477192a03262a6fb08c30e89dda`

## 2026-06-02 10:52 JST

- Summary: Added an HTML paper as the primary GitHub Pages reading surface while retaining the PDF, expanded the README and process report with bilingual production provenance for the Codex/ChatGPT-assisted humanities data-analysis prototype, linked the author name to the author's website, and sanitized public pages to avoid real local paths.
- Files:
  - `README.md`
  - `docs/PUBLICATION.md`
  - `docs/index.html`
  - `docs/paper/index.html`
  - `docs/process/index.html`
  - `docs/repo-launch-process-report.md`
  - `docs/results.md`
  - `experiments/sect_sutra_map/make_paper_html.py`
  - `experiments/sect_sutra_map/make_process_html.py`
  - `memory.md`
- Verification:
  - Ran `python3 experiments/sect_sutra_map/make_paper_html.py`.
  - Ran `python3 experiments/sect_sutra_map/make_process_html.py`.
  - Ran `python3 -m py_compile experiments/sect_sutra_map/make_paper_html.py experiments/sect_sutra_map/make_process_html.py`.
  - Checked the generated HTML paper for leftover LaTeX commands and confirmed bibliography URLs render as links.
  - Checked that the process HTML records OpenAI API, ChatGPT Pro, Codex/Git, BasicTeX/upLaTeX/dvipdfmx, browser verification, and GitHub Pages publication preparation.
  - Verified `paper/` and `process/` in the local browser: author homepage link present, PDF link present, process tooling/publication sections present, and no real local filesystem paths visible.
  - Checked the planned commit files for hardcoded API key patterns.
- Commit: `1ad259cde5f644a202f82491b7c801e60cbb9e31`

## 2026-06-02 11:08 JST

- Summary: Refined the paper's source-credit wording for the Kyogyoshinsho text, added an acknowledgement for ChatGPT 5.5 Pro xhigh review feedback, expanded the paper appendix into a glossary for implementation, visualization, evaluation, and publication terms, and regenerated the HTML paper, PDF, and public viewer data.
- Files:
  - `docs/paper/sect-sutra-map-paper.tex`
  - `docs/paper/sect-sutra-map-paper.pdf`
  - `docs/paper/sect-sutra-map-paper-5.tex`
  - `docs/paper/sect-sutra-map-paper-5.pdf`
  - `docs/paper/index.html`
  - `docs/viewer/viewer_data.json`
  - `docs/results.md`
  - `experiments/sect_sutra_map/manifest.json`
  - `experiments/sect_sutra_map/make_paper_html.py`
  - `memory.md`
- Verification:
  - Ran `python3 experiments/sect_sutra_map/make_paper_html.py`.
  - Ran `python3 -m py_compile experiments/sect_sutra_map/make_paper_html.py experiments/sect_sutra_map/make_public_viewer_data.py experiments/sect_sutra_map/build_corpus.py experiments/sect_sutra_map/embed_texts.py experiments/sect_sutra_map/make_viewer_data.py`.
  - Ran `python3 -m json.tool experiments/sect_sutra_map/manifest.json` and `python3 -m json.tool docs/viewer/viewer_data.json`.
  - Ran `uplatex -interaction=nonstopmode sect-sutra-map-paper.tex` twice and `dvipdfmx sect-sutra-map-paper.dvi`.
  - Confirmed the generated HTML includes the glossary appendix, added terms, source wording, author link, and ChatGPT 5.5 Pro xhigh acknowledgement.
  - Checked public/tracked files for obsolete source-wording phrases, real local paths, hardcoded API key patterns, and leftover LaTeX commands in the generated HTML.
- Commit: `7e93635125564a59fc9d1f0d7595dc899d65d574`

## 2026-06-02 11:35 JST

- Summary: Added a three-layer source-mixture analysis to the paper, including semantic, lexical/style, and citation/reference layers for Amida translations and Kyogyoshinsho; regenerated figures, HTML, and PDF; and normalized bibliography entries away from Japanese full-stop-separated reference formatting.
- Files:
  - `docs/figures/three-layer-concept-map.png`
  - `docs/figures/amida-three-layer-difference.png`
  - `docs/figures/kyogyoshinsho-three-layer-source-mixture.png`
  - `docs/paper/sect-sutra-map-paper.tex`
  - `docs/paper/sect-sutra-map-paper.pdf`
  - `docs/paper/sect-sutra-map-paper-5.tex`
  - `docs/paper/sect-sutra-map-paper-5.pdf`
  - `docs/paper/index.html`
  - `docs/results.md`
  - `experiments/sect_sutra_map/make_three_layer_figures.py`
  - `memory.md`
- Verification:
  - Ran `python3 experiments/sect_sutra_map/make_three_layer_figures.py` and confirmed Amida metrics: semantic cosine `0.8825`, lexical TF-IDF cosine `0.1833`, top-5 chunk mixing `0.3684`.
  - Confirmed Kyogyoshinsho source-mixture mean weights for semantic, lexical/style, and citation/reference layers.
  - Ran `python3 experiments/sect_sutra_map/make_paper_html.py`.
  - Ran `python3 -m py_compile experiments/sect_sutra_map/make_three_layer_figures.py experiments/sect_sutra_map/make_paper_html.py`.
  - Ran `uplatex -interaction=nonstopmode sect-sutra-map-paper.tex` twice and `dvipdfmx sect-sutra-map-paper.dvi`.
  - Confirmed `sect-sutra-map-paper.tex` and `sect-sutra-map-paper-5.tex` are identical, and copied the regenerated PDF to `sect-sutra-map-paper-5.pdf`.
  - Confirmed the bibliography block no longer contains Japanese full stops and the generated HTML references use comma-separated entries with access dates.
  - Checked generated paper files for old development-note style wording.
- Commit: `940403826fbb6735bc01a5afe4c9685f328aae5a`

## 2026-06-02 11:48 JST

- Summary: Redrew Figure 1 of the paper so the three-layer concept diagram is more careful, with clear input, layer, and output sections; fixed text overlap and arrow targeting; updated the figure caption, HTML paper, and PDF.
- Files:
  - `docs/figures/three-layer-concept-map.png`
  - `docs/paper/sect-sutra-map-paper.tex`
  - `docs/paper/sect-sutra-map-paper.pdf`
  - `docs/paper/sect-sutra-map-paper-5.tex`
  - `docs/paper/sect-sutra-map-paper-5.pdf`
  - `docs/paper/index.html`
  - `experiments/sect_sutra_map/make_three_layer_figures.py`
  - `memory.md`
- Verification:
  - Ran `python3 experiments/sect_sutra_map/make_three_layer_figures.py`.
  - Visually inspected `docs/figures/three-layer-concept-map.png` and confirmed the previous text overlap and ambiguous arrows were fixed.
  - Ran `python3 experiments/sect_sutra_map/make_paper_html.py`.
  - Ran `python3 -m py_compile experiments/sect_sutra_map/make_three_layer_figures.py experiments/sect_sutra_map/make_paper_html.py`.
  - Ran `uplatex -interaction=nonstopmode sect-sutra-map-paper.tex` twice and `dvipdfmx sect-sutra-map-paper.dvi`.
  - Browser verification against the currently open `file://` page was blocked by the in-app browser URL policy, so verification used the generated image, HTML source, and rebuilt PDF instead.
- Commit: `db2973ca1003af5394a8b8bd05cca9807b3563f9`

## 2026-06-02 12:16 JST

- Summary: Addressed the post-three-layer review by clarifying the source-mixture method, renaming layers to semantic, lexical/style, and explicit-marker layers, adding method parameters and summary tables, preserving the user-requested ChatGPT 5.5 Pro xhigh acknowledgement, and adding HTML glossary links plus MathJax rendering for paper formulas.
- Files:
  - `docs/figures/three-layer-concept-map.png`
  - `docs/figures/kyogyoshinsho-three-layer-source-mixture.png`
  - `docs/paper/sect-sutra-map-paper.tex`
  - `docs/paper/sect-sutra-map-paper.pdf`
  - `docs/paper/sect-sutra-map-paper-5.tex`
  - `docs/paper/sect-sutra-map-paper-5.pdf`
  - `docs/paper/index.html`
  - `docs/results.md`
  - `experiments/sect_sutra_map/make_paper_html.py`
  - `experiments/sect_sutra_map/make_three_layer_figures.py`
  - `memory.md`
- Verification:
  - Ran `python3 experiments/sect_sutra_map/make_three_layer_figures.py`.
  - Ran `python3 experiments/sect_sutra_map/make_paper_html.py`.
  - Ran `python3 -m py_compile experiments/sect_sutra_map/make_paper_html.py experiments/sect_sutra_map/make_three_layer_figures.py`.
  - Ran `uplatex -interaction=nonstopmode sect-sutra-map-paper.tex` and `dvipdfmx sect-sutra-map-paper.dvi`.
  - Confirmed HTML glossary links have no missing anchor targets.
  - Confirmed the generated HTML includes MathJax, 23 inline math spans, and 2 display math blocks.
  - Visually inspected Figure 1 and Figure 12 after regeneration.
  - Browser verification against the currently open `file://` page was blocked by the in-app browser URL policy, so verification used generated images, HTML source, and rebuilt PDF instead.
- Commit: `546ab6757257a1c9d25786e19101e7b9059941cc`

## 2026-06-02 12:24 JST

- Summary: Extended the public process report to record the recent interactive revision phase, including post-three-layer review handling, glossary links, MathJax formula rendering, user-preserved acknowledgement wording, and the plan to create an English version after the Japanese paper is finalized.
- Files:
  - `docs/repo-launch-process-report.md`
  - `docs/process/index.html`
  - `memory.md`
- Verification:
  - Ran `python3 experiments/sect_sutra_map/make_process_html.py`.
  - Ran `python3 -m py_compile experiments/sect_sutra_map/make_process_html.py`.
  - Checked the generated process Markdown/HTML for the new phase, MathJax mention, English-version plan, and absence of absolute local filesystem paths.
- Commit: `db003ff156761407466eb2d841415266858f3bac`

## 2026-06-02 12:27 JST

- Summary: Added the pre-Codex background that three legacy local exploratory folders existed at project start, reflecting Daishin Ueyama's small embedding experiments from several years earlier, while clarifying that those folders are ignored and not part of the public/reproducible repository.
- Files:
  - `README.md`
  - `docs/repo-launch-process-report.md`
  - `docs/process/index.html`
  - `memory.md`
- Verification:
  - Ran `python3 experiments/sect_sutra_map/make_process_html.py`.
  - Ran `python3 -m py_compile experiments/sect_sutra_map/make_process_html.py`.
  - Checked README and process Markdown/HTML for the legacy folder names and absence of absolute local filesystem paths or API key patterns.
- Commit: `bf83e866367569e13a28e3ef0fa7be48c993e2c7`

## 2026-06-02 12:35 JST

- Summary: Applied the final-stage review corrections: added PDF metadata, clarified that the citation/reference layer is operationalized as an explicit-marker layer, normalized lexical/style terminology, added variant marker spellings for Xuanzang's Praise Pure Land Sutra, linked Taisho IDs such as `T0360` in the HTML paper to SAT text pages, and regenerated three-layer figures, HTML, PDF, results notes, and the public process report.
- Files:
  - `docs/figures/amida-three-layer-difference.png`
  - `docs/figures/kyogyoshinsho-three-layer-source-mixture.png`
  - `docs/paper/sect-sutra-map-paper.tex`
  - `docs/paper/sect-sutra-map-paper-5.tex`
  - `docs/paper/sect-sutra-map-paper.pdf`
  - `docs/paper/sect-sutra-map-paper-5.pdf`
  - `docs/paper/index.html`
  - `docs/process/index.html`
  - `docs/repo-launch-process-report.md`
  - `docs/results.md`
  - `experiments/sect_sutra_map/make_paper_html.py`
  - `experiments/sect_sutra_map/make_three_layer_figures.py`
  - `memory.md`
- Verification:
  - Ran `python3 experiments/sect_sutra_map/make_three_layer_figures.py`.
  - Ran `python3 experiments/sect_sutra_map/make_paper_html.py`.
  - Ran `python3 -m py_compile experiments/sect_sutra_map/make_paper_html.py experiments/sect_sutra_map/make_three_layer_figures.py`.
  - Ran `uplatex -interaction=nonstopmode sect-sutra-map-paper.tex` twice and `dvipdfmx sect-sutra-map-paper.dvi`.
  - Copied regenerated PDF to `sect-sutra-map-paper-5.pdf` and confirmed `sect-sutra-map-paper.tex` matches `sect-sutra-map-paper-5.tex`.
  - Used bundled Python `pypdf` to confirm PDF Title, Author, and Keywords metadata.
  - Confirmed HTML glossary links have no missing anchor targets, MathJax remains enabled, and 33 SAT text links are generated.
  - Visually inspected the regenerated Amida difference and Kyogyoshinsho source-mixture figures.
- Commit: `8f394bc94f69527eaff5ff96d20d16db1c7f3e99`

## 2026-06-02 12:55 JST

- Summary: Reworked publication hygiene for a first GitHub push from `main`. Treated `memory.md` as a public process ledger rather than a private file, removed the public `.gitignore` block that named specific sensitive legacy exploratory files, audited git history for actual API keys and local absolute paths, normalized the final paper filenames to `sect-sutra-map-paper.pdf` and `sect-sutra-map-paper.tex` without numbered draft suffixes, and unified the public site navigation across the top page, paper, viewer, and process pages.
- Files:
  - `.gitignore`
  - `README.md`
  - `docs/PUBLICATION.md`
  - `docs/index.html`
  - `docs/paper/index.html`
  - `docs/paper/sect-sutra-map-paper-2.pdf` (removed)
  - `docs/paper/sect-sutra-map-paper-2.tex` (removed)
  - `docs/paper/sect-sutra-map-paper-3.pdf` (removed)
  - `docs/paper/sect-sutra-map-paper-3.tex` (removed)
  - `docs/paper/sect-sutra-map-paper-4.pdf` (removed)
  - `docs/paper/sect-sutra-map-paper-4.tex` (removed)
  - `docs/paper/sect-sutra-map-paper-5.pdf` (removed)
  - `docs/paper/sect-sutra-map-paper-5.tex` (removed)
  - `docs/process/index.html`
  - `docs/repo-launch-process-report.md`
  - `docs/results.md`
  - `docs/viewer/index.html`
  - `experiments/sect_sutra_map/make_paper_html.py`
  - `experiments/sect_sutra_map/make_process_html.py`
  - `memory.md`
- Verification:
  - Confirmed `.gitignore` no longer contains the specific sensitive legacy file block.
  - Confirmed the legacy exploratory folders remain ignored through folder-level patterns.
  - Confirmed current tracked files contain no actual OpenAI API key prefix pattern.
  - Confirmed git history has no OpenAI API key prefix additions/removals and no local absolute path additions.
  - Confirmed git history has no tracked entries for the legacy exploratory folders or `experiments/amida_compare`.
  - Ran `python3 experiments/sect_sutra_map/make_paper_html.py`.
  - Ran `python3 experiments/sect_sutra_map/make_process_html.py`.
  - Ran `python3 -m py_compile experiments/sect_sutra_map/make_paper_html.py experiments/sect_sutra_map/make_process_html.py`.
  - Confirmed public-facing links no longer refer to `sect-sutra-map-paper-5.pdf` or other numbered paper draft filenames.
  - Confirmed the shared navigation order is `トップ / 論文 / PDF / ビューア / 制作プロセス / 結果ログ` on the top page, paper page, process page, and viewer page.
  - Checked the process and viewer pages in the in-app browser; current-page state is shown with a subtle background rather than a filled primary button.
- Commit: `da3c43e547d57572a05fe2be2496185b2f04399b`

## 2026-06-02 13:26 JST

- Summary: Removed the ambiguous `結果ログ` item from the shared public site navigation and renamed public-facing references to `docs/results.md` as `実験結果メモ`. Kept `docs/results.md` as a supplemental Markdown record rather than a top-level Pages navigation item.
- Files:
  - `README.md`
  - `docs/PUBLICATION.md`
  - `docs/index.html`
  - `docs/paper/index.html`
  - `docs/process/index.html`
  - `docs/repo-launch-process-report.md`
  - `docs/results.md`
  - `docs/viewer/index.html`
  - `experiments/sect_sutra_map/make_paper_html.py`
  - `experiments/sect_sutra_map/make_process_html.py`
  - `memory.md`
- Verification:
  - Ran `python3 experiments/sect_sutra_map/make_process_html.py`.
  - Ran `python3 experiments/sect_sutra_map/make_paper_html.py`.
  - Confirmed with text search that public files no longer contain `結果ログ`, `Results log`, or `実験実験結果メモ`.
  - Checked the top page and process page in the in-app browser. The shared navigation is now `トップ / 論文 / PDF / ビューア / 制作プロセス`, and the process page uses `実験結果メモ` only in body text.
- Commit: `d1c12e428ff4f9a39c5ba6ea2bed9a43e36e900e`

## 2026-06-02 13:36 JST

- Summary: Checked for stale uses of the early v0 project name `宗派別お経マップ` on public-facing pages. Updated the public landing page, README heading, viewer title/H1, process page title/footer, and process report wording to use the broader `意味埋め込みによる仏教文献の探索地図` framing. Kept `宗派別お経マップ v0` only where it refers to the historical v0 implementation phase or planning/result notes.
- Files:
  - `README.md`
  - `docs/index.html`
  - `docs/process/index.html`
  - `docs/repo-launch-process-report.md`
  - `docs/viewer/index.html`
  - `experiments/sect_sutra_map/make_process_html.py`
  - `experiments/sect_sutra_map/viewer/index.html`
  - `memory.md`
- Verification:
  - Ran `python3 experiments/sect_sutra_map/make_process_html.py`.
  - Ran `python3 -m py_compile experiments/sect_sutra_map/make_process_html.py`.
  - Searched public pages and process sources for stale `宗派別お経マップ`, `宗派別意味マップ`, and `宗派重心` uses.
  - Checked the top page, public viewer, process page, and HTML paper in the in-app browser. None uses `宗派別お経マップ` as the page title or H1.
- Commit: `eba8e6780923d27e746f75c219de4fe1a96014e9`

## 2026-06-02 13:48 JST

- Summary: Added a preliminary volume-level reading of `教行信証` to the three-layer source-mixture analysis. Detected the volume headings for 総序, 教巻, 行巻, 信巻, 証巻, 真仏土巻, and 化身土巻, assigned chunks by center-token position, added volume boundary labels to the three-layer figure, added a new volume-average figure/table, and retitled the paper from `意味・文体・引用・参照の三層地図` to `意味・文体・典拠マーカーの三層地図` so the three layers are not read as four. Forced the PDF title page to break after the colon while keeping the HTML title cleaned.
- Files:
  - `docs/figures/three-layer-concept-map.png`
  - `docs/figures/kyogyoshinsho-three-layer-source-mixture.png`
  - `docs/figures/kyogyoshinsho-volume-source-means.png`
  - `docs/paper/index.html`
  - `docs/paper/sect-sutra-map-paper.pdf`
  - `docs/paper/sect-sutra-map-paper.tex`
  - `docs/results.md`
  - `experiments/sect_sutra_map/make_three_layer_figures.py`
  - `experiments/sect_sutra_map/make_paper_html.py`
  - `memory.md`
- Verification:
  - Ran `python3 experiments/sect_sutra_map/make_three_layer_figures.py`.
  - Ran `python3 experiments/sect_sutra_map/make_paper_html.py`.
  - Ran `python3 -m py_compile experiments/sect_sutra_map/make_three_layer_figures.py experiments/sect_sutra_map/make_paper_html.py`.
  - Ran `uplatex -interaction=nonstopmode sect-sutra-map-paper.tex` twice.
  - Ran `dvipdfmx sect-sutra-map-paper.dvi`.
  - Checked `http://localhost:8767/paper/` in the in-app browser. Confirmed the title uses `意味・文体・典拠マーカーの三層地図`, the old `意味・文体・引用・参照` title phrase is absent, and the new volume figure/table are visible.
  - Checked the generated PDF title page in the in-app browser. Confirmed the title breaks after `：` into two lines.
  - Observed that semantic and lexical layers have 無量寿経 as the dominant source for all `教行信証` volumes, while the explicit marker layer is dominated by 未検出 in 信巻, 真仏土巻, and 化身土巻.
- Commit: `746b6c80fb61e5f4ac1bb46fd786b44c0f3b2112`

## 2026-06-02 13:53 JST

- Summary: Adjusted the paper keyword line typography for a more standard Japanese academic style. Changed the visible keyword label to `キーワード：` and separated keyword terms with full-width commas `，` instead of Japanese commas `、`. Regenerated the HTML paper and PDF.
- Files:
  - `docs/paper/index.html`
  - `docs/paper/sect-sutra-map-paper.pdf`
  - `docs/paper/sect-sutra-map-paper.tex`
  - `memory.md`
- Verification:
  - Ran `python3 experiments/sect_sutra_map/make_paper_html.py`.
  - Ran `python3 -m py_compile experiments/sect_sutra_map/make_paper_html.py`.
  - Ran `uplatex -interaction=nonstopmode sect-sutra-map-paper.tex`.
  - Ran `dvipdfmx sect-sutra-map-paper.dvi`.
  - Checked the generated PDF title page in the in-app browser and confirmed the keyword line uses `キーワード：` and `，` separators.
- Commit: `bf6771179178b2900f591a56c3688397cc6aae10`

## 2026-06-02 13:56 JST

- Summary: Improved the PDF layout of Table 1 (`対象テキストとコーパス情報`). Reduced the table font from `small` to `footnotesize`, reduced column padding, and rebalanced column widths so short fields such as `ID・出典`, `全文性`, and `字数/チャンク` wrap less often while the table still fits the page.
- Files:
  - `docs/paper/sect-sutra-map-paper.pdf`
  - `docs/paper/sect-sutra-map-paper.tex`
  - `memory.md`
- Verification:
  - Ran `python3 experiments/sect_sutra_map/make_paper_html.py`.
  - Ran `python3 -m py_compile experiments/sect_sutra_map/make_paper_html.py`.
  - Ran `uplatex -interaction=nonstopmode sect-sutra-map-paper.tex` twice.
  - Ran `dvipdfmx sect-sutra-map-paper.dvi`.
  - Checked page 3 of the generated PDF in the in-app browser at 90% and 125% zoom. Confirmed Table 1 fits the page and the short metadata columns wrap less often.
- Commit: `23b6e00dcedf5727f46cd7cafde863c39e0495a6`

## 2026-06-02 14:02 JST

- Summary: Added an explicit AI-use and author-responsibility disclosure to the paper. Framed the author as `上山大信` and treated Codex GPT-5.5 xhigh and ChatGPT 5.5 Pro xhigh as disclosed AI-support tools rather than authors. Added references for current AI authorship/disclosure norms and CRediT-style role terminology.
- Files:
  - `docs/paper/index.html`
  - `docs/paper/sect-sutra-map-paper.pdf`
  - `docs/paper/sect-sutra-map-paper.tex`
  - `memory.md`
- Verification:
  - Checked current publisher guidance by looking up ICMJE, Elsevier, Springer Nature, and CRediT sources.
  - Ran `python3 experiments/sect_sutra_map/make_paper_html.py`.
  - Ran `python3 -m py_compile experiments/sect_sutra_map/make_paper_html.py`.
  - Ran `uplatex -interaction=nonstopmode sect-sutra-map-paper.tex` twice.
  - Ran `dvipdfmx sect-sutra-map-paper.dvi`.
  - Checked the HTML paper and generated PDF in the in-app browser. Confirmed the disclosure section begins with `本稿の著者は上山大信である` and that `上山さん` does not appear.
- Commit: `pending`
