# Network Package

The goal of this package is to gather all of my network-related configuration. This is where I control and monitor network devices (like computers, network routers, etc.), configure Home Assistant's presence on the network, and monitor the performance of my home's network.

## HTTP Config

It includes my Home Assistant [HTTP configuration](http.yaml). 

I'm using HassOS on a Raspberry Pi, using the default port of 8123. The supervisor has port 80 mapped to [Nginx Proxy Manager](https://github.com/hassio-addons/addon-nginx-proxy-manager), so I need this set up to trust headers inserted by Nginx Proxy Manager to see the real IP.

## My internet

Here is my current network setup.

```

----------------       ----------------
| Raspberry Pi |  <--> | Wi-Fi Router |
----------------       ----------------
                              ^
                              |
                              |
                              |
                        o     |   o c C (  Verizon Wireless
                        |     |   |            (Backup)
                        |     v   |
                      ---------------------
    ----------------> | Cradlepoint Modem |
    |                 ---------------------
    |
    |      ,-.
    |   / \  `.     
    |  :   \    `
    |  |    .     `.   
    |  :     .      `.  Starlink
    |   \     `.      .
    |    \      `.     .
    |     `,       `.   \
    |    ,|,`.        `-.\
    |   '.||  ``-...__..-`
    |    |  |
    |    |__|
    |    /||\
    |   //||\\
    v  // || \\
    __//__||__\\__
   '--------------' 
```

This means that the Cradlepoint modem is actually getting two dynamic WAN IPs.

We are using [Starlink](https://www.starlink.com/) as our primary internet provider, with Verizon cellular as a backup plan for if Starlink has an outage.

## Cradlepoint

My Home Assistant has several sensors to monitor the status of my Cradlepoint modem. These are all configured through HTTP [RESTful sensors](https://www.home-assistant.io/integrations/sensor.rest/) from within the [sensor/cradlepoint]() and [binary_sensor/cradlepoint]() directories.

### Creating a HASS user

I have a separate user set up on Cradlepoint for these Home Assistant queries.

To do this, follow these steps:

1. Log into your Cradlepoint. By default, it is reachable on LAN via `http://192.168.0.1`.
2. Navigate to **System** > **Administration** > **Router Security**
3. Under **Advanced User Management**, click **Add**
4. Set a username (I use `hass`) and a password (I use `nicetry`)
5. Click **Save**

Then, in your `secrets.yaml` file, add `cradlepoint_user` and `cradlepoint_password` secrets corresponding to these values.

### Sensors

The sensors and binary sensors are located in [sensor/cradlepoint]() and [binary_sensor/cradlepoint](), respectively.
