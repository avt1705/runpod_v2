import runpod
import torch
import base64
import os
from io import BytesIO
from diffusers import FluxPipeline
from huggingface_hub import login


login(os.getenv("HUGGINGFACE_HUB_TOKEN"))

pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-dev",
    torch_dtype=torch.bfloat16,
    use_auth_token=os.getenv("HUGGINGFACE_HUB_TOKEN")  # ensure gated repo access
).to("cuda")

def handler(event):
    prompt = event.get("input", {}).get("prompt", None)

    if not prompt:
        return {"error": "No prompt provided in request."}

    image = pipe(
        prompt,
        height=1024,
        width=1024,
        guidance_scale=3.5,
        num_inference_steps=50
    ).images[0]

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    image_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return {
        "image_base64": image_b64
    }

runpod.serverless.start({"handler": handler})

