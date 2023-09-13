#!/usr/bin/env python

from PIL import ImageFile, Image
import io
import base64
import qrcode

ImageFile.LOAD_TRUNCATED_IMAGES = False
# Your base64-encoded image string
#base64_string = "data:image/png;base64,iVBORw0KG...[the rest of your base64 string]"
base64_string = input("Provide the base64 string: ") 
# Remove the "data:image/png;base64," prefix to get just the base64 data
base64_data = base64_string.split(",")[1]

print(len(base64_data))
# Decode the base64 data
image_data = base64.b64decode(base64_data)
#print(image_data[:100])
# Create an image object
image = Image.open(io.BytesIO(image_data))

# Save the image as a PNG file
image.save("output.png", "PNG")

