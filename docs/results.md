# Results

This file records experiment results worth keeping outside generated caches.

## 2026-06-01: 阿弥陀経二訳の比較

### 入力

- `T0366` 佛説阿彌陀經
  - Translator: 姚秦 鳩摩羅什譯
  - SAT: https://21dzk.l.u-tokyo.ac.jp/SAT/T0366_,12,0346b24:0366_,12,0348b20.html
  - Lines: 146
  - Characters: 2117
- `T0367` 稱讃淨土佛攝受經
  - Translator: 大唐 玄奘譯
  - SAT: https://21dzk.l.u-tokyo.ac.jp/SAT/T0367_,12,0348b21:0367_,12,0351b29.html
  - Lines: 259
  - Characters: 4589

### 方法

- Character TF-IDF baseline:
  - Analyzer: char
  - n-gram range: 2 to 5
- Semantic embedding:
  - Model: `text-embedding-3-large`
  - Texts were token-chunked and averaged for the text-level comparison.

### 主要結果

- Character TF-IDF:
  - Full-text cosine: `0.1928`
  - Mean best chunk cosine: `0.1424`
  - Chunks: `T0366=6`, `T0367=12`
- OpenAI embedding:
  - Full average cosine: `0.8943`
  - Mean best chunk cosine: `0.7108`
  - Chunks: `T0366=9`, `T0367=18`

### 解釈

- Semantic embedding は、両テキストをかなり近い内容として捉えている。
- Character n-gram は、語彙や言い回しの差を強く拾い、二訳をかなり遠く見る。
- これは「意味の近さ」と「翻訳・文体の癖」を分けて見る必要があることを示す。

### 目立つ語彙差

- 鳩摩羅什訳:
  - `舍利弗`
  - `衆生`
  - `阿彌陀佛`
  - `恒河沙`
  - `極樂國土`
  - `所護念經`
  - `誠實言`
- 玄奘訳:
  - `舍利子`
  - `有情`
  - `無量壽佛`
  - `殑伽沙`
  - `極樂世界`
  - `攝受法門`
  - `誠諦言`

### 未検証点

- 翻訳者の癖と底本差を切り分けるには、同じ訳者の複数テキストを比較する必要がある。
- 宗派比較に使う場合、経典単位の平均だけでなく、チャンク分布と宗派重心を見る必要がある。
- SAT の利用条件に従い、再配布ではなく研究結果の要約として扱う。

## 2026-06-01: 宗派別お経マップ v0

### 入力

- Texts: `13`
- Chunks: `403`
- Sect centroids: `10`
- Model: `text-embedding-3-large`
- Chunking: `700` tokens with `100` token overlap
- API tokens for initial embedding run: `279172`
- Cache verification: second run with `--no-api` produced `403` cache hits and `0` cache misses.

### コーパス

- 浄土系
  - `T0360` 佛説無量壽經: `27` chunks, `10307` chars
  - `T0365` 佛説觀無量壽佛經: `23` chunks, `9003` chars
  - `T0366` 佛説阿彌陀經: `7` chunks, `2368` chars
  - 教行信証: `197` chunks, `78978` chars
    - 出典: 浄土真宗本願寺派総合研究所『浄土真宗聖典』聖教データベース
- 法華系
  - 妙法蓮華經 抜粋本文: `13` chunks, `4718` chars
  - 觀世音菩薩普門品 SAT range: `6` chunks, `2134` chars
- 真言系
  - `T0848` 大毘盧遮那成佛神變加持經: `28` chunks, `10770` chars
  - `T0865` 金剛頂一切如來眞實攝大乘現證大教王經: `22` chunks, `8342` chars
  - `T0243` 大樂金剛不空眞實三麼耶經: `9` chunks, `3309` chars
- 禅系・般若系
  - `T0251` 般若波羅蜜多心經: `3` chunks, `1307` chars
  - `T0235` 金剛般若波羅蜜經: `15` chunks, `5909` chars
  - `T0475` 維摩詰所説經: `32` chunks, `12129` chars
- 華厳系
  - `T0279` 大方廣佛華嚴經: `21` chunks, `7743` chars

### 主要な近傍

- 阿弥陀経の近傍:
  - 無量寿経: `0.8694`
  - 観無量寿経: `0.8446`
  - 妙法蓮華経抜粋本文: `0.8275`
  - 教行信証: `0.8058`
- 無量寿経の近傍:
  - 妙法蓮華経抜粋本文: `0.9111`
  - 観無量寿経: `0.9102`
  - 教行信証: `0.8797`
  - 阿弥陀経: `0.8694`
- 真言系:
  - 金剛頂経 -> 理趣経: `0.8405`
  - 金剛頂経 -> 大日経: `0.8323`
  - 大日経 -> 理趣経: `0.8512`
- 禅系・般若系:
  - 金剛経 -> 維摩経: `0.8770`
  - 般若心経 -> 金剛経: `0.7622`
  - 般若心経 -> 維摩経: `0.7643`
- 華厳経 sample:
  - 妙法蓮華経抜粋本文: `0.8293`
  - 無量寿経: `0.8221`
  - 大日経: `0.7886`

### 解釈

- 浄土三部経は、阿弥陀経から見ると無量寿経・観無量寿経が上位に来ており、初期仮説どおりまとまりが見える。
- 真言系では、金剛頂経・理趣経・大日経が互いに近く、密教経典クラスタとして観察できる。
- 禅系の経典だけでは、曹洞・臨済・黄檗の差はまだ出ない。これは予想どおりで、祖師文献や語録を足す必要がある。
- 教行信証は浄土三部経にも近いが、維摩経や大日経にも高く出る。全文平均では、宗派性だけでなく引用・総合文献としての広がりが強く出ている可能性がある。
- 妙法蓮華経の抜粋本文は `4718` chars と短く、全文ではない可能性が高い。法華系の評価は SAT full text 取得後に再確認する。

### 生成物

