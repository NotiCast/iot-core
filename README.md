# iot-core
AWS IoT Core Subscriber Setup for NotiCast

**Note:** This is intended to be used via the [device-bootstrap
repository](https://github.com/NotiCast/device-bootstrap).

# Dependencies

- `AWSIoTPythonSDK`
- `requests`
- `raven`

# main.py

The `main.py` program opens a connection to the specified endpoint
and configures the provided credentials to connect to the IoT. It
also downloads audio from the s3 bucket to be played.
