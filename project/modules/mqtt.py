import network
import time
from umqtt.simple import MQTTClient
import config


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if wlan.isconnected():
        return True
    print(f"Connecting to WiFi {config.WIFI_SSID}...")
    wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
    for _ in range(20):
        if wlan.isconnected():
            print(f"WiFi connected: {wlan.ifconfig()[0]}")
            return True
        time.sleep(1)
    print("WiFi connection failed")
    return False


class MQTTManager:
    def __init__(self):
        self.clients = []
        self._init_clients()

    def _init_clients(self):
        for broker in config.MQTT_BROKERS:
            if not broker["enabled"]:
                continue
            try:
                client = MQTTClient(
                    client_id=f"{config.MQTT_CLIENT_ID}_{broker['name']}",
                    server=broker["host"],
                    port=broker["port"],
                    keepalive=60,
                    **({"user": broker["user"], "password": broker["password"]}
                       if broker.get("user") else {})
                )
                client.connect()
                self.clients.append({"name": broker["name"], "client": client})
                print(f"MQTT connected: {broker['name']}")
            except Exception as e:
                print(f"MQTT failed ({broker['name']}): {e}")

    def publish(self, data):
        if not self.clients:
            return
        for item in self.clients:
            try:
                for key, value in data.items():
                    if value is None:
                        continue
                    topic = f"{config.MQTT_TOPIC_PREFIX}/{key}"
                    item["client"].publish(topic, str(value))
            except Exception as e:
                print(f"MQTT publish failed ({item['name']}): {e}")
                # try to reconnect
                try:
                    item["client"].connect()
                except:
                    pass

    def disconnect(self):
        for item in self.clients:
            try:
                item["client"].disconnect()
            except:
                pass
