"""Heat-gain elements and explicit unit contracts.

This is an educational, steady-state sensible-load model.  It is not an
equipment-sizing or building-code calculation engine.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WeatherPoint:
    """One hourly weather point.

    ``dry_bulb_c`` is degrees Celsius. ``irradiance_w_m2`` maps orientation
    codes (H, S, W, N, E, P) to incident solar irradiance in W/m².
    """

    timestamp: str
    dry_bulb_c: float
    irradiance_w_m2: dict[str, float]

    def irradiance(self, orientation: str) -> float:
        try:
            return float(self.irradiance_w_m2[orientation])
        except KeyError as exc:
            raise KeyError(f"Missing irradiance for orientation {orientation!r}") from exc


@dataclass(frozen=True)
class Wall:
    """Opaque surface using a sol-air temperature approximation."""

    u_value_w_m2k: float
    orientation: str
    solar_absorptance: float
    area_m2: float
    outside_film_w_m2k: float = 23.0

    def __post_init__(self) -> None:
        if self.u_value_w_m2k <= 0 or self.area_m2 <= 0:
            raise ValueError("Wall U-value and area must be positive")
        if not 0 <= self.solar_absorptance <= 1:
            raise ValueError("Solar absorptance must be between 0 and 1")
        if self.outside_film_w_m2k <= 0:
            raise ValueError("Outside film coefficient must be positive")

    @property
    def conductance_w_k(self) -> float:
        return self.u_value_w_m2k * self.area_m2

    def heat_gain_w(self, weather: WeatherPoint, indoor_temp_c: float) -> float:
        sol_air_c = (
            weather.dry_bulb_c
            + self.solar_absorptance
            * weather.irradiance(self.orientation)
            / self.outside_film_w_m2k
        )
        return self.conductance_w_k * (sol_air_c - indoor_temp_c)


@dataclass(frozen=True)
class Window:
    """Window conduction plus a simplified solar heat-gain term."""

    u_value_w_m2k: float
    solar_heat_gain_coefficient: float
    orientation: str
    area_m2: float

    def __post_init__(self) -> None:
        if self.u_value_w_m2k <= 0 or self.area_m2 <= 0:
            raise ValueError("Window U-value and area must be positive")
        if not 0 <= self.solar_heat_gain_coefficient <= 1:
            raise ValueError("Window solar heat-gain coefficient must be between 0 and 1")

    def conduction_w(self, weather: WeatherPoint, indoor_temp_c: float) -> float:
        return self.u_value_w_m2k * self.area_m2 * (weather.dry_bulb_c - indoor_temp_c)

    def solar_gain_w(self, weather: WeatherPoint) -> float:
        return (
            self.solar_heat_gain_coefficient
            * self.area_m2
            * weather.irradiance(self.orientation)
        )


@dataclass(frozen=True)
class InternalGain:
    """Constant internal sensible gain in watts."""

    watts: float

    def __post_init__(self) -> None:
        if self.watts < 0:
            raise ValueError("Internal gain cannot be negative")


@dataclass(frozen=True)
class Ventilation:
    """Sensible ventilation gain from room volume and air-change rate."""

    room_volume_m3: float
    air_changes_per_hour: float
    air_density_kg_m3: float = 1.2
    air_specific_heat_j_kgk: float = 1006.0

    def __post_init__(self) -> None:
        if self.room_volume_m3 < 0 or self.air_changes_per_hour < 0:
            raise ValueError("Room volume and air changes cannot be negative")
        if self.air_density_kg_m3 <= 0 or self.air_specific_heat_j_kgk <= 0:
            raise ValueError("Air properties must be positive")

    @property
    def conductance_w_k(self) -> float:
        flow_m3_s = self.room_volume_m3 * self.air_changes_per_hour / 3600.0
        return flow_m3_s * self.air_density_kg_m3 * self.air_specific_heat_j_kgk

    def heat_gain_w(self, weather: WeatherPoint, indoor_temp_c: float) -> float:
        return self.conductance_w_k * (weather.dry_bulb_c - indoor_temp_c)
