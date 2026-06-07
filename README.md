#  ISS Overhead Notifier

A Python script that tracks the International Space Station in real time and sends you an email the moment it passes over your location.

---

## What it does

The ISS orbits Earth at 28,000 km/h, completing a full orbit every 90 minutes. This script polls its live position every 60 seconds, calculates the distance between you and the station using the Haversine formula, and fires off an email notification when it comes within 1,000 km overhead — without spamming you during the same pass.

---

## How it works

```
while True:
    fetch ISS position from API
    calculate distance using Haversine formula
    if distance < 1000 km and email not already sent:
        send email
        mark email as sent
    if ISS moves out of range:
        reset flag (ready for next pass)
    wait 60 seconds
```

---

## Flow diagram

```
Start
  │
  ▼
Fetch ISS coordinates (wheretheiss.at API)
  │
  ▼
Calculate distance using Haversine formula
  │
  ├── distance < 1000 km AND email not sent?
  │         │
  │         ▼ YES
  │     Send Gmail notification
  │     Set email_sent = True
  │
  ├── distance >= 1000 km?
  │         │
  │         ▼ YES
  │     Reset email_sent = False
  │
  ▼
Wait 60 seconds → repeat
```

---

## Features

- Tracks the ISS using a live public API
- Calculates distance using the Haversine formula (accounts for Earth's curvature)
- Sends email alerts through Gmail SMTP
- Checks ISS position every 60 seconds
- Prevents duplicate notifications during the same ISS pass

---

## Technologies

| Library / Module | Purpose |
|---|---|
| `requests` | Fetching live ISS coordinates from the REST API |
| `smtplib` | Sending email via Gmail SMTP |
| `math` | Haversine formula calculations |
| `time` | Polling interval (60-second loop) |

---

## Concepts demonstrated

- REST API consumption and JSON parsing
- Geospatial distance calculation (Haversine formula)
- SMTP email automation
- Continuous monitoring with a polling loop
- State management using a boolean flag

---

## The Haversine formula

The script uses the Haversine formula to calculate the great-circle distance between two points on Earth's surface given their latitude and longitude:

```
d = 2R · arcsin( √( sin²(Δφ/2) + cos(φ₁)·cos(φ₂)·sin²(Δλ/2) ) )
```

Where:
- `φ` = latitude in radians
- `λ` = longitude in radians  
- `R` = Earth's radius (6,371 km)
- `d` = distance in km

This is more accurate than naive degree-difference checks because it accounts for the curvature of the Earth. Longitude degrees get physically shorter as you move toward the poles — a flat comparison would overestimate east-west distances at high latitudes.

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/iss-notifier.git
cd iss-notifier
```

### 2. Install dependencies

```bash
pip install requests
```

### 3. Configure your details

Open `main.py` and replace the placeholder values:

```python
my_lat = 20.500000       # your latitude
my_lon = 120.70000       # your longitude

sender_email   = "you@gmail.com"
receiver_email = "you@gmail.com"
password       = "your_app_password"
```

### 4. Generate a Gmail app password

Gmail blocks direct password login for scripts. You need an app-specific password:

1. Go to [myaccount.google.com](https://myaccount.google.com)
2. Security → 2-Step Verification → App passwords
3. Generate a password for "Mail"
4. Paste it into the `password` field above

### 5. Run the script

```bash
python main.py
```

The script will run indefinitely, checking every 60 seconds. Keep the terminal open or deploy to a cloud service to run 24/7.

---

## Future improvements

- Detect whether the ISS is visible at night (only passes above the local horizon in darkness are visible to the naked eye)
- Add support for multiple recipients
- Configurable distance threshold
- GUI dashboard with live map
- Deploy as a cloud service with environment variable support

---

## API used

[wheretheiss.at](https://wheretheiss.at) — returns live latitude, longitude, altitude, and velocity of the ISS. No API key required.

---

## License

MIT
