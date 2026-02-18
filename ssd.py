#!/usr/bin/env python3
"""
⚡ Antigravity SSD - Spec-Driven Development CLI

Backward compatibility wrapper.
Nếu đã pip install, dùng lệnh `ssd` trực tiếp.
File này cho phép chạy `python ssd.py` khi chưa install package.
"""
import sys
import os

# Đảm bảo package antigravity_ssd có thể import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from antigravity_ssd.cli import main

if __name__ == "__main__":
    main()