- Corpus index: `experiments/sect_sutra_map/data/processed/corpus_index.json`
- Embeddings: `experiments/sect_sutra_map/outputs/embeddings.json`
- Viewer data: `experiments/sect_sutra_map/outputs/viewer_data.json`
- Static viewer: `experiments/sect_sutra_map/viewer/index.html`

Generated corpus/output files are not committed. The viewer is served locally from `experiments/sect_sutra_map`.

### 未検証点

- 大部経典は SAT の直接表示範囲を v0 corpus としているため、全文比較ではないものがある。
- 法華経抜粋本文 は短く、全文 SAT に差し替える必要がある。
- 宗派重心は `core_sutra` と `founder_text` の単純平均なので、宗派ごとの重み付けは未実装。
- 祖師文献は教行信証だけで、禅・天台・真言・日蓮の祖師文献は未投入。
- PCA 2D map は可視化用であり、距離の厳密解釈には heatmap と nearest list を併用する必要がある。

## 2026-06-01: 訳者比較 v0.1

### 入力

- Texts: `15`
- Chunks: `433`
- Sect centroids: `11`
- Translator centroids: `3`
- Model: `text-embedding-3-large`
- Added texts:
  - `T0367` 稱讃淨土佛攝受經: 玄奘訳の阿弥陀経系別訳
  - `T0676` 解深密經: 玄奘訳の法相・瑜伽行系代表経典
- Incremental embedding run:
  - Previous cache hits: `403`
  - New cache misses: `30`
  - API tokens for new chunks: `20869`
  - Cache verification with `--no-api`: `433` cache hits, `0` cache misses

### 訳者重心

- 不空: `2` texts
  - `T0865` 金剛頂経
  - `T0243` 理趣経
- 玄奘: `3` texts
  - `T0367` 稱讃淨土佛攝受經
  - `T0251` 般若心経
  - `T0676` 解深密經
- 鳩摩羅什: `5` texts
  - `T0366` 阿弥陀経
  - `T0262` 法華経抜粋本文
  - `T0262` 観音経相当部分
  - `T0235` 金剛経
  - `T0475` 維摩経

### 主要な近傍

- 玄奘訳 `T0367` 稱讃淨土佛攝受經:
  - 鳩摩羅什訳 `T0366` 阿弥陀経: `0.8825`
  - `T0360` 無量寿経: `0.8798`
  - `T0262` 法華経抜粋本文: `0.8469`
  - `T0365` 観無量寿経: `0.8412`
  - 教行信証: `0.8152`
- 玄奘訳 `T0676` 解深密經:
  - 教行信証: `0.8548`
  - `T0848` 大日経: `0.8478`
  - `T0475` 維摩経: `0.8370`
  - `T0235` 金剛経: `0.8308`
  - `T0360` 無量寿経: `0.7838`

### 解釈

- `T0367` と `T0366` は訳者が違ってもかなり近く出る。これは semantic embedding が「同じ、または非常に近い原内容」を強く拾っているためと見られる。
- 一方で、玄奘訳同士である `T0367`・般若心経・`T0676` が、訳者だけを理由に強くまとまるわけではない。特に `T0676` は瑜伽行・法相系の内容差が大きく、意味ベクトルではトピックが支配的になる。
- 訳者重心は、ビューア上で「この訳者の既知テキスト群がどのあたりに散るか」を見る補助線としては有用。ただし、翻訳の癖そのものを抽出するには semantic embedding だけでは足りない。
- 翻訳癖を見るには、次に character n-gram、助字・句法、固有訳語対応、文長、句読点なしの文字列特徴などを別レイヤーにした style vector を作る必要がある。

### 生成物

- Viewer data: `experiments/sect_sutra_map/outputs/viewer_data.json`
- Static viewer: `experiments/sect_sutra_map/viewer/index.html`
- Visual check: headless Chrome で訳者比較マップを確認。

### 未検証点

- 訳者重心は、同一訳者の投入テキスト数が少ないため安定しない。
- 鳩摩羅什の法華経抜粋本文 は短いため、全文 SAT に差し替える必要がある。
- 玄奘・不空以外の訳者サンプルを増やさないと、訳者特徴とジャンル特徴を切り分けられない。
- 現時点のビューアは semantic map であり、style map は未実装。

## 2026-06-01: 多言語比較パイロット v0.1

### 入力

- Goal: チベット大蔵経由来の 84000 英訳と漢訳が、意味埋め込みで同一経典として近く出るかを確認する。
- Main pair:
  - `T0676` 解深密經: SAT 由来の既存 processed text
  - `Toh 106` The Teaching Explaining the Thought: 84000 Reading Room の公開英訳 HTML から抽出
- Controls:
  - `T0235` 金剛般若波羅蜜經
  - `T0475` 維摩詰所說經
  - `T0251` 般若波羅蜜多心經
  - `T0366` 佛說阿彌陀經
- Model: `text-embedding-3-large`
- Texts: `6`
- Chunks: `105`
- API tokens: `71630`
- Cache verification: `105` cache hits, `0` cache misses, `0` API tokens

### 最近傍結果

Query: `toh106_samdhinirmocana_en`

| Rank | Target | Same work | Cosine |
| --- | --- | --- | --- |
| 1 | `t0676_samdhinirmocana_zh` | yes | `0.7662` |
| 2 | `t0475_vimalakirti_zh` | no | `0.6926` |
| 3 | `t0235_diamond_zh` | no | `0.6922` |
| 4 | `t0251_heart_zh` | no | `0.6167` |
| 5 | `t0366_amida_zh` | no | `0.5683` |

### 解釈

- 初回パイロットでは、84000 英訳 `Toh 106` の最近傍が漢訳 `T0676` になった。これは、少なくともこの組み合わせでは、言語を越えて「同一経典らしさ」を semantic embedding が拾えていることを示す。
- ただし、次点の維摩経・金剛経も `0.69` 台であり、大乗経典一般の語彙・主題に由来する近さもある。したがって、「同一経典判定」として使うには、同一 work の異言語ペアを増やして margin を見る必要がある。
- 現段階ではチベット語本文そのものではなく、チベット大蔵経由来の英訳を使った cross-language pilot である。チベット語本文を入れる場合は、BDRC/Adarshah/84000 Scholar Room などの安定した取得元と利用条件を別途確認する。

