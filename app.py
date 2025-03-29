from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from ddtrace import patch_all, config
from ddtrace.contrib.asgi import TraceMiddleware
from combined_app.routers import image_processing, ai_tools

# Patch all libraries supported by ddtrace
patch_all()

# Datadog configuration
config.fastapi["service_name"] = "combined-application"
config.fastapi["env"] = "production"
config.fastapi["version"] = "1.0.0"

# Initialize FastAPI app
app = FastAPI(title="Combined Application")

# Add Datadog tracing middleware
app.add_middleware(TraceMiddleware)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(image_processing.router, prefix="/image_processing")
app.include_router(ai_tools.router, prefix="/ai_tools")

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Frontend router
frontend_router = APIRouter(tags=["Front-End"])

@frontend_router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def read_root():
    with open("static/index.html", "r") as file:
        return file.read()

app.include_router(frontend_router)


@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Welcome to the Combined App!"}
