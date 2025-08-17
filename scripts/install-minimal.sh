#!/usr/bin/env bash

echo "=== Minimal A1111 Installation Script ==="
echo "This installs only basic Automatic1111 without extensions"
echo ""

echo "Deleting existing Automatic1111 Web UI"
rm -rf /workspace/stable-diffusion-webui

echo "Deleting existing venv"
rm -rf /workspace/venv

echo "Cloning A1111 repo to /workspace"
cd /workspace
git clone --depth=1 https://github.com/AUTOMATIC1111/stable-diffusion-webui.git

echo "Installing Ubuntu updates"
apt update
apt -y upgrade

echo "Installing essential Ubuntu packages"
apt -y install bc aria2

echo "Creating and activating Python virtual environment"
cd stable-diffusion-webui
python3 -m venv /workspace/venv
source /workspace/venv/bin/activate

echo "Installing PyTorch (CUDA 11.8)"
pip3 install --no-cache-dir torch==2.1.2+cu118 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

echo "Installing xformers"
pip3 install --no-cache-dir xformers==0.0.23.post1 --index-url https://download.pytorch.org/whl/cu118

echo "Installing A1111 Web UI dependencies"
wget https://raw.githubusercontent.com/ashleykleynhans/runpod-worker-a1111/main/install-automatic.py
python3 -m install-automatic --skip-torch-cuda-test

echo "Installing RunPod Serverless dependencies"
cd /workspace/stable-diffusion-webui
pip3 install huggingface_hub runpod

echo "Creating essential directories"
mkdir -p /workspace/logs
mkdir -p /workspace/stable-diffusion-webui/models/Stable-diffusion
mkdir -p /workspace/stable-diffusion-webui/models/VAE
mkdir -p /workspace/stable-diffusion-webui/models/ESRGAN

echo ""
echo "=== Optional: Download basic models ==="
echo "Downloading Deliberate v2 model (SD 1.5)"
cd /workspace/stable-diffusion-webui/models/Stable-diffusion
aria2c -o deliberate_v2.safetensors https://huggingface.co/ashleykleynhans/a1111-models/resolve/main/Stable-diffusion/deliberate_v2.safetensors

echo "Downloading SD 1.5 VAE"
cd /workspace/stable-diffusion-webui/models/VAE
aria2c -o vae-ft-mse-840000-ema-pruned.safetensors https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors

echo "Downloading basic upscaler"
cd /workspace/stable-diffusion-webui/models/ESRGAN
aria2c -o 4x-UltraSharp.pth https://huggingface.co/ashleykleynhans/upscalers/resolve/main/4x-UltraSharp.pth

echo "Installing minimal config files"
cd /workspace/stable-diffusion-webui
rm -f webui-user.sh config.json ui-config.json

# Create minimal config files
cat > webui-user.sh << 'EOF'
#!/bin/bash
export COMMANDLINE_ARGS="--listen --port 3000 --api --skip-version-check --no-download-sd-model"
EOF

cat > config.json << 'EOF'
{
  "outdir_samples": "",
  "outdir_txt2img_samples": "/workspace/stable-diffusion-webui/outputs/txt2img-images",
  "outdir_img2img_samples": "/workspace/stable-diffusion-webui/outputs/img2img-images",
  "outdir_grids": "/workspace/stable-diffusion-webui/outputs/txt2img-grids",
  "outdir_txt2img_grids": "/workspace/stable-diffusion-webui/outputs/txt2img-grids",
  "outdir_save": "/workspace/stable-diffusion-webui/log/images",
  "samples_format": "png",
  "grid_format": "png",
  "samples_filename_pattern": "",
  "save_images_add_number": true,
  "save_grid": true,
  "return_grid": true,
  "grid_prevent_empty_spots": false,
  "save_incomplete_images": false,
  "export_for_4chan": true,
  "img_downscale_threshold": 4.0,
  "target_side_length": 4000,
  "img_max_size_mp": 200,
  "use_original_name_batch": true,
  "use_upscaler_name_as_suffix": false,
  "save_selected_only": true,
  "do_not_add_watermark": false
}
EOF

cat > ui-config.json << 'EOF'
{
  "txt2img/Prompt/visible": true,
  "txt2img/Prompt/value": "",
  "txt2img/Negative prompt/visible": true,
  "txt2img/Negative prompt/value": "",
  "txt2img/Sampling method/visible": true,
  "txt2img/Sampling method/value": "DPM++ SDE",
  "txt2img/Sampling steps/visible": true,
  "txt2img/Sampling steps/value": 20,
  "txt2img/Width/visible": true,
  "txt2img/Width/value": 512,
  "txt2img/Height/visible": true,
  "txt2img/Height/value": 512,
  "txt2img/CFG Scale/visible": true,
  "txt2img/CFG Scale/value": 7.0,
  "txt2img/Seed/visible": true,
  "txt2img/Seed/value": -1
}
EOF

chmod +x webui-user.sh

echo ""
echo "=== Testing A1111 Installation ==="
echo "Starting A1111 Web UI for initial setup..."
deactivate
export HF_HOME="/workspace"
cd /workspace/stable-diffusion-webui
./webui.sh -f &

echo ""
echo "=== Installation Complete ==="
echo ""
echo "✅ Minimal A1111 installation completed!"
echo ""
echo "What was installed:"
echo "  - Basic Automatic1111 WebUI"
echo "  - PyTorch + xformers"
echo "  - RunPod serverless dependencies"
echo "  - Deliberate v2 model (SD 1.5)"
echo "  - Basic VAE and upscaler"
echo ""
echo "What was NOT installed:"
echo "  ❌ ControlNet extension"
echo "  ❌ ReActor extension"
echo "  ❌ ADetailer extension"
echo "  ❌ Extension-specific models"
echo ""
echo "To add your own models:"
echo "  - Checkpoints: /workspace/stable-diffusion-webui/models/Stable-diffusion/"
echo "  - VAE models: /workspace/stable-diffusion-webui/models/VAE/"
echo "  - LoRA models: /workspace/stable-diffusion-webui/models/Lora/"
echo "  - Embeddings: /workspace/stable-diffusion-webui/embeddings/"
echo ""
echo "Wait for A1111 to finish loading, then press Ctrl+C to stop and terminate the pod."