### 生成物

- Plan: `docs/multilingual-sutra-map-plan.md`
- Manifest: `experiments/multilingual_sutra_map/manifest.json`
- Script: `experiments/multilingual_sutra_map/run_pilot.py`
- Raw/processed/output cache: `experiments/multilingual_sutra_map/data/` and `experiments/multilingual_sutra_map/outputs/` are ignored by git.

### 未検証点

- 84000 HTML の抽出は v0 の研究用キャッシュであり、安定 API ではない。
- 英訳と漢訳の章・段落対応はまだ取っていない。
- 同じ英語翻訳スタイルに由来するクラスタリングは、英訳サンプルを複数入れないと評価できない。
- チベット語本文、サンスクリット、パーリは未投入。

## 2026-06-01: チャンク分布マップ v0.1

### 入力

- Source: `experiments/sect_sutra_map/outputs/embeddings.json`
- Model: `text-embedding-3-large`
- Texts: `15`
- Chunks: `433`
- Main idea: 本文平均ベクトルだけではなく、各本文を構成する chunk embeddings の分布として可視化する。

### 追加図

- `docs/figures/sect-sutra-chunk-distribution-overview.png`
  - 主要テキストの全体チャンク分布と 1σ 楕円。
- `docs/figures/sect-sutra-chunk-distribution-focus.png`
  - 阿弥陀経二訳、真言系密教経典、般若・法相・禅系対照を別パネルで表示。
- `docs/figures/sect-sutra-chunk-overlap-heatmap.png`
  - 高次元 embedding 空間での top-5 チャンク近傍混合率。
- `docs/figures/sect-sutra-overlap-vs-centroid.png`
  - 本文平均ベクトルの類似度とチャンク近傍混合率の散布図。

### 主要な混合率

| Pair | top-5 chunk neighbor mixing |
| --- | --- |
| 阿弥陀経 / 稱讃淨土経 | `0.37` |
| 稱讃淨土経 / 無量寿経 | `0.19` |
| 無量寿経 / 観無量寿経 | `0.17` |
| 金剛経 / 維摩経 | `0.14` |
| 金剛頂経 / 理趣経 | `0.12` |
| 教行信証 / 無量寿経 | `0.04` |
| 教行信証 / 阿弥陀経 | `0.01` |
| 教行信証 / 観無量寿経 | `0.01` |
| 阿弥陀経 / 理趣経 | `0.04` |

### 橋渡しチャンク

本文転載を避けるため、chunk id と数値だけを記録する。

| Pair | Best bridge chunks | Bridge cosine | Text cosine | top-5 mixing |
| --- | --- | ---: | ---: | ---: |
| 阿弥陀 / 稱讃 | `T0366 0005 / T0367 0010` | `0.7672` | `0.8825` | `0.3684` |
| 教行 / 無量寿 | `KGS 0002 / T0360 0004` | `0.7969` | `0.8797` | `0.0438` |
| 教行 / 観無量寿 | `KGS 0088 / T0365 0002` | `0.7095` | `0.8375` | `0.0127` |
| 教行 / 阿弥陀 | `KGS 0098 / T0366 0005` | `0.7250` | `0.8058` | `0.0147` |
| 無量寿 / 観無量寿 | `T0360 0021 / T0365 0008` | `0.7660` | `0.9102` | `0.1680` |
| 金剛頂 / 理趣 | `T0865 0000 / T0243 0000` | `0.8176` | `0.8405` | `0.1161` |
| 金剛 / 維摩 | `T0235 0004 / T0475 0022` | `0.7235` | `0.8770` | `0.1404` |
| 阿弥陀 / 理趣 | `T0366 0005 / T0243 0007` | `0.5900` | `0.6816` | `0.0375` |

### 解釈

- 平均点マップは全体の位置を読むには便利だが、経典内部の主題の広がりを消してしまう。
- 阿弥陀経二訳は平均ベクトルでも近く、チャンク近傍混合率も高い。内容対応が部分単位でも出ている可能性がある。
- 教行信証は浄土三部経を根拠としているため本文平均ベクトルでは三部経に近く、橋渡しチャンクの類似度も高い。一方で top-5 混合率は低く、引用・釈義・論述を含む複合文献としての広がりが出ている。
- 2D の楕円は PCA 投影上の見え方なので、重なりの判定には高次元空間の近傍混合率を併用する。

### 未検証点

- チャンク境界は 700 tokens / 100 overlap の機械分割で、巻・品・段落などの自然単位ではない。
- 楕円は 2D PCA 上の 1σ 近似なので、非楕円形・多峰性の分布を十分には表現できない。
- 今後は chapter/section 単位での分布、密度推定、Earth Mover's Distance なども比較候補にする。

## 2026-06-01: 親鸞の阿弥陀経二訳参照分析 v0.1

### 入力

- Target translations:
  - `T0366` 羅什訳『佛説阿彌陀經』
  - `T0367` 玄奘訳『稱讃淨土佛攝受經』
- Shinran-side sources:
  - 『教行信証』: J-SOKEN 聖教DB由来の既存 processed text
  - 『入出二門偈』p543: 真宗大谷派（東本願寺）真宗聖典検索サイトから取得
- Literature notes:
  - 『観無量寿経集註附阿弥陀経集註』
  - 千葉隆誓「親鸞『阿弥陀経集註』における元照『阿弥陀経義疏』引文について」

### 生成物

- Script: `experiments/shinran_amida_sources/run_analysis.py`
- Manifest: `experiments/shinran_amida_sources/manifest.json`
- Detailed note: `docs/shinran-amida-source-analysis.md`
- Figures:
  - `docs/figures/shinran-amida-source-markers.png`
  - `docs/figures/shinran-kyogyoshinsho-amida-chunk-affinity.png`
