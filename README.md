# 宗派別お経マップ

意味埋め込みを使って、漢訳仏典・日本撰述仏教文献・異訳・多言語対応関係を探索するためのローカル研究リポジトリです。現在の中心成果は、宗派別参照群、阿弥陀経二訳、親鸞文献、多言語パイロットをまとめた予備論文と静的ビューアです。

## Public Artifacts

- 論文PDF: `docs/paper/sect-sutra-map-paper-5.pdf`
- 論文TeX: `docs/paper/sect-sutra-map-paper-5.tex`
- GitHub Pages entry point: `docs/index.html`
- Public viewer: `docs/viewer/index.html`
- Results log: `docs/results.md`

## Repository Layout

- `experiments/sect_sutra_map/`: 宗派別お経マップの主要パイプライン
- `experiments/multilingual_sutra_map/`: 解深密経の漢訳・英訳パイロット
- `experiments/shinran_amida_sources/`: 親鸞文献と阿弥陀経二訳の参照指標分析
- `docs/figures/`: 論文・Pages 用の図
- `docs/paper/`: TeXソースとPDF
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

See `docs/PUBLICATION.md` for the publication checklist.

## GitHub Pages

Use GitHub Pages with:

- Source: `main` branch
- Folder: `/docs`

Then open the generated Pages URL and confirm that the landing page, paper PDF, figures, and public viewer load correctly.

## License

No repository-wide license has been selected yet. Choose a license before encouraging reuse beyond viewing the public repository.
