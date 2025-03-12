import numpy as np
from PIL import Image, ImageDraw
import os

def create_directory(directory):
    """Create directory if it doesn't exist"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def create_gradient_image(size=(300, 300), direction='horizontal'):
    """Create a gradient image"""
    if direction == 'horizontal':
        gradient = np.linspace(0, 255, size[0], dtype=np.uint8)
        gradient = np.tile(gradient, (size[1], 1))
    else:  # vertical
        gradient = np.linspace(0, 255, size[1], dtype=np.uint8)
        gradient = np.tile(gradient.reshape(-1, 1), (1, size[0]))
    
    return Image.fromarray(gradient)

def create_circle_image(size=(300, 300), radius=100):
    """Create an image with a circle"""
    img = Image.new('L', size, color=50)
    draw = ImageDraw.Draw(img)
    center = (size[0] // 2, size[1] // 2)
    draw.ellipse((center[0] - radius, center[1] - radius, 
                  center[0] + radius, center[1] + radius), fill=200)
    return img

def create_checkerboard(size=(300, 300), box_size=50):
    """Create a checkerboard pattern"""
    img = Image.new('L', size, color=0)
    draw = ImageDraw.Draw(img)
    
    for i in range(0, size[0], box_size * 2):
        for j in range(0, size[1], box_size * 2):
            draw.rectangle((i, j, i + box_size, j + box_size), fill=255)
            draw.rectangle((i + box_size, j + box_size, 
                           i + box_size * 2, j + box_size * 2), fill=255)
    
    return img

def create_random_shapes(size=(300, 300), num_shapes=5):
    """Create an image with random shapes"""
    img = Image.new('L', size, color=50)
    draw = ImageDraw.Draw(img)
    
    for _ in range(num_shapes):
        shape_type = np.random.choice(['rectangle', 'ellipse'])
        x1 = np.random.randint(0, size[0] - 50)
        y1 = np.random.randint(0, size[1] - 50)
        x2 = x1 + np.random.randint(30, 100)
        y2 = y1 + np.random.randint(30, 100)
        
        fill_value = np.random.randint(100, 250)
        
        if shape_type == 'rectangle':
            draw.rectangle((x1, y1, x2, y2), fill=fill_value)
        else:
            draw.ellipse((x1, y1, x2, y2), fill=fill_value)
    
    return img

def main():
    # Create test images directory
    output_dir = '../test_images'
    create_directory(output_dir)
    
    # Create different test images
    images = [
        ('horizontal_gradient.jpg', create_gradient_image(direction='horizontal')),
        ('vertical_gradient.jpg', create_gradient_image(direction='vertical')),
        ('circle.jpg', create_circle_image()),
        ('checkerboard.jpg', create_checkerboard()),
        ('random_shapes.jpg', create_random_shapes())
    ]
    
    # Save images
    for filename, img in images:
        img_path = os.path.join(output_dir, filename)
        img.save(img_path)
        print(f"Created {img_path}")

if __name__ == "__main__":
    main() 