import torch
from diffusers import StableDiffusionPipeline

# Выбор устройства
device = "cuda" if torch.cuda.is_available() else "cpu"

# Загружаем Stable Diffusion (обычная FP16 модель, без 8-бит)
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",  # Или другой совместимый checkpoint
    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    use_safetensors=True
).to(device)

# Загрузка LoRA адаптера
lora_paths = [ "lora\AbstractHeart.safetensors", "lora\CloudyHearts.safetensors", "lora\CrystalsHeart.safetensors" ]

for lora_path in lora_paths:
    # Загружаем LoRA адаптер
    pipe.load_lora_weights(lora_path)

    # (необязательно) Можно ослабить или усилить влияние LoRA:
    pipe.fuse_lora(lora_scale=1.0)

    # Промпт
    prompt = "a cute heart with flames, fire, love, centered on a white background, white bachground, minimalistic flat design, highly aesthetic, high resolution"
    negative_prompt = "blue, brown, patterns, gradients, multiple hearts, recursive shapes, frames, shadows, clutter"

    # Генерация
    image = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        guidance_scale=7.5,
        num_inference_steps=30
    ).images[0]

    # Сохраняем результат
    picture_name = lora_path.split("\\")[-1].split(".")[0]  # Извлекаем имя файла без расширения
    image.save(f"{picture_name}_heart.png")
    print(f"Изображение сохранено как {picture_name}_heart.png")