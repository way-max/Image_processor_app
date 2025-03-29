from fastapi import APIRouter, UploadFile, HTTPException, FastAPI, Request
import httpx
from fastapi.responses import StreamingResponse
from ddtrace import tracer
import asyncio
import io
import os
from PIL import Image
import shutil

app = FastAPI(title="Image Uploader, Resizer with Progress")
router = APIRouter(prefix="/api", tags=["Image Uploader, Resizer and Progress Monitor"])

async def resize_image(file: UploadFile, width: int, height: int):
    """
    Resizes the uploaded image to the specified width and height.

    Args:
        file: The image file to be resized.
        width: The target width for resizing.
        height: The target height for resizing.

    Returns:
        A StreamingResponse with the resized image.
    """
    try:
        image = Image.open(io.BytesIO(await file.read()))

        if image.mode == "RGBA":
            image = image.convert("RGB")

        resized_image = image.resize((width, height))

        output = io.BytesIO()
        resized_image.save(output, format="JPEG")
        output.seek(0)

        return StreamingResponse(output, media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {e}")


@router.post("/upload")
async def upload_image(file: UploadFile, client_id: str, width: int, height: int):
    """
    Uploads an image file, processes it by resizing, and returns the resized image.
    Tracks the upload progress and returns it through the SSE endpoint.

    Args:
        file: The image file to be uploaded and resized.
        client_id: Unique identifier for the client.
        width: The target width for resizing.
        height: The target height for resizing.

    Returns:
        A StreamingResponse containing the resized image.
    """
    with tracer.trace("upload_image") as span:
        if not file.content_type.startswith("image/"):
            span.set_tag("error", "Invalid file type")
            raise HTTPException(status_code=400, detail="Invalid file type. Only images are allowed.")

        file_data = await file.read()
        resized_image = await process_upload(file_data, client_id, width, height)
        span.set_tag("client_id", client_id)
        return StreamingResponse(resized_image, media_type="image/jpeg")


async def process_upload(file_data: bytes, client_id: str, width: int, height: int) -> io.BytesIO:
    """
    Simulates image processing, updates progress, and resizes the image.

    Args:
        file_data: The raw bytes of the image file.
        client_id: Unique identifier for the client.
        width: The target width for resizing.
        height: The target height for resizing.

    Returns:
        A BytesIO object containing the resized image.
    """
    try:
        total_steps = 10
        for step in range(1, total_steps + 1):
            await asyncio.sleep(0.5)
            upload_progress[client_id] = (step / total_steps) * 100

        image = Image.open(io.BytesIO(file_data))
        output_dir = "uploaded_images"
        os.makedirs(output_dir, exist_ok=True)
        file_path = f"{output_dir}/{client_id}_uploaded_image.png"
        image.save(file_path)

        upload_progress[client_id] = 100

        image = image.convert("RGB") if image.mode == "RGBA" else image
        resized_image = image.resize((width, height))

        output = io.BytesIO()
        resized_image.save(output, format="JPEG")
        output.seek(0)

        shutil.rmtree(output_dir, ignore_errors=True)

        return output
    except Exception as e:
        upload_progress[client_id] = -1
        raise HTTPException(status_code=500, detail=f"Error processing image: {e}")


@router.get("/progress/{client_id}")
async def progress(client_id: str):
    """
    Endpoint to get the progress of an image upload process.

    Args:
        client_id: Unique identifier for the client to track progress.

    Returns:
        A StreamingResponse containing the progress updates via SSE.
    """
    async def event_stream():
        while True:
            progress = upload_progress.get(client_id, 0)
            yield f"data: {progress}\n\n"
            await asyncio.sleep(0.5)
            if progress == 100 or progress == -1:
                break

    return StreamingResponse(event_stream(), media_type="text/event-stream")



async def video_streamer(url: str):
    # Stream video from the source URL
    async with httpx.AsyncClient() as client:
        response = await client.get(url, stream=True)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error fetching video")
        async for chunk in response.aiter_bytes(chunk_size=1024 * 1024):
            yield chunk

@router.get("/stream-video")
async def stream_video(request: Request, url: str):
    # Check if the URL parameter is provided
    if not url:
        raise HTTPException(status_code=400, detail="Video URL is required")

    # Stream the video
    return StreamingResponse(video_streamer(url), media_type="video/mp4")
