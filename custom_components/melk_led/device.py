"""Minimal Elkotrol-style BLE client: connect → (login) → write → disconnect."""
from __future__ import annotations

import asyncio
import logging
from typing import Iterable

from bleak_retry_connector import (
    BleakClientWithServiceCache,
    BleakNotFoundError,
    establish_connection,
)
from homeassistant.components import bluetooth
from homeassistant.core import HomeAssistant

from .const import (
    CMD_OFF,
    CMD_OFF_ALT,
    CMD_ON,
    CMD_ON_ALT,
    EFFECTS,
    LOGIN_1,
    LOGIN_2,
    WRITE_UUID,
)

_LOGGER = logging.getLogger(__name__)


class MelkDevice:
    def __init__(self, hass: HomeAssistant, address: str, name: str) -> None:
        self.hass = hass
        self.address = address
        self.name = name
        self._lock = asyncio.Lock()
        self.is_on = False
        self.rgb = (255, 255, 255)
        self.brightness = 255  # 1..255
        self.effect = "none"

    def _ble_device(self):
        dev = bluetooth.async_ble_device_from_address(
            self.hass, self.address, connectable=True
        )
        if dev is None:
            dev = bluetooth.async_ble_device_from_address(self.hass, self.address)
        return dev

    async def _send(self, payloads: Iterable[bytes]) -> None:
        """One short session: connect, optional login, writes, disconnect."""
        async with self._lock:
            ble_device = self._ble_device()
            if ble_device is None:
                raise BleakNotFoundError(
                    f"{self.address}: not in Bluetooth discovery right now "
                    "(нужен активный proxy/scanner)"
                )

            client = None
            try:
                client = await establish_connection(
                    BleakClientWithServiceCache,
                    ble_device,
                    self.name or self.address,
                    lambda _c: None,
                )

                char = client.services.get_characteristic(WRITE_UUID)
                if char is None:
                    # fallback: first writable char under FFF0-like services
                    for service in client.services:
                        for c in service.characteristics:
                            if "write" in c.properties or "write-without-response" in c.properties:
                                if "fff3" in c.uuid.lower() or "ffe1" in c.uuid.lower():
                                    char = c
                                    break
                        if char:
                            break
                if char is None:
                    raise RuntimeError("Write characteristic FFF3/FFE1 not found")

                # MELK login (harmless on non-MELK if ignored)
                try:
                    await client.write_gatt_char(char, LOGIN_1, response=False)
                    await asyncio.sleep(0.15)
                    await client.write_gatt_char(char, LOGIN_2, response=False)
                    await asyncio.sleep(0.15)
                except Exception as err:
                    _LOGGER.debug("%s: login write skipped/failed: %s", self.address, err)

                for payload in payloads:
                    await client.write_gatt_char(char, payload, response=False)
                    await asyncio.sleep(0.05)

                _LOGGER.debug(
                    "%s: sent %s",
                    self.address,
                    [p.hex() for p in payloads],
                )
            finally:
                if client is not None and client.is_connected:
                    try:
                        await client.disconnect()
                    except Exception:
                        pass
                await asyncio.sleep(0.25)

    @staticmethod
    def _color_frame(r: int, g: int, b: int) -> bytes:
        return bytes([0x7E, 0x00, 0x05, 0x03, r & 0xFF, g & 0xFF, b & 0xFF, 0x00, 0xEF])

    @staticmethod
    def _brightness_frame(percent: int) -> bytes:
        p = max(0, min(100, int(percent)))
        return bytes([0x7E, 0x04, 0x01, p, 0xFF, 0x00, 0xFF, 0x00, 0xEF])

    @staticmethod
    def _effect_frame(effect_id: int) -> bytes:
        return bytes([0x7E, 0x00, 0x03, effect_id & 0xFF, 0x03, 0x00, 0x00, 0x00, 0xEF])

    async def async_turn_on(self) -> None:
        # dual on frames — different MELK firmwares accept different ones
        await self._send([CMD_ON, CMD_ON_ALT])
        self.is_on = True

    async def async_turn_off(self) -> None:
        await self._send([CMD_OFF, CMD_OFF_ALT])
        self.is_on = False

    async def async_set_rgb(self, r: int, g: int, b: int, brightness: int | None = None) -> None:
        if brightness is not None:
            self.brightness = max(1, min(255, int(brightness)))
        self.rgb = (r & 0xFF, g & 0xFF, b & 0xFF)
        scale = self.brightness / 255.0
        rr = int(self.rgb[0] * scale)
        gg = int(self.rgb[1] * scale)
        bb = int(self.rgb[2] * scale)
        # on + color in one session (Elkotrol-like)
        await self._send([CMD_ON, self._color_frame(rr, gg, bb)])
        self.is_on = True
        self.effect = "none"

    async def async_set_brightness(self, brightness: int) -> None:
        self.brightness = max(1, min(255, int(brightness)))
        percent = round(self.brightness * 100 / 255)
        r, g, b = self.rgb
        scale = self.brightness / 255.0
        await self._send(
            [
                self._brightness_frame(percent),
                self._color_frame(int(r * scale), int(g * scale), int(b * scale)),
            ]
        )
        self.is_on = True

    async def async_set_effect(self, effect_key: str) -> None:
        key = effect_key if effect_key in EFFECTS else "none"
        self.effect = key
        if key == "none":
            await self.async_set_rgb(*self.rgb)
            return
        await self._send([self._effect_frame(EFFECTS[key])])
        self.is_on = True
