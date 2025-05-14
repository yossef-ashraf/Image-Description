from transformers import VisionEncoderDecoderModel, ViTFeatureExtractor, AutoTokenizer
import torch
from PIL import Image

class ImageDescriber:
    def __init__(self):
        # Load the pre-trained model
        self.model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.feature_extractor = ViTFeatureExtractor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        
        # Move the model to GPU if available
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def generate_description(self, image_path, max_length=30, num_beams=4):
        try:
            # Open and load the image
            image = Image.open(image_path).convert('RGB')
            
            # Extract image features
            pixel_values = self.feature_extractor(image, return_tensors="pt").pixel_values
            pixel_values = pixel_values.to(self.device)

            # Generate the description
            output_ids = self.model.generate(
                pixel_values,
                max_length=max_length,
                num_beams=num_beams,
                early_stopping=True
            )

            # Decode the result to text
            description = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
            return description

        except Exception as e:
            return f"An error occurred while processing the image: {str(e)}"

def main():
    # Create an instance of the class
    describer = ImageDescriber()
    
    # Example usage
    image_path = "egypt-flag.jpg"  # Change this path to your image path
    description = describer.generate_description(image_path)
    print(f"Image description: {description}")

if __name__ == "__main__":
    main()