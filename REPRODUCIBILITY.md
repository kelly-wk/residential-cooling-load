# 再現手順 / Reproducibility

## 必要条件 / Requirements

- Python 3.10 以上 / Python 3.10+
- 外部 Python パッケージ不要 / no third-party Python dependency

## 1. テスト / Tests

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

期待値 / Expected: `Ran 5 tests ... OK`.

## 2. 合成例 / Synthetic example

```bash
PYTHONPATH=src python -m residential_cooling_load \
  --config examples/building.txt \
  --weather examples/weather_synthetic.csv \
  --output outputs/example_results.csv
```

期待されるピーク / Expected peak:

```text
rows=4 elements=9
peak=3491.187 W at synthetic-summer-noon
```

## 3. 入力契約 / Input contract

建物設定の例は `examples/building.txt`、気象 CSV の列は `Date,DBO,H,S,W,N,E,P` です。`DBO` は ℃、各方位日射は W/m² です。

See `examples/building.txt` for the building grammar. Weather columns are `Date,DBO,H,S,W,N,E,P`; `DBO` is °C and directional irradiance is W/m².

## 再現性の境界 / Reproducibility boundary

元の `Tokyo_2020_Ave.csv` は含まれず、保存出力にも完全な時系列結果はありません。したがって、このリポジトリは修復済み計算系と合成例を再現しますが、原授業データでの数値結果は再現しません。

The original `Tokyo_2020_Ave.csv` is not included and the saved notebook output does not contain its complete time series. This repository reproduces the repaired calculation path and synthetic example, not results from the unavailable course data.
