"""Platform for Broadlink AC climate integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.climate import (
    FAN_AUTO,
    FAN_HIGH,
    FAN_LOW,
    FAN_MEDIUM,
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .ac_db import ac_db
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SUPPORTED_FAN_MODES = [FAN_AUTO, FAN_LOW, FAN_MEDIUM, FAN_HIGH]
SUPPORTED_HVAC_MODES = [
    HVACMode.OFF,
    HVACMode.COOL,
    HVACMode.HEAT,
    HVACMode.DRY,
    HVACMode.FAN_ONLY,
]


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Broadlink AC climate entity from a config entry."""
    ac_instance: ac_db = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([BroadlinkACClimate(ac_instance, entry)])


class BroadlinkACClimate(ClimateEntity):
    """Representation of a Broadlink AC climate entity."""

    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_supported_features = (
        ClimateEntityFeature.TARGET_TEMPERATURE
        | ClimateEntityFeature.FAN_MODE
        | ClimateEntityFeature.TURN_ON
        | ClimateEntityFeature.TURN_OFF
    )
    _attr_hvac_modes = SUPPORTED_HVAC_MODES
    _attr_fan_modes = SUPPORTED_FAN_MODES

    def __init__(self, ac_instance: ac_db, entry: ConfigEntry) -> None:
        """Initialize the climate entity."""
        self._ac = ac_instance
        self._entry = entry
        self._attr_name = f"Broadlink AC {entry.entry_id}"
        self._attr_unique_id = entry.entry_id
        self._attr_current_temperature = None
        self._attr_target_temperature = None
        self._attr_hvac_mode = HVACMode.OFF
        self._attr_fan_mode = FAN_AUTO

    async def async_update(self) -> None:
        """Fetch the latest state from the AC."""
        status = self._ac.get_ac_status(force_update=True)
        if status is bool:
            _LOGGER.error("Failed to get AC status")
            return
        self._attr_current_temperature = status.get("ambient_temp")
        self._attr_target_temperature = status.get("temp")
        if status.get("power") == "OFF":
            self._attr_hvac_mode = HVACMode.OFF
        else:
            self._attr_hvac_mode = self._map_mode_to_hvac(status.get("mode"))
        self._attr_fan_mode = status.get("fanspeed").lower()

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set the target temperature."""
        if (temperature := kwargs.get(ATTR_TEMPERATURE)) is not None:
            self._ac.set_temperature(temperature)
            self._attr_target_temperature = temperature
            self.async_write_ha_state()

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set the HVAC mode."""
        self._ac.set_homeassistant_mode(str(hvac_mode))
        self._attr_hvac_mode = hvac_mode
        self.async_write_ha_state()

    async def async_set_fan_mode(self, fan_mode: str) -> None:
        """Set the fan mode."""
        self._ac.set_fanspeed(fan_mode.upper())
        self._attr_fan_mode = fan_mode
        self.async_write_ha_state()

    async def async_turn_on(self) -> None:
        """Turn the device on."""
        await self.async_set_hvac_mode(HVACMode.AUTO)

    async def async_turn_off(self) -> None:
        """Turn the device off."""
        await self.async_set_hvac_mode(HVACMode.OFF)

    async def start(self) -> None:
        """Start the device."""
        await self.async_turn_on()

    async def stop(self) -> None:
        """Stop the device."""
        await self.async_turn_off()

    def _map_mode_to_hvac(self, mode: str) -> HVACMode:
        """Map AC mode to Home Assistant HVAC mode."""
        return {
            "COOLING": HVACMode.COOL,
            "HEATING": HVACMode.HEAT,
            "DRY": HVACMode.DRY,
            "FAN": HVACMode.FAN_ONLY,
            "AUTO": HVACMode.AUTO,
        }.get(mode.upper(), HVACMode.OFF)

    def _map_hvac_to_mode(self, hvac_mode: HVACMode) -> str:
        """Map Home Assistant HVAC mode to AC mode."""
        return {
            HVACMode.COOL: "COOLING",
            HVACMode.HEAT: "HEATING",
            HVACMode.DRY: "DRY",
            HVACMode.FAN_ONLY: "FAN",
            HVACMode.AUTO: "AUTO",
        }[hvac_mode]
