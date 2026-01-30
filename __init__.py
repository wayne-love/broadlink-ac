"""The broadlink_ac integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.exceptions import ConfigEntryNotReady

from .ac_db import ac_db, ConnectError, ConnectTimeout

_PLATFORMS: list[Platform] = [Platform.CLIMATE]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Broadlink integration."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up broadlink_ac from a config entry."""

    # Remove ':' characters from MAC and convert to byte array
    mac_bytes = bytes.fromhex(entry.data["mac"].replace(":", ""))

    try:
        ac_db_instance = ac_db(
            host=(entry.data["host"], 80),
            mac=mac_bytes,
        )
    except (ConnectTimeout, ConnectError) as err:
        raise ConfigEntryNotReady(
            f"Broadlink AC not ready at {entry.data['host']}"
        ) from err
    entry.runtime_data = ac_db_instance

    # Store the AC instance in hass.data for use in the climate platform
    hass.data.setdefault("broadlink_ac", {})[entry.entry_id] = ac_db_instance

    await hass.config_entries.async_forward_entry_setups(entry, _PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, _PLATFORMS)

    if unload_ok:
        hass.data["broadlink_ac"].pop(entry.entry_id)

    return unload_ok
