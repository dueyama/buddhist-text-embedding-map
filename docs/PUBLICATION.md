# GitHub / GitHub Pages 公開チェックリスト

## 公開するもの

- 論文HTML: `docs/paper/index.html`
- 論文PDF・TeX: `docs/paper/sect-sutra-map-paper.pdf`, `docs/paper/sect-sutra-map-paper.tex`
- 英語AI支援翻訳版HTML・PDF・TeX: `docs/paper/en/index.html`, `docs/paper/en/sect-sutra-map-paper-en.pdf`, `docs/paper/en/sect-sutra-map-paper-en.tex`
- 図: `docs/figures/*.png`, `docs/figures/en/*.png`
- 静的サイト: `docs/index.html`, `docs/en/index.html`
- 公開版ビューア: `docs/viewer/index.html`, `docs/viewer/viewer_data.json`
- 制作プロセス: `docs/process/index.html`, `docs/repo-launch-process-report.md`
- 英語制作プロセス: `docs/process/en/index.html`, `docs/repo-launch-process-report-en.md`
- 再現用コード: `experiments/sect_sutra_map/`, `experiments/multilingual_sutra_map/`, `experiments/shinran_amida_sources/`
- 実験結果メモ・計画書: `docs/*.md`

## 公開しないもの

- `.env`
- OpenAI API key を含むファイル
- SAT、J-SOKEN、84000 などから取得した raw/processed 本文
- embedding cache
- legacy local corpus and exploratory folders
- older exploratory notebooks/scripts that may contain API keys

## 公開用履歴の考え方

このローカル作業リポジトリでは、`memory.md` をgit管理して作業ごとの日時、検証、commit hashを記録している。これは研究制作の作業台帳であり、AI支援研究制作のプロセスを示す公開可能な記録として扱う。

初回公開前には、最新状態だけでなくgit履歴も含めて、実際のAPIキー、raw/processed本文、embedding cache、ローカル絶対パス、legacy exploratory folders が追跡されていないことを確認する。

## GitHub Pages 設定

1. GitHub に repository を作成する。
2. ローカルで remote を追加し、`main` を push する。
3. GitHub repository settings で Pages を有効化する。
4. Source は `Deploy from a branch`、branch は `main`、folder は `/docs` を選ぶ。
5. 公開URLで次を確認する。
   - `index.html` が表示される。
   - `en/` で英語トップが表示される。
   - `paper/` でHTML論文が表示される。
   - `paper/sect-sutra-map-paper.pdf` が開く。
   - `paper/en/` で英語AI支援翻訳版HTMLが表示される。
   - `paper/en/sect-sutra-map-paper-en.pdf` が開く。
   - `process/` で制作プロセス文書が表示される。
   - `process/en/` で英語制作プロセス文書が表示される。
   - `viewer/index.html` が `viewer_data.json` を自動読み込みする。
   - 主要図が表示される。
   - HTMLページでは日本語・英語が言語スイッチで切り替わり、PDFは `PDF JP` / `PDF EN` として別リンクになっている。

## 公開前コマンド

```bash
git status --short
rg -n 'sk[-][A-Za-z0-9]' README.md docs experiments/sect_sutra_map experiments/multilingual_sutra_map experiments/shinran_amida_sources
rg -n '/Users|Documents/Codex' README.md docs experiments/sect_sutra_map experiments/multilingual_sutra_map experiments/shinran_amida_sources --glob '!docs/PUBLICATION.md'
git grep --cached -n 'sk[-][A-Za-z0-9]'
git log --all --oneline -G'sk[-][A-Za-z0-9]'
git log --all --oneline -G'/Users|Documents/Codex'
python3 -m py_compile experiments/sect_sutra_map/*.py experiments/multilingual_sutra_map/*.py experiments/shinran_amida_sources/*.py
python3 experiments/sect_sutra_map/make_public_viewer_data.py
python3 experiments/sect_sutra_map/make_paper_figures.py --lang en
python3 experiments/sect_sutra_map/make_three_layer_figures.py --lang en
python3 experiments/shinran_amida_sources/run_analysis.py --lang en
python3 experiments/sect_sutra_map/make_paper_html.py
python3 experiments/sect_sutra_map/make_paper_html.py --input docs/paper/en/sect-sutra-map-paper-en.tex --output docs/paper/en/index.html --lang en --pdf-name sect-sutra-map-paper-en.pdf
python3 experiments/sect_sutra_map/make_process_html.py
python3 experiments/sect_sutra_map/make_process_html.py --input docs/repo-launch-process-report-en.md --output docs/process/en/index.html --lang en
```

追跡対象ファイルとして、次が出ないことを確認する。

```bash
git ls-files | rg '^お経/|^埋め込みお経/|^埋め込みテスト/|^experiments/.*/data/|^experiments/.*/outputs/|^\.env$'
```

このコマンドが何も出ない状態にしてから公開する。

## 注意

公開版 `docs/viewer/viewer_data.json` は、本文プレビューとローカル本文パスを除いた派生データである。本文の再取得・再利用は各提供元の利用条件に従うこと。

論文はWebで読みやすい `docs/paper/index.html` を主表示とし、PDF版も同じディレクトリに保持する。PDFはページ固定の引用・印刷・オフライン閲覧用として扱う。

日本語論文を正式な製本版とし、英語版は `docs/paper/en/` のAI支援翻訳版として扱う。英語版には、引用や細かなニュアンス確認では日本語版を主たる本文とする旨を明記する。

HTMLページの日本語・英語導線は、個別メニュー項目を増やすのではなく、ページごとの言語スイッチで切り替える。PDFは版の違いが明確なため、`PDF JP` と `PDF EN` の別リンクとして残す。

ライセンスは未選択。コード再利用を許可したい場合は MIT、論文・図を再利用可能にしたい場合は CC BY 4.0 など、公開方針に合わせて別途決める。
