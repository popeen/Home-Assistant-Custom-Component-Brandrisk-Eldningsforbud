"""Platform for sensor integration."""
from datetime import timedelta

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

from . import common

CONF_LAT = "latitude"
CONF_LONG = "longitude"

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=30)

SCAN_INTERVAL = timedelta(minutes=30)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_NAME): cv.string,
        vol.Required(CONF_LAT): cv.string,
        vol.Required(CONF_LONG): cv.string,
    }
)

async def get_brandrisk(session, lat, long):
    url = "https://api.msb.se/brandrisk/v2/CurrentRisk/sv/ " + str(lat) + "/" + str(long)
    async with session.get(url) as resp:
        data = await resp.json()
        return replace_nulls_with_empty_string(data)

async def get_fire_prohibition(session, lat, long):
    url = "https://api.msb.se/brandrisk/v2/FireProhibition/sv/ " + str(lat) + "/" + str(long)
    async with session.get(url) as resp:
        data = await resp.json()
        return replace_nulls_with_empty_string(data)

def replace_nulls_with_empty_string(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if value is None:
                obj[key] = ""
            else:
                replace_nulls_with_empty_string(value)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            if item is None:
                obj[i] = ""
            else:
                replace_nulls_with_empty_string(item)
    return obj

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    session = async_get_clientsession(hass)
    config = hass.data[common.DOMAIN][config_entry.entry_id]

    latitude = config[0]
    longitude = config[1]
    name = config[2]

    async_add_entities([BrandriskSensor(name, latitude, longitude),FireProhibitionSensor(name, latitude, longitude)], update_before_add=True)


class BrandriskSensor(Entity):
    """Representation of a Brandrisk sensor."""

    def __init__(self, name, latitude, longitude):
        """Initialize a Brandrisk sensor."""
        self._attr_unique_id = f"{common.DOMAIN}_{name}_{latitude}_{longitude}"

        self._state = None
        self._name = name
        self.latitude = latitude
        self.longitude = longitude
        self._icon = "mdi:fire-alert"
        self._rawData = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the sensor."""
        attributes = self._rawData['forecast']
        attributes['latitude'] = self.latitude
        attributes['longitude'] = self.longitude
        return attributes

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self) -> None:
        """Get the latest data and updates the states."""
        session = async_get_clientsession(self.hass)
        
        self._rawData = await get_brandrisk(session, self.latitude, self.longitude)
        self._state = self._rawData['forecast']['riskIndex']

class FireProhibitionSensor(Entity):
    """Representation of a Brandrisk sensor."""

    def __init__(self, name, latitude, longitude):
        """Initialize a Brandrisk sensor."""
        self._attr_unique_id = f"{common.DOMAIN}_{name}_{latitude}_{longitude}_prohibition"

        self._state = None
        self._name = name
        self.latitude = latitude
        self.longitude = longitude
        self._icon = "mdi:fire-off"
        self._rawData = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name + " Fire Prohibition"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the sensor."""
        attributes = self._rawData['fireProhibition']
        attributes['county'] = self._rawData['county']
        attributes['countyCode'] = self._rawData['countyCode']
        attributes['municipality'] = self._rawData['municipality']
        attributes['municipalityCode'] = self._rawData['municipalityCode']
        attributes['latitude'] = self.latitude
        attributes['longitude'] = self.longitude
        return attributes

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self) -> None:
        """Get the latest data and updates the states."""
        session = async_get_clientsession(self.hass)
        
        self._rawData = await get_fire_prohibition(session, self.latitude, self.longitude)
        self._state = self._rawData['fireProhibition']['status']
