from typing import Tuple
from PIL import Image, ImageDraw
from colour import Color
import discord
import threading
from threading import Lock

# Define the canvas size
canvas_width = 800
canvas_height = 800

# Create a blank canvas
# This is cached in memory, so it isnt saved on bot restart
canvas = Image.new("RGB", (canvas_width, canvas_height), color="white")

# Mutex lock so the canvas doesn't get all weird with async requests
canvas_mutex: Lock = threading.Lock()

def draw_line_on_image(
    color: str = "black", 
    direction: str = "right", 
    length: float = 0, 
    start: Tuple[int, int] = (canvas_height//2, canvas_width//2)) -> Tuple[int, int]:
    """Draw a line on the image and return the end point of the line."""
    
    width, height = canvas_width, canvas_height

    # Adjust the length if it exceeds the image size
    if length > width or length > height:
        length = min(width, height)

    # Create a Color object from the specified color
    color_obj = Color(color)
    # Convert the color to RGB values
    rgb_color = tuple(int(c * 255) for c in color_obj.rgb)

    start_x, start_y = start

    # Define the map for direction cases
    direction_map = {
        "up": lambda: (start_x, max(start_y - length, 0)),
        "down": lambda: (start_x, min(start_y + length, height)),
        "left": lambda: (max(start_x - length, 0), start_y),
        "right": lambda: (min(start_x + length, width), start_y)
    }

    # Calculate the end point based on the direction and length
    end_x, end_y = direction_map[direction]()

    # Draw the line on the image
    canvas_mutex.acquire()
    try:
        draw = ImageDraw.Draw(canvas)
        draw.line([(start_x, start_y), (end_x, end_y)], fill=rgb_color, width=5)
    finally:
        canvas_mutex.release()

    return (end_x, end_y)


async def create_image_file(image: Image.Image) -> discord.File:
    # Save the image to a temporary file
    temp_filename = "drawn_image.png"
    image.save(temp_filename)

    # Create a discord.File from the temporary file
    image_file = discord.File(temp_filename, filename="drawn_image.png")

    return image_file


async def get_discord_embed() -> Tuple[discord.Embed, discord.File]:
    file = await create_image_file(canvas)
    embed = discord.Embed()
    embed.set_image(url="attachment://drawn_image.png")
    return (embed, file)
