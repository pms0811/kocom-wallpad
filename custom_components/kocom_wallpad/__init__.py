from __future__ import annotations

from typing import Any
import asyncio

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.const import CONF_HOST, CONF_PORT

from .const import DOMAIN, PLATFORMS, DISPATCH_DEVICE_ADDED
from .gateway import KocomGateway


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    host: str = entry.data[CONF_HOST]
    port: int | None = entry.data[CONF_PORT]

    gateway = KocomGateway(hass, host=host, port=port)
    await gateway.async_start()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = gateway

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    for dev in gateway.registry.all_entities():
        async_dispatcher_send(hass, DISPATCH_DEVICE_ADDED, entry.entry_id, dev)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        gateway: KocomGateway = hass.data[DOMAIN].pop(entry.entry_id)
        await gateway.async_stop()
    return unload_ok