- Raw/output cache:
  - `experiments/shinran_amida_sources/data/`
  - `experiments/shinran_amida_sources/outputs/`
  - Both are ignored by git.

### 主要結果

- 『入出二門偈』p543 は『称讃浄土経』を玄奘訳として明示し、玄奘訳 `T0367` 側の讃嘆モチーフに対応する句を持つ。
- 『教行信証』本文平均ベクトル:
  - `T0366`: `0.8058`
  - `T0367`: `0.8152`
  - 玄奘訳の方がわずかに高いが、差は小さく、これだけでは決定打にならない。
- 『教行信証』の上位 chunk affinity:

| Target | Kyogyoshinsho chunk | Target chunk | Cosine |
| --- | --- | --- | ---: |
| `T0366` | `kyogyoshinsho::chunk_0098` | `t0366_amida_sutra::chunk_0005` | `0.7250` |
| `T0366` | `kyogyoshinsho::chunk_0019` | `t0366_amida_sutra::chunk_0005` | `0.7103` |
| `T0366` | `kyogyoshinsho::chunk_0018` | `t0366_amida_sutra::chunk_0005` | `0.7088` |
| `T0367` | `kyogyoshinsho::chunk_0023` | `t0367_praise_pure_land::chunk_0006` | `0.7033` |

### 解釈

- 親鸞の阿弥陀経理解は「羅什訳か玄奘訳か」の二択ではなく、羅什訳を標準的な小経として持ちつつ、玄奘訳『称讃浄土経』も明示的に用いる多層構造として見るのがよい。
- 『教行信証』単体では、意味的に二訳へ近いが、訳系統の決定には弱い。文字列・明示引用・注釈伝統を別レイヤーにする必要がある。
- 『入出二門偈』は玄奘訳参照の強い証拠になる。
- 次の本命は『阿弥陀経集註』であり、経文本文・註記・裏書を分けて解析する必要がある。

### 未検証点

- 『阿弥陀経集註』本文はまだ機械可読テキストとして投入していない。
- 今回の文字列一致は異体字正規化と簡易 marker に基づく。校訂本文・訓点・注記を分けた厳密な処理は未実装。
- 真宗聖典検索の raw HTML は研究用キャッシュであり、本文再配布はしない。

## 2026-06-02: 査読コメント対応 v0.2

### 入力

- Review file: `sect-sutra-map-review.md`
- Target paper: `docs/paper/sect-sutra-map-paper.tex`
- Supporting script:
  - `experiments/sect_sutra_map/review_stats.py`

### 主要対応

- 論文タイトルを「探索地図」「宗派別参照群」「異訳比較」中心に変更した。
- 「宗派別お経マップ」「宗派重心」のような強い表現を、「宗派別参照テキスト群の意味配置」「宗派別参照群重心」に弱めた。
- 対象テキスト表に、出典、全文性、文字数、チャンク数、備考を追加した。
- チャンク化、前処理、`tiktoken` tokenizer、PCA seed、L2正規化の有無を方法節に追記した。
- PCA寄与率を図軸および本文に追加した。
- 阿弥陀経二訳の `0.8943` と `0.8825` の差を、全文直接埋め込みとチャンク平均ベクトルの違いとして整理した。
- チャンク近傍混合率の top-k 感度分析を追加した。
- ラベルシャッフルは通常の有意差検定としては解釈せず、完全混合に近い参照値として扱うことを明記した。
- 意味マップ、文体マップ、引用・参照マップの三層モデルを考察に追加した。

### 追加数値

- 本文平均点マップ PCA:
  - PC1: `0.2331`
  - PC2: `0.1874`
  - Total: `0.4204`
- 阿弥陀経二訳 top-k 感度:

| top-k | Observed mixing | Rank among 55 pairs | Complete-mixing reference mean | Complete-mixing reference 95% range |
| ---: | ---: | ---: | ---: | --- |
| 1 | `0.1579` | `1` | `0.4897` | `0.2105-0.7368` |
| 3 | `0.2632` | `1` | `0.4911` | `0.3333-0.6140` |
| 5 | `0.3684` | `1` | `0.4911` | `0.3787-0.5789` |
| 10 | `0.4474` | `1` | `0.4908` | `0.4263-0.5421` |

### 解釈

- 阿弥陀経二訳は、比較した実テキスト55ペアの中では一貫して最も高い混合率を示した。
- 一方、完全混合参照平均は観測値より高い。これは混合率が「ランダムにラベルが混ざるほど高くなる」指標であるためで、通常の「観測値がランダムより高い」検定としては読めない。
- 予備論文としては、ランダム化検定だけでなく、実ペア間順位、top-k 感度、平均類似度との併読が重要である。

### 未検証点

- チャンク数を揃えたサブサンプリングは未実装。
- ブートストラップ信頼区間は未実装。
- 法華経全文への差し替えは未実施。
- 『阿弥陀経集註』本文の機械可読化は未実施。

## 2026-06-02: 査読レポート2 小修正対応

### 入力

- Review file: `sect-sutra-map-review-report-2.md`
- Target paper: `docs/paper/sect-sutra-map-paper.tex`
- Target figure script: `experiments/sect_sutra_map/make_paper_figures.py`

### 主要対応

- 著者名 `未定` をローカル git 設定に合わせて `dueyama` へ置換した。
- 表1の訳者名字形を確認し、T0365 は `畺良耶舍`、T0279 は `實叉難陀` とした旨を表注に追加した。
- 法華経抜粋を `序品第一` 相当の既存取得抜粋として明記した。
- 表2のラベルシャッフル系見出しを、`完全混合参照平均` と `完全混合参照分布の95%範囲` へ変更した。
- 本文中の `上限的参照` を避け、ラベルランダム化を `ラベルが意味構造と独立に割り当てられた場合の完全混合参照` として説明した。
- 図7の凡例を `意味埋め込み` に、横軸を `全文直接埋め込み` に変更し、キャプションで `チャンク最良一致平均` がチャンク平均ベクトル類似度とは別指標であることを補足した。
- コード・派生データの公開方針、自然単位チャンク化との比較、結論での三層モデル再掲を追加した。

