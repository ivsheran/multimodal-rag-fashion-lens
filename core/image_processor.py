import base64
import ollama
from PIL import Image
from io import BytesIO
from core.config_loader import ConfigLoader

class ImageProcessor:
    def __init__(self, config: ConfigLoader):
        self.vision_model = config.vision_model
        self.ollama_base_url = config.ollama_base_url

    def load_image(self, image_path):
        # Load the image from interface input (e.g., file upload))
        image = Image.open(image_path)

        # Resize and preprocess the image as required by the vision model
        image = image.resize((512, 512)) 
        image = image.convert('RGB')

        # Convert image to Base64 string
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        base64_string = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return base64_string

    def describe_image(self, image):
        # Load vision prompt
        with open('prompts/vision_prompt.txt', 'r') as f:
            prompt = f.read()    

        # Use the vision model to generate a description of the image
        
        # Return the description as text
        response = ollama.chat(
            model=self.vision_model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": "Describe this image", "images": [image]}
            ]
        )
        description = response['message']['content']
        return description

    