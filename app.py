
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from combined_app.routers import image_processing
from combined_app.routers import ai_tools
from ddtrace import patch_all, config
from ddtrace.contrib.asgi import TraceMiddleware

# Patch all libraries supported by ddtrace
patch_all()

# Datadog configuration
config.fastapi["service_name"] = "combined-application"  # Set the service name here
config.fastapi["env"] = "production"  # Change to your environment (e.g., dev, staging, production)
config.fastapi["version"] = "1.0.0"

app = FastAPI(title="Combined Application")

# Add Datadog tracing middleware
app.add_middleware(TraceMiddleware)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust to restrict origins if needed
    allow_credentials=True,
    allow_methods=["*"],  # Specify allowed methods (GET, POST, etc.)
    allow_headers=["*"],  # Specify allowed headers
)

# Include routers
app.include_router(ai_tools.router, prefix="/image_processing")
app.include_router(image_processing.router, prefix="/image_processing")

@app.get("/")
async def root():
    return {"message": "Welcome to the Combined App!"}
