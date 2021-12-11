from homeassistant.const import (
    PERCENTAGE,
    TIME_MILLISECONDS,
    DATA_RATE_MEGABITS_PER_SECOND,
    DEGREE,
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
    def state(self):
        return round(self.dish.status.ping_drop_rate * 100.0, 2)


class PingLatency(StarlinkSensorEntity):
    base_name = "Ping Latency"
    unit_of_measurement = TIME_MILLISECONDS

    @property
    def state(self):
        return round(self.dish.status.ping_latency, 3)


class DownlinkThroughput(StarlinkSensorEntity):
    base_name = "Downlink Throughput"
    unit_of_measurement = DATA_RATE_MEGABITS_PER_SECOND

    @property
    def state(self):
        return round(self.dish.status.downlink_throughput / (1000 ** 2), 3)


class UplinkThroughput(StarlinkSensorEntity):
    base_name = "Uplink Throughput"
    unit_of_measurement = DATA_RATE_MEGABITS_PER_SECOND

    @property
    def state(self):
        return round(self.dish.status.uplink_throughput / (1000 ** 2), 3)


class Azimuth(StarlinkSensorEntity):
    base_name = "Azimuth"
    unit_of_measurement = DEGREE

    @property
    def state(self):
        return round(self.dish.status.azimuth_deg, 2)


class Elevation(StarlinkSensorEntity):
    base_name = "Elevation"
    unit_of_measurement = DEGREE

    @property
    def state(self):
        return round(self.dish.status.elevation_deg, 2)


class NumberOfAlerts(StarlinkSensorEntity):
    base_name = "Number of Alerts"

    @property
    def state(self):
        return len(self.dish.status.alerts)

    @property
    def state_attributes(self):
        return {alert.label: alert in self.dish.status.alerts for alert in DishAlert}
