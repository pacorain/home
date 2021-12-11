"""The Starlink integration."""
from __future__ import annotations
from abc import ABC

from datetime import timedelta
import logging
import async_timeout

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from spacex.starlink.dish import StarlinkDish

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# TODO List the platforms that you want to support.
# For your initial PR, limit it to 1 platform.
PLATFORMS: list[str] = ["binary_sensor", "sensor"]
SCAN_INTERVAL = timedelta(seconds=5)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Starlink from a config entry."""
    dish = StarlinkDish(address=entry.data["address"], autoconnect=True)

    async def async_update_data():
        async with async_timeout.timeout(10):
            dish.refresh()

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="Starlink",
        update_method=async_update_data,
        update_interval=timedelta(seconds=entry.data["update_interval"] or 5),
    )

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = dict()
    hass.data[DOMAIN][entry.entry_id] = (dish, coordinator)

    await coordinator.async_refresh()
    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True


class BaseStarlinkEntity(CoordinatorEntity, ABC):
    base_name = NotImplemented

    def __init__(self, coordinator: DataUpdateCoordinator, dish: StarlinkDish):
        super().__init__(coordinator)
        self.dish = dish

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        if not self.dish.connected:
            self.dish.connect()

        # TODO: Disconnect if the last entity is removed

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.dish.id)},
            "name": "Starlink",
            "model": "Dishy McFlatface",  # TODO: Get the actual model from the satellite
            "manufacturer": "SpaceX",
            "sw_version": self.dish.software_version,
            "hw_version": self.dish.hardware_version,
        }

    @property
    def name(self):
        return self.device_info["name"] + " " + self.base_name


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
