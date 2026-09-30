from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from residential_cooling_load.config import BuildingConfig, parse_building_config
from residential_cooling_load.elements import InternalGain, Ventilation, Wall, WeatherPoint, Window
from residential_cooling_load.model import calculate_hour, read_weather_csv


ROOT = Path(__file__).resolve().parents[1]


class ElementTests(unittest.TestCase):
    def test_recovered_wall_equation_matches_hand_calculation(self) -> None:
        walls = (
            Wall(0.518, "H", 0.4, 16),
            Wall(0.518, "S", 0.4, 6),
            Wall(0.518, "W", 0.4, 12),
            Wall(0.518, "N", 0.4, 12),
            Wall(0.518, "E", 0.4, 12),
            Wall(0.518, "P", 0.4, 16),
        )
        config = BuildingConfig(walls, (), (), ())
        weather = WeatherPoint(
            "golden",
            20.0,
            {"H": 400.0, "S": 200.0, "W": 100.0, "N": 50.0, "E": 100.0, "P": 0.0},
        )
        row = calculate_hour(config, weather, indoor_temp_c=24.0)
        self.assertAlmostEqual(float(row["signed_sensible_gain_w"]), -57.83582608695667, places=9)

    def test_component_balance_and_positive_part(self) -> None:
        config = BuildingConfig(
            walls=(Wall(0.5, "S", 0.4, 10),),
            windows=(Window(2.0, 0.5, "S", 2),),
            internal_gains=(InternalGain(100),),
            ventilation=(Ventilation(50, 0.5),),
        )
        weather = WeatherPoint("case", 30, {key: 0 for key in "HSWNEP"} | {"S": 400})
        row = calculate_hour(config, weather, 24)
        parts = sum(
            float(row[key])
            for key in (
                "wall_gain_w",
                "window_conduction_w",
                "window_solar_w",
                "ventilation_gain_w",
                "internal_gain_w",
            )
        )
        self.assertAlmostEqual(parts, float(row["signed_sensible_gain_w"]))
        self.assertAlmostEqual(float(row["cooling_load_w"]), max(parts, 0))
        self.assertAlmostEqual(float(row["heating_load_w"]), max(-parts, 0))


class PipelineTests(unittest.TestCase):
    def test_sample_config_and_weather(self) -> None:
        config = parse_building_config(ROOT / "examples" / "building.txt")
        weather = read_weather_csv(ROOT / "examples" / "weather_synthetic.csv")
        self.assertEqual(config.element_count, 9)
        self.assertEqual(len(weather), 4)
        rows = [calculate_hour(config, point) for point in weather]
        self.assertGreater(float(rows[-1]["cooling_load_w"]), 0)
        self.assertGreater(float(rows[0]["heating_load_w"]), 0)

    def test_empty_configuration_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "empty.txt"
            path.write_text("# no elements\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "no load elements"):
                parse_building_config(path)

    def test_missing_weather_column_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.csv"
            path.write_text("Date,DBO,H,S,W,N,E\ncase,20,0,0,0,0,0\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "missing columns"):
                read_weather_csv(path)


if __name__ == "__main__":
    unittest.main()
