import torch
from diffusers import StableDiffusionPipeline
from PIL import Image

# Убедимся, что используем CPU
device = "cpu"

# Загружаем модель (это может занять некоторое время и потребовать несколько гигабайт памяти)
pipe = StableDiffusionPipeline.from_pretrained(
    "playgroundai/playground-v2.5-1024px-aesthetic",
    torch_dtype=torch.float16,  # Используем float32 для CPU
    safety_checker=None,        # Отключаем safety checker для ускорени
    revision="fp16",           # Используем fp16 для экономии памяти
).to(device)

# Функция для генерации изображения сердца
def generate_heart(prompt="A beautiful red heart, shiny, aesthetic, high quality", 
                  negative_prompt="text, watermark, low quality, blurry",
                  steps=20, guidance_scale=7.5):
    # Генерируем изображение
    image = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=steps,
        guidance_scale=guidance_scale,
        width=1024,
        height=1024,
    ).images[0]
    
    return image

# Генерируем и сохраняем изображение
heart_image = generate_heart()
heart_image.save("generated_heart.png")
heart_image.show()

print("Изображение сердца успешно сгенерировано и сохранено как 'generated_heart.png'")