import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
from First_org import create_visual_vocabulary, create_bovw

def load_and_preprocess_images(image_dir, target_size=(300, 300)):
    """
    Load and preprocess images from a directory
    
    Parameters:
    - image_dir: Directory containing images
    - target_size: Size to resize images to
    
    Returns:
    - List of preprocessed images as numpy arrays
    """
    images = []
    image_paths = []
    
    for filename in os.listdir(image_dir):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            img_path = os.path.join(image_dir, filename)
            image_paths.append(img_path)
            
            # Load and convert to grayscale
            img = Image.open(img_path).convert('L')
            
            # Resize to target size
            img = img.resize(target_size)
            
            # Convert to numpy array
            img_array = np.array(img)
            
            images.append(img_array)
    
    return images, image_paths

def visualize_patches(image, patch_dim):
    """Visualize image patches"""
    plt.figure(figsize=(10, 10))
    
    # Original image
    plt.subplot(1, 2, 1)
    plt.imshow(image, cmap='gray')
    plt.title('Original Image')
    
    # Image with patch grid
    plt.subplot(1, 2, 2)
    plt.imshow(image, cmap='gray')
    plt.title(f'Patches (size: {patch_dim}x{patch_dim})')
    
    # Draw grid lines
    for i in range(0, image.shape[0], patch_dim):
        plt.axhline(i, color='r', linestyle='-', linewidth=1)
    for j in range(0, image.shape[1], patch_dim):
        plt.axvline(j, color='r', linestyle='-', linewidth=1)
    
    plt.tight_layout()
    plt.savefig('patch_visualization.png')
    plt.close()

def visualize_bovw(bovw_vectors, image_paths):
    """Visualize BoVW representations"""
    plt.figure(figsize=(15, 5))
    
    for i, (bovw, img_path) in enumerate(zip(bovw_vectors, image_paths)):
        # Display image
        plt.subplot(2, len(bovw_vectors), i+1)
        img = Image.open(img_path).convert('L')
        plt.imshow(img, cmap='gray')
        plt.title(f'Image {i+1}')
        plt.axis('off')
        
        # Display BoVW histogram
        plt.subplot(2, len(bovw_vectors), i+1+len(bovw_vectors))
        plt.bar(range(len(bovw)), bovw)
        plt.title(f'BoVW Histogram {i+1}')
        plt.xlabel('Visual Word Index')
        plt.ylabel('Frequency')
    
    plt.tight_layout()
    plt.savefig('bovw_visualization.png')
    plt.close()

def main():
    # Parameters
    image_dir = '../test_images'
    patch_dim = 20  # Size of patches (visual words)
    
    # Load and preprocess images
    images, image_paths = load_and_preprocess_images(image_dir)
    
    if not images:
        print("No images found in the directory!")
        return
    
    print(f"Loaded {len(images)} images")
    
    # Visualize patches for the first image
    visualize_patches(images[0], patch_dim)
    
    # Create visual vocabulary from all images
    visual_vocab = create_visual_vocabulary(images, patch_dim)
    print(f"Created visual vocabulary with {len(visual_vocab)} visual words")
    
    # Create BoVW for each image
    bovw_vectors = []
    for i, image in enumerate(images):
        bovw = create_bovw(image, visual_vocab, patch_dim)
        bovw_vectors.append(bovw)
        print(f"Created BoVW for image {i+1} with shape {bovw.shape}")
    
    # Visualize BoVW representations
    visualize_bovw(bovw_vectors, image_paths)
    
    # Calculate similarity between images using BoVW
    print("\nSimilarity between images (cosine similarity):")
    for i in range(len(bovw_vectors)):
        for j in range(i+1, len(bovw_vectors)):
            # Normalize vectors
            norm_i = bovw_vectors[i] / np.linalg.norm(bovw_vectors[i])
            norm_j = bovw_vectors[j] / np.linalg.norm(bovw_vectors[j])
            
            # Calculate cosine similarity
            similarity = np.dot(norm_i, norm_j)
            print(f"Similarity between image {i+1} and image {j+1}: {similarity:.4f}")

if __name__ == "__main__":
    main() 