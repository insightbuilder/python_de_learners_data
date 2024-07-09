# script is described by gpt4o model

import drawsvg as draw

# Initialize the drawing canvas
d = draw.Drawing(800, 1000, origin='center', displayInline=False)

# Function to add a character with an icon, name, and role
def add_character(x, y, name, role, image_url):
    # Draw a circle for the character's icon
    d.append(draw.Circle(x, y, 50, fill='white', stroke='black', stroke_width=2))
    # Add character image
    d.append(draw.Image(x-40, y-40, 80, 80, image_url))
    # Add character name below the icon
    d.append(draw.Text(name, 12, x, y-60, center=True))
    # Add character role below the name
    d.append(draw.Text(role, 10, x, y-75, center=True, fill='gray'))

# Example character data
characters = [
    {"name": "YURI ISMAYLOV", "role": "Herald", "image_url": "path/to/image1.png"},
    {"name": "VECNA", "role": "Shadow", "image_url": "path/to/image2.png"},
    # Add more characters as needed...
]

# Position and add each character to the canvas
start_x, start_y = -200, 400
for i, char in enumerate(characters):
    x = start_x + (i % 5) * 100
    y = start_y - (i // 5) * 150
    add_character(x, y, char["name"], char["role"], char["image_url"])

# Save the drawing to an SVG file
d.save_svg('infographic.svg')

# Display the drawing
d.rasterize()  # Open in viewer