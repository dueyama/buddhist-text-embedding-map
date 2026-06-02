# GitHub / GitHub Pages 公開チェックリスト

## 公開するもの

- 論文HTML: `docs/paper/index.html`
- 論文PDF・TeX: `docs/paper/sect-sutra-map-paper-5.pdf`, `docs/paper/sect-sutra-map-paper-5.tex`
- 図: `docs/figures/*.png`
- 静的サイト: `docs/index.html`
- 公開版ビューア: `docs/viewer/index.html`, `docs/viewer/viewer_data.json`
- 制作プロセス: `docs/process/index.html`, `docs/repo-launch-process-report.md`
- 再現用コード: `experiments/sect_sutra_map/`, `experiments/multilingual_sutra_map/`, `experiments/shinran_amida_sources/`
- 結果ログ・計画書: `docs/*.md`

## 公開しないもの

- `.env`
- OpenAI API key を含むファイル
- SAT、J-SOKEN、84000 などから取得した raw/processed 本文
- embedding cache
- legacy local corpus and exploratory folders
- older exploratory notebooks/scripts that may contain API keys

## GitHub Pages 設定

1. GitHub に repository を作成する。
2. ローカルで remote を追加し、`main` を push する。
3. GitHub repository settings で Pages を有効化する。
4. Source は `Deploy from a branch`、branch は `main`、folder は `/docs` を選ぶ。
5. 公開URLで次を確認する。
   - `index.html` が表示される。
   - `paper/` でHTML論文が表示される。
   - `paper/sect-sutra-map-paper-5.pdf` が開く。
   - `process/` で制作プロセス文書が表示される。
   - `viewer/index.html` が `viewer_data.json` を自動読み込みする。
   - 主要図が表示される。

## 公開前コマンド

```bash
git status --short
rg -n 'sk[-]' README.md docs experiments/sect_sutra_map experiments/multilingual_sutra_map experiments/shinran_amida_sources
git grep --cached -n 'sk[-]'
python3 -m py_compile experiments/sect_sutra_map/*.py experiments/multilingual_sutra_map/*.py experiments/shinran_amida_sources/*.py
python3 experiments/sect_sutra_map/make_public_viewer_data.py
python3 experiments/sect_sutra_map/make_paper_html.py
python3 experiments/sect_sutra_map/make_process_html.py
```

## 注意

公開版 `docs/viewer/viewer_data.json` は、本文プレビューとローカル本文パスを除いた派生データである。本文の再取得・再利用は各提供元の利用条件に従うこと。

論文はWebで読みやすい `docs/paper/index.html` を主表示とし、PDF版も同じディレクトリに保持する。PDFはページ固定の引用・印刷・オフライン閲覧用として扱う。

ライセンスは未選択。コード再利用を許可したい場合は MIT、論文・図を再利用可能にしたい場合は CC BY 4.0 など、公開方針に合わせて別途決める。
