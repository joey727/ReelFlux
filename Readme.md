# REELFLUX: Video-to-MP3 Microservice Architecture

This project is a microservice-based system that takes a **video file as input** and returns the **audio extracted as an MP3**. The system is containerized using Docker and deployed using **Kubernetes (Minikube)**.

---

## Architecture Overview

The system is composed of the following services:

| Service         | Description |
|----------------|-------------|
| **Gateway**     | Accepts incoming video uploads and routes requests to appropriate services. |
| **Video Service** | Handles storage of uploaded video files (GridFS + MongoDB). |
| **Converter Service** | Converts video to MP3 using tools like FFmpeg. |
| **Notification Service** | Sends push notifications to users upon file conversion completion. |
| **Auth Service** | Basic HTTP and JWT authentication for users. |
| **MongoDB**     | Stores video and MP3 files using GridFS. |
| **Rabbit MQ**   | Handles message queuing to appropraite services.  |

All services communicate via internal Kubernetes networking.

---

## How It Works

1. **Client uploads a video** to the `gateway`.
2. **Gateway** authenticates the user and forwards the video to the `converter service`.
3. The **Converter service** retrieves the video, extracts audio, and stores the MP3 in the `mp3 database(GridFS)`.
4. The **client receives a download id** to the converted MP3.
5. Client can now use the download id to **download the mp3 file**

---

## Tech Used

- **Python + Flask** for microservices
- **MongoDB + GridFS** for file storage
- **FFmpeg** for video-to-audio conversion
- **Docker** for containerization
- **Kubernetes (Minikube)** for orchestration

---

##  Deployment (via Minikube)

1. Start Minikube:
   ```bash
   minikube start
2. Docker build services:
    ```bash
    docker build ...**appropraite service** 
3. Alternatively can pull images i already built but it's better make changes (which best suit)
    and rebuild 
4. Apply kubernetes configurations
    ```bash
    kubectl apply -f manifests


#### Contributions and Improvements are welcome 