from __future__ import annotations

from typing import Any

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import Entity

from .const import DISPATCH_DEVICE_UPDATED
from .gateway import DeviceKey, DeviceState
from .helpers import KocomEntityInfo


class KocomEntity(Entity):
    _attr_has_entity_name = True

    def __init__(self, hass: HomeAssistant, info: KocomEntityInfo) -> None:
        super().__init__()
        self.hass = hass
        self._info = info
        self._attr_unique_id = info.unique_id
        self._attr_device_info = info.device_info()

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass, DISPATCH_DEVICE_UPDATED, self._handle_device_update
            )
        )

    @callback
    def _handle_device_update(self, entry_id: str, dev: DeviceState) -> None:
        # 하위 클래스에서 key 비교 후 상태 동기화
        pass
