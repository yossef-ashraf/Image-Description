from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer

def download_models():
    print("Downloading pre-trained models...")
    
    # This will download the models to the cache directory
    model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    
    print("Models downloaded successfully!")

if __name__ == "__main__":
    download_models()