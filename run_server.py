#!/usr/bin/env python3
"""Run the Living Script API server. Usage: python run_server.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent / ".env")

import uvicorn
# reload=False avoids subprocess conflicts when run via run.sh
uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=False)
