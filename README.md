# Distributed Drone Telemetry System  
CSE 5306 – Project 2  
gRPC + Docker Compose

---

# 1. Overview

This project implements a distributed telemetry processing pipeline for a drone using:

- Python 3.11
- gRPC
- Docker Compose

The system simulates multiple sensor nodes that generate telemetry and alerts.  
Telemetry flows through a multi-stage processing pipeline before reaching an interactive client.

Two architectures are provided:

1. Distributed Microservices Architecture
2. Monolithic Architecture (Single Container) for performance comparison

Docker Compose profiles are used to switch between architectures.

---

# 2. System Architecture

## Distributed Telemetry Flow

Sensors → Aggregation → Analysis → Update → Server → Client

Command Flow:

Client ↔ Server ↔ Update

Each stage runs in its own Docker container.

---

## Monolithic Architecture

All processing (aggregation, analysis, update, server logic) runs inside a single container.

This version removes inter-container RPC overhead to allow performance comparison.

---

# 3. Project Structure

```
src/
  aggregation.py
  analysis.py
  update.py
  server.py
  client.py
  monolith.py
  imu_sensor.py
  gps_sensor.py
  engine_sensor.py
  battery_sensor.py
  airdata_sensor.py
  drone.proto
  drone_pb2.py
  drone_pb2_grpc.py

Dockerfiles/
  Dockerfile.airdata
  Dockerfile.battery
  Dockerfile.engine
  Dockerfile.gps
  Dockerfile.imu
  Dockerfile.aggregation
  Dockerfile.analysis
  Dockerfile.update
  Dockerfile.server
  Dockerfile.client
  Dockerfile.monolith

docker-compose.yml
run.sh
README.md
```

All Python source code resides in `src/`.

---

# 4. Build & Run Instructions

Run all commands from the project root (where docker-compose.yml is located).

---

# A. Run Distributed Architecture

Clean previous containers:

```
docker compose down -v --remove-orphans
```

Start distributed services:

```
docker compose --profile distributed up -d
```

Run client:

```
docker compose run --rm client
```

If you exit the client and want to reconnect:

```
docker compose run --rm client
```

---

# B. Run Monolithic Architecture (Performance Comparison)

Clean previous containers:

```
docker compose down -v --remove-orphans
```

Start monolith:

```
docker compose --profile monolith up -d
```

Run client:

```
docker compose run --rm client
```

If you exit the client and want to reconnect:

```
docker compose run --rm client
```

---

# IMPORTANT

You must always run:

```
docker compose down -v --remove-orphans
```

before switching between distributed and monolith modes.

Do NOT run both architectures simultaneously.

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

Sensors:
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
```
sensor voltage
```

alerts  
Displays all currently active alerts.

quit  
Exits the client.

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

# 7. Performance Comparison

The monolithic architecture is used to measure performance differences.

Expected characteristics:

Distributed Architecture:
- Higher modularity
- Network overhead between services
- Better separation of concerns

Monolithic Architecture:
- Lower latency
- Higher throughput
- Reduced RPC overhead

This comparison demonstrates architectural trade-offs between modularity and performance efficiency.

---

# 8. Troubleshooting

If you receive container name conflicts:

```
docker compose down -v --remove-orphans
docker rm -f server 2>/dev/null
```

If client does not accept input:
Always use:
```
docker compose run --rm client
```

Do NOT use:
```
docker attach client
```

Check running containers:
```
docker ps
```

---

# 9. Quick Command Summary

Distributed:

```
docker compose down -v --remove-orphans
docker compose --profile distributed up -d
docker compose run --rm client
```

Monolith:

```
docker compose down -v --remove-orphans
docker compose --profile monolith up -d
docker compose run --rm client
```

Stop everything:

```
docker compose down -v --remove-orphans
```