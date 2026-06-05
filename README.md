# 意味埋め込みによる仏教文献の探索地図

意味埋め込みを使って、漢訳仏典・日本撰述仏教文献・異訳・多言語対応関係を探索するためのローカル研究リポジトリです。現在の中心成果は、宗派別参照群、阿弥陀経二訳、親鸞文献、多言語パイロットをまとめた予備論文と静的ビューアです。

## Project Position / プロジェクトの位置づけ

This repository is a prototype and experiment in producing a humanities data-analysis paper with Codex. It is intended to be readable not only as a Buddhist-text embedding study, but also as a reproducible example of how this kind of research can be carried out semi-automatically with AI assistance. The assumed environment is an OpenAI API key for embeddings, a ChatGPT Pro account for review-style discussion, and a local Codex/Git workflow. The research questions, source choices, interpretation, and publication direction were guided by [上山大信 (Daishin Ueyama)](https://sites.google.com/site/dueyama/). The code, figures, paper drafts, and revision workflow were developed through iterative work with Codex GPT-5.5 xhigh, with review-style exchanges involving ChatGPT 5.5 Pro.

本リポジトリは、Codexを用いた人文系データ解析型の論文制作プロトタイプであり、実験的な制作記録でもあります。単なる仏教文献の意味埋め込み分析としてだけでなく、「OpenAI APIキー、ChatGPT Proアカウント、ローカルのCodex/Git環境があれば、この種の探索的研究をAI支援で半自動的に進められる」という再現可能なワークフロー例として読めることを意図しています。研究上の問い、対象文献の選定、解釈、公開方針は[上山大信](https://sites.google.com/site/dueyama/)の指示にもとづき、コード、図、論文草稿、改稿作業は Codex GPT-5.5 xhigh との反復的な作業を通じて作成しました。また、ChatGPT 5.5 Pro との査読形式のやり取りを反映しながら、論文としての構成、先行研究整理、限界の記述を調整しています。

At the start of this Codex workflow, the local workspace also contained three legacy exploratory folders, `お経`, `埋め込みお経`, and `埋め込みテスト`, reflecting small embedding experiments previously conducted by Daishin Ueyama several years earlier. They served as background context for the renewed project, but they are not part of the public/reproducible repository and are intentionally ignored by git.

このCodex作業の開始時点では、ローカル作業環境に `お経`、`埋め込みお経`、`埋め込みテスト` という三つの過去実験フォルダがありました。これらは上山大信が数年前に少し試した埋め込み実験の痕跡であり、今回の研究の前提・背景として参照されました。ただし、公開・再現用の成果物ではないため、gitでは追跡せず、現在の公開用コードと文書は `experiments/` と `docs/` に整理し直しています。

The local development repository also uses `memory.md` as a project ledger. It records timestamps, change summaries, verification steps, and commit hashes for the Codex-assisted workflow. This practice is documented here because it is useful for reproducing the process and understanding how the research artifact was assembled.

また、ローカル開発用リポジトリでは、作業台帳として `memory.md` をgit管理しています。ここにはJST日時、変更概要、検証内容、commit hashを記録し、Codex支援による研究制作の流れを追跡できるようにしました。この記録方法自体も、再現可能なワークフローの一部として参考になることを意図しています。

## Methodological Note / 方法上の立場

このリポジトリは、仏教文献の意味や思想史的関係を AI に最終判定させることを目的としたものではありません。ここで行っているのは、本文をチャンク化し、意味埋め込みによる近傍関係を作り、そこに語彙・典拠・文献単位の情報を重ねることで、研究者が読み直すべき領域を探すための探索地図を作る試みです。

人文学的解釈には、問いの立て方、対象範囲、先行研究の系譜、研究者ごとの重みづけが必ず入ります。本プロジェクトが期待しているのは、それらを消すことではなく、解釈が分岐する前に共有できる本文側の意味的地形を、できるだけ再現可能な形で示すことです。

したがって、本リポジトリの図や数値は、教義・影響関係・文献史の結論ではなく、精査候補を抽出するための補助線として読まれるべきものです。結果は、埋め込みモデル、チャンク化、対象文献、投影法によって変わりえます。今後は、複数のモデル・複数の前処理条件・既存の文献学的知見との照合を通じて、どの近傍構造が安定して残るのかを確認していく必要があります。

This repository does not aim to let AI make final judgments about the meaning of Buddhist texts or their historical relationships. Its more modest aim is to divide texts into chunks, represent them in an embedding space, and overlay lexical, bibliographic, and source-marker information in order to build exploratory maps for close reading.

Humanistic interpretation inevitably depends on research questions, corpus boundaries, scholarly traditions, and the reader's own weighting of passages. The hope of this project is not to remove such interpretation, but to provide a reproducible semantic terrain of the texts before interpretations diverge.

The figures and statistics in this repository should therefore be read as guides to passages worth inspecting, not as proofs of doctrinal meaning, historical influence, or textual genealogy. Results may vary with the embedding model, chunking scheme, projection method, and corpus selection. A major task for future work is to test which neighborhood structures remain stable across models and preprocessing choices, and how they correspond to established philological and doctrinal scholarship.

## Replication Assumptions / 再現の前提

- OpenAI API key for generating embeddings.
- ChatGPT Pro account for review-style discussion and iterative paper critique.
- Local Codex environment with git.
- Python 3 for corpus construction, embedding cache handling, figure generation, and static viewer data export.
- A local Japanese TeX environment only if rebuilding the PDF; the HTML paper can be read from `docs/paper/index.html`.
- Confirmation of each text provider's terms of use before downloading or reusing source texts.

- 埋め込み生成用の OpenAI APIキー。
- 査読形式の相談・論文批評に使う ChatGPT Pro アカウント。
- gitを使えるローカルCodex環境。
- コーパス構築、embedding cache、図生成、viewer data生成のための Python 3。
- PDFを再生成する場合のみ、日本語TeX環境。HTML論文は `docs/paper/index.html` で閲覧できる。
- SAT、J-SOKEN、84000 など、各本文提供元の利用条件確認。

## Public Artifacts

- Current public release: v1.0.1, adding the Unicode-aware chunking errata and validation.
- 論文HTML: `docs/paper/index.html`
- 論文PDF: `docs/paper/sect-sutra-map-paper.pdf`
- 論文TeX: `docs/paper/sect-sutra-map-paper.tex`
- English AI-assisted translation HTML: `docs/paper/en/index.html`
- English AI-assisted translation PDF: `docs/paper/en/sect-sutra-map-paper-en.pdf`
- Errata / post-release validation for Unicode-aware chunk boundaries: `docs/errata/index.html`, `docs/errata/unicode-safe-chunking-errata-ja.pdf`, `docs/errata/en/index.html`, `docs/errata/en/unicode-safe-chunking-errata-en.pdf`
- English figure variants: `docs/figures/en/*.png`
- GitHub Pages entry point: `docs/index.html`
- English GitHub Pages entry point: `docs/en/index.html`
- Public viewer: `docs/viewer/index.html`
- Publication checksum record: `docs/checksums.txt`
- Experiment result notes: `docs/results.md`
- Process report: `docs/process/index.html`, `docs/repo-launch-process-report.md`
- English process report: `docs/process/en/index.html`, `docs/repo-launch-process-report-en.md`
- AI researcher guide: `AI_RESEARCHER_GUIDE.md`

The Japanese paper is the authoritative print/book edition. The English paper is provided as an AI-assisted translation for access by English-language readers; when citing or checking nuance, use the Japanese edition as the primary text.

日本語論文を正式な製本版とし、英語版は英語読者のためのAI支援翻訳版として公開します。引用や細かなニュアンス確認では、日本語版を主たる本文として扱ってください。

## Publication Integrity / 公開版の固定

The Japanese paper PDF and Japanese errata PDF are treated as the fixed public Japanese editions. Their SHA-256 checksums are recorded in `docs/checksums.txt`:

```text
92be9d3cb008b4e1fa368fe2fc9e72d141194e980a63e83ae8645ad9ab079845  docs/paper/sect-sutra-map-paper.pdf
6dd41cd62c314e2844c19a8801f9ce5b5f2be8f673326ab19f96a5848b46f708  docs/errata/unicode-safe-chunking-errata-ja.pdf
```

The paper PDF checksum matches the PDF stored at git tags `v1.0.0` and `v1.0.1`; the Japanese errata PDF checksum matches the PDF stored at git tag `v1.0.1`. Later corrections are therefore published as separate supplements or errata, rather than as silent rewrites of the fixed PDFs.

論文本体の日本語PDFとerrataの日本語PDFを、公開された固定版として扱います。SHA-256ハッシュは `docs/checksums.txt` に記録しています。論文本体PDFのハッシュは git tag `v1.0.0` および `v1.0.1` に含まれるPDFと一致し、errata日本語PDFのハッシュは git tag `v1.0.1` に含まれるPDFと一致します。以後の訂正や検証は、PDF本文を黙って書き換えるのではなく、追補・errata として別に公開します。

This repository also treats the publication method itself as an experiment: a humanities data-analysis paper is published through GitHub Pages and GitHub Releases, while git history, release tags, checksums, and process notes make the public artifact and its later supplements traceable.

本リポジトリでは、この公開方法そのものも試行対象としています。人文系データ解析論文を GitHub Pages と GitHub Releases で公開し、git履歴、release tag、checksum、制作記録によって、公開版と後続の追補を追跡できる形にします。

## Repository Layout

- `AI_RESEARCHER_GUIDE.md`: AIエージェントに読ませるための再現・発展ガイド
- `experiments/sect_sutra_map/`: 宗派別参照テキスト群分析の主要パイプライン
- `experiments/multilingual_sutra_map/`: 解深密経の漢訳・英訳パイロット
- `experiments/shinran_amida_sources/`: 親鸞文献と阿弥陀経二訳の参照指標分析
- `docs/figures/`: 論文・Pages 用の図
- `docs/figures/en/`: 英語AI支援翻訳版用の英語ラベル図
- `docs/paper/`: HTML論文、PDF、TeXソース
- `docs/process/`: 制作プロセス文書
- `docs/viewer/`: GitHub Pages 用の公開版ビューア

## Reproducibility

The core sect-sutra map pipeline is:

```bash
python3 experiments/sect_sutra_map/build_corpus.py
python3 experiments/sect_sutra_map/embed_texts.py
python3 experiments/sect_sutra_map/make_viewer_data.py
python3 experiments/sect_sutra_map/make_public_viewer_data.py
```

`embed_texts.py` reads `OPENAI_API_KEY` from `.env`. The default embedding model is `text-embedding-3-large`; generated raw text, processed text, embedding cache, and experiment outputs are ignored by git.

## Publication Policy

This repository is prepared for public GitHub/GitHub Pages use, but it does not redistribute raw source texts from SAT, J-SOKEN, 84000, or other providers. Public Pages data omits chunk text previews and local source paths. Re-run the build scripts locally after confirming each source's terms of use.

Before the first public push, verify that the tracked history does not contain actual API keys, raw/processed text data, embedding caches, local absolute paths, or legacy exploratory folders. The `memory.md` ledger is intentionally tracked as a process record.

See `docs/PUBLICATION.md` for the publication checklist.

## GitHub Pages

Public site: https://dueyama.github.io/buddhist-text-embedding-map/

Use GitHub Pages with:

- Source: `main` branch
- Folder: `/docs`

Then open the generated Pages URL and confirm that the landing page, paper PDF, figures, and public viewer load correctly.
The landing page links primarily to the HTML paper, while the PDF version remains in `docs/paper/` for citation and offline reading.
HTML pages use a language switch between Japanese and English pages; PDF links remain separate as `PDF JP` and `PDF EN`.
The English AI-assisted translation is available under `docs/paper/en/`.
The English process report is available under `docs/process/en/`.

## License

This repository uses a split license.

- Code is licensed under the MIT License. See `LICENSE-CODE`.
- The paper, figures, documentation, process reports, citation metadata, and public derived data are licensed under Creative Commons Attribution 4.0 International (CC BY 4.0). See `LICENSE-CONTENT`.
- Source texts retrieved from SAT, J-SOKEN, 84000, or other providers are not redistributed here and are not covered by this repository's licenses.

本リポジトリは分割ライセンスを採用しています。

- コードは MIT License です。`LICENSE-CODE` を参照してください。
- 論文、図、公開文書、制作プロセス、citation metadata、公開用派生データは Creative Commons Attribution 4.0 International (CC BY 4.0) です。`LICENSE-CONTENT` を参照してください。
- SAT、J-SOKEN、84000 などから取得した元本文は本リポジトリでは再配布しておらず、本リポジトリのライセンス対象外です。
