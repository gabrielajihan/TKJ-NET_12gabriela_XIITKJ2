#!/usr/bin/env bash
set -euo pipefail

sudo apt-get update
sudo apt-get install -y --no-install-recommends \
    autoconf \
    automake \
    build-essential \
    cmake \
    git \
    libffi-dev \
    libltdl-dev \
    libncurses-dev \
    libssl-dev \
    openjdk-17-jdk \
    pkg-config \
    python3.12-dev \
    python3.12-venv \
    unzip \
    zip \
    zlib1g-dev