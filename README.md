# VideoHub Python SDK

Official Python SDK for VideoHub – build video calls, audio rooms, and real-time communication applications with ease.

VideoHub enables developers to integrate video conferencing, audio rooms, real-time chat, AI chatbot integration, screen sharing, and real-time communication into their applications using simple APIs.

---

## Installation

Install from PyPI:

```bash
pip install videohub-python
```

---

## Requirements

* Python 3.9+
* Python 3.11+ (recommended)
* VideoHub API Key
* App credentials:

  * App ID
  * App Secret
  * App Platform (`web`, `android`, `ios`)
  * App Identifier (domain or package name)

---

## Quick Start

```python
from videohub.client import Client

videoHub = Client(
    api_key="vhub_live_xxxxxxxxx",
    app_id="your_app_id",
    app_secret="your_app_secret",
    app_platform="web",
    app_identifier="example.com"
)

# Create a room
videoHub.rooms.create(
    room_name="my-room",
    max_participants=5
)

# Generate a host token
token = videoHub.rooms.host_token("my-room")

print(token)
```

---

## Authentication

All API requests require the following credentials:

| Field          | Description                          |
| -------------- | ------------------------------------ |
| API Key        | Account authentication key           |
| App ID         | Unique application identifier        |
| App Secret     | Secret used for request verification |
| App Platform   | `web`, `android`, or `ios`           |
| App Identifier | Domain or package name               |

---

## Features

* Video calling
* Audio calling
* Screen sharing
* Room management
* Call management
* Admin APIs
* Secure authentication
* & more
---

## Examples

### Create Room

```python
room = videoHub.rooms.create(
    room_name="demo-room",
    max_participants=5
)

print(room)
```

---

### Generate Room Token

```python
token = videoHub.rooms.host_token("demo-room")

print(json.dumps({
    "token": token["token"],
    "rtc": videoHub.rtc
}, indent=4))
```

---

## Error Handling

The SDK raises structured exceptions for API errors:

```python
from videohub.exceptions import VideoHubError

try:
    client.rooms.create("room1")
except VideoHubError as e:
    print(e)
```


---

### Subscriber

```python
auth = videoHub.rooms.guest_token("demo-room", "app_id")

print(json.dumps({
    "token": auth["token"],
    "rtc": videoHub.rtc
}, indent=4))
```

---

## Project Structure

```
videohub/
├── client.py
├── config.py
├── constants.py
├── exceptions.py
├── http.py
│
├── services/
│   ├── auth.py
│   ├── rooms.py
│   ├── calls.py
│   └── admin.py
│
└── utils/
    └── validators.py
```

---

## Documentation

Full API documentation is available at:

https://docs.videohub.dev

---

## Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -m "Add feature"`)
4. Push to the branch (`git push origin feature-name`)
5. Open a Pull Request

---

## Reporting Issues

If you encounter a bug or want to request a feature, please open an issue:

https://github.com/letscms/videohub-python/issues

---

## License

This project is licensed under the MIT License.