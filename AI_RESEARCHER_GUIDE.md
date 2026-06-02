# AI Researcher Guide

この文書は、他の研究者が本リポジトリをAIエージェントや大規模言語モデルに読ませ、研究を再現・点検・発展させるための案内である。人間向けの概要は `README.md`、公開前チェックは `docs/PUBLICATION.md`、作業経緯は `docs/repo-launch-process-report.md` と `memory.md` を参照する。

## Intended Use

AIにこのリポジトリを読ませる場合は、次の目的を想定する。

- 既存論文・図・ビューアの内容を説明する。
- 既存パイプラインを再実行し、公開版成果物を再生成する。
- 新しい仏教文献、宗派参照群、異訳、多言語対応資料を追加する。
- 意味埋め込み、文体・語彙特徴、典拠マーカーを分けて比較する。
- 研究上の限界、出典クレジット、公開時の危険を点検する。

このリポジトリは、AIが自律的に仏教学的結論を出すためのものではない。研究者が問い、資料選択、解釈、公開判断を行い、AIは実装、再計算、可視化、文書化、検証を補助する。

## First Files To Read

AIには、まず次の順番で読ませるとよい。

1. `README.md`
   - プロジェクトの位置づけ、公開物、再現前提、ライセンス。
2. `docs/paper/sect-sutra-map-paper.tex`
   - 日本語正式版論文。細かな解釈や引用確認ではこれを主本文とする。
3. `docs/paper/en/sect-sutra-map-paper-en.tex`
   - 英語AI支援翻訳版。英語読者向けの補助本文。
4. `docs/results.md`
   - 実験結果、主要数値、検証、未検証点。
5. `docs/repo-launch-process-report.md`
   - 研究制作プロセス、AI支援の使い方、反復的な改稿経緯。
6. `docs/PUBLICATION.md`
   - 公開対象、公開しないもの、安全確認コマンド。
7. `experiments/sect_sutra_map/manifest.json`
   - 宗派別参照群マップの対象テキスト一覧。
8. `experiments/sect_sutra_map/*.py`
   - コーパス構築、埋め込み、可視化データ、公開版データ、HTML/PDF生成の実装。
9. `experiments/multilingual_sutra_map/manifest.json` と `experiments/multilingual_sutra_map/run_pilot.py`
   - 多言語比較パイロット。
10. `experiments/shinran_amida_sources/manifest.json` と `experiments/shinran_amida_sources/run_analysis.py`
   - 親鸞文献と浄土三部経・阿弥陀経二訳の参照関係分析。

`memory.md` は、Codex支援作業の日時、変更概要、検証、commit hash を記録した作業台帳である。研究制作過程を追跡するには有用だが、まず全体像を把握する場合は上記の公開文書と実験コードを優先する。

## Current Public Artifacts

主要な公開成果物は次の通りである。

- HTML論文: `docs/paper/index.html`
- PDF論文: `docs/paper/sect-sutra-map-paper.pdf`
- TeX本文: `docs/paper/sect-sutra-map-paper.tex`
- 英語AI支援翻訳版HTML: `docs/paper/en/index.html`
- 英語AI支援翻訳版PDF: `docs/paper/en/sect-sutra-map-paper-en.pdf`
- GitHub Pagesトップ: `docs/index.html`
- 公開版ビューア: `docs/viewer/index.html`
- 公開版ビューアデータ: `docs/viewer/viewer_data.json`
- 制作プロセスHTML: `docs/process/index.html`
- 英語制作プロセスHTML: `docs/process/en/index.html`
- 実験結果メモ: `docs/results.md`

公開版 `docs/viewer/viewer_data.json` は、本文断片やローカルパスを除いた派生データである。本文再配布のためのデータではない。

## What Is Not In The Public Repo

次のものは公開・追跡しない。

- `.env`
- OpenAI API key
- SAT、J-SOKEN、84000 などから取得した raw/processed 本文
- embedding cache
- `experiments/*/outputs/`
- `experiments/*/data/`
- 旧ローカル探索フォルダやAPIキーを含み得る古いnotebook/script

AIエージェントは、これらをgitに追加してはならない。本文を再取得する場合は、各提供元の利用条件を確認し、raw本文やprocessed本文を公開用commitに含めないこと。

