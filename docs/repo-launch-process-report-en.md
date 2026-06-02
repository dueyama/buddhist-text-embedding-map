# Process Report from Repository Setup to Publication Preparation

Period covered: June 1, 2026 17:33 JST to June 2, 2026 14:54 JST
Repository: `Okyou/`

## Position

This document summarizes the process by which the Okyou research repository was set up, developed, revised, and prepared for GitHub Pages publication.

The project is both a preliminary study of Buddhist texts using semantic embeddings and a prototype for AI-assisted humanities data-analysis paper production. The research questions, source selection, interpretation, and publication policy were directed by [Daishin Ueyama](https://sites.google.com/site/dueyama/). Codex GPT-5.5 xhigh supported code implementation, data processing, visualization, drafting, revision, verification, and local Git recording. ChatGPT 5.5 Pro xhigh was used in a reviewer-like role for comments on framing, literature review, originality, limitations, and public wording.

The point is not that AI independently conducted the research. Rather, the project tests how a human researcher can direct the questions and interpretation while AI tools help assemble scripts, figures, drafts, local infrastructure, and publication-ready pages at high speed.

## Preconditions

This workflow assumes the following environment.

- An OpenAI API key for generating embeddings.
- A ChatGPT Pro account for review-style discussion and critique.
- A local Codex environment for file editing, scripting, verification, and Git work.
- Python 3 for corpus construction, embedding cache handling, figure generation, and static viewer data export.
- A local Japanese TeX environment only when rebuilding the Japanese and English PDFs.
- Confirmation of the terms of use for text providers such as SAT, J-SOKEN, and 84000.

## Prior Local Experiments

The Codex workflow did not begin from a blank slate. At the start, the local workspace contained three older exploratory folders: `お経`, `埋め込みお経`, and `埋め込みテスト`. These reflected small embedding experiments conducted by Daishin Ueyama several years earlier.

Those folders provided background context for the renewed question: can Buddhist texts, translations, and sectarian reference sets be explored with embeddings? They are not part of the public reproducible repository, because they may contain API keys, raw source text, or other local-only material. The publishable work was reorganized under `experiments/` and `docs/`.

## Tool Preparation

The project also demonstrates that AI assistance can prepare the research tools themselves, not only prose.

- `.env` was used for the OpenAI API key, while `.env` and legacy key-containing files were kept out of public tracking.
- Embedding cache logic was added so that the same text and model would not be charged repeatedly.
- Raw and processed source texts from SAT, J-SOKEN, and 84000 were excluded from public redistribution.
- Python scripts were written for text acquisition, preprocessing, chunking, embedding, figure generation, viewer data generation, and public data sanitization.
- A local static viewer was built and tested through a local HTTP server.
- BasicTeX plus upLaTeX and dvipdfmx were prepared for PDF generation.
- The paper was made available both as PDF and as ordinary HTML for GitHub Pages.
- MathJax was added so that formulas in the HTML paper render as formulas rather than raw TeX.
- A public landing page, paper pages, process pages, public viewer, checklist, and README were prepared.
- `memory.md` was used as a local project ledger recording JST time, change summary, verification, and commit hash.

## Workflow Phases

1. The initial question was whether sutras could be compared or loosely classified with embeddings.
2. The first concrete experiment compared the two Chinese translations of the Amitabha Sutra.
3. The project expanded into a sectarian reference-text map for Japanese Buddhist traditions.
4. The pipeline was organized as manifest, corpus builder, embedding cache, viewer-data export, and static viewer.
5. Translator centroids and chunk-level nearest neighbors were added after the user asked whether translator style could be visible.
6. The analysis moved from mean-vector points to chunk distributions, one-standard-deviation ellipses, overlap heatmaps, and bridge chunks.
7. A multilingual pilot compared the 84000 English Toh 106 translation with the SAT Chinese T0676 text.
8. A Shinran-focused pilot examined the two Amitabha translations through explicit names, markers, and chunk affinity.
9. Review-style feedback from ChatGPT 5.5 Pro xhigh was incorporated through multiple revisions.
10. The paper was reframed around a three-layer map: semantic layer, style/lexical layer, and source-marker layer.
11. Public hygiene checks removed raw text, body previews, local paths, API keys, and legacy folders from the public surface.
12. GitHub Pages assets were prepared under `docs/`.
13. After the Japanese edition was finalized as the authoritative print/book edition, an English AI-assisted translation was created under `docs/paper/en/`.

## Publication Surface

The public surface is organized as follows.

- Top page: `docs/index.html`
- Japanese paper HTML: `docs/paper/index.html`
- Japanese paper PDF: `docs/paper/sect-sutra-map-paper.pdf`
- English AI-assisted translation HTML: `docs/paper/en/index.html`
- English AI-assisted translation PDF: `docs/paper/en/sect-sutra-map-paper-en.pdf`
- Japanese process report: `docs/process/index.html`
- English process report: `docs/process/en/index.html`
- Public viewer: `docs/viewer/index.html`

The Japanese paper is the authoritative print/book edition. The English paper is an AI-assisted translation intended to make the work accessible to English-language readers. For citation and fine nuance, the Japanese edition should be checked.

## What Can Be Reused

This prototype can be adapted to other humanities materials such as classical literature, historical documents, translation pairs, legal texts, diaries, letters, or philosophical corpora.

The reusable pattern is simple.

1. Define a small research question.
2. Put source metadata in a manifest.
3. Script text acquisition and preprocessing.
4. Chunk texts and generate cached embeddings.
5. Compare both mean vectors and chunk distributions.
6. Build a static viewer so the researcher can inspect the results.
7. Record results, verification, and limitations in documents.
8. Use review-style AI critique to improve framing and limitations.
9. Prepare HTML/PDF outputs and publication hygiene checks.
10. Preserve a process report so others can understand how the research artifact was assembled.

## Remaining Tasks

- Update citation metadata after the GitHub repository URL is fixed.
- Decide the license for code, paper, figures, and derived data.
- Recheck source-provider terms of use before public release.
- Test chunk-size dependency, natural-unit chunking, character normalization, and variant forms.
- Extend the method to stronger style features and source-marker dictionaries.
- Compare Tibetan, Sanskrit, or Pali sources directly where possible.
- Compare Shinran-related results with existing source-critical research.
- Verify the final GitHub Pages deployment after the first push.

## Summary

The project turned an exploratory question about Buddhist-text embeddings into a small research repository containing code, figures, viewer data, a Japanese paper, an English AI-assisted translation, and a process report. The key feature is not only the analysis result, but the workflow: a human researcher directs the questions and interpretation, while Codex and ChatGPT help accelerate implementation, review, documentation, and publication preparation.
