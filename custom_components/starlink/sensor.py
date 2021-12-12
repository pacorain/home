from homeassistant.const import (
    PERCENTAGE,
    TIME_MILLISECONDS,
    DATA_RATE_MEGABITS_PER_SECOND,
    DEGREE,
    ENTITY_CATEGORY_DIAGNOSTIC
)
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import SensorEntity

from .const import DOMAIN
from . import BaseStarlinkEntity

from spacex.starlink import DishAlert


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
):
    dish, coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [entity(coordinator, dish) for entity in StarlinkSensorEntity.__subclasses__()]
    )

    return True


class StarlinkSensorEntity(BaseStarlinkEntity, SensorEntity):
    pass


class PingDropRate(StarlinkSensorEntity):
    base_name = "Ping Drop Rate"
    unit_of_measurement = PERCENTAGE

    @property
    def unique_id(self):
        return f"{self.dish.id}.drop_rate"

    @property
    def icon(self):
        if self.state > 0:
            return "mdi:close-network"
        else:
            return "mdi:check-network"

    @property
    def entity_category(self):
        return ENTITY_CATEGORY_DIAGNOSTIC

    @property
    def state(self):
        return round(self.dish.status.ping_drop_rate * 100.0, 2)


class PingLatency(StarlinkSensorEntity):
    base_name = "Ping Latency"
    unit_of_measurement = TIME_MILLISECONDS

    @property
    def unique_id(self):
        return f"{self.dish.id}.ping_latency"

    @property
    def icon(self):
        return "mdi:timeline-clock"

    @property
    def entity_category(self):
        return ENTITY_CATEGORY_DIAGNOSTIC

    @property
    def state(self):
        return round(self.dish.status.ping_latency, 3)


class DownlinkThroughput(StarlinkSensorEntity):
    base_name = "Downlink Throughput"
    unit_of_measurement = DATA_RATE_MEGABITS_PER_SECOND

    @property
    def icon(self):
        return "mdi:download"

    @property
    def unique_id(self):
        return f"{self.dish.id}.downlink_throughput"

    @property
    def state(self):
        return round(self.dish.status.downlink_throughput / (1000 ** 2), 3)


class UplinkThroughput(StarlinkSensorEntity):
    base_name = "Uplink Throughput"
    unit_of_measurement = DATA_RATE_MEGABITS_PER_SECOND

    @property
    def icon(self):
        return "mdi:upload"

    @property
    def unique_id(self):
        return f"{self.dish.id}.uplink_throughput"

    @property
    def state(self):
        return round(self.dish.status.uplink_throughput / (1000 ** 2), 3)


class Azimuth(StarlinkSensorEntity):
    base_name = "Azimuth"
    unit_of_measurement = DEGREE

    @property
    def icon(self):
        return "mdi:axis-z-rotate-clockwise"

    @property
    def unique_id(self):
        return f"{self.dish.id}.azimuth"

    @property
    def entity_category(self):
        return ENTITY_CATEGORY_DIAGNOSTIC

    @property
    def state(self):
        return round(self.dish.status.azimuth_deg, 2)


class Elevation(StarlinkSensorEntity):
    base_name = "Elevation"
    unit_of_measurement = DEGREE

    @property
    def icon(self):
        return "mdi:angle-acute"

    @property
    def unique_id(self):
        return f"{self.dish.id}.elevation"

    @property
    def entity_category(self):
        return ENTITY_CATEGORY_DIAGNOSTIC

    @property
    def state(self):
        return round(self.dish.status.elevation_deg, 2)


class NumberOfAlerts(StarlinkSensorEntity):
    base_name = "Number of Alerts"

    @property
    def unique_id(self):
        return f"{self.dish.id}.alerts"

    @property
    def icon(self):
        if self.state == 0:
            return "mdi:check-circle"
        else:
            return "mdi:alert"

    @property
    def state(self):
        return len(self.dish.status.alerts)

    @property
    def entity_category(self):
        return ENTITY_CATEGORY_DIAGNOSTIC

    @property
    def state_attributes(self):
        return {alert.label: alert in self.dish.status.alerts for alert in DishAlert}
