#!/usr/bin/env python3
"""CLI entry point for scene generation. Run from project root."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent / ".env")
from engine.generator import main
main()
