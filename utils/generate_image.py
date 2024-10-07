import os
from dotenv import load_dotenv

load_dotenv()
secret_key = os.getenv('Secret_Key')

api_key = secret_key


def generate_card_image(prompt=""):
    # !Esto quedó de Open AI, actualmente es obsoleto
    try: 
        response = openai.images.generate(
            model="dall-e-3",
            prompt = prompt,
            size = "1024x1024",
            quality="standard",
            n = 1,
        )
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        print(f"Error al generar la imagen: {e}")
        return None