from __future__ import annotations

from dataclasses import dataclass
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN, DeviceType


@dataclass(slots=True)
class KocomEntityInfo:
    platform: str
    key_tuple: tuple[int, int, int, int]  # (dt, room, idx, sub)
    name_key: str  # translations key path
    sub_id: int

    @property
    def unique_id(self) -> str:
        dt, room, idx, sub = self.key_tuple
        return f"{dt}_{room}_{idx}_{sub}"

    @property
    def entity_id_hint(self) -> str:
        dt, room, idx, sub = self.key_tuple
        return ""

    def device_info(self) -> DeviceInfo:
        dt, room, idx, sub = self.key_tuple
        return DeviceInfo(
            identifiers={(DOMAIN, "")},
            name="",
            manufacturer="",
            model="",
        )