import numpy as np
from PIL import Image
import random

class WasteClassifier:
    def __init__(self):
        self.classes = ['Biodegradable', 'Non-Biodegradable']
        # Color-based heuristics for demo purposes
        # Green/brown tones = biodegradable, other colors = non-biodegradable
        
    def preprocess_image(self, image_path):
        """Preprocess image for analysis"""
        img = Image.open(image_path).convert('RGB')
        img = img.resize((224, 224))
        img_array = np.array(img)
        return img_array
    
    def analyze_color_features(self, img_array):
        """Analyze color features to classify waste"""
        # Calculate average RGB values
        avg_r = np.mean(img_array[:, :, 0])
        avg_g = np.mean(img_array[:, :, 1])
        avg_b = np.mean(img_array[:, :, 2])
        
        # Calculate color ratios
        total = avg_r + avg_g + avg_b
        if total == 0:
            return 0.5
        
        # Green/brown dominance suggests organic/biodegradable
        green_ratio = avg_g / total
        brown_score = min(avg_r, avg_g) / max(avg_b, 1)
        
        # Calculate brightness
        brightness = (avg_r + avg_g + avg_b) / 3
        
        # Heuristic scoring
        bio_score = 0
        
        # Green tones (leaves, food waste)
        if green_ratio > 0.35:
            bio_score += 0.3
            
        # Brown tones (organic matter)
        if brown_score > 1.2:
            bio_score += 0.3
            
        # Darker colors often indicate organic matter
        if brightness < 120:
            bio_score += 0.2
            
        # Add some randomness for variety (simulating model uncertainty)
        bio_score += random.uniform(-0.1, 0.1)
        
        return bio_score
    
    def predict(self, image_path):
        """Predict waste type from image using color-based heuristics"""
        img_array = self.preprocess_image(image_path)
        bio_score = self.analyze_color_features(img_array)
        
        # Determine classification
        if bio_score > 0.5:
            class_idx = 0  # Biodegradable
            confidence = 50 + (bio_score - 0.5) * 100
        else:
            class_idx = 1  # Non-Biodegradable
            confidence = 50 + (0.5 - bio_score) * 100
        
        # Cap confidence at reasonable levels
        confidence = min(confidence, 95)
        confidence = max(confidence, 55)
        
        return self.classes[class_idx], confidence
