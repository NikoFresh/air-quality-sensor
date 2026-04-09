WIFI_SSID = "."
WIFI_PASSWORD = "puntopunto"

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
