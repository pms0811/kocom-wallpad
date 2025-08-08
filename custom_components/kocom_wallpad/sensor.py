"""Sensor Platform for Kocom Wallpad."""

from __future__ import annotations

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)

from homeassistant.const import (
    Platform,
    UnitOfTemperature,
    PERCENTAGE,
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    CONCENTRATION_PARTS_PER_MILLION,
    CONCENTRATION_PARTS_PER_BILLION,
)
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
    """Set up Kocom sensor platform."""



class KocomSensorEntity(SensorEntity):
    """Representation of a Kocom sensor."""
    
    def __init__(self, gateway: KocomGateway) -> None:
        """Initialize the sensor."""
        super().__init__(gateway)

    @property
    def native_value(self) -> int:
        """Return the state of the sensor."""
        return 0
    
    @property
    def device_class(self) -> SensorDeviceClass | None:
        """Return the device class of the sensor."""
        return 0
    
    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return the native unit of measurement."""
        return 0