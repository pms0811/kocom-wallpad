from __future__ import annotations

import logging
from enum import IntEnum, Enum
from homeassistant.const import Platform

LOGGER = logging.getLogger(__name__)

DOMAIN = "kocom_wallpad"
PLATFORMS = [
    Platform.LIGHT,
    Platform.SWITCH,
    Platform.CLIMATE,
    Platform.FAN,
    Platform.BINARY_SENSOR,
    Platform.SENSOR,
]

DISPATCH_DEVICE_ADDED = f"{DOMAIN}_device_added"
DISPATCH_DEVICE_UPDATED = f"{DOMAIN}_device_updated"
DISPATCH_DEVICE_REMOVED = f"{DOMAIN}_device_removed"

PACKET_PREFIX = bytes([0xAA, 0x55])
PACKET_SUFFIX = bytes([0x0D, 0x0D])
PACKET_LEN = 21

DEFAULT_TCP_PORT = 8899
RECV_POLL_SEC = 0.05  # 50ms polling
IDLE_GAP_SEC = 0.20   # 보내기 전 라인 유휴로 보고 싶은 최소 간격
SEND_RETRY_MAX = 3
SEND_RETRY_GAP = 0.15


class DeviceType(IntEnum):
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


class SubType(IntEnum):
    NONE = 0
