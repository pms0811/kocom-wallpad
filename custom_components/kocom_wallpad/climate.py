"""Climate platform for Kocom Wallpad."""

from __future__ import annotations

from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    ClimateEntityFeature,
    HVACMode,
    PRESET_AWAY,
    PRESET_NONE,
    FAN_LOW,
    FAN_MEDIUM,
    FAN_HIGH,
)

from homeassistant.const import Platform, UnitOfTemperature, ATTR_TEMPERATURE
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
    """Set up Kocom climate platform."""


class KocomThermostatEntity(ClimateEntity):
    """Representation of a Kocom thermostat."""

    def __init__(self, gateway: KocomGateway) -> None:
        """Initialize the thermostat."""
        super().__init__(gateway)

    @property
    def hvac_mode(self) -> HVACMode:
        """Return the current HVAC mode."""
        return HVACMode.OFF

    @property
    def preset_mode(self) -> str:
        """Return the current preset mode."""
        return ""

    @property
    def current_temperature(self) -> int:
        """Return the current temperature."""
        return 0

    @property
    def target_temperature(self) -> int:
        """Return the target temperature."""
        return 0
    
    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set the HVAC mode."""

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        """Set the preset mode."""

    async def async_set_temperature(self, **kwargs) -> None:
        """Set the target temperature."""



class KocomAirConditionerEntity(ClimateEntity):
    """Representation of a Kocom climate."""

    _enable_turn_on_off_backwards_compatibility = False

    def __init__(self, gateway: KocomGateway) -> None:
        """Initialize the climate."""
        super().__init__(gateway)

    @property
    def hvac_mode(self) -> HVACMode:
        """Return current HVAC mode."""
        return HVACMode.OFF

    @property
    def fan_mode(self) -> str:
        """Return current fan mode."""
        return ""

    @property
    def current_temperature(self) -> int:
        """Return the current temperature."""
        return 0

    @property
    def target_temperature(self) -> int:
        """Return the target temperature."""
        return 0

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set a new target HVAC mode."""

    async def async_set_fan_mode(self, fan_mode: str) -> None:
        """Set a new target fan mode."""

    async def async_set_temperature(self, **kwargs) -> None:
        """Set a new target temperature."""
