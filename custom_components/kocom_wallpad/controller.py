from __future__ import annotations

from typing import Callable, Dict, List, Optional
from dataclasses import dataclass

from homeassistant.helpers.dispatcher import async_dispatcher_send

from .const import (
    LOGGER,
    PACKET_PREFIX,
    PACKET_SUFFIX,
    PACKET_LEN,
    DISPATCH_DEVICE_ADDED,
    DISPATCH_DEVICE_UPDATED,
    DeviceType,
    SubType,
)
from .gateway import DeviceKey, DeviceState


@dataclass(slots=True, frozen=True)
class PacketStruct:
    raw: bytes

    @property
    def packet_type(self) -> int:
        return (self.raw[3] >> 4) & 0x0F

    @property
    def dest(self) -> bytes:
        return self.raw[5:7]

    @property
    def src(self) -> bytes:
        return self.raw[7:9]

    @property
    def command(self) -> int:
        return self.raw[9]

    @property
    def payload(self) -> bytes:
        return self.raw[10:18]

    @property
    def checksum(self) -> int:
        return self.raw[18]
        
    @property
    def peer(self) -> tuple[int | None, int | None]:
        if self.dest[0] == 0x01:
            return (self.src[0], self.src[1])
        elif self.src[0] == 0x01:
            return (self.dest[0], self.dest[1])
        else:
            LOGGER.warning("Peer resolution failed: dest=%s, src=%s", self.dest.hex(), self.src.hex())
            return (None, None)

    @property
    def dev_type(self) -> DeviceType:
        code_map = {
            0x0E: DeviceType.LIGHT,
            0x3B: DeviceType.OUTLET,
            0x36: DeviceType.THERMOSTAT,
            0x48: DeviceType.VENTILATION,
            0x2C: DeviceType.GASVALVE,
            0x44: DeviceType.ELEVATOR
        }
        if dev_type := code_map.get(self.peer[0], DeviceType.UNKNOWN):
            LOGGER.warning("Unknown device type: %s, raw: %s", hex(self.peer[0]), self.raw.hex())
        return dev_type
    
    @property
    def dev_room(self) -> int | None:
        return self.peer[1]


class KocomController:

    def __init__(self, gateway: "KocomGateway") -> None:
        self.gateway = gateway
        self._rx_buf = bytearray()

    @staticmethod
    def _checksum(buf: bytes) -> int:
        return (256 - (sum(buf) % 256)) % 256

    def feed(self, chunk: bytes) -> None:
        if not chunk:
            return
        self._rx_buf.extend(chunk)
        for pkt in self._split_buf():
            self._dispatch_packet(pkt)

    def _split_buf(self) -> List[bytes]:
        packets: List[bytes] = []
        buf = self._rx_buf
        while True:
            start = buf.find(PACKET_PREFIX)
            if start < 0:
                # 프리픽스 이전의 쓰레기 데이터 제거
                buf.clear()
                break
            if start > 0:
                del buf[:start]
            if len(buf) < PACKET_LEN:
                # 더 받을 때까지 대기
                break
            # 고정 길이 확인 후 서픽스 검사
            candidate = bytes(buf[:PACKET_LEN])
            if not candidate.endswith(PACKET_SUFFIX):
                # 한 바이트 밀어서 재탐색 (프레이밍 어긋남 복구)
                del buf[0]
                continue
            packets.append(candidate)
            del buf[:PACKET_LEN]
        return packets

    def _dispatch_packet(self, packet: bytes) -> None:
        ps = PacketStruct(packet)
        if self._checksum(packet[2:18]) != ps.checksum:
            return
        
        handler = None
        if ps.dev_type == DeviceType.LIGHT:
            handler = self._handle_light(ps)
        elif ps.dev_type == DeviceType.OUTLET:
            handler = self._handle_outlet(ps)
        elif ps.dev_type == DeviceType.THERMOSTAT:
            handler = self._handle_thermostat(ps)
        elif ps.dev_type == DeviceType.VENTILATION:
            handler = self._handle_ventilation(ps)
        elif ps.dev_type == DeviceType.ELEVATOR:
            handler = self._handle_elevator(ps)
            
        if handler is not None:
            if self.gateway.registry.get(handler.key) is None:
                async_dispatcher_send(self.gateway.hass, DISPATCH_DEVICE_ADDED, self.gateway.entry_id, handler)
            if self.gateway.registry.upsert(handler):
                async_dispatcher_send(self.gateway.hass, DISPATCH_DEVICE_UPDATED, self.gateway.entry_id, handler)

    def _handle_light(self, ps: PacketStruct) -> DeviceState:
        pass

    def _handle_outlet(self, ps: PacketStruct) -> DeviceState:
        pass
    
    def _handle_thermostat(self, ps: PacketStruct) -> DeviceState:
        pass
    
    def _handle_ventilation(self, ps: PacketStruct) -> DeviceState:
        pass
    
    def _handle_elevator(self, ps: PacketStruct) -> DeviceState:
        pass

    def _default_handle(self, ps: PacketStruct) -> None:
        try:
            platform = None
        except Exception:
            platform = None
        if platform is None:
            return
        key = DeviceKey(
            device_type=ps.dev_type,
            room_index=ps.dev_room,
            device_index=0,
            sub_type=SubType.NONE,
        )
        attrib = {"state": False}
        dev = DeviceState(key=key, platform=platform, attributes=attrib)

        if self.gateway.registry.upsert(dev):
            async_dispatcher_send(self.gateway.hass, DISPATCH_DEVICE_ADDED, self.gateway.entry_id, dev)
            async_dispatcher_send(self.gateway.hass, DISPATCH_DEVICE_UPDATED, self.gateway.entry_id, dev)
