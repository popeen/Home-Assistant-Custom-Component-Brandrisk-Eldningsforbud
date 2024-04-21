"""Config flow for Hello World integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries, exceptions
from homeassistant.core import HomeAssistant

from . import common

async def validate_input(hass: HomeAssistant, data: dict) -> dict[str, Any]:
    """Validate the user input."""
    return True


class ConfigFlow(config_entries.ConfigFlow, domain=common.DOMAIN):

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""

        errors = {}
        if user_input is not None:
            try:
                valid = await validate_input(self.hass, user_input)
                return self.async_create_entry(title=user_input["name"], data=user_input)
            except InvalidCoords:
                errors["base"] = "invalid_coordinates"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("name", default="Brandrisk"): str,
                    vol.Required("latitude", default=str(self.hass.config.latitude)): str,
                    vol.Required("longitude", default=str(self.hass.config.longitude)): str
                }
            ),
            errors=errors
        )

class InvalidCoords(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""
