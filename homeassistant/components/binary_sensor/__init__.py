"""
Component to interface with binary sensors.

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/binary_sensor/
"""
import logging

from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.helpers.entity import Entity
from homeassistant.const import (STATE_ON, STATE_OFF)
from homeassistant.components import (
    bloomsky, mysensors, zwave, vera, wemo, wink)
from homeassistant.helpers.config_validation import PLATFORM_SCHEMA  # noqa

DOMAIN = 'binary_sensor'
SCAN_INTERVAL = 30

ENTITY_ID_FORMAT = DOMAIN + '.{}'
SENSOR_CLASSES = [
    None,            # Generic on/off
    'cold',          # On means cold (or too cold)
    'connectivity',  # On means connection present, Off = no connection
    'gas',           # CO, CO2, etc.
    'heat',          # On means hot (or too hot)
    'light',         # Lightness threshold
    'moisture',      # Specifically a wetness sensor
    'motion',        # Motion sensor
    'moving',        # On means moving, Off means stopped
    'opening',       # Door, window, etc.
    'power',         # Power, over-current, etc
    'safety',        # Generic on=unsafe, off=safe
    'smoke',         # Smoke detector
    'sound',         # On means sound detected, Off means no sound
    'vibration',     # On means vibration detected, Off means no vibration
]

# Maps discovered services to their platforms
DISCOVERY_PLATFORMS = {
    bloomsky.DISCOVER_BINARY_SENSORS: 'bloomsky',
    mysensors.DISCOVER_BINARY_SENSORS: 'mysensors',
    zwave.DISCOVER_BINARY_SENSORS: 'zwave',
    vera.DISCOVER_BINARY_SENSORS: 'vera',
    wemo.DISCOVER_BINARY_SENSORS: 'wemo',
    wink.DISCOVER_BINARY_SENSORS: 'wink'
}


def setup(hass, config):
    """Track states and offer events for binary sensors."""
    component = EntityComponent(
        logging.getLogger(__name__), DOMAIN, hass, SCAN_INTERVAL,
        DISCOVERY_PLATFORMS)

    component.setup(config)

    return True


# pylint: disable=no-self-use
class BinarySensorDevice(Entity):
    """Represent a binary sensor."""

    @property
    def is_on(self):
        """Return True if the binary sensor is on."""
        return None

    @property
    def state(self):
        """Return the state of the binary sensor."""
        return STATE_ON if self.is_on else STATE_OFF

    @property
    def sensor_class(self):
        """Return the class of this sensor, from SENSOR_CLASSES."""
        return None

    @property
    def state_attributes(self):
        """Return device specific state attributes."""
        attr = {}

        if self.sensor_class is not None:
            attr['sensor_class'] = self.sensor_class

        return attr
