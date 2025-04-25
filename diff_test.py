from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
import torch
import time
from datetime import datetime

with open('prompt.txt', 'r', encoding='utf-8') as f:
    prompt = f.read().strip()

with open('neg_prompt.txt', 'r', encoding='utf-8') as f:
    neg_prompt = f.read().strip()

def generate_image(
    prompt: str,
    negative_prompt: str = "",
    height: int = 512,
    width: int = 512,
    num_inference_steps: int = 20,  # Уменьшено для CPU
    guidance_scale: float = 7.5,
    seed: int = None,
    output_path: str = "output.png",
    verbose: bool = True,
    device: str = "auto"  # "auto", "cuda" или "cpu"
):
    # Определение устройства
    if device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Настройки для CPU
    if device == "cpu":
        num_inference_steps = min(num_inference_steps, 20)  # Ограничение шагов для CPU
        torch_dtype = torch.float32  # float16 не всегда хорошо работает на CPU
    else:
        torch_dtype = torch.float16

    # Начало отсчета времени
    start_time = time.time()
    
    if verbose:
        print(f"\n{'='*50}")
        print(f"Stable Diffusion запущен | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Устройство выполнения: {device.upper()}")
        print(f"Prompt: {prompt}")
        if negative_prompt:
            print(f"Negative prompt: {negative_prompt}")
        print(f"Размер изображения: {width}x{height}")
        print(f"Шагов генерации: {num_inference_steps}")
        print(f"Guidance scale: {guidance_scale}")
        if seed is not None:
            print(f"Seed: {seed}")
        print(f"{'-'*50}")
        print("Этап 1/4: Загрузка модели...")

    # Загрузка модели
    model_id = "runwayml/stable-diffusion-v1-5"
    
    try:
        scheduler = EulerDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler")
        pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            scheduler=scheduler,
            torch_dtype=torch_dtype,
            safety_checker=None
        )
        
        if verbose:
            print("Модель успешно загружена")
            print(f"Этап 2/4: Перенос модели на {device.upper()}...")
        
        pipe = pipe.to(device)
        
        # Оптимизации для CPU
        if device == "cpu":
            pipe.enable_attention_slicing()  # Обязательно для CPU
            if verbose:
                print("Внимание: Работа на CPU будет медленной!")
                print("Рекомендуется использовать небольшие размеры изображений (до 512x512)")
                print("и уменьшенное количество шагов (15-20)")
        
        if verbose:
            print(f"Используется устройство: {pipe.device}")
            print("Этап 3/4: Подготовка генератора...")
        
        if seed is not None:
            generator = torch.Generator(device).manual_seed(seed)
            if verbose:
                print(f"Установлен seed: {seed}")
        else:
            generator = None
            if verbose:
                print("Случайный seed")
        
        if verbose:
            print("Этап 4/4: Генерация изображения...")
            print(f"{'-'*50}")
            print("Прогресс:")
        
        # Callback для отображения прогресса
        def progress_callback(step, timestep, latents):
            if verbose:  # Реже выводим прогресс для CPU
                progress = (step + 1) / num_inference_steps * 100
                print(f"Шаг {step+1}/{num_inference_steps} ({progress:.1f}%)")
        
        # Генерация изображения
        image = pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            height=height,
            width=width,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            generator=generator,
            callback=progress_callback,
            callback_steps=2
        ).images[0]
        
        # Сохранение результата
        image.save(output_path)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        if verbose:
            print(f"{'-'*50}")
            print(f"Генерация завершена успешно!")
            print(f"Изображение сохранено как: {output_path}")
            print(f"Общее время выполнения: {elapsed_time:.2f} секунд")
            print(f"{'='*50}\n")
        
        return image
    
    except Exception as e:
        if verbose:
            print(f"\nОШИБКА: {str(e)}")
        raise

# Пример использования на CPU
if __name__ == "__main__":
    generate_image(
        prompt=prompt,
        negative_prompt=neg_prompt,
        seed=42,
        num_inference_steps=10,  # Меньше шагов для CPU
        width=384,  # Меньший размер для CPU
        height=384,
        output_path="heart.png",
        verbose=True,
        device="cpu"  # Явно указываем CPU
    )