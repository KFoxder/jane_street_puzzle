from PIL import Image, ImageDraw, ImageFont
import numpy as np


# Load the provided grid image
img_path = './matrix.png'
grid_img = Image.open(img_path)

# Create a draw object to edit the image
draw = ImageDraw.Draw(grid_img)
font = ImageFont.load_default(size=24)

# Since PIL's default font does not support resizing directly, let's specify a larger font size directly.
# Typically, default font size is around 10 or 12, let's increase it significantly.
# font = ImageFont.truetype("arial", size=24)  # Using a common font with increased size

# Define the matrix of numbers
numbers = [
    [1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4],
    [1, 3, 3, 3, 2, "X", 3, 4, 4, 4, "X"],
    [1, 3, 3, 1, "X", 7, 3, 4, 4, 4, 9],
    [1, 3, 3, "X", 1, 0, 0, 4, 1, 1, "X"],
    [1, 3, "X", 1, 4, 4, "X", 4, 1, 8, 1],
    [1, 4, 4, 4, "X", 4, 4, 4, 8, 8, 9],
    [7, 4, 4, 4, 4, "X", 7, 4, 8, 8, 8],
    [7, 7, 1, 4, 1, 7, 7, "X", 9, 8, 9],
    [7, 7, 1, 1, 1, 7, 7, 9, 9, 9, 9],
    ["X", 1, 1, 4, 4, "X", 7, 9, 9, 9, 2],
    [4, 4, 4, 4, 4, 3, "X", 3, 9, 9, 2]
]

# Dimensions for cell
cell_width = grid_img.width // 11
cell_height = grid_img.height // 11

def textsize(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height

# Place numbers in the grid
for i, row in enumerate(numbers):
    for j, num in enumerate(row):
        text = str(num)
        text_width, text_height = textsize(text, font=font)
        x = j * cell_width + (cell_width - text_width) / 2
        y = i * cell_height + (cell_height - text_height) / 2
        draw.text((x, y), text, fill="black", font=font)

# Save the edited image
edited_img_path = './numbered_matrix.png'
grid_img.save(edited_img_path)
edited_img_path