## Minimal Reproduction Path

既存の公開物を点検・再生成するだけなら、まず次を実行する。

```bash
git status --short
python3 -m py_compile experiments/sect_sutra_map/*.py experiments/multilingual_sutra_map/*.py experiments/shinran_amida_sources/*.py scripts/*.py
python3 experiments/sect_sutra_map/make_public_viewer_data.py
python3 experiments/sect_sutra_map/make_paper_html.py
python3 experiments/sect_sutra_map/make_paper_html.py --input docs/paper/en/sect-sutra-map-paper-en.tex --output docs/paper/en/index.html --lang en --pdf-name sect-sutra-map-paper-en.pdf
python3 experiments/sect_sutra_map/make_process_html.py
python3 experiments/sect_sutra_map/make_process_html.py --input docs/repo-launch-process-report-en.md --output docs/process/en/index.html --lang en
python3 scripts/serve_pages_preview.py --bind tailscale --check
```

PDFを再生成する場合は、ローカルに `upLaTeX + dvipdfmx` が必要である。

```bash
cd docs/paper
uplatex -interaction=nonstopmode sect-sutra-map-paper.tex
uplatex -interaction=nonstopmode sect-sutra-map-paper.tex
dvipdfmx sect-sutra-map-paper.dvi

cd en
uplatex -interaction=nonstopmode sect-sutra-map-paper-en.tex
uplatex -interaction=nonstopmode sect-sutra-map-paper-en.tex
dvipdfmx sect-sutra-map-paper-en.dvi
```

LaTeX中間ファイルはgit管理しない。

## Full Re-run With Embeddings

埋め込みを再生成する場合は、OpenAI API key が必要である。`.env` に `OPENAI_API_KEY` を置くが、`.env` は絶対にcommitしない。

宗派別参照群マップの基本パイプラインは次の通りである。

```bash
python3 experiments/sect_sutra_map/build_corpus.py
python3 experiments/sect_sutra_map/embed_texts.py
python3 experiments/sect_sutra_map/make_viewer_data.py
python3 experiments/sect_sutra_map/make_public_viewer_data.py
python3 experiments/sect_sutra_map/make_paper_figures.py
python3 experiments/sect_sutra_map/make_three_layer_figures.py
python3 experiments/shinran_amida_sources/run_analysis.py
```

英語ラベル図を作る場合:

```bash
python3 experiments/sect_sutra_map/make_paper_figures.py --lang en
python3 experiments/sect_sutra_map/make_three_layer_figures.py --lang en
python3 experiments/shinran_amida_sources/run_analysis.py --lang en
```

`embed_texts.py` の既定モデルは `text-embedding-3-large` である。生成済みcacheがある場合は、同一本文・同一モデルでは再課金を避ける設計になっている。cacheやoutputsは公開commitに含めない。

## How To Extend The Research

AIエージェントに発展作業を頼む場合は、次の順序を守るとよい。

1. 研究者に問いを確認する。
   - 例: 宗派比較を増やすのか、異訳比較を増やすのか、多言語比較を増やすのか、文体比較を増やすのか。
2. 既存manifestを読む。
   - `experiments/sect_sutra_map/manifest.json`
   - `experiments/multilingual_sutra_map/manifest.json`
   - `experiments/shinran_amida_sources/manifest.json`
3. 新しい対象文献の出典、利用条件、本文取得方法を確認する。
4. raw本文・processed本文を公開対象から除外する。
5. チャンク化、埋め込み、図、viewer dataを再生成する。
6. `docs/results.md` に入力データ、モデル、chunk数、主要数値、解釈、未検証点を記録する。
7. 論文やプロセス文書を更新する場合は、HTML/PDFも再生成する。
8. `memory.md` にJST日時、変更概要、検証、commit hashを記録する。
9. 秘密情報とローカルパスを確認してからcommitする。

## Good Extension Ideas

このrepoから自然に発展できる方向は次の通りである。

- 宗派別参照群の拡張。
  - 天台、日蓮、真言、浄土、禅、華厳などについて、経典だけでなく祖師文献、注釈書、勤行文を追加する。
