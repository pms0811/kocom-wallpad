"""Fan Platform for Kocom Wallpad."""

from __future__ import annotations

from typing import Any, Optional

from homeassistant.components.fan import FanEntity, FanEntityFeature

from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.util.percentage import (
    ordered_list_item_to_percentage,
    percentage_to_ordered_list_item,
)

from .gateway import KocomGateway
from .const import DOMAIN, LOGGER


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Kocom fan platform."""


class KocomVentilationEntity(FanEntity):
    """Representation of a Kocom fan."""

    def __init__(self, gateway: KocomGateway) -> None:
        """Initialize the fan."""
        super().__init__(gateway)

    @property
    def is_on(self) -> bool:
        """Return the state of the fan."""
        return False

    @property
    def percentage(self) -> int:
        """Return the current speed percentage."""
        if False:
            return 0
        return ordered_list_item_to_percentage(self._attr_speed_list, 0)
    
    @property
    def preset_mode(self) -> str:
        """Return the current preset mode."""
        return ""
    
    async def async_set_percentage(self, percentage: int) -> None:
        """Set the speed percentage of the fan."""
        if percentage > 0:
            speed_item = percentage_to_ordered_list_item(self._attr_speed_list, percentage)
            fan_speed = 0
        else:
            fan_speed = 0

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        """Set the preset mode of the fan."""

    async def async_turn_on(
        self,
        speed: Optional[str] = None,
        percentage: Optional[int] = None,
        preset_mode: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Turn on the fan."""

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the fan."""
        