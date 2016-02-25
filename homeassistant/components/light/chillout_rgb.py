"""
ChillOut RGB light platform that implements lights.

For more details about this platform, please refer to the documentation
https://home-assistant.io/components/chillout/
"""
import random
import logging
import urllib.request
#import urllib.parse

from homeassistant.components.light import (
#    ATTR_BRIGHTNESS, ATTR_COLOR_TEMP, ATTR_RGB_COLOR, Light)
    ATTR_BRIGHTNESS, ATTR_RGB_COLOR, Light)

LIGHT_COLORS = [
    [237, 224, 33],
    [255, 63, 111],
]

DEFAULT_PORT = 80

# LIGHT_TEMPS = [240, 380]
_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    """ Gets the ChillOut RGB lights. """

    ETHtoRFgw = config.get('host', None)

    if ETHtoRFgw is None:
        _LOGGER.error('No host found in configuration')
        return False

    remote_port = config.get('port', DEFAULT_PORT)

    lights_list = config.get('lights', {})
    lights = []

    for dev_name,properties in lights_list.items():
#        _LOGGER.info('Detectred ChillOut RGB: %s - %s', dev_name, properties)
        lights.append(
            ChillOutLight(
                ETHtoRFgw,
                remote_port,
                dev_name,
                properties.get('devid'),
                properties.get('groupid')))
#        _LOGGER.info('Added ChillOut RGB light: %s', dev_name)
    add_devices_callback(lights)

class ChillOutLight(Light):
    """Provides a demo light."""
    # pylint: disable=too-many-arguments
    def __init__(self, RFgw, RFgwP, name, devid, groupid):
        self._state = False
        self._RFgw = RFgw
        self._RFgwP = RFgwP
        self._name = name
        self._devid = devid
        self._groupid = groupid
        self._rgb = [255, 255, 255]
        self._brightness = 255

    @property
    def should_poll(self):
        """No polling needed for a ChillOut RGB light."""
        return False

    @property
    def name(self):
        """Return the name of the light if any."""
        return self._name

    @property
    def brightness(self):
        """Return the brightness of this light between 0..255."""
        return self._brightness

    @property
    def rgb_color(self):
        """Return the RBG color value."""
        return self._rgb

    @property
    def is_on(self):
        """Return true if light is on."""
        return self._state

    def turn_on(self, **kwargs):
        """Turn the light on."""
        _LOGGER.info('ChillOut RGB System - dev: %s - Turning On: %s', self._name, kwargs)

        group_dest = "%0.1X" % self._groupid
        device_dest = "%0.2X" % self._devid

        if ATTR_RGB_COLOR in kwargs:
            self._rgb = kwargs[ATTR_RGB_COLOR]
            self._brightness = 0

            rr = "%0.2x" % self._rgb[0]
            gg = "%0.2x" % self._rgb[1]
            bb = "%0.2x" % self._rgb[2]
            string_command = 'rgb_'+rr+gg+bb+group_dest+device_dest

        if ATTR_BRIGHTNESS in kwargs:
            self._brightness = kwargs[ATTR_BRIGHTNESS]
            self._rgb = [ kwargs[ATTR_BRIGHTNESS], kwargs[ATTR_BRIGHTNESS], kwargs[ATTR_BRIGHTNESS] ]

            rr = "%0.2x" % self._rgb[0]
            gg = "%0.2x" % self._rgb[1]
            bb = "%0.2x" % self._rgb[2]
            string_command = 'rgb_'+rr+gg+bb+group_dest+device_dest

        if (ATTR_RGB_COLOR or ATTR_BRIGHTNESS) in kwargs:
            _LOGGER.info('ChillOut RGB System - RGB or BRIGHT %s', kwargs)

        if all(rgb == self._rgb[0] for rgb in self._rgb):
            self._brightness = self._rgb[0]

        if not kwargs:
            self._brightness = 255
            string_command = 'set_100000'+group_dest+device_dest

        command_url = 'http://'+self._RFgw+'/parsed.html?RGB=' + string_command

        _LOGGER.info('ChillOut RGB System - cmd url: %s', command_url)

        urllib.request.urlopen(command_url).read()

        self._state = True
        self.update_ha_state()

    def turn_off(self, **kwargs):
        """Turn the light off."""
        _LOGGER.info('ChillOut RGB System - dev: %s - Turning Off: %s', self._name, kwargs)

        group_dest = "%0.1X" % self._groupid
        device_dest = "%0.2X" % self._devid
        string_command = 'set_000000'+group_dest+device_dest
        command_url = 'http://'+self._RFgw+'/parsed.html?RGB=' + string_command

        _LOGGER.info('ChillOut RGB System - cmd url: %s', command_url)

        urllib.request.urlopen(command_url).read()

        self._state = False
        self.update_ha_state()

