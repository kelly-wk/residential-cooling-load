# 住宅の時間別冷房負荷モデル / Hourly Residential Cooling-Load Model

**Colab 記録からの修復版・教育用途 / Repaired from Colab evidence · educational use**

住宅の壁、窓、日射、換気、内部発熱を、成分別に追跡できる定常顕熱モデルです。元の 4 本の Colab は、壁だけの動作例、インデントエラー、欠落モジュール、空の要素リストによるゼロ出力という段階に分かれていました。本リポジトリは、その履歴を隠さず、単位契約・入力検証・ゴールデンテストを備えた再現可能な教育モデルへ修復したものです。

This repository turns four fragmented Colab records into a reproducible steady-state sensible-load model. The historical notebooks included a working wall-only example, an indentation failure, an unavailable module, and a zero-output path caused by an empty element list. The repair adds explicit units, validated inputs, component-level output, and golden tests without claiming that the original notebooks had already achieved this state.

[紹介ページ / Presentation](./docs/index.html) · [研究報告 / Report](./REPORT.md) · [再現手順 / Reproduce](./REPRODUCIBILITY.md) · [Colab](./notebooks/reproduction.public.ipynb) · [来歴 / Provenance](./PROVENANCE.md)

## 何が再現できるか / What is reproducible

- 壁の sol-air 温度近似 / wall sol-air approximation
- 窓の貫流熱と日射取得 / window conduction and solar gain
- 換気顕熱 / ventilation sensible gain
- 内部発熱 / internal sensible gain
- 正味顕熱、冷房側・暖房側の正部分 / signed sensible gain and nonnegative cooling/heating indicators
- 合成気象 4 時点を使う完全なテスト実行 / end-to-end run on four synthetic weather points

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m residential_cooling_load \
  --config examples/building.txt \
  --weather examples/weather_synthetic.csv \
  --output outputs/example_results.csv
```

検証済みの合成例では 5 テストが成功し、最大冷房指標は `3,491.187 W`（`synthetic-summer-noon`）です。この値は実測気象や設計条件に基づく成果ではなく、計算経路を検証するための fixture です。

The verified synthetic example passes five tests and produces a peak cooling indicator of `3,491.187 W` at `synthetic-summer-noon`. This is a fixture for checking the calculation path, not a weather-derived design result.

## 公開境界 / Publication boundary

元の `Tokyo_2020_Ave.csv`、`Step2_input.txt`、`loadelement.py` は回収できませんでした。したがって、来歴不明の気象データや、それに由来すると装える実測結果は含めていません。`examples/building.txt` は保存された Colab 出力に見える数値を再構成した監査用 fixture、気象表は明示的な合成データです。

The historical weather CSV, configuration file, and `loadelement.py` were not recovered. No source-derived weather result is published. The building fixture reconstructs values visible in saved Colab output, and the weather fixture is explicitly synthetic.

## 適用範囲 / Scope

これは定常・顕熱のみの教育モデルです。熱容量、潜熱、機器効率、動的蓄熱、法規計算は扱わないため、設備選定や実建物の設計には使用しないでください。

This is a steady-state sensible-load teaching model. It excludes thermal mass, latent loads, equipment efficiency, dynamic storage, and code-compliance procedures and must not be used for HVAC sizing or real-building design.
