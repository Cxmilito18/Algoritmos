#!/usr/bin/env python3
import os
import sys
import subprocess

# Instalar dependencias
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"], check=False)

# Ejecutar Streamlit
os.system("streamlit run app.py --server.port=$PORT --server.address=0.0.0.0")
