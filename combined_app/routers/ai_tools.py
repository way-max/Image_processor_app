from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import json
import traceback
import random
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

# Create a router with the "Logo Maker with AI" tag
router = APIRouter(tags=["Logo Maker with AI"])

# Request model for generating logos
class LogoPrompt(BaseModel):
    prompt: str  # Prompt for generating the color palette
    country_name: str  # Name to display on the logo

# Function to generate a color palette using OpenAI
async def generate_palette(prompt: str):
    """
    Generates a list of colors based on the input prompt.

    Parameters:
        prompt (str): A description or theme for the logo's color palette.

    Returns:
        List[dict]: A list of dictionaries with color values in RGB format.
    """
    try:
        # Use OpenAI to create a palette based on the prompt
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"{prompt} Return only a list of the color palettes in the form of "
                        "[{{'color': 'RGB'}}]. No question, no comments requested, just the Python "
                        "list of colors that match the country. There must be at least three colors. "
                        "You must check how many colors are there in the country flag and return the "
                        "colors according to how they are positioned in the country flag."
                    )
                }
            ]
        )

        # Extract the response and convert to JSON
        response_content = completion.choices[0].message.content
        data_str = response_content.replace("'", '"')  # Fix quotes for JSON compatibility
        data = json.loads(data_str)  # Parse JSON into Python objects

        return data

    except Exception as e:
        # Log the error and raise an HTTPException
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Error occurred while generating the palette.")

# Endpoint to generate a logo
@router.post("/generate-logo/")
async def generate_logo(request: LogoPrompt):
    """
    Generates a country flag logo based on the provided prompt and country name.

    Request Body:
        prompt (str): A description or theme for the logo's color palette.
        country_name (str): The country name to display on the logo.

    Returns:
        StreamingResponse: The generated logo image as a PNG file.
    """
    try:
        # Generate the color palette using OpenAI
        palette_response = await generate_palette(request.prompt)

        # Validate the response from OpenAI
        if not palette_response:
            raise HTTPException(status_code=500, detail="Empty response from OpenAI.")
        if not isinstance(palette_response, list):
            raise HTTPException(status_code=400, detail="Invalid palette format.")

        # Create an image canvas
        img_width, img_height = 500, 500
        img = Image.new("RGB", (img_width, img_height))  # Blank RGB image
        draw = ImageDraw.Draw(img)

        # Divide the canvas into blocks for each color in the palette
        color_blocks = len(palette_response)
        block_width = img_width // color_blocks

        for i, color_data in enumerate(palette_response):
            color_str = color_data.get("color")  # Extract RGB string
            if not color_str:
                continue

            # Parse RGB values
            rgb_values = tuple(map(int, color_str.replace("RGB(", "").replace(")", "").split(", ")))
            block_start_x = i * block_width
            block_end_x = (i + 1) * block_width if i + 1 < color_blocks else img_width
            draw.rectangle([block_start_x, 0, block_end_x, img_height], fill=rgb_values)

        # Add the logo name text centered on the image
        font = ImageFont.load_default()  # Use default font
        text = request.country_name

        # Calculate text size and position
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        position = ((img.width - text_width) // 2, (img.height - text_height) // 2)

        draw.text(position, text, fill="black", font=font)  # Draw text on the image

        # Save the image to a BytesIO stream
        img_io = BytesIO()
        img.save(img_io, "PNG")
        img_io.seek(0)

        # Return the image as a streaming response
        return StreamingResponse(img_io, media_type="image/png")

    except HTTPException as e:
        # Handle known exceptions
        raise e
    except Exception as e:
        # Log unexpected exceptions and raise an HTTP error
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
