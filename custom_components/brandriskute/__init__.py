"""brandrisk_ute.""" 
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from . import common

PLATFORMS: list[str] = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(common.DOMAIN, {})[entry.entry_id] = [
        entry.data["latitude"],
        entry.data["longitude"],
        entry.data["name"]
    ]
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True