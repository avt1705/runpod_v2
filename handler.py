import runpod
from diffusers import DiffusionPipeline
import torch
import base64
from io import BytesIO

# Load the Hugging Face model
pipe = DiffusionPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-dev",
    torch_dtype=torch.float16
).to("cuda")

def handler(event):
    """
    event: JSON input from RunPod request
    Example request:
    {
      "input": {
        "prompt": "A futuristic city skyline at sunset"
      }
    }
    """
    # Get user input prompt
    prompt = event.get("input", {}).get("prompt", None)

    if not prompt:
        return {"error": "No prompt provided in request."}

    # Generate image from prompt
    image = pipe(prompt).images[0]

    # Save image temporarily
    output_path = "/tmp/generated.png"
    image.save(output_path)

    # Convert image to base64 string
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    image_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    # Return both path and base64
    return {
        "output_path": output_path,
        "image_base64": image_b64
    }

# Start RunPod serverless handler
runpod.serverless.start({"handler": handler})