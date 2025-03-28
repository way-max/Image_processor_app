# Image Processor App: Logo Maker, Notifications, and Image Processing API

## Overview
This is a FastAPI application combining three distinct features:
1. **Logo Maker**: Generate and customize logos for various purposes.
2. **Notification System**: Manage and send notifications to users.
3. **Image Processing API**: Resize and process images with progress tracking.

The application is designed with scalability, performance, and monitoring in mind, utilizing **Datadog** for tracing and **ddtrace** for application monitoring.

---

## Features

### 1. Logo Maker
- Generate logos based on user-provided inputs.
- Customize logos with text, colors, and styles.

### 2. Notification System
- Send real-time notifications to users.
- Track notification history and status.

### 3. Image Processing API
- Upload images for resizing.
- Track image processing progress using Server-Sent Events (SSE).

---

## Technologies Used
- **Framework**: FastAPI
- **Languages**: Python for backend and javascript and html for front-end
- **Monitoring**: Datadog (`ddtrace`)
- **Image Processing**: Pillow
- **Async Programming**: asyncio
- **Streaming**: SSE (Server-Sent Events)

---

## Installation

1. Clone the repository:
   ```bash
   https://github.com/way-max/Image_processor_app
