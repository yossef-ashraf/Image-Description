from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import mysql.connector
from PIL import Image
import os

class ImageSimilarityFinder:
    def __init__(self, db_config):
        # Set up ResNet50 model for feature extraction
        self.model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
        
        # Connect to the database
        self.db = mysql.connector.connect(**db_config)
        self.cursor = self.db.cursor()

    def extract_features(self, img_path):
        # Load and prepare the image
        img = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        
        # Extract features
        features = self.model.predict(x)
        return features.flatten()

    def find_similar_images(self, query_image_path, threshold=0.85):
        # Extract features of the query image
        query_features = self.extract_features(query_image_path)
        
        # Search in the database
        similar_images = []
        self.cursor.execute("SELECT id, path FROM images")
        
        for image_id, db_image_path in self.cursor:
            if os.path.exists(db_image_path):
                # Extract features of the database image
                db_features = self.extract_features(db_image_path)
                
                # Calculate similarity
                similarity = cosine_similarity(
                    query_features.reshape(1, -1),
                    db_features.reshape(1, -1)
                )[0][0]
                
                if similarity >= threshold:
                    similar_images.append({
                        'id': image_id,
                        'path': db_image_path,
                        'similarity': similarity
                    })
        
        # Sort results by similarity score
        similar_images.sort(key=lambda x: x['similarity'], reverse=True)
        return similar_images

    def close(self):
        self.cursor.close()
        self.db.close()

# Example usage
db_config = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'your_database'
}

def search_similar_images(query_image_path):
    finder = ImageSimilarityFinder(db_config)
    try:
        similar_images = finder.find_similar_images(query_image_path)
        return similar_images
    finally:
        finder.close()