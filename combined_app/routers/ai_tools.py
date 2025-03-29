from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import json
import traceback
import random
import ast
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

# Create a router with the "Logo Maker with AI" tag
router = APIRouter(tags=["Logo Maker with AI"])

# Request model for generating logos
class LogoPrompt(BaseModel):
    prompt: str  # Prompt for generating the color palette

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
                        "[{{'color': 'RGB', 'country': 'name'}}]. No question, no comments requested, just the Python "
                        "list of colors that match the country flag color "
                        "You must check how many colors are there in the country flag and return the "
                        "colors according to how they are positioned in the country flag. You must treat every request as logo not flag or image even you are asked to generate  image just return the colors. There must be no quation, explanation only list. Even a country name is provided, return the colors that belongs to the country flag"
                    )
                }
            ]
        )

        # Extract the response and convert to JSON
        response_content = completion.choices[0].message.content
        # Replace single quotes with double quotes
        valid_json_data = response_content.replace("'", '"')
        # Load JSON
        parsed_data = json.loads(valid_json_data)
        return parsed_data
    except Exception as e:
        # Log the error and raise an HTTPException
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Error occurred while generating the palette.")



# Define a helper function to implement retry logic
async def retry_logic(func, *args, retries=4, delay=2, **kwargs):
    last_exception = None
    for attempt in range(retries):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            last_exception = e
            if attempt < retries - 1:
                # Wait for a while before retrying
                time.sleep(delay)
            else:
                # If retry attempts are exhausted, raise the last exception
                raise last_exception

# Endpoint to generate a logo with retry logic
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
        # Call the retry_logic function to handle retries
        palette_response = await retry_logic(generate_palette, request.prompt)

        country = palette_response[0]["country"]  # extract the country name

        # Validate the response from OpenAI
        if not palette_response:
            raise HTTPException(status_code=500, detail="Empty response from OpenAI.")
        if not isinstance(palette_response, list):
            raise HTTPException(status_code=400, detail="Invalid palette format.")

        # Create an image canvas
        img_width, img_height = 500, 300  # Dimensions suitable for flag
        img = Image.new("RGB", (img_width, img_height))  # Blank RGB image
        draw = ImageDraw.Draw(img)

        # Divide the canvas into horizontal stripes for each color in the palette
        color_stripes = len(palette_response)
        stripe_height = img_height // color_stripes

        for i, color_data in enumerate(palette_response):
            color_str = color_data.get("color")  # Extract RGB string
            if not color_str:
                continue

            # Parse RGB values
            rgb_values = tuple(map(int, color_str.replace("RGB(", "").replace(")", "").split(", ")))
            stripe_start_y = i * stripe_height
            stripe_end_y = (i + 1) * stripe_height if i + 1 < color_stripes else img_height
            draw.rectangle([0, stripe_start_y, img_width, stripe_end_y], fill=rgb_values)

        # Load a custom font and set the size (you can replace the font path with your own .ttf file)
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Use a bold font
        font_size = 60  # Set a larger font size
        font = ImageFont.truetype(font_path, font_size)

        # Add the logo name text centered on the image
        text = country  # Set the country name on the logo

        # Calculate text size and position
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        position = ((img.width - text_width) // 2, (img.height - text_height) // 2)
        draw.text(position, text, fill="gray", font=font)  # Draw text on the image

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
