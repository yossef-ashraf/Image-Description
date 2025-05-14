import torch
from PIL import Image
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer, BlipProcessor, BlipForConditionalGeneration
import os
import numpy as np

class ImageAnalyzer:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")
        
        # Load primary caption model (ViT-GPT2)
        print("Loading ViT-GPT2 model...")
        self.caption_model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        
        self.caption_model.to(self.device)
        
        # Set special tokens
        self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Model parameters
        self.max_length = 30  # Increased for more detailed captions
        self.num_beams = 5    # Increased for better beam search
        self.gen_kwargs = {"max_length": self.max_length, "num_beams": self.num_beams}
        
        # Load BLIP model for more detailed descriptions
        try:
            print("Loading BLIP model for detailed descriptions...")
            self.blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
            self.blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
            self.blip_model.to(self.device)
            self.has_blip = True
        except Exception as e:
            print(f"Could not load BLIP model: {e}")
            self.has_blip = False
    
    def predict_caption(self, image_path):
        """Generate a basic caption for the image at the given path."""
        try:
            i_image = Image.open(image_path)
            if i_image.mode != "RGB":
                i_image = i_image.convert(mode="RGB")
                
            pixel_values = self.feature_extractor(images=[i_image], return_tensors="pt").pixel_values
            pixel_values = pixel_values.to(self.device)
            
            output_ids = self.caption_model.generate(pixel_values, **self.gen_kwargs)
            
            preds = self.tokenizer.batch_decode(output_ids, skip_special_tokens=True)
            basic_caption = preds[0].strip()
            
            # Get detailed description if BLIP is available
            detailed_description = self.generate_detailed_description(i_image) if self.has_blip else ""
            
            # Get image analysis
            analysis = self.analyze_image(i_image)
            
            # Combine all information
            full_description = {
                "basic_caption": basic_caption,
                "detailed_description": detailed_description,
                "analysis": analysis
            }
            
            return full_description
        except Exception as e:
            return {"error": f"Error analyzing image: {str(e)}"}
    
    def generate_detailed_description(self, image):
        """Generate a more detailed description using BLIP model."""
        try:
            if not self.has_blip:
                return "Detailed description not available (BLIP model not loaded)"
                
            # Generate unconditional caption
            inputs = self.blip_processor(image, return_tensors="pt").to(self.device)
            out = self.blip_model.generate(**inputs, max_length=75)
            unconditional = self.blip_processor.decode(out[0], skip_special_tokens=True)
            
            # Generate conditional captions with different prompts
            prompts = [
                "a photo of",
                "an image showing",
                "the image contains"
            ]
            
            conditional_results = []
            for prompt in prompts:
                inputs = self.blip_processor(image, text=prompt, return_tensors="pt").to(self.device)
                out = self.blip_model.generate(**inputs, max_length=75)
                conditional_results.append(self.blip_processor.decode(out[0], skip_special_tokens=True))
            
            # Return the most detailed description (usually the longest one)
            all_descriptions = [unconditional] + conditional_results
            return max(all_descriptions, key=len)
            
        except Exception as e:
            return f"Error generating detailed description: {str(e)}"
    
    def analyze_image(self, image):
        """Analyze image properties like colors, brightness, etc."""
        try:
            # Convert to numpy array
            img_array = np.array(image)
            
            # Get image dimensions
            height, width, channels = img_array.shape
            
            # Calculate average color
            avg_color = img_array.mean(axis=(0, 1))
            
            # Calculate brightness
            brightness = np.mean(img_array)
            brightness_level = "dark" if brightness < 85 else "medium" if brightness < 170 else "bright"
            
            # Determine if image is colorful or grayscale-like
            color_std = np.std(img_array, axis=(0, 1))
            color_variance = np.mean(color_std)
            is_colorful = color_variance > 30
            
            # Dominant color analysis
            r, g, b = avg_color
            
            # Simple color naming
            colors = {
                "red": r > max(g, b) and r > 150,
                "green": g > max(r, b) and g > 150,
                "blue": b > max(r, g) and b > 150,
                "yellow": r > 200 and g > 200 and b < 100,
                "purple": r > 120 and b > 120 and g < 100,
                "orange": r > 200 and g > 100 and b < 100,
                "black": np.mean(avg_color) < 50,
                "white": np.mean(avg_color) > 200,
                "gray": np.std(avg_color) < 20 and 50 <= np.mean(avg_color) <= 200
            }
            
            dominant_colors = [color for color, is_dominant in colors.items() if is_dominant]
            if not dominant_colors:
                dominant_colors = ["mixed"]
            
            return {
                "dimensions": f"{width}x{height}",
                "brightness": brightness_level,
                "colorfulness": "colorful" if is_colorful else "muted",
                "dominant_colors": dominant_colors
            }
            
        except Exception as e:
            return f"Error analyzing image properties: {str(e)}"