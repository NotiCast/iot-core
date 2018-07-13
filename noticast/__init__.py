import subprocess
import json
import time

import logging

import raven
import requests
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

ravenclient = raven.Client('https://3cb64c355d7f4c5790b0ade37a86405f:ceb81b7b1'
                           '0704f178e69b6b701588434@sentry.io/1243070')

VENDOR_DIR = "/home/pi/.config/noticast"

with open("/etc/machine-id") as machine_file:
    CLIENT_ID = machine_file.read().strip()
with open("%s/connection/iot-endpoint" % VENDOR_DIR) as endpoint:
    HOSTNAME = endpoint.read().strip()

CA_CHAIN = "%s/chain.pem" % VENDOR_DIR
PRIVATE_KEY = "%s/connection/key" % VENDOR_DIR
CERTIFICATE = "%s/connection/cert.crt" % VENDOR_DIR

# Init AWSIoTMQTTClient
client = AWSIoTMQTTClient(CLIENT_ID)
client.configureEndpoint(HOSTNAME, 8883)
client.configureCredentials(CA_CHAIN, PRIVATE_KEY, CERTIFICATE)

# AWSIoTMQTTClient connection configuration
client.configureAutoReconnectBackoffTime(1, 32, 20)
client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
client.configureDrainingFrequency(2)  # Draining: 2 Hz
client.configureConnectDisconnectTimeout(100)  # 10 sec
client.configureMQTTOperationTimeout(50)  # 5 sec


def handler(_0, _1, message):
    payload = json.loads(message.payload.decode('ascii'))
    uri = payload["uri"]
    with open("/tmp/file.mp3", "wb") as f:
        try:
            for chunk in requests.get(uri, stream=True).iter_content(
                    chunk_size=128):
                f.write(chunk)
        except:  # noqa
            print("Got exception")
            ravenclient.captureException()
    subprocess.call(["/usr/bin/ffplay", "/tmp/file.mp3",
                     "-nodisp", "-autoexit"])
    print(repr(payload))


client.connect()
client.subscribe("noticast-messages", 1, handler)

# wtf AWSIoTPythonSDK, threads?
while True:
    time.sleep(1)
