# Gas Tracking

This is a sub-package that helps to monitor how much gas we're using and estimate the tank level, so
that we can let our gas company know when we need a refuel.

This works because we currently have a propane tank that is only hooked up to our gas furnace.

## How it works

The measurement starts with checking the meter that is already on the tank. That value goes into
`input_number.measured_tank_level` (in [input.yaml]()).

This value keeps track of the *last measured* tank level, and when it was changed. This ensures 
that we have visibility of both what Home Assistant is guessing the level is, and what we last
actually saw it as.

Instead, a few sensors are set up to get how long the furnace has run since this change, and that
value can be checked on `sensor.furnace_usage_since_last_check` (in [furnace_runtime.yaml]()).

Finally, that value is multiplied by a specific factor (right now, this is just defined in another
[input_number](input.yaml), but I might change it to be calculated in the future), and that result
is subtracted from the last measured tank percent to get an estimation.