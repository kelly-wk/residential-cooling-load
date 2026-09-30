"""Command-line entry point."""

from __future__ import annotations

import argparse

from .config import parse_building_config
from .model import read_weather_csv, run_weather_series, write_results_csv


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the educational hourly sensible-load model")
    parser.add_argument("--config", required=True)
    parser.add_argument("--weather", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--indoor-temp", type=float, default=24.0)
    args = parser.parse_args()

    config = parse_building_config(args.config)
    weather = read_weather_csv(args.weather)
    rows = run_weather_series(config, weather, args.indoor_temp)
    write_results_csv(rows, args.output)

    peak = max(rows, key=lambda row: float(row["cooling_load_w"]))
    print(f"rows={len(rows)} elements={config.element_count}")
    print(f"peak={float(peak['cooling_load_w']):.3f} W at {peak['timestamp']}")
    print(f"output={args.output}")


if __name__ == "__main__":
    main()
