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
- 法華系
  - 妙法蓮華經 local text: `13` chunks, `4718` chars
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
  - 妙法蓮華経 local text: `0.8275`
  - 教行信証: `0.8058`
- 無量寿経の近傍:
  - 妙法蓮華経 local text: `0.9111`
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
  - 妙法蓮華経 local text: `0.8293`
  - 無量寿経: `0.8221`
  - 大日経: `0.7886`

### 解釈

- 浄土三部経は、阿弥陀経から見ると無量寿経・観無量寿経が上位に来ており、初期仮説どおりまとまりが見える。
- 真言系では、金剛頂経・理趣経・大日経が互いに近く、密教経典クラスタとして観察できる。
- 禅系の経典だけでは、曹洞・臨済・黄檗の差はまだ出ない。これは予想どおりで、祖師文献や語録を足す必要がある。
- 教行信証は浄土三部経にも近いが、維摩経や大日経にも高く出る。全文平均では、宗派性だけでなく引用・総合文献としての広がりが強く出ている可能性がある。
- 妙法蓮華経の local text は `4718` chars と短く、全文ではない可能性が高い。法華系の評価は SAT full text 取得後に再確認する。

### 生成物

- Corpus index: `experiments/sect_sutra_map/data/processed/corpus_index.json`
- Embeddings: `experiments/sect_sutra_map/outputs/embeddings.json`
- Viewer data: `experiments/sect_sutra_map/outputs/viewer_data.json`
- Static viewer: `experiments/sect_sutra_map/viewer/index.html`

Generated corpus/output files are not committed. The viewer is served locally from `experiments/sect_sutra_map`.

### 未検証点

- 大部経典は SAT の直接表示範囲を v0 corpus としているため、全文比較ではないものがある。
- 法華経 local text は短く、全文 SAT に差し替える必要がある。
- 宗派重心は `core_sutra` と `founder_text` の単純平均なので、宗派ごとの重み付けは未実装。
- 祖師文献は教行信証だけで、禅・天台・真言・日蓮の祖師文献は未投入。
- PCA 2D map は可視化用であり、距離の厳密解釈には heatmap と nearest list を併用する必要がある。
