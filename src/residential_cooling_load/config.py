"""Parser for the line-oriented configuration found in the recovered Colab record."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .elements import InternalGain, Ventilation, Wall, Window


@dataclass(frozen=True)
class BuildingConfig:
    walls: tuple[Wall, ...]
    windows: tuple[Window, ...]
    internal_gains: tuple[InternalGain, ...]
    ventilation: tuple[Ventilation, ...]

    @property
    def element_count(self) -> int:
        return len(self.walls) + len(self.windows) + len(self.internal_gains) + len(self.ventilation)


def _positive(value: str, label: str, line_number: int) -> float:
    number = float(value)
    if number <= 0:
        raise ValueError(f"Line {line_number}: {label} must be positive")
    return number


def parse_building_config(path: str | Path) -> BuildingConfig:
    """Parse materials, assemblies, and load elements from a text file.

    Supported records are ``material``, ``layers``, ``window``, ``awall``,
    ``awindow``, ``again``, and ``avent``. Units are documented in the sample
    configuration and checked where possible.
    """

    materials: dict[str, float] = {}
    wall_u_values: dict[str, float] = {}
    window_properties: dict[str, tuple[float, float]] = {}
    walls: list[Wall] = []
    windows: list[Window] = []
    gains: list[InternalGain] = []
    ventilation: list[Ventilation] = []

    source = Path(path)
    for line_number, raw in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
        text = raw.split("#", 1)[0].strip()
        if not text:
            continue
        items = text.split()
        kind = items[0].lower()

        try:
            if kind == "material":
                if len(items) != 3:
                    raise ValueError("expected: material NAME conductivity_W_mK")
                materials[items[1]] = _positive(items[2], "conductivity", line_number)

            elif kind == "layers":
                if len(items) < 4 or (len(items) - 2) % 2:
                    raise ValueError("expected material/thickness pairs")
                resistance_m2k_w = 1 / 8.0 + 1 / 23.0
                for material, thickness in zip(items[2::2], items[3::2]):
                    if material not in materials:
                        raise ValueError(f"unknown material {material!r}")
                    resistance_m2k_w += _positive(thickness, "thickness", line_number) / materials[material]
                wall_u_values[items[1]] = 1.0 / resistance_m2k_w

            elif kind == "window":
                if len(items) != 4:
                    raise ValueError("expected: window NAME U_VALUE SHGC")
                u_value = _positive(items[2], "window U-value", line_number)
                shgc = float(items[3])
                if not 0 <= shgc <= 1:
                    raise ValueError("SHGC must be between 0 and 1")
                window_properties[items[1]] = (u_value, shgc)

            elif kind == "awall":
                if len(items) != 5 or items[1] not in wall_u_values:
                    raise ValueError("expected a known wall assembly, orientation, absorptance, and area")
                walls.append(
                    Wall(
                        wall_u_values[items[1]],
                        items[2],
                        float(items[3]),
                        _positive(items[4], "wall area", line_number),
                    )
                )

            elif kind == "awindow":
                if len(items) != 4 or items[1] not in window_properties:
                    raise ValueError("expected a known window type, orientation, and area")
                u_value, shgc = window_properties[items[1]]
                windows.append(Window(u_value, shgc, items[2], _positive(items[3], "window area", line_number)))

            elif kind == "again":
                if len(items) != 2:
                    raise ValueError("expected: again sensible_gain_W")
                gains.append(InternalGain(float(items[1])))

            elif kind == "avent":
                if len(items) != 3:
                    raise ValueError("expected: avent room_volume_m3 air_changes_per_hour")
                ventilation.append(Ventilation(float(items[1]), float(items[2])))

            else:
                raise ValueError(f"unknown record type {kind!r}")
        except (IndexError, ValueError) as exc:
            if isinstance(exc, ValueError) and str(exc).startswith("Line "):
                raise
            raise ValueError(f"Line {line_number}: {exc}") from exc

    config = BuildingConfig(tuple(walls), tuple(windows), tuple(gains), tuple(ventilation))
    if config.element_count == 0:
        raise ValueError("Configuration contains no load elements")
    return config
