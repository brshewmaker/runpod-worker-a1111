# Minimal A1111 Stable Diffusion | RunPod Serverless Worker

This is a streamlined version of the RunPod A1111 worker that includes **only basic Automatic1111** functionality without extensions.

## What's Included ✅

- ✅ Basic Automatic1111 WebUI
- ✅ Text-to-Image generation  
- ✅ Image-to-Image generation
- ✅ Interrogation (image-to-prompt)
- ✅ Model management (loading, switching)
- ✅ Basic upscaling
- ✅ RunPod serverless integration

## What's NOT Included ❌

- ❌ ControlNet extension
- ❌ ReActor (face swapping) extension  
- ❌ ADetailer (face enhancement) extension
- ❌ Extension-specific models and dependencies
- ❌ InstantID functionality

## Installation

### 1. Network Volume Setup

Create a RunPod Network Volume and run the minimal installation script:

```bash
# Download and run the minimal installer
wget https://raw.githubusercontent.com/YOUR_REPO/main/scripts/install-minimal.sh
chmod +x install-minimal.sh
./install-minimal.sh
```

This installs:
- Basic A1111 WebUI
- Python environment with PyTorch + xformers
- One basic SD 1.5 model (Deliberate v2)
- Basic VAE and upscaler

### 2. Add Your Own Models

Place your models in these directories on the network volume:

```bash
# Stable Diffusion checkpoints
/workspace/stable-diffusion-webui/models/Stable-diffusion/

# VAE models  
/workspace/stable-diffusion-webui/models/VAE/

# LoRA models
/workspace/stable-diffusion-webui/models/Lora/

# Embeddings
/workspace/stable-diffusion-webui/embeddings/
```

### 3. Build Docker Image

```bash
# Build minimal image
docker build -f Dockerfile.minimal -t your-username/runpod-worker-a1111-minimal .

# Push to registry
docker push your-username/runpod-worker-a1111-minimal
```

### 4. Deploy Serverless Endpoint

Create a RunPod serverless endpoint using:
- Docker image: `your-username/runpod-worker-a1111-minimal`
- Attach your network volume

## Supported API Endpoints

### Core A1111 APIs
- Text-to-Image: `POST /sdapi/v1/txt2img`
- Image-to-Image: `POST /sdapi/v1/img2img`  
- Interrogate: `POST /sdapi/v1/interrogate`
- Get Models: `GET /sdapi/v1/sd-models`
- Set Model: `POST /sdapi/v1/options`
- Get Samplers: `GET /sdapi/v1/samplers`
- Get Schedulers: `GET /sdapi/v1/schedulers`
- Get VAE: `GET /sdapi/v1/sd-vae`
- Refresh Models: `POST /sdapi/v1/refresh-checkpoints`

### Helper APIs
- Download: `POST /v1/download`
- Sync: `POST /v1/sync`

## Testing

Use the provided test script:

```bash
python test_runpod_a1111.py
```

## Benefits of Minimal Version

1. **Faster Cold Starts** - No extension loading time
2. **Lower Memory Usage** - No extension overhead  
3. **Simpler Maintenance** - Fewer dependencies to manage
4. **Smaller Network Volume** - Only essential files
5. **More Reliable** - Fewer points of failure

## Migration from Full Version

If you're migrating from the full version:

1. Your existing models in `/workspace/stable-diffusion-webui/models/` will work as-is
2. Remove extension directories if desired:
   ```bash
   rm -rf /workspace/stable-diffusion-webui/extensions/sd-webui-controlnet
   rm -rf /workspace/stable-diffusion-webui/extensions/sd-webui-reactor  
   rm -rf /workspace/stable-diffusion-webui/extensions/adetailer
   ```
3. Deploy using the minimal Docker image

## File Structure

```
/workspace/
├── stable-diffusion-webui/           # A1111 installation
│   ├── models/
│   │   ├── Stable-diffusion/         # Your checkpoint files
│   │   ├── VAE/                      # VAE files
│   │   ├── Lora/                     # LoRA files
│   │   └── ESRGAN/                   # Upscaler models
│   ├── embeddings/                   # Textual inversion embeddings
│   └── outputs/                      # Generated images
├── venv/                             # Python virtual environment
└── logs/                             # Application logs
```

## Limitations

- No ControlNet image conditioning
- No face swapping/enhancement features
- No InstantID functionality
- Fewer artistic control options

For basic text-to-image and image-to-image generation with your own models, this minimal version provides everything you need with better performance.