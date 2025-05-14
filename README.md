


          
# Advanced Image AI - README

## Overview

Advanced Image AI is a powerful web application that analyzes images and generates detailed descriptions using state-of-the-art AI models. The application provides users with basic captions, detailed descriptions, and image property analysis.

## Features

- **Image Upload**: Drag and drop or select images for analysis
- **Basic Caption Generation**: Quick summary of image content using ViT-GPT2 model
- **Detailed Description**: In-depth analysis using BLIP model (when available)
- **Image Property Analysis**: Provides information about:
  - Image dimensions
  - Brightness level (dark, medium, bright)
  - Color profile (colorful or muted)
  - Dominant colors

## Technology Stack

- **Backend**: Python with Flask
- **Frontend**: HTML, CSS, JavaScript
- **AI Models**:
  - ViT-GPT2 for basic image captioning
  - BLIP for detailed descriptions
- **Containerization**: Docker and Docker Compose

## Requirements

- Python 3.9+
- Flask 2.0.1+
- PyTorch 1.9.0+
- Transformers 4.9.2+
- Pillow 8.3.1+
- NumPy 1.21.2+

## Installation

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd Image-Ai
```

2. Build and run with Docker Compose:
```bash
docker-compose up --build
```

3. Access the application at http://localhost:5000

### Manual Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Image-Ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download the required models:
```bash
python app/models/download_model.py
```

4. Run the application:
```bash
cd app
python app.py
```

5. Access the application at http://localhost:5000

## Project Structure

```
Image-Ai/
├── app/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── main.js
│   ├── templates/
│   │   └── index.html
│   ├── models/
│   │   └── download_model.py
│   ├── uploads/
│   ├── app.py
│   └── image_analyzer.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## How It Works

1. **Image Upload**: Users can upload images through the web interface by dragging and dropping or selecting files.

2. **Image Processing**: The backend processes the uploaded image using the `ImageAnalyzer` class.

3. **AI Analysis**: 
   - The primary ViT-GPT2 model generates a basic caption
   - If available, the BLIP model creates a more detailed description
   - Image properties are analyzed (dimensions, brightness, colors)

4. **Result Display**: The application presents the analysis results in an organized format on the web interface.

## API Endpoints

- **GET /** - Serves the main application page
- **POST /analyze** - Accepts image uploads and returns analysis results

## Docker Configuration

The application is containerized using Docker with the following configuration:
- Base image: Python 3.9-slim
- Exposed port: 5000
- Volume mapping for uploads directory
- Automatic model download during build

## Development

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Acknowledgements

- The project uses pre-trained models from Hugging Face:
  - [ViT-GPT2 Image Captioning](https://huggingface.co/nlpconnect/vit-gpt2-image-captioning)
  - [BLIP Image Captioning](https://huggingface.co/Salesforce/blip-image-captioning-large)

        