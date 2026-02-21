# Distributed Drone Telemetry System  
CSE 5306 – Project 2  
gRPC + Docker Compose

---

# 1. Overview

This project implements a distributed telemetry pipeline for a single drone using:

- Python 3.11
- gRPC
- Docker Compose

The system simulates multiple sensor nodes that generate telemetry and alerts.  
Telemetry flows through a multi-stage processing pipeline before reaching an interactive client.

---

# 2. System Architecture

Telemetry Flow:
Sensors → Aggregation → Analysis → Update → Server → Client

Command Flow:
Client → Server → Update

Each stage runs in its own Docker container.

---

## Sensors

Containers:
- imu
- gps
- engine
- battery
- airdata

Each sensor:
- Generates a telemetry value
- Determines alert conditions
- Responds to GetTelemetry RPC

---

## Aggregation (port 50051)

- Connects to all sensor nodes
- Collects telemetry
- Streams telemetry upward

---

## Analysis (port 50052)

- Receives telemetry stream
- Performs optional alert checks
- Passes stream upward

---

## Update (port 50054)

- Forwards telemetry stream
- Processes command requests

---

## Server (port 50053)

- Provides command interface for client
- Forwards commands to Update service

---

## Client

- Interactive command-line interface
- Sends commands to Server
- Displays formatted output

---

# 3. Project Structure

src/
  aggregation.py
  analysis.py
  update.py
  server.py
  client.py
  imu_sensor.py
  gps_sensor.py
  engine_sensor.py
  battery_sensor.py
  airdata_sensor.py
  drone.proto
  drone_pb2.py
  drone_pb2_grpc.py

Dockerfile.*
docker-compose.yml
run.sh
README.md

All Python source code resides in `src/`.

---

# 4. Build & Run Instructions

Run all commands from the project root (where docker-compose.yml is located).

---

## Option A – Recommended (Use Script)

Make script executable:

chmod +x run.sh

Run:

./run.sh

The script performs:

docker compose down -v
docker compose build --no-cache
docker compose up -d
docker compose run --rm client

---

## Option B – Manual Execution

1. Clean previous containers:

docker compose down -v

2. Build images:

docker compose build --no-cache

3. Start infrastructure (background mode):

docker compose up -d

4. Run client interactively:

docker compose run --rm client

You should see:

Client ready. Type help.
>

---

# 5. Available Client Commands

help  
Displays available commands.

status  
Displays system status.

health  
Displays overall health (based on alerts).

list  
Lists available sensor names.

Expected sensors:
- altitude
- airspeed
- voltage
- egt
- latitude
- longitude
- vibration

sensor <name>  
Displays current value for a specific sensor.

Example:
sensor voltage

alerts  
Displays all currently active alerts.

If no alerts:
No active alerts.

quit  
Exits the client.

---

# 6. Units Used

Sensor     | Units
-----------|------
altitude   | ft
airspeed   | kt
voltage    | V
egt        | °C
latitude   | deg
longitude  | deg
vibration  | g

---

# 7. Troubleshooting

Client won’t accept input:

Correct startup:
docker compose up -d
docker compose run --rm client

Do NOT use:
docker attach client

Method not implemented:
docker compose down -v
docker compose build --no-cache
docker compose up -d

Containers not starting:
docker ps

---

# 8. End-to-End Execution Summary

docker compose down -v
docker compose build --no-cache
docker compose up -d
docker compose run --rm client

Then type:

help
status
list
sensor voltage
alerts