from __future__ import annotations

import logging

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_EFFECT,
    ATTR_RGB_COLOR,
    ColorMode,
    LightEntity,
    LightEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers import device_registry as dr

from .const import DOMAIN, EFFECT_LABELS, EFFECTS
from .device import MelkDevice

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    device: MelkDevice = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([MelkLight(device, entry)])


class MelkLight(LightEntity):
    _attr_supported_color_modes = {ColorMode.RGB}
    _attr_color_mode = ColorMode.RGB
    _attr_supported_features = LightEntityFeature.EFFECT
    _attr_icon = "mdi:led-strip-variant"

    def __init__(self, device: MelkDevice, entry: ConfigEntry) -> None:
        self._device = device
        self._attr_name = device.name
        self._attr_unique_id = f"{device.address}_light"
        self._attr_effect_list = [EFFECT_LABELS[k] for k in EFFECTS]
        self._label_to_key = {v: k for k, v in EFFECT_LABELS.items()}

    @property
    def is_on(self) -> bool:
        return self._device.is_on

    @property
    def brightness(self) -> int:
        return self._device.brightness

    @property
    def rgb_color(self) -> tuple[int, int, int]:
        return self._device.rgb

    @property
    def effect(self) -> str | None:
        return EFFECT_LABELS.get(self._device.effect, "Static")

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._device.address)},
            name=self._device.name,
            manufacturer="MELK",
            model="MELK LED Controller",
            connections={(dr.CONNECTION_NETWORK_MAC, self._device.address)},
        )

    async def async_turn_on(self, **kwargs) -> None:
        try:
            if ATTR_RGB_COLOR in kwargs:
                r, g, b = kwargs[ATTR_RGB_COLOR]
                await self._device.async_set_rgb(
                    r, g, b, kwargs.get(ATTR_BRIGHTNESS)
                )
            elif ATTR_BRIGHTNESS in kwargs:
                await self._device.async_set_brightness(kwargs[ATTR_BRIGHTNESS])
            elif ATTR_EFFECT in kwargs:
                label = kwargs[ATTR_EFFECT]
                key = self._label_to_key.get(label, "none")
                await self._device.async_set_effect(key)
            else:
                await self._device.async_turn_on()
        except Exception as err:
            _LOGGER.error("turn_on failed: %s", err)
            raise
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        try:
            await self._device.async_turn_off()
        except Exception as err:
            _LOGGER.error("turn_off failed: %s", err)
            raise
        self.async_write_ha_state()
