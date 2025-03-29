from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Mount the static directory for assets like JavaScript, CSS, and images
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the index.html at the root endpoint
@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html", "r") as file:
        return file.read()
