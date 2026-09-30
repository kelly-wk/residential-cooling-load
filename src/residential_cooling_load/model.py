"""Calculation pipeline with component-level audit output."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

from .config import BuildingConfig
from .elements import WeatherPoint


ORIENTATIONS = ("H", "S", "W", "N", "E", "P")


def calculate_hour(
    config: BuildingConfig,
    weather: WeatherPoint,
    indoor_temp_c: float = 24.0,
) -> dict[str, float | str]:
    """Return signed heat gains and nonnegative cooling/heating indicators.

    Positive signed gain means net sensible heat enters the room. Negative
    signed gain means net heat loss. ``cooling_load_w`` and ``heating_load_w``
    are the positive and negative parts respectively; no HVAC efficiency or
    latent load is modeled.
    """

    wall_gain = sum(wall.heat_gain_w(weather, indoor_temp_c) for wall in config.walls)
    window_conduction = sum(
        window.conduction_w(weather, indoor_temp_c) for window in config.windows
    )
    window_solar = sum(window.solar_gain_w(weather) for window in config.windows)
    ventilation = sum(
        item.heat_gain_w(weather, indoor_temp_c) for item in config.ventilation
    )
    internal = sum(item.watts for item in config.internal_gains)
    signed = wall_gain + window_conduction + window_solar + ventilation + internal
    return {
        "timestamp": weather.timestamp,
        "outside_temp_c": weather.dry_bulb_c,
        "wall_gain_w": wall_gain,
        "window_conduction_w": window_conduction,
        "window_solar_w": window_solar,
        "ventilation_gain_w": ventilation,
        "internal_gain_w": internal,
        "signed_sensible_gain_w": signed,
        "cooling_load_w": max(signed, 0.0),
        "heating_load_w": max(-signed, 0.0),
    }


def read_weather_csv(path: str | Path) -> list[WeatherPoint]:
    """Read Date, DBO, H, S, W, N, E, P columns from an hourly CSV."""

    points: list[WeatherPoint] = []
    with Path(path).open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"Date", "DBO", *ORIENTATIONS}
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            missing = sorted(required - set(reader.fieldnames or []))
            raise ValueError(f"Weather CSV is missing columns: {', '.join(missing)}")
        for line_number, row in enumerate(reader, 2):
            try:
                points.append(
                    WeatherPoint(
                        timestamp=row["Date"],
                        dry_bulb_c=float(row["DBO"]),
                        irradiance_w_m2={key: float(row[key]) for key in ORIENTATIONS},
                    )
                )
            except (TypeError, ValueError) as exc:
                raise ValueError(f"Invalid weather value on line {line_number}: {exc}") from exc
    if not points:
        raise ValueError("Weather CSV contains no data rows")
    return points


def run_weather_series(
    config: BuildingConfig,
    weather: Iterable[WeatherPoint],
    indoor_temp_c: float = 24.0,
) -> list[dict[str, float | str]]:
    return [calculate_hour(config, point, indoor_temp_c) for point in weather]


def write_results_csv(rows: Iterable[dict[str, float | str]], path: str | Path) -> None:
    records = list(rows)
    if not records:
        raise ValueError("No result rows to write")
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(records[0]),
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(records)
