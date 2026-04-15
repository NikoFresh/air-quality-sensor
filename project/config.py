import json


def load_wifi_networks(path="wifi.json"):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except OSError:
        print("[WARN] wifi_config.json non trovato, uso lista vuota")
        return []
    except ValueError:
        print("[WARN] wifi_config.json non è JSON valido")
        return []


WIFI_NETWORKS = load_wifi_networks()

MQTT_CLIENT_ID = "esp32_air_quality_nf"
MQTT_TOPIC_PREFIX = "nfsensors/air"

MQTT_BROKERS = [
    {
        "name": "home_assistant",
        "host": "100.71.89.77",
        "port": 1883,
        "user": "mqtt_user",
        "password": "mqtt_pass",
        "enabled": False,
    },
    {
        "name": "cloud",
        "host": "broker.emqx.io",
        "port": 1883,
        "user": None,
        "password": None,
        "enabled": True,
    },
]
