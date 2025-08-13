from __future__ import annotations

import asyncio
import contextlib
from dataclasses import dataclass
from typing import Optional, Dict, Tuple, List

from homeassistant.core import HomeAssistant
from homeassistant.const import Platform
from homeassistant.helpers.dispatcher import async_dispatcher_send

from .const import (
    DOMAIN,
    DISPATCH_DEVICE_ADDED,
    DISPATCH_DEVICE_UPDATED,
    PACKET_PREFIX,
    PACKET_SUFFIX,
    PACKET_LEN,
    RECV_POLL_SEC,
    IDLE_GAP_SEC,
    SEND_RETRY_MAX,
    SEND_RETRY_GAP,
    DeviceType,
    SubType,
)
from .transport import SyncConnectionWrapper
from .controller import KocomController


@dataclass(frozen=True)
class DeviceKey:
    device_type: DeviceType
    room_index: int
    device_index: int
    sub_type: SubType

    def unique_id(self, platform: str) -> str:
        # ex) 1-1_1-0 -> deviceType-roomIndex_deviceIndex-subType
        return f"{self.device_type.value}-{self.room_index}_{self.device_index}-{self.sub_type.value}"

    @property
    def key(self) -> Tuple[int, int, int, int]:
        return (self.device_type.value, self.room_index, self.device_index, self.sub_type.value)


@dataclass
class DeviceState:
    key: DeviceKey
    platform: Platform
    attributes: Dict[str, int | float | str | bool]


class EntityRegistry:
    """In-memory entity registry (for gateway internal use)."""

    def __init__(self) -> None:
        self._states: Dict[Tuple[int, int, int, int], DeviceState] = {}

    def upsert(self, dev: DeviceState) -> bool:
        k = dev.key.key
        old = self._states.get(k)
        changed = (old is None) or (old.attributes != dev.attributes)
        self._states[k] = dev
        return changed

    def get(self, key: DeviceKey) -> Optional[DeviceState]:
        return self._states.get(key.key)

    def all_entities(self) -> List[DeviceState]:
        return list(self._states.values())


class KocomGateway:
    """Connection/Receive Loop/Transmission Queue/Entity Registry Management Hub."""

    def __init__(self, hass: HomeAssistant, host: str, port: int | None) -> None:
        self.hass = hass
        self.entry_id: str = ""
        self.host = host
        self.port = port
        self.conn = SyncConnectionWrapper(host=host, port=port)
        self.controller = KocomController(self)
        self.registry = EntityRegistry()
        self._task_reader: asyncio.Task | None = None
        self._send_lock = asyncio.Lock()
        self._last_rx_monotonic: float = 0.0
        self._last_tx_monotonic: float = 0.0

    async def async_start(self) -> None:
        await self.hass.async_add_executor_job(self.conn.open)
        self._last_rx_monotonic = self.conn.idle_since()
        self._last_tx_monotonic = self.conn.idle_since()
        self._task_reader = asyncio.create_task(self._read_loop())

    async def async_stop(self) -> None:
        if self._task_reader:
            self._task_reader.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._task_reader
        await self.hass.async_add_executor_job(self.conn.close)

    def attach_entry(self, entry_id: str) -> None:
        self.entry_id = entry_id

    def is_idle(self) -> bool:
        return self.conn.idle_since() >= IDLE_GAP_SEC

    async def _read_loop(self) -> None:
        try:
            while True:
                # blocking recv를 executor에서 짧게 폴링
                chunk = await self.hass.async_add_executor_job(self.conn.recv, 512, RECV_POLL_SEC)
                if chunk:
                    self._last_rx_monotonic = asyncio.get_running_loop().time()
                    self.controller.feed(chunk)
        except asyncio.CancelledError:
            raise

    async def async_send_packet(self, packet: bytes) -> bool:
        async with self._send_lock:
            for attempt in range(1, SEND_RETRY_MAX + 1):
                # idle 대기
                t0 = asyncio.get_running_loop().time()
                while not self.is_idle():
                    await asyncio.sleep(0.01)
                    if asyncio.get_running_loop().time() - t0 > 1.0:
                        break
                # 전송
                await self.hass.async_add_executor_job(self.conn.send, packet, 1.0)
                self._last_tx_monotonic = asyncio.get_running_loop().time()
                # 실패 시 재시도
                if attempt < SEND_RETRY_MAX:
                    await asyncio.sleep(SEND_RETRY_GAP)
            return True
