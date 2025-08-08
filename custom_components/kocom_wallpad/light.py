"""Light Platform for Kocom Wallpad."""

from __future__ import annotations

from typing import Any

from homeassistant.components.light import LightEntity, ColorMode, ATTR_BRIGHTNESS

from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .gateway import KocomGateway
from .const import DOMAIN, LOGGER


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Kocom light platform."""


class KocomLightEntity(LightEntity):
    """Representation of a Kocom light."""

    _attr_supported_color_modes = {ColorMode.ONOFF}
    _attr_color_mode = ColorMode.ONOFF
    
    def __init__(self, gateway: KocomGateway) -> None:
        """Initialize the light."""
        super().__init__(gateway)

    @property
    def is_brightness(self) -> bool:
        """Return whether brightness is supported."""
        return False
    
    @property
    def max_brightness(self) -> int:
        """Return the maximum supported brightness."""
        return 0

    @property
    def is_on(self) -> bool:
        """Return true if light is on."""
        return False
    
    @property
    def brightness(self) -> int:
        """Return the brightness of this light between 0..255."""
        return 0 
    
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on light."""

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off light."""

