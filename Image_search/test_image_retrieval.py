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
    filenames = []
    
    for filename in os.listdir(image_dir):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            img_path = os.path.join(image_dir, filename)
            image_paths.append(img_path)
            filenames.append(filename)
            
            # Load and convert to grayscale
            img = Image.open(img_path).convert('L')
            
            # Resize to target size
            img = img.resize(target_size)
            
            # Convert to numpy array
            img_array = np.array(img)
            
            images.append(img_array)
    
    return images, image_paths, filenames

def retrieve_similar_images(query_bovw, database_bovws, filenames, top_k=3):
    """
    Retrieve the most similar images to the query image
    
    Parameters:
    - query_bovw: BoVW of the query image
    - database_bovws: List of BoVWs for all images in the database
    - filenames: List of filenames corresponding to database_bovws
    - top_k: Number of most similar images to retrieve
    
    Returns:
    - List of (filename, similarity) tuples for the top_k most similar images
    """
    similarities = []
    
    # Normalize query vector
    query_norm = query_bovw / np.linalg.norm(query_bovw)
    
    # Calculate similarity with each database image
    for i, db_bovw in enumerate(database_bovws):
        # Normalize database vector
        db_norm = db_bovw / np.linalg.norm(db_bovw)
        
        # Calculate cosine similarity
        similarity = np.dot(query_norm, db_norm)
        similarities.append((filenames[i], similarity))
    
    # Sort by similarity (descending)
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    # Return top_k most similar images
    return similarities[:top_k]

def visualize_retrieval_results(query_image_path, results, image_dir):
    """
    Visualize the query image and the retrieved images
    
    Parameters:
    - query_image_path: Path to the query image
    - results: List of (filename, similarity) tuples for the retrieved images
    - image_dir: Directory containing the images
    """
    plt.figure(figsize=(15, 8))
    
    # Display query image
    plt.subplot(1, len(results) + 1, 1)
    query_img = Image.open(query_image_path).convert('L')
    plt.imshow(query_img, cmap='gray')
    plt.title('Query Image')
    plt.axis('off')
    
    # Display retrieved images
    for i, (filename, similarity) in enumerate(results):
        plt.subplot(1, len(results) + 1, i + 2)
        img_path = os.path.join(image_dir, filename)
        img = Image.open(img_path).convert('L')
        plt.imshow(img, cmap='gray')
        plt.title(f'Similarity: {similarity:.4f}')
        plt.axis('off')
    
    plt.tight_layout()
    plt.savefig('retrieval_results.png')
    plt.close()

def main():
    # Parameters
    image_dir = '../test_images'
    patch_dim = 20  # Size of patches (visual words)
    query_image_index = 3  # Index of the image to use as query (changed from 2 to 3)
    
    # Load and preprocess images
    images, image_paths, filenames = load_and_preprocess_images(image_dir)
    
    if not images:
        print("No images found in the directory!")
        return
    
    print(f"Loaded {len(images)} images")
    
    # Create visual vocabulary from all images
    visual_vocab = create_visual_vocabulary(images, patch_dim)
    print(f"Created visual vocabulary with {len(visual_vocab)} visual words")
    
    # Create BoVW for each image
    bovw_vectors = []
    for i, image in enumerate(images):
        bovw = create_bovw(image, visual_vocab, patch_dim)
        bovw_vectors.append(bovw)
        print(f"Created BoVW for image {i+1} with shape {bovw.shape}")
    
    # Select query image
    query_image = images[query_image_index]
    query_image_path = image_paths[query_image_index]
    query_bovw = bovw_vectors[query_image_index]
    
    print(f"\nUsing image {query_image_index + 1} as query")
    
    # Retrieve similar images
    results = retrieve_similar_images(query_bovw, bovw_vectors, filenames)
    
    print("\nRetrieval results:")
    for filename, similarity in results:
        print(f"Image: {filename}, Similarity: {similarity:.4f}")
    
    # Visualize retrieval results
    visualize_retrieval_results(query_image_path, results, image_dir)

if __name__ == "__main__":
    main() 