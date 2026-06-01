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
