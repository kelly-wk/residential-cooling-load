# 来歴と公開判断 / Provenance and Publication Decision

## 一次証拠 / Primary evidence

| Colab notebook | Role |
|---|---|
| `Step4_HeatLoadOfHouse_1.ipynb` | 壁クラスとゴールデン出力 / wall class and golden output |
| `Step4_HeatLoadOfHouse_2.ipynb` | 気象ループ、IndentationError / weather loop ending in an indentation error |
| `Step4_HeatLoadOfHouse_3.ipynb` | 入力 grammar と欠落依存 / input grammar and missing dependencies |
| `Step4_HeatLoadOfHouse_4.ipynb` | 空リストによるゼロ出力 / zero-output path caused by an empty list |

Google Drive のファイル ID は非公開の復元監査にのみ保持し、この公開リポジトリには含めません。

Google Drive file identifiers are retained only in the private recovery audit, not in this public repository.

## 修復コードの位置付け / Status of the repaired code

公開コードは原 notebook の直接コピーではありません。保存記録から確認できた入力 grammar、壁式、物性値を根拠に、標準的な定常顕熱式でクリーンルーム再実装したものです。元 notebook は再配布しません。

The public code is not a verbatim export of the notebooks. It is a clean-room reconstruction based on the recorded input grammar, wall equation, and material values, completed with standard steady-state sensible-load equations. The source notebooks are not redistributed.

## データ / Data

- `examples/weather_synthetic.csv`: 本リポジトリ用に作成した合成 fixture。
- `examples/building.txt`: notebook 保存出力に表示された設定値の再構成。
- `Tokyo_2020_Ave.csv`: 未回収、未配布、結果主張に不使用。
- `loadelement.py`: 未回収。公開実装はこれをコピーしていない。

- `examples/weather_synthetic.csv`: synthetic fixture created for this repository.
- `examples/building.txt`: reconstruction of values visible in saved notebook output.
- `Tokyo_2020_Ave.csv`: not recovered, not redistributed, and not used for claims.
- `loadelement.py`: not recovered; the public implementation does not copy it.

## 帰属 / Attribution

これは授業過程の修復・再構成であり、建築熱負荷の新規理論を提案する研究ではありません。公開時は「coursework reconstruction / 教育課題の修復」と明示してください。

This is a repaired coursework reconstruction, not a claim of a novel building-physics method. Any public presentation should retain that label.
