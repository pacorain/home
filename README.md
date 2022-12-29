# My Home Assistant config

This is my configuration for my smart home.

I've laid everything out using Home Assistant's [package system](https://www.home-assistant.io/docs/configuration/packages/).

## Overview

I have a mix of Zigbee and Z-Wave devices, which I've set up via the UI (so you won't see them here).

## Custom Compoents

I have a mix of custom components. Because I use HACS, by default, any custom component is ignored.

This makes it so I don't have to commit any updates, and also is better for security because any
vulnerabilities in HACS plugins can't be linked specifically to my home.

I've started using git submodules to store my custom compnents. Some of them may be linked to public
repositories; others may be private. This may be for a variety of reasons. However, if you're 
interested in learning more about a specific custom compnent, please 
[let me know](mailto:hey@paco.wtf) -- there may just be some obstacles from making the code public 
that I can work around if someone gives me a heads up.