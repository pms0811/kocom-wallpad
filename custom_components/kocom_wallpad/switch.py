"""Switch Platform for Kocom Wallpad."""

from __future__ import annotations

from typing import Any

from homeassistant.components.switch import SwitchEntity, SwitchDeviceClass

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
    """Set up Kocom switch platform."""



class KocomSwitchEntity(SwitchEntity):
    """Representation of a Kocom switch."""

    _attr_device_class = SwitchDeviceClass.SWITCH
    
    def __init__(self, gateway: KocomGateway) -> None:
        """Initialize the switch."""
        super().__init__(gateway)

    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        return False
    
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on switch."""

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off switch."""

