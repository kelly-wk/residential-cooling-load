# 研究報告 / Research Report

## 1. 課題 / Question

回収された Colab 群は、住宅の時間別冷房負荷を計算しようとしていましたが、一連の notebook としては再現不能でした。目的は、元記録から確認できる式と入力形式を保ちつつ、どの成分が最終値に寄与したかを監査できる最小モデルへ修復することです。

The recovered Colab cluster attempted an hourly residential cooling-load calculation but was not reproducible as a sequence. The repair preserves the equations and input grammar supported by the record while making every component of the final value auditable.

## 2. 原記録の診断 / Diagnosis of the record

| Colab | 保存状態 / Saved state | 判定 / Finding |
|---|---|---|
| `Step4_HeatLoadOfHouse_1` | 4/4 code cells executed | `Wall` と 6 方位の例は動作。保存出力 `-57.835826... W` を確認。 / Working wall-only example with a saved `-57.835826... W` result. |
| `Step4_HeatLoadOfHouse_2` | 2/3 code cells executed | 主要ループに `IndentationError`。 / Main loop ended with `IndentationError`. |
| `Step4_HeatLoadOfHouse_3` | 未実行 / not executed | `loadelement`、気象 CSV、入力ファイルが欠落。後半には仮式 `100 * outside_temp`。 / Missing module and files; later cell contains a placeholder formula. |
| `Step4_HeatLoadOfHouse_4` | 1/1 code cell executed | `lelements=[]` のままなので全時刻 `0 W` を書き出す論理不具合。 / Empty element list makes every written load zero. |

## 3. 方法 / Method

各時刻の正味顕熱を次の成分和として定義しました。

The signed sensible gain is defined as the sum of:

\[
Q_{net}=Q_{wall}+Q_{win,cond}+Q_{win,solar}+Q_{vent}+Q_{internal}.
\]

壁は原 notebook と同じ sol-air 近似を使います。

The wall term follows the recovered sol-air approximation:

\[
Q_{wall}=UA\left(T_o+\frac{\alpha I}{h_o}-T_i\right).
\]

窓の貫流熱と日射取得、換気顕熱はそれぞれ次式です。

Window conduction, window solar gain, and ventilation sensible gain are:

\[
Q_{win,cond}=UA(T_o-T_i),\quad
Q_{win,solar}=SHGC\,A\,I,
\]

\[
Q_{vent}=\rho c_p\frac{V\,ACH}{3600}(T_o-T_i).
\]

冷房・暖房指標は符号付き熱量の正負を分けただけであり、機器消費電力ではありません。

Cooling and heating indicators are the positive and negative parts of the signed gain; they are not equipment electricity consumption.

## 4. 検証 / Validation

1. 原 notebook の壁だけの例を手計算ゴールデンケースとして固定し、`-57.83582608695667 W` と 9 桁で一致。
2. 5 成分の和が `signed_sensible_gain_w` と一致する保存則テスト。
3. 冷房側・暖房側が符号付き値の正部分として一致する境界テスト。
4. 空の建物設定と列不足の気象 CSV を明示的に拒否。
5. 9 要素・4 合成時点の end-to-end 実行を確認。

1. The wall-only record is fixed as a golden case and matches `-57.83582608695667 W` to nine decimal places.
2. A conservation test reconciles the five components with the signed total.
3. Boundary tests verify the nonnegative cooling/heating split.
4. Empty building inputs and incomplete weather tables are rejected.
5. An end-to-end run covers nine elements and four synthetic hours.

## 5. 結果 / Results

`python -m unittest` は 5/5 成功。合成 fixture の最大冷房指標は `3,491.187 W`、冬夜の暖房指標は `1,388.627 W` でした。これらは計算検証用であり、東京 2020 年の気象結果ではありません。

All five tests pass. The synthetic fixture yields a `3,491.187 W` peak cooling indicator and a `1,388.627 W` winter-night heating indicator. These verify the pipeline and are not Tokyo-2020 weather findings.

## 6. 限界 / Limitations

- 元の気象表と `loadelement.py` は未回収。
- 定常モデルで熱容量・時間遅れを扱わない。
- 潜熱、人体・機器スケジュール、ガラス入射角、日影、設備効率を扱わない。
- 合成 4 時点は妥当性検証ではなくソフトウェア検証。

- The source weather table and `loadelement.py` were not recovered.
- The steady-state model omits thermal mass and lag.
- Latent loads, schedules, glazing angle effects, shading, and HVAC efficiency are excluded.
- Four synthetic points test software behavior, not physical validity.
