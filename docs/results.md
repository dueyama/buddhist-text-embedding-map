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
    - 出典確認先: 浄土真宗本願寺派総合研究所『浄土真宗聖典』聖教データベース
    - 利用規定: 成果公表時は同データベースを利用した旨を明記する必要がある
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
- Visual check: `/private/tmp/okyou-translator-map.png`

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

### 主要な混合率

| Pair | top-5 chunk neighbor mixing |
| --- | --- |
| 阿弥陀経 / 稱讃淨土経 | `0.37` |
| 稱讃淨土経 / 無量寿経 | `0.19` |
| 無量寿経 / 観無量寿経 | `0.17` |
| 金剛経 / 維摩経 | `0.14` |
| 金剛頂経 / 理趣経 | `0.12` |
| 阿弥陀経 / 理趣経 | `0.04` |

### 解釈

- 平均点マップは全体の位置を読むには便利だが、経典内部の主題の広がりを消してしまう。
- 阿弥陀経二訳は平均ベクトルでも近く、チャンク近傍混合率も高い。内容対応が部分単位でも出ている可能性がある。
- 教行信証は引用・教義的総合を含むため、チャンク分布の広がりが大きい。祖師文献を一点で扱うと情報を落としやすい。
- 2D の楕円は PCA 投影上の見え方なので、重なりの判定には高次元空間の近傍混合率を併用する。

### 未検証点

- チャンク境界は 700 tokens / 100 overlap の機械分割で、巻・品・段落などの自然単位ではない。
- 楕円は 2D PCA 上の 1σ 近似なので、非楕円形・多峰性の分布を十分には表現できない。
- 今後は chapter/section 単位での分布、密度推定、Earth Mover's Distance なども比較候補にする。
