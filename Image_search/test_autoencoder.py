import torch
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import torchvision.transforms as transforms
from second import AutoEncoder

def load_and_preprocess_images(image_dir, target_size=(224, 224)):
    """
    Load and preprocess images from a directory for the autoencoder
    
    Parameters:
    - image_dir: Directory containing images
    - target_size: Size to resize images to
    
    Returns:
    - List of preprocessed images as PyTorch tensors
    """
    images = []
    image_paths = []
    filenames = []
    
    # Define transformations
    transform = transforms.Compose([
        transforms.Resize(target_size),
        transforms.ToTensor()
    ])
    
    for filename in os.listdir(image_dir):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            img_path = os.path.join(image_dir, filename)
            image_paths.append(img_path)
            filenames.append(filename)
            
            # Load and convert to RGB
            img = Image.open(img_path).convert('RGB')
            
            # Apply transformations
            img_tensor = transform(img)
            
            images.append(img_tensor)
    
    return images, image_paths, filenames

def compute_embedding_similarity(embed1, embed2):
    """
    Compute cosine similarity between two embeddings
    """
    # Flatten embeddings
    embed1_flat = embed1.view(embed1.size(0), -1)
    embed2_flat = embed2.view(embed2.size(0), -1)
    
    # Normalize
    embed1_norm = embed1_flat / torch.norm(embed1_flat, dim=1, keepdim=True)
    embed2_norm = embed2_flat / torch.norm(embed2_flat, dim=1, keepdim=True)
    
    # Compute similarity
    similarity = torch.sum(embed1_norm * embed2_norm, dim=1)
    
    return similarity.item()

def visualize_reconstructions(model, images, image_paths):
    """
    Visualize original images and their reconstructions
    """
    plt.figure(figsize=(15, 5))
    
    for i, (img_tensor, img_path) in enumerate(zip(images[:3], image_paths[:3])):
        # Get original image
        original_img = img_tensor.permute(1, 2, 0).numpy()
        
        # Get reconstruction
        with torch.no_grad():
            reconstruction = model(img_tensor.unsqueeze(0)).squeeze(0)
        
        recon_img = reconstruction.permute(1, 2, 0).numpy()
        
        # Display original
        plt.subplot(2, 3, i+1)
        plt.imshow(original_img)
        plt.title(f'Original {i+1}')
        plt.axis('off')
        
        # Display reconstruction
        plt.subplot(2, 3, i+4)
        plt.imshow(recon_img)
        plt.title(f'Reconstruction {i+1}')
        plt.axis('off')
    
    plt.tight_layout()
    plt.savefig('autoencoder_reconstructions.png')
    plt.close()

def retrieve_similar_images(query_embedding, embeddings, filenames, top_k=3):
    """
    Retrieve the most similar images to the query image based on embedding similarity
    """
    similarities = []
    
    for i, embedding in enumerate(embeddings):
        similarity = compute_embedding_similarity(query_embedding, embedding)
        similarities.append((filenames[i], similarity))
    
    # Sort by similarity (descending)
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    # Return top_k most similar images
    return similarities[:top_k]

def visualize_retrieval_results(query_image_path, results, image_dir):
    """
    Visualize the query image and the retrieved images
    """
    plt.figure(figsize=(15, 8))
    
    # Display query image
    plt.subplot(1, len(results) + 1, 1)
    query_img = Image.open(query_image_path).convert('RGB')
    plt.imshow(query_img)
    plt.title('Query Image')
    plt.axis('off')
    
    # Display retrieved images
    for i, (filename, similarity) in enumerate(results):
        plt.subplot(1, len(results) + 1, i + 2)
        img_path = os.path.join(image_dir, filename)
        img = Image.open(img_path).convert('RGB')
        plt.imshow(img)
        plt.title(f'Similarity: {similarity:.4f}')
        plt.axis('off')
    
    plt.tight_layout()
    plt.savefig('autoencoder_retrieval_results.png')
    plt.close()

def main():
    # Parameters
    image_dir = '../test_images'
    input_channels = 3  # RGB images
    hidden_dim = 32
    embed_dim = 16
    query_image_index = 2
    
    # Load and preprocess images
    images, image_paths, filenames = load_and_preprocess_images(image_dir)
    
    if not images:
        print("No images found in the directory!")
        return
    
    print(f"Loaded {len(images)} images")
    
    # Create and initialize the autoencoder
    model = AutoEncoder(input_channels, hidden_dim, embed_dim)
    print("Created autoencoder model")
    
    # Train the autoencoder (simplified training for testing)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = torch.nn.MSELoss()
    
    print("Training autoencoder for 10 epochs...")
    for epoch in range(10):
        total_loss = 0
        for img in images:
            # Forward pass
            img_batch = img.unsqueeze(0)  # Add batch dimension
            output = model(img_batch)
            
            # Compute loss
            loss = criterion(output, img_batch)
            
            # Backward pass and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
        
        print(f"Epoch {epoch+1}/10, Loss: {total_loss/len(images):.6f}")
    
    # Visualize reconstructions
    visualize_reconstructions(model, images, image_paths)
    
    # Compute embeddings for all images
    embeddings = []
    for img in images:
        with torch.no_grad():
            embedding = model.encode(img.unsqueeze(0))
            embeddings.append(embedding)
    
    # Select query image
    query_image = images[query_image_index]
    query_image_path = image_paths[query_image_index]
    query_embedding = embeddings[query_image_index]
    
    print(f"\nUsing image {query_image_index + 1} as query")
    
    # Retrieve similar images
    results = retrieve_similar_images(query_embedding, embeddings, filenames)
    
    print("\nRetrieval results:")
    for filename, similarity in results:
        print(f"Image: {filename}, Similarity: {similarity:.4f}")
    
    # Visualize retrieval results
    visualize_retrieval_results(query_image_path, results, image_dir)

if __name__ == "__main__":
    main() 