# hmip2mqtt

Connects a [Homematic IP Cloud](https://www.homematic-ip.com/en/start.html) installation to MQTT.

In intervals defined by the teleperiod option (defaults to 60 seconds), the current state of all Homematic devices is published to MQTT with the messages
* `tele/<prefix><device name>/STATE`
* `tele/<prefix><device id>/STATE`

## Installation

You need to have a working Python 3.8+ installation. The easiest way to install is with `pip3` from the command line:

```pip3 install -U hmip2mqtt```

 This will install (and update) all required packages.

Run the program from the command line with:

``` hmip2mqtt <broker address>```

where `<broker address>` is the IP address or the domain name of your MQTT broker. The program will run until terminated.

On first run, it will ask you for the required data to access your Homematic installation. You will need to have physical access to your access point.
On subsequent runs, this information will be used.

To see all available options, run
``` hmip2mqtt --help```

## Implementation

All the heavy lifting is done with the packages [Homematic IP REST API](https://github.com/coreGreenberet/homematicip-rest-api) and [Eclipse Paho™ MQTT Python Client](https://github.com/eclipse/paho.mqtt.python).

## How to build
You need to have Python 3.8+ and the [Poetry](https://python-poetry.org/) package manager.
1. Clone the repository
2. Run `poetry install` in the project folder
