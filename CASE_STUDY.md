# 住宅の時間別冷房負荷モデル / Hourly Residential Cooling-Load Model

[紹介ページを開く / Open the presentation page](https://kelly-wk.github.io/residential-cooling-load/)

> **教育モデル修復済み・データ由来結果非公開 / Educational model repaired · source-derived results withheld**  
> 公開ケーススタディ / Public case study

## 概要 / Overview

ゼロ出力だった熱負荷計算を、単位契約・成分分解・保存則テストを備えた教育モデルへ修復。

An all-zero cooling-load pipeline repaired into an educational model with unit contracts, component breakdowns, and conservation tests.

## 主なポイント / Highlights

1. **全時刻ゼロだった計算経路を修復し、非ゼロの負荷成分を追跡可能にした。**  
   Repaired an all-zero computation path and made nonzero load components traceable.
2. **壁・窓・換気・内部発熱などを透明に分解し、入出力単位を設定で明示。**  
   Exposed wall, window, ventilation, and internal-gain components with explicit input/output units.
3. **エネルギーバランスと手計算ゴールデンケースで、主要式の整合性を検証。**  
   Checked core equations with energy-balance assertions and hand-calculated golden cases.

## 研究の流れ / Research Flow

| 段階 / Stage | 内容 / Evidence |
|---|---|
| **課題 / Problem** | 無効なゼロ出力を検出・修復し、時間別冷房負荷の計算根拠を監査可能にする。<br>Detect and repair invalid zero output while making hourly cooling-load calculations auditable. |
| **方法 / Method** | 簡略熱収支を成分別に実装し、単位付き設定とシナリオ入力で駆動する。<br>Implement a simplified component-wise heat balance driven by unit-aware configuration and scenarios. |
| **検証 / Validation** | 保存則、符号、手計算値、境界条件をテストし、成分合計と総負荷を照合する。<br>Test conservation, signs, hand calculations, and boundary cases, reconciling component sums with total load. |
| **成果 / Outcome** | 説明可能な教育用プロトタイプへ修復したが、設計用計算としては位置付けない。<br>Repaired the pipeline into an explainable educational prototype, not a design-calculation tool. |

## 使用手法 / Methods

Python standard library, Heat-balance modeling, Unit-aware configuration, Conservation tests, Golden tests, Scenario analysis

## 限界と適用範囲 / Limitations & Scope

- 気象表の来歴が未確認で、モデルも定常顕熱のみを扱うため、設備選定や法規適合には使用できない。  
  Weather-table provenance is unconfirmed, and the model covers only steady sensible loads, so it is unsuitable for equipment sizing or code compliance.

## 公開範囲 / Publication Boundary

教育モデルの設計と検証は紹介可能だが、来歴未確認の気象データと派生結果は除外。

The educational model and its checks can be described, while weather data of unclear provenance and derived results are excluded.

---

この文書は公開可能な範囲だけで構成されています。  
This document contains only material cleared for public presentation.