### 未検証点

- `dueyama` はローカル git 設定から採った仮の著者表記であり、外部提出時は正式な著者名・所属に置換する必要がある。

## 2026-06-02: 査読レポート3 最終微修正

### 入力

- Review file: `sect-sutra-map-review-report-3.md`
- Target paper: `docs/paper/sect-sutra-map-paper-2.pdf`
- Target response memo: `docs/sect-sutra-map-review-response-2.md`

### 主要対応

- 第3ラウンド査読の判定は「採択可。編集上の微修正のみ。再査読不要」。
- 著者名を内部識別子 `dueyama` から `上山大信` へ置換した。
- データ節の `v0.1で用いたテキスト数は15、チャンク数は433である` を、投稿版向けに `本稿で用いたテキスト数は15、チャンク数は433である` へ変更した。
- 表1の `畺良耶舍`、`實叉難陀` と参考文献の `Kumārajīva` は、PDF表示の最終確認対象として扱った。
- 第3稿ファイルとして `docs/paper/sect-sutra-map-paper-3.pdf`、`docs/paper/sect-sutra-map-paper-3.tex`、`docs/sect-sutra-map-review-response-3.md` を作成した。

### 残る投稿前確認

- 所属、連絡先、投稿先スタイルが必要な場合は、投稿先の指定に合わせて表紙・参考文献体裁を調整する。

## 2026-06-02: オリジナリティ・先行研究レポート対応

### 入力

- Report file: `sect-sutra-map-author-report-originality.md`
- Target paper: `docs/paper/sect-sutra-map-paper.tex`

### 主要対応

- レポートの主旨は、本稿の新規性を「仏教文献への embedding 初適用」ではなく、「日本仏教の宗派別参照群・異訳・親鸞文献・チャンク分布・多言語パイロットを統合した探索地図」として明確化すること。
- 要旨に、word embedding、parallel passage detection、cross-lingual semantic textual similarity、stylometry の既存研究を踏まえた位置づけを追記した。
- 導入部に、Buddhist NLP / Buddhist DH の簡潔な先行研究レビューを追加した。
- 考察に、阿弥陀経二訳と word embedding / stylometry、教行信証と parallel passage / intertextuality、多言語パイロットと cross-lingual STS / MITRA の関係を追記した。
- 結論に、既存研究を置き換えるのではなく、意味マップ・文体マップ・引用参照マップを分離して重ねる探索基盤であることを再掲した。
- 参考文献に、CBETA、BDRC、Hung et al. 2010、Bingenheimer et al. 2017、Huang and Wang 2023、Nehrdich 2020、Felbur et al. 2022、Lugli et al. 2022、DharmaNexus、MITRA を追加した。

### 生成物

- `docs/paper/sect-sutra-map-paper-4.tex`
- `docs/paper/sect-sutra-map-paper-4.pdf`
- `docs/sect-sutra-map-author-report-originality-response.md`

### 残る投稿前確認

- 投稿先の参考文献スタイルに応じて、句読点、アクセス日、DOI表記、プレプリントの扱いを整える。

## 2026-06-02: 先行研究レビュー追加後レポート微修正

### 入力

- Report file: `sect-sutra-map-author-report-literature-review-after-revision.md`
- Target paper: `docs/paper/sect-sutra-map-paper-4.pdf`
- Target response memo: `docs/sect-sutra-map-author-report-originality-response.md`

### 主要対応

- レポートの総合判断は「採択可に近い。編集上の微修正のみ。再査読不要相当」。
- 導入部に `問題設定` と `関連研究と本稿の位置づけ` の小見出しを追加し、読者が問題設定と先行研究レビューを追いやすい構成にした。
- 導入部のデジタル資源に関する引用順を調整した。
- MITRA について、本文では `近年のプレプリント`、参考文献では `arXiv preprint` と明記した。
- 第5稿ファイルとして `docs/paper/sect-sutra-map-paper-5.pdf`、`docs/paper/sect-sutra-map-paper-5.tex`、`docs/sect-sutra-map-author-report-literature-review-after-revision-response.md` を作成した。

### 残る投稿前確認

- 参考文献全体の句読点、アクセス日、DOI表記、URL改行は、投稿先スタイルに合わせて最終調整する。
- `Kumārajīva`、`Gaṇḍavyūha`、`Pāli` などの特殊文字はPDF上の表示を確認する。投稿先のPDFテキスト抽出仕様によっては追加調整が必要になる可能性がある。

## 2026-06-02: GitHub / GitHub Pages 公開準備

### 主要対応

- ルートに `README.md` と `CITATION.cff` を追加し、公開対象、再現手順、GitHub Pages 設定、未選択ライセンスを明記した。
- `docs/index.html` を追加し、論文PDF、公開版ビューア、主要図へリンクする GitHub Pages 用トップページを作成した。
- `docs/viewer/index.html` と `docs/viewer/viewer_data.json` を追加し、GitHub Pages 上で動く公開版ビューアを作成した。
- `experiments/sect_sutra_map/make_public_viewer_data.py` を追加し、本文プレビューとローカル本文パスを除いた公開用 viewer data を生成できるようにした。
- `docs/PUBLICATION.md` と `docs/.nojekyll` を追加し、公開前チェックリストと Pages 用設定を記録した。
- `.gitignore` に legacy local corpus folders を追加し、未整理本文・探索フォルダを誤って公開しないようにした。

### 検証

- `python3 -m py_compile experiments/sect_sutra_map/*.py experiments/multilingual_sutra_map/*.py experiments/shinran_amida_sources/*.py` を実行。
- `python3 experiments/sect_sutra_map/make_public_viewer_data.py` を実行し、公開版 viewer data が 15 texts / 433 chunks で生成されることを確認。
- `docs/viewer/viewer_data.json` に local source path、本文冒頭断片、legacy local corpus path が残っていないことを確認。
- ローカル `http.server` で `docs/` を配信し、ブラウザでトップページと公開版ビューアを確認。ビューアは `15 texts / 433 chunks` を読み込み、Nearest chunks では本文プレビュー省略文を表示した。

