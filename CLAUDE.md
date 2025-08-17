# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a RunPod Serverless worker that provides an API interface to Automatic1111 Stable Diffusion for AI image generation. The worker is designed to run in a containerized environment on RunPod's serverless platform.

## Key Architecture Components

- **rp_handler.py**: Main serverless handler that processes RunPod API requests and routes them to the A1111 API
- **schemas/**: Input validation schemas for different API endpoints (txt2img, img2img, interrogate, etc.)
- **tests/**: Comprehensive test suite covering all API endpoints
- **start.sh**: Container startup script that launches A1111 WebUI API and the RunPod handler
- **Dockerfile**: Container configuration for CUDA-enabled environment

## Development Commands

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
- **Pillow**: Image processing

## API Architecture

The worker validates requests using Pydantic schemas and routes them to appropriate A1111 endpoints:

1. Input validation via schemas in `schemas/` directory
2. Request routing through `rp_handler.py`
3. A1111 API communication at `http://127.0.0.1:3000`
4. Response formatting for RunPod API standards

## Important Notes

- A1111 WebUI runs on port 3000 internally
- The worker expects A1111 to be pre-installed on a RunPod Network Volume at `/workspace`
- All A1111 extensions (ControlNet, ReActor, ADetailer) are included
- API format changed significantly in A1111 1.9.0 - use worker version 2.5.0 for backwards compatibility with A1111 1.8.0

## File Structure Context

- `docs/api/`: Comprehensive API documentation for all endpoints
- `config.json` & `ui-config.json`: A1111 configuration files
- `install-automatic.py`: A1111 installation script
- `webui-user.sh`: A1111 startup configuration