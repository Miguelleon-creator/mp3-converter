#!/usr/bin/env bash

# Instala ffmpeg en el entorno de Render
apt-get update
apt-get install -y ffmpeg

# Instala las dependencias de Python
pip install -r requirements.txt
