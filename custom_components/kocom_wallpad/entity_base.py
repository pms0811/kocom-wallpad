"""Base platform for Kocom Wallpad."""

from __future__ import annotations

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.restore_state import RestoreEntity, RestoredExtraData
from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import EntityDescription

from .const import DOMAIN, DeviceType, SubType


class KocomBaseEntity(RestoreEntity):
    """Base class for Kocom entities."""

    def __init__(self, gateway, device) -> None:
        """Initialize the base entity."""
        super().__init__()
        self.gateway = gateway
        self._device = device
        self._unsubs: list[callable] = []

        self._attr_unique_id = device.key.unique_id
        self.entity_description = EntityDescription(
            key=device.key.device_type.name.lower(),
            has_entity_name=True,
            translation_key=device.key.device_type.name.lower(),
            translation_placeholders={"id": self.format_translation_placeholders}
        )
        self._attr_device_info = DeviceInfo(
            connections={(self.gateway.host, self.unique_id)},
            identifiers={(DOMAIN, f"{self.format_identifiers}")},
            manufacturer="KOCOM Co., Ltd",
            model="Smart Wallpad",
            name=f"{self.format_identifiers}",
            via_device=(DOMAIN, str(self.gateway.host)),
        )

    @property
    def format_translation_placeholders(self) -> str:
        if self._device.key.sub_type == SubType.NONE:
            return f"{str(self._device.key.room_index)}-{str(self._device.key.device_index)}"
        else:
            return f"{str(self._device.key.room_index)}-{str(self._device.key.device_index)}"

    @property
    def format_identifiers(self) -> str:
        if self._device.key.device_type in {
            DeviceType.VENTILATION, DeviceType.GASVALVE, DeviceType.ELEVATOR, DeviceType.MOTION
        }:
            return f"KOCOM"
        elif self._device.key.device_type in {
            DeviceType.LIGHT, DeviceType.LIGHTCUTOFF, DeviceType.DIMMINGLIGHT
        }:
            return f"KOCOM LIGHT"
        else:
            return f"KOCOM {self._device.key.device_type.name}"

    async def async_added_to_hass(self):
        sig = self.gateway.async_signal_device_updated(self._device.key.unique_id)

        @callback
        def _handle_update(dev):
            self._device = dev
            self.update_from_state()
        self._unsubs.append(async_dispatcher_connect(self.hass, sig, _handle_update))

    async def async_will_remove_from_hass(self) -> None:
        for unsub in self._unsubs:
            try:
                unsub()
            except Exception:
                pass
        self._unsubs.clear()

    @callback
    def update_from_state(self) -> None:
        self.async_write_ha_state()

    @property
    def extra_restore_state_data(self) -> RestoredExtraData:
        return RestoredExtraData({"store_packet": self._device._store_packet})
