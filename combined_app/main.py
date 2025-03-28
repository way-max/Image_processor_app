from fastapi import FastAPI
from routers import image_processing

app = FastAPI(title="Image Processing API")

# Include routers
app.include_router(image_processing.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Image Processing API!"}
