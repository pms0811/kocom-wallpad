from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import os
import time

import socket, select
try:
    import serial  # type: ignore
except Exception:  # pragma: no cover
    serial = None  # type: ignore


@dataclass
class SyncConnectionWrapper:
    host: str
    port: Optional[int] = None  # None이면 시리얼
    serial_baud: int = 9600

    def __post_init__(self) -> None:
        self._sock: Optional[socket.socket] = None
        self._ser = None
        self._last_activity_mono: float = time.monotonic()

    # public
    def open(self) -> None:
        if self.host.startswith("/"):
            if serial is None:
                raise RuntimeError("pyserial required for serial port")
            self._ser = serial.Serial(self.host, self.serial_baud, timeout=0, write_timeout=0)
            self._sock = None
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setblocking(False)
            try:
                try:
                    s.connect((self.host, self.port or 8899))
                except (BlockingIOError, InterruptedError):
                    pass
                _, w, e = select.select([], [s], [s], 5.0)
                if s in e or not w:
                    s.close()
                    raise TimeoutError("connect timeout")
                if s.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR) != 0:
                    s.close()
                    raise OSError("connect failed")
                self._sock = s
                self._ser = None
            except Exception:
                s.close()
                raise
        self._last_activity_mono = time.monotonic()

    def close(self) -> None:
        if self._sock is not None:
            try:
                self._sock.close()
            finally:
                self._sock = None
        if self._ser is not None:
            try:
                self._ser.close()
            finally:
                self._ser = None

    def idle_since(self) -> float:
        return max(0.0, time.monotonic() - self._last_activity_mono)

    def send(self, data: bytes, timeout: float = 1.0) -> int:
        if self._sock is not None:
            total = 0
            end = time.monotonic() + timeout
            while total < len(data):
                tleft = max(0.0, end - time.monotonic())
                if tleft == 0.0:
                    raise TimeoutError("send timeout")
                _, w, _ = select.select([], [self._sock], [], tleft)
                if not w:
                    continue
                n = self._sock.send(data[total:])
                if n == 0:
                    raise OSError("socket closed")
                total += n
                self._last_activity_mono = time.monotonic()
            return total
        elif self._ser is not None:
            n = self._ser.write(data)
            self._last_activity_mono = time.monotonic()
            return int(n or 0)
        else:
            raise RuntimeError("not open")

    def recv(self, nbytes: int, timeout: float = 0.05) -> bytes:
        if self._sock is not None:
            r, _, _ = select.select([self._sock], [], [], timeout)
            if not r:
                return b""
            data = self._sock.recv(nbytes)
            if data:
                self._last_activity_mono = time.monotonic()
            return data
        elif self._ser is not None:
            if self._ser.in_waiting <= 0:
                r, _, _ = select.select([self._ser.fileno()], [], [], timeout)
                if not r:
                    return b""
            data = self._ser.read(nbytes)
            if data:
                self._last_activity_mono = time.monotonic()
            return data
        else:
            raise RuntimeError("not open")
