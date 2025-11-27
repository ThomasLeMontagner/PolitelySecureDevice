# PolitelySecureDevice

Device that greets recognized faces and can alert the tenant on intrusion. The architecture is designed with Capella; implementation runs on Raspberry Pi with a camera and speaker.

## Quickstart
- Install Python deps: `pip install -r requirements.txt`
- Set email env vars for alerts:
  - `ALERT_SENDER_EMAIL`
  - `ALERT_EMAIL_PASSWORD`
  - `ALERT_RECEIVER_EMAIL`
- Train encodings: `python facial_recognition/train_model.py`
- Run recognition + greeting loop: `python facial_recognition/run.py`
- Capture new headshots (PiCamera): `python facial_recognition/headshots_picam.py` (press Space to save, Esc to quit)

## Requirements
- Capella 5.2.0 (to open the system model)
- Raspberry Pi 4 with camera and audio output (for runtime)

## System Model
### Logical Architecture
The Logical Architecture describes the main architectural concepts. On the diagram below, the high-level architectural components and their functionalities are presented. Some design decisions are also made such as the choice of an audio message rather than a text message to greet people.

![Logical Architecture](images/[LAB]_Structure.jpg)

### Physical Architecture
The Physical Architecture describes the technological choices. Here we will make use of a RaspberryPi 4 and a camera to detect and recognize faces.

#### Implementation of "Greeting"
![Greeting](images/[PAB]_Greet_human.jpg)

#### Implementation of "Alert tenant"
![Alert Tenant](images/[PAB]_Alert_tenant_when_intrusion.jpg)