### 残る公開前確認

- GitHub repository 名と owner が確定したら、`CITATION.cff` の `repository-code` を実URLに更新する。
- コード・論文・図のライセンス方針を決める。
- remote 作成、push、GitHub Pages 有効化は未実施。

## 2026-06-02: HTML論文ページとREADME制作経緯

### 主要対応

- `docs/paper/sect-sutra-map-paper.tex` から `docs/paper/index.html` を生成する `experiments/sect_sutra_map/make_paper_html.py` を追加した。
- GitHub Pages のトップページでは、主導線をPDFからHTML論文へ変更し、PDF版も同じ `docs/paper/` 配下に保持する構成にした。
- READMEに、上山大信の指示、Codex GPT-5.5 xhigh との反復作業、ChatGPT 5.5 Pro との査読形式のやり取りを経た、人文系データ解析論文制作プロトタイプとしての位置づけを日英で追記した。
- `docs/PUBLICATION.md` に、HTML論文、PDF版、公開版ビューアの確認項目を追加した。
- リポジトリ立ち上げから公開準備までをまとめた制作プロセス文書とHTML版を追加し、AI支援で道具準備・検証・公開物整備まで行う半自動ワークフローとして記録した。
- HTML論文と制作プロセス文書の上山大信表記を、本人Webサイトへのリンクにした。
- 公開ページから実ローカルパスを除き、プロジェクトルート表記を `Okyou/` に抽象化した。

### 検証

- `python3 experiments/sect_sutra_map/make_paper_html.py` を実行し、HTML論文を再生成した。
- `python3 experiments/sect_sutra_map/make_process_html.py` を実行し、制作プロセスHTMLを生成した。
- `python3 -m py_compile experiments/sect_sutra_map/make_paper_html.py` を実行した。
- 生成HTMLに `\begin{...}`、`\cite{...}`、`\ref{...}` などの主要な未変換LaTeX断片が残っていないことを確認した。
- 参考文献URLがHTMLリンクとして出力されることを確認した。
- ローカルブラウザで `paper/` と `process/` を確認し、著者リンク、PDFリンク、制作プロセスの道具準備・公開準備節、実ローカルパス非表示を確認した。

### 残る公開前確認

- GitHub Pages 公開後、`paper/`、PDF、公開版ビューアのリンクを実URLで再確認する。
- READMEのAI支援制作プロセス記述は、公開時のクレジット方針に合わせて必要ならさらに調整する。

## 2026-06-02: 論文の出典表現と用語付録の調整

### 主要対応

- 『顯淨土眞實教行證文類』の出典説明から、規定確認の手続き自体を本文で説明するような不自然な書き方を外し、本文では聖教DBを利用したこと、参考文献では同データベースを掲げる形に整理した。
- 謝辞に、査読者役として用いた `ChatGPT 5.5 Pro xhigh` から有益な指摘を得た旨を追記した。
- 付録「用語・モデル・ツール」を追加し、`tiktoken`、`cl100k_base`、`text-embedding-3-large`、OpenAI API、APIキー、SDK、キャッシュ、コサイン類似度、PCA、TF-IDF、GitHub Pages などを説明した。
- さらに読者がつまずきやすい語として、コーパス、前処理、正規化、埋め込み空間、L2正規化、寄与率、1標準偏差楕円、stylometry、ラベルランダム化、MRR、ROC-AUC、parallel句、intertextuality、manifest、JSON、HTML を付録に追加した。
- `docs/paper/index.html`、`docs/paper/sect-sutra-map-paper.pdf`、公開版 `docs/viewer/viewer_data.json` を再生成した。

### 検証

- `python3 experiments/sect_sutra_map/make_paper_html.py` を実行し、HTML論文を再生成した。
- `python3 -m py_compile experiments/sect_sutra_map/make_paper_html.py experiments/sect_sutra_map/make_public_viewer_data.py experiments/sect_sutra_map/build_corpus.py experiments/sect_sutra_map/embed_texts.py experiments/sect_sutra_map/make_viewer_data.py` を実行した。
- `python3 -m json.tool experiments/sect_sutra_map/manifest.json` と `python3 -m json.tool docs/viewer/viewer_data.json` を実行した。
- `uplatex -interaction=nonstopmode sect-sutra-map-paper.tex` を2回実行し、`dvipdfmx sect-sutra-map-paper.dvi` で18ページのPDFを生成した。
- 生成HTMLに、付録、追加用語、謝辞、著者リンク、聖教DBの自然な出典表現が入っていることを確認した。
- 旧文言、実ローカルパス、APIキー形式の文字列、未変換LaTeX断片が公開対象ファイルに残っていないことを確認した。

### 残る公開前確認

- GitHub Pages 公開後、`paper/` とPDFリンクを実URLで再確認する。
- 用語付録は読者反応に応じて、今後さらに短い脚注版と詳細付録版に分けてもよい。

## 2026-06-02: 三層 source-mixture map と参考文献スタイル調整

### 主要対応

- ユーザー提供の新規性改善メモを踏まえ、論文の中心を「意味・文体・引用参照の三層地図」に寄せた。
- `make_three_layer_figures.py` を追加し、既存の埋め込みキャッシュと処理済み本文から三つの図を生成した。
  - `three-layer-concept-map.png`
  - `amida-three-layer-difference.png`
  - `kyogyoshinsho-three-layer-source-mixture.png`
- 阿弥陀経二訳について、意味層、文字n-gram文体層、チャンク分布層の差分を明示した。
- 『教行信証』197チャンクについて、無量寿経、観無量寿経、羅什訳阿弥陀経、玄奘訳称讃浄土経への source-mixture を意味層・文体層・引用参照層で可視化した。
- 付録の用語見出しを `コーパス：` 形式に統一した。
- 論文本文の開発メモ風の語を、`試験的な枠組み`、`プロトタイプ`、`基礎的な前処理` などに改めた。
- 参考文献の `著者。題名。` 形式をやめ、著者・資料名・URL・閲覧日をカンマ区切りで示す形式に整えた。

