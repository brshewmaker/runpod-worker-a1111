# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **minimal** RunPod Serverless worker that provides an API interface to Automatic1111 Stable Diffusion for AI image generation. This version includes only core A1111 functionality without extensions, making it lightweight and fast to deploy.

## Key Architecture Components

- **rp_handler.py**: Main serverless handler that processes RunPod API requests and routes them to the A1111 API
- **schemas/**: Input validation schemas for core API endpoints (txt2img, img2img, interrogate, etc.)
- **tests/**: Comprehensive test suite covering all API endpoints
- **start.sh**: Container startup script that launches A1111 WebUI API and the RunPod handler
- **Dockerfile**: Minimal container configuration for CUDA-enabled environment

## Development Commands

### Installation
```bash
# Run the minimal installation script on your Network Volume
bash scripts/install.sh
```

### Testing
```bash
# Run individual test files from the tests/ directory
python3 tests/txt2img.py
python3 tests/img2img.py
python3 tests/get_models.py
```

### Docker Operations
```bash
# Build the Docker image
docker build -t runpod-worker-a1111 .

# Run locally for testing
docker run --gpus all -p 8000:8000 runpod-worker-a1111
```

### Dependencies
```bash
# Install Python dependencies
pip install -r requirements.txt
```

## Core Dependencies

- **runpod**: RunPod Python SDK for serverless operations
- **requests**: HTTP client for A1111 API communication
- **huggingface_hub**: For model syncing and downloads

## API Architecture

The worker validates requests using schemas and routes them to appropriate A1111 endpoints:

1. Input validation via schemas in `schemas/` directory
2. Request routing through `rp_handler.py`
3. A1111 API communication at `http://127.0.0.1:3000`
4. Response formatting for RunPod API standards

## What's Included vs Original

### ✅ Included (Minimal)
- Core Automatic1111 WebUI
- txt2img and img2img generation
- Basic model management
- Image interrogation
- Standard samplers and schedulers

### ❌ Removed (Extensions)
- ControlNet extension
- ReActor face swapping
- ADetailer enhancement
- Extension-specific models and dependencies

## Important Notes

- A1111 WebUI runs on port 3000 internally
- The worker expects A1111 to be pre-installed on a RunPod Network Volume at `/workspace`
- Use `bash scripts/install.sh` to install minimal A1111
- Much faster startup and smaller resource footprint compared to full version

## File Structure Context

- `docs/api/`: API documentation for supported endpoints
- `config.json` & `ui-config.json`: Minimal A1111 configuration files
- `install-automatic.py`: A1111 installation script
- `webui-user.sh`: A1111 startup configuration