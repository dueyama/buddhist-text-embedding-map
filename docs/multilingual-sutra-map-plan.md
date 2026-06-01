# 多言語お経比較 v0 計画

## 目的

漢訳仏典、チベット訳、英訳、将来的にはパーリ・サンスクリットを同じ意味空間に置き、同一または近縁の経典が言語を越えて近く出るかを検証する。

この実験では、宗派の正解分類ではなく、次の二つを分けて見る。

- 意味一致: 同じ経典または近い原典に由来するテキストが、言語を越えて近くなるか。
- 言語・翻訳差: 同じ言語、同じ翻訳文化、同じ文体の影響で近くなるか。

## 基本方針

- raw text は git 管理しない。
- source URL、利用条件、credit は manifest に明示する。
- 公開物には本文を転載せず、要約・数値・図・出典表記だけを残す。
- 全文ベクトルだけでなく、チャンク単位の最近傍も見る。
- まず `text-embedding-3-large` を基準線にする。
- チベット語を本格的に扱う段階で、仏教文献向けの MITRA-E 系 embedding も比較する。

## データ源候補

| 対象 | 用途 | 備考 |
| --- | --- | --- |
| SAT 大正新脩大藏經テキストデータベース | 漢訳仏典 | 既存 pipeline で利用中。 |
| 84000 Reading Room | チベット大蔵経由来の英訳、Toh 番号確認 | 出典表記が必須。本文利用は CC BY-NC-ND 4.0 の範囲に注意。API は公開 API としては使わない。 |
| BDRC / BUDA | チベット語本文・書誌情報 | 大規模なチベット仏教文献アーカイブ。本文取得方法と利用条件は個別確認。 |
| Adarshah | チベット語検索・本文確認 | 初期調査・照合用候補。 |
| SuttaCentral / sc-data | パーリ、漢訳、チベット、サンスクリット系の並行関係 | 初期仏教文献や対応表の確認に有用。 |

## 初回候補

初回は、同一経典性を見やすいものを優先する。般若心経は有名だが、短本・長本・漢訳起源説・チベット大蔵経収載系統の差が絡むため、最初の判定対象としては少し難しい。

| 優先 | 経典ファミリー | 漢訳候補 | チベット/英訳候補 | 理由 |
| --- | --- | --- | --- | --- |
| 1 | 金剛経 | `T0235` | 84000 `Toh 16` | 既存 corpus に漢訳があり、初回の多言語比較に向く。 |
| 2 | 維摩経 | `T0475` | Toh 番号は要確認 | 既存 corpus に漢訳があり、大乗経典として比較しやすい。 |
| 3 | 解深密経 | `T0676` | Toh 番号は要確認 | 既存 corpus に玄奘訳があり、瑜伽行・唯識系の意味まとまりを見やすい。 |
| 4 | 法華経 | `T0262` | `Toh 113` 候補 | 長文なので、章単位の対応付けが必要。 |
| 5 | 般若心経 | `T0251` | `Toh 21` / `Toh 531` 候補 | 有名で短いが、版差が強いため検証対象として扱う。 |

## manifest 拡張案

既存の `experiments/sect_sutra_map/manifest.json` を直接肥大化させず、まずは `experiments/multilingual_sutra_map/manifest.json` を別に作る。

追加したいフィールド:

- `work_id`: 同じ経典ファミリーを束ねる ID。例: `diamond_sutra`
- `language`: `lzh`, `bo`, `en`, `pi`, `sa` など。
- `script`: `Han`, `Tibt`, `Latn`, `Deva` など。
- `canonical_id`: `T0235`, `Toh16` など。
- `source_license`: 利用条件の短い記録。
- `credit`: 成果物に出す出典表記。
- `source_kind`: `sat`, `84000_html`, `bdrc`, `local` など。
- `source_url`: 公式確認先。
- `source_path`: raw text をローカル保存する場合の ignored path。
- `alignment_level`: `whole_text`, `chapter`, `section`, `chunk`。
- `notes`: 版差・対応の未確定点。

## 評価指標

- Cross-language nearest neighbor: 漢訳の最近傍に同じ `work_id` の英訳・チベット訳が入るか。
- Family margin: 同じ `work_id` 内の平均類似度が、別 `work_id` との平均類似度より高いか。
- Language clustering: 同じ言語だけが固まってしまっていないか。
- Chunk retrieval: 漢訳チャンクから、同じ経典の英訳/チベット訳チャンクが上位に来るか。
- Negative control: 同じ般若部でも別経典、同じ訳者でも別主題、などが過度に近くなっていないか。

## viewer 拡張案

- 色: `work_id`、つまり同一経典ファミリー。
- 形: `language`。
- 線: 同じ `work_id` の異言語テキストを結ぶ。
- tooltip/detail: canonical ID、source、credit、license note、最近傍。
- filter: language、source、work_id、canonical tradition。

## 初回実装ステップ

1. `experiments/multilingual_sutra_map/manifest.json` を作り、金剛経だけを登録する。
2. 漢訳 `T0235` は既存 processed text を再利用する。
3. 84000 `Toh 16` はまず英訳を対象にし、本文利用条件と credit を manifest に入れる。
4. チベット語本文は BDRC/Adarshah/84000 Scholar Room の取得可能性を確認してから追加する。
5. `text-embedding-3-large` で漢訳・英訳を比較し、可能なら MITRA-E でも同じ評価を行う。
6. 結果は `docs/results.md` に、raw text なしで数値と解釈だけ追記する。

## 注意点

- 「意味で一緒になるか」を見るには、単なる全文平均だけでは弱い。長文同士では構成差が埋もれるため、チャンク単位の対応検索が重要。
- 般若心経は短くて便利だが、短本と長本の差が大きいため、初回成功/失敗の判定には使いにくい。
- 84000 は翻訳本文を公開しているが、利用条件上、出典表示と非商用・改変禁止の扱いに注意する。実験結果には本文抜粋を載せない。
- チベット語本文の取得元は、利用条件と安定した URL を確認してから pipeline に入れる。

## 参考資料

- SAT 大正新脩大藏經テキストデータベース: https://21dzk.l.u-tokyo.ac.jp/SAT/
- 84000 Reading Room: https://84000.co/all-publications
- 84000 Terms of Use: https://www.84000.co/documents/terms-of-use
- BDRC: https://www.bdrc.io/
- SuttaCentral sc-data: https://github.com/suttacentral/sc-data
- MITRA paper: https://arxiv.org/abs/2601.06400
