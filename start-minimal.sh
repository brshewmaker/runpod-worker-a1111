#!/usr/bin/env bash

echo "Minimal A1111 Worker Initiated"

echo "Symlinking files from Network Volume"
rm -rf /workspace && \
  ln -s /runpod-volume /workspace

if [ -f "/workspace/venv/bin/activate" ]; then
    echo "Starting Minimal WebUI API"
    source /workspace/venv/bin/activate
    TCMALLOC="$(ldconfig -p | grep -Po "libtcmalloc.so.\d" | head -n 1)"
    export LD_PRELOAD="${TCMALLOC}"
    export PYTHONUNBUFFERED=true
    export HF_HOME="/workspace"
    
    # Start A1111 with minimal flags (no extension-specific arguments)
    python3 /workspace/stable-diffusion-webui/webui.py \
      --xformers \
      --no-half-vae \
      --skip-python-version-check \
      --skip-torch-cuda-test \
      --skip-install \
      --lowram \
      --opt-sdp-attention \
      --disable-safe-unpickle \
      --port 3000 \
      --api \
      --nowebui \
      --skip-version-check \
      --no-hashing \
      --no-download-sd-model > /workspace/logs/webui.log 2>&1 &
    deactivate
else
    echo "ERROR: The Python Virtual Environment (/workspace/venv/bin/activate) could not be activated"
    echo "Troubleshooting steps:"
    echo "1. Ensure you have run the minimal installation script on your Network Volume"
    echo "2. Use the command: wget https://raw.githubusercontent.com/YOUR_REPO/main/scripts/install-minimal.sh && chmod +x install-minimal.sh && ./install-minimal.sh"
    echo "3. Ensure you used a PyTorch base image for installation (not a Stable Diffusion image)"
    echo "4. Ensure your Network Volume is properly attached to the endpoint"
    echo "5. Check that the installation completed successfully without errors"
fi

echo "Starting RunPod Handler"
python3 -u /rp_handler.py