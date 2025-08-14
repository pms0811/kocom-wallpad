from __future__ import annotations

from homeassistant.helpers.entity import Entity, DeviceInfo
from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .gateway import KocomGateway, DeviceState
from .const import DOMAIN


class KocomBaseEntity(Entity):
    _attr_has_entity_name = True
    _attr_available = True

    def __init__(self, gateway: KocomGateway, device: DeviceState) -> None:
        super().__init__()
        self.gateway = gateway
        self._device = device
        self._attr_unique_id = device.key.unique_id
        self._attr_name = device.key.name
        self.entity_description = ""
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"")},
            manufacturer="",
            model=f"",
            name=f"",
        )
        self._state_cache = dict(device.attributes)

    async def async_added_to_hass(self):
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass,
                f"{DOMAIN}_state_update_{self._attr_unique_id}",
                self._handle_state_update
            )
        )
        
    async def async_will_remove_from_hass(self) -> None:
        pass

    @callback
    def update_from_state(self, new_state: DeviceState) -> bool:
        if new_state.attributes != self._state_cache:
            self._state_cache = dict(new_state.attributes)
            self._device = new_state
            self.async_write_ha_state()
