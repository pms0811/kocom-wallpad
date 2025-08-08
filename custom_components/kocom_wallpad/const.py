"""Constants for the Kocom Wallpad integration."""

from __future__ import annotations

from homeassistant.const import Platform
from enum import Enum, IntEnum
import logging

DOMAIN = "kocom_wallpad"

LOGGER = logging.getLogger(__package__)

DEFAULT_PORT = 8899

class PT2DT(Enum):
    UNKNOWN = None
    LIGHT = Platform.LIGHT
    LIGHTCUTOFF = Platform.LIGHT
    DIMMINGLIGHT = Platform.LIGHT
    OUTLET = Platform.SWITCH
    THERMOSTAT = Platform.CLIMATE
    AIRCONDITIONER = Platform.CLIMATE
    VENTILATION = Platform.FAN
    GASVALVE = Platform.SWITCH
    ELEVATOR = Platform.SWITCH
    MOTION = Platform.BINARY_SENSOR
    AIRQUALITY = Platform.SENSOR

class DT(IntEnum):
    UNKNOWN = 0
    LIGHT = 1
    LIGHTCUTOFF = 2
    DIMMINGLIGHT = 3
    OUTLET = 4
    THERMOSTAT = 5
    AIRCONDITIONER = 6
    VENTILATION = 7
    GASVALVE = 8
    ELEVATOR = 9
    MOTION = 10
    AIRQUALITY = 11

class ST(IntEnum):
    NONE = 0
