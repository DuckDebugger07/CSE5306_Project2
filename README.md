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
2. Monolithic Architecture (Single Container)

Both architectures expose the same gRPC interface to ensure functional equivalence while enabling performance comparison.

---

# 2. System Architecture

## Distributed Telemetry Flow

Sensors → Aggregation → Analysis → Update → Server → Client  

Command Flow:  
Client ↔ Server ↔ Update  

Each stage runs in its own Docker container.

---

## Monolithic Architecture

All telemetry generation and processing logic runs inside a single container.

This removes inter-container RPC overhead while preserving identical client behavior.

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

run_distributed.sh
run_monolith.sh

README.md
```

All Python source code resides in `src/`.

---

# 4. Running the System

Run all commands from the project root (where docker-compose.yml is located).

---

## 🔵 Run Distributed Architecture

```
./run_distributed.sh
```

This script will:

1. Stop and remove existing containers
2. Build distributed services
3. Start all distributed containers
4. Launch the client

---

## 🟣 Run Monolithic Architecture

```
./run_monolith.sh
```

This script will:

1. Stop and remove existing containers
2. Build the monolith container
3. Start the monolith
4. Launch the client

---

## 🔄 Switching Architectures

No manual cleanup is required.  
Each script automatically performs:

```
docker compose down -v --remove-orphans
```

before starting the selected architecture.

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

The monolithic architecture removes network serialization and RPC chaining overhead.

Expected trade-offs:

Distributed Architecture:
- Higher modularity
- Service isolation
- Increased RPC overhead

Monolithic Architecture:
- Lower latency
- Higher throughput
- Reduced architectural separation

---

# 8. Troubleshooting

If scripts are not executable:

```
chmod +x run_distributed.sh
chmod +x run_monolith.sh
```

Check running containers:

```
docker ps
```

Stop everything manually:

```
docker compose down -v --remove-orphans
```

---

# 9. Manual Commands (Optional)

Distributed:

```
docker compose --profile distributed up -d
docker compose run --rm client
```

Monolith:

```
docker compose --profile monolith up -d
docker compose run --rm client
```