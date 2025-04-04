

## 📞 **Contact**  
- **Author**: James Akandu  
- **Email**: zurumdev@gmail.com  
- **GitHub**: [GitHub Profile](https://github.com/way-max)  
- **LinkedIn**: [LinkedIn Profile](https://linkedin.com/in/zurum)

---

# **Image Processor App: The Ultimate Logo Maker & Image Processor**

## 🚀 **Overview**  
Welcome to the **Image Processor App**—a high-performance, FastAPI-powered application built to transform your creative ideas into reality. Featuring three amazing tools, it’s designed for speed, scalability, and efficiency:

1. **Logo Maker**: Create stunning logos, customized to your unique vision.  
2. **Notification System**: Engage users instantly with real-time notifications.  
3. **Image Processing API**: Resize images efficiently, retaining quality with lightning-fast processing.

Whether you're designing logos, managing notifications, or processing images in real-time, this app has you covered with its seamless integration of **Datadog** for monitoring, **SSE (Server-Sent Events)** for live updates, and **ddtrace** for performance tracking. You’ve got the power of FastAPI at your fingertips!

---

## 🌟 **Key Features**  

### 1. **Logo Maker**  
- **Instant Logo Generation**: Automatically create beautiful logos based on your inputs.  
- **Customization**: Modify text, color schemes, and styles to suit your brand.  
- **Flag Creation**: Craft flags for any country using powerful OpenAI APIs and **Pillow** for image generation.

### 2. **Notification System**  
- **Real-Time Notifications**: Send notifications instantly to all users, ensuring they stay engaged.  
- **Notification History**: Keep track of sent notifications and monitor their status.  
- **Built with SSE**: Receive real-time updates without refreshing, so you’re always in the loop.

### 3. **Image Processing API**  
- **Super-Fast Image Resizing**: Upload and resize images without losing quality. Example, image of size 4MB can be reduced to 95% of its original size (e.g., 4mb to 40kB) in less than 4 seconds!  
- **Real-Time Progress**: Know exactly when your image is ready with live progress tracking powered by SSE.

---

## 🛠 **Technologies Used**  
- **Framework**: FastAPI (known for its blazing-fast performance in API development)  
- **Languages**: Python (Backend), HTML & JavaScript (Frontend)  
- **Real-Time Updates**: **SSE (Server-Sent Events)** for live notifications and progress tracking  
- **Monitoring & Performance**: **Datadog** & **ddtrace** for performance monitoring and tracing  
- **Image Processing**: **Pillow** for image manipulation, **NumPy** for efficient array-based image operations  
- **Cloud Hosting**: Render for deployment with CI/CD integration via **GitHub Actions**  
- **Async Programming**: **asyncio** ensures a responsive, non-blocking experience throughout the app  

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
Interact directly with the API and explore all available endpoints with our interactive Swagger UI:  
[API Docs](https://image-processor-app.onrender.com/docs)  

**Note**: Due to Render's free plan, the app may take up to 30 seconds for the initial load.

### Front-End Experience:  
Dive into the app and experience the magic of logo creation and real-time image processing:  
[Image Processor App Live](https://image-processor-app.onrender.com)  

---

Get ready to unlock your creativity with the **Image Processor App**—whether you’re designing, processing, or engaging, everything is fast, smooth, and real-time. Start exploring today!

