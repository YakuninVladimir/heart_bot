import torch
from diffusers import StableDiffusionXLPipeline

# Определение устройства
device = "cuda" if torch.cuda.is_available() else "cpu"

# Модель Playground v2.5
model_id = "playgroundai/playground-v2.5-1024px-aesthetic"

# Загрузка пайплайна
pipe = StableDiffusionXLPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    variant="fp16" if device == "cuda" else None,
    use_safetensors=True,
).to(device)

# Промпты
prompt = "a cute heart with flames, fire, love, centered on a white background, minimalistic flat design, highly aesthetic, high resolution"
negative_prompt = "blue, brown, patterns, gradients, multiple hearts, recursive shapes, frames, shadows, clutter"

# Генерация изображения
result = pipe(
    prompt=prompt,
    negative_prompt=negative_prompt,
    num_inference_steps=20,
    guidance_scale=7.5,
    width=512,
    height=512,
    num_images_per_prompt=1,
)

# Извлечение изображения
image = result.images[0]

# Сохранение изображения
image.save("playground_heart.png")
print("✅ Сохранено как 'playground_heart.png'")
