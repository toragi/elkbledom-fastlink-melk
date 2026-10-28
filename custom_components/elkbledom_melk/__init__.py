from __future__ import annotations

import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, Event
from homeassistant.const import CONF_MAC, EVENT_HOMEASSISTANT_STOP, Platform

from .const import DOMAIN, CONF_RESET, CONF_DELAY
from .elkbledom import BLEDOMInstance

LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.LIGHT,
    Platform.NUMBER,
    Platform.SELECT,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up ELK-BLEDOM MELK from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    reset = entry.options.get(CONF_RESET, entry.data.get(CONF_RESET, False))
    delay = entry.options.get(CONF_DELAY, entry.data.get(CONF_DELAY, 120))
    mac = entry.data.get(CONF_MAC) or entry.options.get(CONF_MAC)

    if not mac:
        LOGGER.error("ELK-BLEDOM MELK: MAC address missing in entry %s", entry.entry_id)
        return False

    LOGGER.info("Initializing ELK-BLEDOM MELK: MAC=%s | reset=%s | delay=%s", mac, reset, delay)

    instance = BLEDOMInstance(mac, reset, delay, hass)
    hass.data[DOMAIN][entry.entry_id] = instance

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(_async_update_listener))

    async def _async_stop(event: Event) -> None:
        LOGGER.debug("Stopping ELK-BLEDOM MELK (%s) due to HA shutdown", mac)
        await instance.stop()

    entry.async_on_unload(
        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, _async_stop)
    )

    LOGGER.info("ELK-BLEDOM MELK integration successfully loaded for %s", mac)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    LOGGER.info("Unloading ELK-BLEDOM MELK: %s", entry.entry_id)
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        instance: BLEDOMInstance = hass.data[DOMAIN].pop(entry.entry_id, None)
        if instance:
            await instance.stop()
    return unload_ok


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    LOGGER.debug("Reloading ELK-BLEDOM MELK after options change")
    await hass.config_entries.async_reload(entry.entry_id)
