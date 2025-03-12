from PIL import Image, ImageDraw, ImageFont
import os

# Create 8 simple JPG images for testing
for i in range(1, 9):
    # Create a new image with white background
    img = Image.new('RGB', (300, 200), color=(255, 255, 255))
    
    # Get a drawing context
    draw = ImageDraw.Draw(img)
    
    # Draw a rectangle
    draw.rectangle([(20, 20), (280, 180)], outline=(0, 0, 0), width=2)
    
    # Add text
    draw.text((100, 90), f"Sconto {i}", fill=(0, 0, 0))
    
    # Save the image
    filename = f"sconto{i}.jpg"
    img.save(filename)
    print(f"Created {filename}")

print("All test images created successfully.") 