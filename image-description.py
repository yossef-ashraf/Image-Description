from transformers import VisionEncoderDecoderModel, ViTFeatureExtractor, AutoTokenizer
import torch
from PIL import Image

class ImageDescriber:
    def __init__(self):
        # تحميل النموذج المدرب مسبقاً
        self.model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.feature_extractor = ViTFeatureExtractor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        
        # نقل النموذج إلى GPU إذا كان متوفراً
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def generate_description(self, image_path, max_length=30, num_beams=4):
        try:
            # فتح وتحميل الصورة
            image = Image.open(image_path).convert('RGB')
            
            # استخراج خصائص الصورة
            pixel_values = self.feature_extractor(image, return_tensors="pt").pixel_values
            pixel_values = pixel_values.to(self.device)

            # توليد الوصف
            output_ids = self.model.generate(
                pixel_values,
                max_length=max_length,
                num_beams=num_beams,
                early_stopping=True
            )

            # فك ترميز النتيجة إلى نص
            description = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
            return description

        except Exception as e:
            return f"حدث خطأ أثناء معالجة الصورة: {str(e)}"

def main():
    # إنشاء كائن من الفئة
    describer = ImageDescriber()
    
    # مثال على الاستخدام
    image_path = "egypt-flag.jpg"  # قم بتغيير هذا المسار إلى مسار الصورة الخاصة بك
    description = describer.generate_description(image_path)
    print(f"وصف الصورة: {description}")

if __name__ == "__main__":
    main()