- チャンク化の改善。
  - 固定長チャンクだけでなく、巻、品、段落、引用単位などの自然単位で比較する。
- 意味・文体・典拠マーカーの分離。
  - 意味埋め込みだけでなく、文字n-gram、語彙、固有句、典拠マーカー辞書を分けて地図化する。
- 親鸞文献の巻別分析。
  - `教`, `行`, `信`, `証`, `真仏土`, `化身土` など、巻ごとの参照源混合を既存研究と照合する。
- 多言語比較。
  - チベット語、サンスクリット、パーリ、英訳、漢訳を、対応句・章単位で比較する。
- 対照実験の追加。
  - ラベルランダム化、chunk size sensitivity、別モデル比較、PCA以外の次元削減を行う。
- ビューアの改善。
  - 点だけでなく分布、重なり、近傍chunk、層別フィルタ、巻別フィルタを増やす。

## Interpretation Rules

AIは次の点を守って解釈する。

- この研究は宗派の「正解分類」を作るものではない。
- 表示される地図は、宗派が参照するテキスト群の配置を探索する予備的可視化である。
- 意味埋め込みの近さは、引用・影響・典拠を直接証明しない。
- 文体・語彙の近さと意味の近さは分けて考える。
- 『教行信証』と浄土三部経の関係は、伝統的・文献学的研究と照合して読む必要がある。
- 英語版論文はAI支援翻訳であり、日本語版が正式な主本文である。
- AI出力は一次情報源ではない。SAT、聖教DB、84000、論文、辞書、先行研究などを確認する。

## Safety And Publication Checks

公開前またはcommit前には、最低限次を確認する。

```bash
git status --short
rg -n 'sk[-][A-Za-z0-9]' README.md docs experiments scripts memory.md LICENSE LICENSE-CODE LICENSE-CONTENT CITATION.cff
rg -n '<local-absolute-path-pattern>' README.md docs experiments scripts
git grep --cached -n 'sk[-][A-Za-z0-9]'
git ls-files | rg '^お経/|^埋め込みお経/|^埋め込みテスト/|^experiments/.*/data/|^experiments/.*/outputs/|^\.env$'
git diff --check
```

`<local-absolute-path-pattern>` は、研究者の環境で実際に漏れてはいけないローカル絶対パスのパターンに置き換える。`docs/PUBLICATION.md` には、公開前に実行すべきより長いチェックリストがある。

## Suggested Initial Prompt For AI

研究者が別のAIにこのrepoを渡す場合、次のようなプロンプトから始めるとよい。

```text
このリポジトリは、仏教文献の意味埋め込み分析とAI支援による人文学研究制作のプロトタイプです。
まず README.md と AI_RESEARCHER_GUIDE.md を読み、その後 docs/paper/sect-sutra-map-paper.tex、
docs/results.md、docs/PUBLICATION.md、experiments/sect_sutra_map/manifest.json を読んでください。

目的は、既存成果を過大評価せずに説明し、再現可能性と公開上の安全性を保ちながら、
新しい文献群または比較軸を追加することです。

守ること:
- .env、API key、raw/processed本文、embedding cache、outputsをcommitしない。
- SAT、J-SOKEN、84000など提供元の利用条件を確認する。
- 意味埋め込みの近さを引用・影響の証明として扱わない。
- 日本語版論文を主本文として扱う。
- 変更後は docs/results.md と memory.md に検証内容を記録する。

まず、現在のリポジトリ構成、再現コマンド、未検証点、発展案を短く要約してください。
```

## Suggested Review Prompt

論文や結果をAIに査読させる場合は、次の観点を指定するとよい。

```text
この論文を、デジタル人文学・仏教学・NLPの予備研究として査読してください。
新規性を過大評価していないか、意味埋め込みと典拠研究を混同していないか、
出典クレジットと本文再配布制限が十分か、図と表から読めることと読めないことが区別されているかを見てください。
改善提案は、実装可能な追試・追加図・追加対照実験に分けてください。
```

## License Summary

コードは MIT License、論文・図・公開文書・制作プロセス・citation metadata・公開用派生データは CC BY 4.0 である。SAT、J-SOKEN、84000 などから取得した元本文は、本リポジトリでは再配布せず、本リポジトリのライセンス対象外である。
