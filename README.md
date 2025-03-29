---

## 📞 **Contact**
- **Author**: James Akandu
- **Email**: zurumdev@gmail.com
- **GitHub**: [Your GitHub Profile](https://github.com/way-max)
- **linkedin**: [Your linkedin Profile](https://linkedin.com/in/zurum)

---


# **Image Processor App: Logo Maker, Notifications, and Image Processing API**

## 🚀 **Overview**
Welcome to the **Image Processor App**, a fast and scalable FastAPI-powered application that integrates three fantastic features:
1. **Logo Maker**: Create and customize logos tailored to your needs.
2. **Notification System**: Real-time notifications for seamless user engagement.
3. **Image Processing API**: Resize and process images with intuitive progress tracking.

Designed for performance and scalability, this app includes **Datadog** for advanced tracing and **ddtrace** for continuous monitoring to ensure everything runs smoothly.

---

## 🌟 **Features**

### 1. **Logo Maker**
- Generate stunning logos based on user-provided inputs.
- Customize logos with text, colors, and styles.
- Leverage powerful OpenAI APIs, **Pillow**, and **NumPy** to create flags for any country, giving you the ability to make logos that represent nations.
  
### 2. **Notification System**
- Send real-time notifications directly to users.
- Manage notification history and track status for better user engagement.
- Built with **Server-Sent Events (SSE)** for instantaneous updates, ensuring you never miss a beat.

### 3. **Image Processing API**
- Upload images and resize them quickly and easily.
- Track image processing progress in real time with SSE, so users know exactly when their image is ready.
  
---

## 🛠 **Technologies Used**
- **Framework**: FastAPI (the fastest web framework for building APIs with Python)
- **Languages**: Python for the backend, HTML & JavaScript for the frontend
- **Monitoring**: **Datadog** for tracing and app monitoring via `ddtrace`
- **Image Processing**: **Pillow** (for image manipulation) and **NumPy** (for array-based image operations)
- **Cloud Hosting**: Render for hosting, CI/CD integration with **GitHub Actions**
- **Async Programming**: **asyncio** for asynchronous operations, providing seamless experience
- **Streaming**: **SSE (Server-Sent Events)** for real-time updates and progress tracking

---

## 🚀 **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/way-max/Image_processor_app
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the FastAPI app:
   ```bash
   uvicorn app.main:app --reload
   ```

---

## 🔍 **Test the App**

### API Documentation:
Test all endpoints directly in your browser by visiting the interactive Swagger UI:
[API Docs](https://image-processor-app.onrender.com/docs)

**Note**: This app is hosted on Render's free plan, so the initial load may take up to 30 seconds.

### Front-End Experience:
Visit the live app and try it out! Get creative with logos and see image processing in action:
[Image Processor App Live](https://image-processor-app.onrender.com)

---

Enjoy creating logos, processing images, and sending notifications in real-time with ease!
