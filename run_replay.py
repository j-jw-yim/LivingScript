#!/usr/bin/env python3
"""CLI entry point for replay mode. Run from project root."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from engine.replay import main
main()
