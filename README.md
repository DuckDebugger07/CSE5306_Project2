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

Telemetry flow:
Sensors → Aggregation → Analysis → Update → Server → Client

Command flow:
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
- Determines if an alert condition exists
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

```
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
README.md
```

All Python code resides in `src/`.

---

# 4. Build & Run Instructions

You MUST run commands from the project root (where docker-compose.yml is located).

---

## Step 1 – Stop and Clean

```
docker compose down -v
docker system prune -f
```

- Stops containers
- Removes volumes
- Cleans unused images

---

## Step 2 – Build Images

```
docker compose build --no-cache
```

Ensures fresh rebuild of all services.

---

## Step 3 – Start Infrastructure (Background Mode)

```
docker compose up -d
```

Starts:
- sensors
- aggregation
- analysis
- update
- server

Verify containers are running:

```
docker ps
```

---

## Step 4 – Run Client Interactively

Do NOT use `docker compose up` for client interaction.

Instead:

```
docker compose run --rm client
```

You should see:

```
Client ready. Type help.
>
```

Now you can enter commands.

---

# 5. Available Client Commands

---

## help

Displays available commands.

```
help
```

---

## status

Displays system status.

```
status
```

---

## health

Displays overall health (based on alerts).

```
health
```

---

## list

Lists available sensor names.

```
list
```

Expected output:

- altitude
- airspeed
- voltage
- egt
- latitude
- longitude
- vibration

---

## sensor <name>

Displays current value for specific sensor.

Example:

```
sensor voltage
```

Example output:

```
voltage: 24.50 V
```

---

## alerts

Displays all currently active sensor alerts.

```
alerts
```

---

### Example – No Alerts Active

```
alerts
```

Output:

```
No active alerts.
```

---

### Example – Single Alert

If the battery voltage drops below its threshold:

```
alerts
```

Output:

```
voltage: Battery low (18.90 V)
```

---

### Example – Multiple Alerts

If multiple sensors report alert conditions:

```
alerts
```

Output:

```
voltage: Battery critical (17.80 V)
egt: Engine temperature high (720.50 °C)
altitude: Altitude critically low (42.00 ft)
```

---

### How Alerts Work

Each sensor determines its own alert condition based on thresholds.  
If `alert == true` in the telemetry message, the system:

1. Propagates the alert through Aggregation → Analysis → Update  
2. Makes it available to the Server  
3. Displays it when the `alerts` command is issued  

Alerts are generated in the **sensor nodes**, not fabricated by the server.
---

## quit

Exits client.

```
quit
```

---

# 6. Units Used

| Sensor     | Units |
|------------|-------|
| altitude   | ft    |
| airspeed   | kt    |
| voltage    | V     |
| egt        | °C    |
| latitude   | deg   |
| longitude  | deg   |
| vibration  | g     |

---

# 7. Troubleshooting

---

## Client Won’t Accept Input

You likely ran:

```
docker compose up
```

Correct approach:

```
docker compose up -d
docker compose run --rm client
```

---

## Method Not Implemented

Rebuild everything:

```
docker compose down -v
docker compose build --no-cache
docker compose up -d
```

---

## DNS Resolution Errors

Ensure aggregation and analysis containers are running:

```
docker ps
```

---

# 8. End-to-End Execution Summary

```
docker compose down -v
docker compose build --no-cache
docker compose up -d
docker compose run --rm client
```

Then type:

```
help
status
list
sensor voltage
alerts
```

---
