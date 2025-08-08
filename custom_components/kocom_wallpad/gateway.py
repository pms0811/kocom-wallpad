"""Gateway module for Kocom Wallpad."""

from __future__ import annotations

from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.dispatcher import async_dispatcher_send

from .const import DOMAIN, LOGGER


class KocomGateway:

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        pass
    
    