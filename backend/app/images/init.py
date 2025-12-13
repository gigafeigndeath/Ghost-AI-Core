from .kandinsky import generate_with_kandinsky
from .stable_diffusion import generate_with_sd

def get_image_generator(method: str):
    if method == "kandinsky":
        return generate_with_kandinsky
    elif method == "stable_diffusion":
        return generate_with_sd
    else:
        raise ValueError("Unknown image generator")

def generate_image(prompt: str, style: str):
    # Default to kandinsky
    return generate_with_kandinsky(prompt, style)