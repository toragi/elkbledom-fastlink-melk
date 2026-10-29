from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.components import bluetooth
from homeassistant.const import CONF_ADDRESS, CONF_NAME
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN


class MelkConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        errors = {}

        # discovered MELK/ELK devices
        discovered = []
        for service_info in bluetooth.async_discovered_service_info(self.hass, False):
            name = service_info.name or ""
            if name.upper().startswith(("MELK", "ELK-", "LEDBLE")):
                discovered.append((service_info.address, name))

        if user_input is not None:
            address = user_input[CONF_ADDRESS].strip().upper()
            name = (user_input.get(CONF_NAME) or address).strip()
            await self.async_set_unique_id(address)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=name,
                data={CONF_ADDRESS: address, CONF_NAME: name},
            )

        schema = {
            vol.Required(CONF_ADDRESS): str,
            vol.Optional(CONF_NAME): str,
        }

        # helper text via description placeholders
        placeholders = {
            "hint": "MAC вида BE:67:01:03:09:E0",
            "found": ", ".join(f"{n} ({a})" for a, n in discovered[:8])
            or "пока не найдено — нужен активный Bluetooth proxy",
        }

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(schema),
            errors=errors,
            description_placeholders=placeholders,
        )

    async def async_step_bluetooth(self, discovery_info) -> FlowResult:
        address = discovery_info.address
        await self.async_set_unique_id(address)
        self._abort_if_unique_id_configured()
        name = discovery_info.name or address
        return self.async_create_entry(
            title=name,
            data={CONF_ADDRESS: address, CONF_NAME: name},
        )
