FROM nvidia/cuda:12.1.1-cudnn8-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=on \
    SHELL=/bin/bash

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

WORKDIR /

# Upgrade apt packages and install essential dependencies for minimal A1111
RUN apt update && \
    apt upgrade -y && \
    apt install -y \
      python3-dev \
      python3-pip \
      fonts-dejavu-core \
      rsync \
      git \
      aria2 \
      wget \
      curl \
      libglib2.0-0 \
      libsm6 \
      libgl1 \
      libxrender1 \
      libxext6 \
      bc \
      libgoogle-perftools4 \
      libtcmalloc-minimal4 \
      procps && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean -y

# Set Python
RUN ln -s /usr/bin/python3.10 /usr/bin/python

# Install minimal Worker dependencies (removed extension-specific packages)
RUN pip install requests runpod==1.7.7 huggingface_hub

# Add RunPod Handler and Docker container start script
COPY start.sh rp_handler.py ./
COPY schemas/input.py schemas/api.py schemas/txt2img.py schemas/img2img.py schemas/interrogate.py schemas/sync.py schemas/download.py /schemas/

# Start the container
RUN chmod +x /start.sh
ENTRYPOINT /start.sh