### 主要数値

- Model: `text-embedding-3-large`
- 阿弥陀経二訳:
  - 意味層の本文平均ベクトル類似度: `0.8825`
  - 文体層の文字n-gram TF-IDF 類似度: `0.1833`
  - top-5チャンク近傍混合率: `0.3684`
- 『教行信証』source-mixture 平均重み:
  - 意味層: 無量寿経 `0.3705`、観無量寿経 `0.2642`、羅什訳阿弥陀経 `0.2135`、玄奘訳称讃浄土経 `0.1517`
  - 文体層: 無量寿経 `0.2942`、観無量寿経 `0.2402`、羅什訳阿弥陀経 `0.2369`、玄奘訳称讃浄土経 `0.2288`
  - 引用参照層: 未検出 `0.4958`、無量寿経 `0.4682`、観無量寿経 `0.0306`、羅什訳阿弥陀経 `0.0034`、玄奘訳称讃浄土経 `0.0020`

### 解釈

- 阿弥陀経二訳は、意味層では高く近接する一方、文字n-gram文体層では大きく離れる。これは、原内容の近さと訳語・表記の差を分けて読む必要を示す。
- 『教行信証』は、意味層では浄土三部経、とくに無量寿経へ強く寄る。一方、文体層では四参照源がより均され、引用参照層では小規模マーカー辞書で拾える明示的手がかりが断続的に現れる。
- この結果は、『教行信証』が三部経を根拠とするという文献学的理解と矛盾せず、むしろ「意味的近さ」「文体的近さ」「引用・学習経路としての近さ」を分けて可視化する必要を示す。

### 検証

- `python3 experiments/sect_sutra_map/make_three_layer_figures.py`
- `python3 experiments/sect_sutra_map/make_paper_html.py`
- `python3 -m py_compile experiments/sect_sutra_map/make_three_layer_figures.py experiments/sect_sutra_map/make_paper_html.py`
- `uplatex -interaction=nonstopmode sect-sutra-map-paper.tex` を2回実行。
- `dvipdfmx sect-sutra-map-paper.dvi`
- 参考文献ブロックに `。` が残っていないことを確認した。
- HTML論文に開発メモ風の旧表現が残っていないことを確認した。

### 未検証点

- 引用参照層は小規模なマーカー辞書に依存するため、典拠関係の有無を判定する指標ではない。
- 文体層は文字n-gram TF-IDF による初期的な操作化であり、助字、虚詞、句法、固有訳語対応はまだ組み込んでいない。
- source-mixture は softmax による重み付けであり、今後は章・巻・品の位置情報や unbalanced optimal transport などとの比較が必要である。

## 2026-06-02: 三層追加後査読への対応とHTML用語リンク

### 主要対応

- `sect-sutra-map-review-after-three-layer-addition.md` の指摘を踏まえ、三層分析の用語を整理した。
  - `文体層` を `文体・語彙層` に改めた。
  - `引用参照層` を、現状の実装に即して `明示マーカー層` とした。
  - `source-mixture map` の日本語名を `三層参照源混合地図` とした。
- 方法節に、三層参照源混合地図の操作的定義を詳述した。
  - TF-IDF の fit 対象は『教行信証』チャンクと四参照源チャンクの合併集合であることを明記した。
  - 意味層・文体・語彙層は参照源内最大類似度を用いるため、参照源チャンク数の偏りを受けうることを明記した。
  - softmax 温度を、意味層 `0.04`、文体・語彙層 `0.025` と明記した。
  - z-score 標準化は行わず、数値安定化のため行最大値を差し引く実装であることを明記した。
  - 意味層・文体・語彙層には `その他` カテゴリをまだ導入していないことを限界として明記した。
- 明示マーカー辞書の代表例表と、『教行信証』三層参照源混合地図の平均重み表を追加した。
- 図1と図12の図中表記を、本文の `三層参照源混合地図`、`文体・語彙層`、`明示マーカー層` に合わせた。
- 参考文献中の特殊文字を一部ASCII表記に変更し、PDF/HTML公開時の文字化けリスクを下げた。
- ユーザー希望により、謝辞の `ChatGPT 5.5 Pro xhigh を査読者役として` という記述は保持した。
- HTML論文では、付録「用語・モデル・ツール」に説明がある語の初出箇所から該当付録項目へ飛べるリンクを追加した。
- HTML論文の数式表示を、TeX断片をそのまま見せる方式から MathJax レンダリング方式へ変更した。HTMLソース上には `\(...\)`、`\[...\]` が残るが、ブラウザ表示では数式として組版される。

### 検証

- `python3 experiments/sect_sutra_map/make_three_layer_figures.py`
- `python3 experiments/sect_sutra_map/make_paper_html.py`
- `python3 -m py_compile experiments/sect_sutra_map/make_paper_html.py experiments/sect_sutra_map/make_three_layer_figures.py`
- `uplatex -interaction=nonstopmode sect-sutra-map-paper.tex`
- `dvipdfmx sect-sutra-map-paper.dvi`
- HTML用語リンク38件について、すべての `href="#..."` が既存IDを指すことを確認した。
- HTMLに MathJax の `tex-svg.js` 読み込みが入り、インライン数式23件・表示数式2件がMathJax対象になっていることを確認した。
- 図1と図12を目視し、主要ラベル・凡例・タイトルが重なっていないことを確認した。

### 未検証点

- in-app browser での `file://` 直接検証は、ブラウザ安全ポリシーにより実行できなかった。代替としてHTMLソース、生成図、PDF生成ログを確認した。
- `dvipdfmx` はCMap警告を1件出すが、PDF生成は完了している。PDF本文の実表示は今後の目視確認で必要に応じて調整する。

## 2026-06-02: 最終段階査読への対応

### 査読判定

