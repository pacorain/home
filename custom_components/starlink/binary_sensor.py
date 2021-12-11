from spacex.starlink.outage_reason import OutageReason
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    DEVICE_CLASS_PROBLEM,
    DEVICE_CLASS_CONNECTIVITY,
)

from .const import DOMAIN
from . import BaseStarlinkEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
):
    dish, coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [entity(coordinator, dish) for entity in StarlinkBinaryEntity.__subclasses__()]
    )

    return True


class StarlinkBinaryEntity(BaseStarlinkEntity, BinarySensorEntity):
    pass


class ConnectedEntity(StarlinkBinaryEntity):
    base_name = "Connected"
    device_class = DEVICE_CLASS_CONNECTIVITY

    @property
    def unique_id(self):
        return f"{self.dish.id}.connected"

    @property
    def icon(self) -> str:
        if self.is_on:
            return "mdi:check-network-outline"
        elif self.dish.status.outage_reason == OutageReason.OBSTRUCTED:
            return "mdi:weather-cloudy-alert"
        elif self.dish.status.outage_reason == OutageReason.BOOTING:
            return "mdi:update"
        elif self.dish.status.outage_reason == OutageReason.NO_SCHEDULE:
            return "mdi:satellite-uplink"
        elif self.dish.status.outage_reason == OutageReason.THERMAL_SHUTDOWN:
            return "mdi:thermometer-alert"
        elif self.dish.status.outage_reason == OutageReason.STOWED:
            return "mdi:stop-circle"
        else:
            return "mdi:alert"

    @property
    def state_attributes(self):
        return {
            "Problem": "None"
            if self.dish.status.outage_reason is None
            else self.dish.status.outage_reason.label
        }

    @property
    def is_on(self):
        return self.dish.status.connected


class ObstructedEntity(StarlinkBinaryEntity):
    base_name = "Starlink Obstructed"
    device_class = DEVICE_CLASS_PROBLEM

    @property
    def unique_id(self):
        return f"{self.dish.id}.obstructed"

    @property
    def is_on(self):
        return self.dish.status.obstructed