- `sect-sutra-map-final-stage-review.md` では、内容面は「ほぼ投稿可能。内容面では最終盤。再査読不要相当」と評価された。
- 残る修正は、用語統一、表2の字形・表記確認、PDFメタデータ、参考文献体裁などの最終校正項目とされた。

### 主要対応

- PDFメタデータとして `pdftitle`、`pdfauthor`、`pdfkeywords` を `hyperref` に追加した。
- 4.3節に、タイトルおよび問題設定でいう引用・参照層は、現段階では経名・訳者名・固定句辞書による明示マーカー層として操作化する、という定義文を追加した。
- 表2の玄奘訳称讃浄土経マーカー例を、`稱讃淨土／稱讚淨土`、`稱讃淨土經／稱讚淨土經`、`恒河沙／殑伽沙` のように表記揺れを併記する形へ改めた。
- 図生成スクリプトの明示マーカー辞書にも `稱讃淨土`、`稱讃淨土經`、`恒河沙` を追加した。
- 阿弥陀経二訳差分図の図中表記とキャプションを `文体・語彙` に寄せた。
- マーカー辞書更新により、『教行信証』明示マーカー層の平均重みを更新した。
  - 未検出 `0.4958`
  - 無量寿経 `0.4659`
  - 観無量寿経 `0.0303`
  - 羅什訳阿弥陀経 `0.0025`
  - 玄奘訳称讃浄土経 `0.0054`
- HTML論文では、`T0360/SAT` のような大正蔵IDを `https://21dzk.l.u-tokyo.ac.jp/SAT2018/T0360.html` 形式のSAT個別ページへリンクするようにした。

### 検証

- `python3 experiments/sect_sutra_map/make_three_layer_figures.py`
- `python3 experiments/sect_sutra_map/make_paper_html.py`
- `python3 -m py_compile experiments/sect_sutra_map/make_paper_html.py experiments/sect_sutra_map/make_three_layer_figures.py`
- `uplatex -interaction=nonstopmode sect-sutra-map-paper.tex` を2回実行。
- `dvipdfmx sect-sutra-map-paper.dvi`
- bundled Python の `pypdf` でPDFメタデータを確認し、Title、Author、Keywords が入っていることを確認した。
- HTML用語リンクに欠けたアンカーがなく、MathJax読み込みが残っていることを確認した。
- HTML論文にSAT個別ページへのリンクが33件生成され、`T0360` リンクがSAT2018の該当URLを指すことを確認した。
- 阿弥陀経二訳差分図を目視し、`文体・語彙` 表記が反映されていることを確認した。

### 未検証点

- `dvipdfmx` のCMap警告は残っている。
- `pypdf` による日本語本文抽出では、固有名を含む日本語テキスト抽出が十分に機能しなかった。PDFの視覚表示は生成図・PDFで確認する必要がある。

## 2026-06-02: 『教行信証』巻別参照源傾向の追加

### 目的

- 『教行信証』のチャンク列に、総序、教巻、行巻、信巻、証巻、真仏土巻、化身土巻の巻区分を付記し、三層参照源混合地図を巻別に読めるようにした。
- 伝統的な巻別理解と照合するための予備的補助線として、各巻が無量寿経、観無量寿経、阿弥陀経二訳のどれに相対的に寄るかを確認した。

### 実装

- 本文中の巻見出しを検出し、各チャンクの中心トークンが属する見出しへ巻ラベルを割り当てた。
- 図12の『教行信証』三層参照源混合地図に巻境界と短い巻ラベルを追加した。
- 新図 `docs/figures/kyogyoshinsho-volume-source-means.png` を追加し、巻別平均の意味層、文体・語彙層、明示マーカー層を横棒で示した。
- 論文タイトルを、三層が明確に読めるよう `意味・文体・典拠マーカーの三層地図` に改めた。第三層は、経名・訳者名・固定句などの典拠マーカーにもとづく近接であり、`引用` と `参照` が独立した別層ではない。

### 主要結果

- 意味層では、総序を含む全巻で無量寿経が最大となった。
  - 教巻 `0.5744`
  - 真仏土巻 `0.5287`
  - 総序 `0.5008`
  - 証巻 `0.4648`
  - 行巻 `0.3436`
  - 化身土巻 `0.3408`
  - 信巻 `0.3188`
- 文体・語彙層でも全巻で無量寿経が最大となったが、行巻、信巻、化身土巻では観無量寿経・阿弥陀経二訳も一定の比率で混ざった。
- 明示マーカー層では、総序、教巻、行巻、証巻で無量寿経系マーカーが最大となった。一方、信巻、真仏土巻、化身土巻では `未検出` が最大となった。

### 解釈

- この結果は、『教行信証』が浄土三部経、とくに無量寿経を中心的根拠とするという理解と矛盾しない。
- ただし、巻ごとの教義的性格を自動判定するものではない。巻別平均は、伝統的読解や精密な引文調査と照合するための探索的な補助線である。
- 明示マーカー層の `未検出` は、典拠関係がないことを意味しない。固定句・経名・訳者名だけでは拾えない議論、釈義、引用経路が多い可能性を示す。

### 検証

- `python3 experiments/sect_sutra_map/make_three_layer_figures.py`
- `python3 experiments/sect_sutra_map/make_paper_html.py`
- `python3 -m py_compile experiments/sect_sutra_map/make_three_layer_figures.py experiments/sect_sutra_map/make_paper_html.py`
- `uplatex -interaction=nonstopmode sect-sutra-map-paper.tex` を2回実行。
- `dvipdfmx sect-sutra-map-paper.dvi`
- ローカルプレビューで論文HTMLを確認し、旧タイトル `意味・文体・引用・参照` が消え、新タイトル、図13、表9が表示されることを確認した。

### 未検証点

- 巻区分はチャンク中心位置による推定であり、巻境界付近のチャンクは厳密な本文単位ではない。
- 今後は固定長チャンクではなく、巻・段落・引用単位にもとづく自然単位チャンク化と比較する必要がある。
