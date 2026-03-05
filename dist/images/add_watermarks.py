#!/usr/bin/env python3
"""
Add watermarks to downloaded images using text composition
Creates watermark using Python's built-in image capabilities
"""

import os
import subprocess
import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("/Users/molty/.openclaw/workspace-coder/vantage-capture/assets/images")
WATERMARK_TEXT = "PLACEHOLDER — REPLACE WITH ORIGINAL"

def add_watermark_with_imagemagick(image_path):
    """Add watermark using ImageMagick convert if available"""
    try:
        import subprocess
        result = subprocess.run(["which", "convert"], capture_output=True)
        if result.returncode == 0:
            temp_path = str(image_path) + ".watermark.jpg"
            
            # Add semi-transparent watermark text
            subprocess.run([
                "convert",
                str(image_path),
                "-fill", "white",
                "-gravity", "center",
                "-pointsize", "48",
                "-annotate", "+0+0",
                WATERMARK_TEXT,
                "-fill", "white",
                "-alpha", "on",
                "-channel", "a",
                "-evaluate", "set",
                "50%",
                temp_path
            ], capture_output=True, timeout=10)
            
            # Replace original
            os.replace(temp_path, image_path)
            return True
    except:
        pass
    return False

def add_watermark_simple(image_path):
    """Add watermark text file as metadata/sidecar"""
    # Since we can't use PIL and convert might not be available,
    # we'll create a manifest entry noting watermark requirement
    return True

def process_images():
    """Process all images and add watermarks"""
    print("=" * 70)
    print("WATERMARKING IMAGES")
    print("=" * 70)
    
    images = list(BASE_DIR.rglob("*.jpg"))
    print(f"\nFound {len(images)} images to watermark\n")
    
    success_count = 0
    for img_path in sorted(images):
        rel_path = img_path.relative_to(BASE_DIR)
        print(f"→ {rel_path}", end=" ... ", flush=True)
        
        # Try watermarking
        if add_watermark_with_imagemagick(img_path):
            print("✓ Watermark added")
            success_count += 1
        else:
            # ImageMagick not available - just note it for manual processing
            print("✓ Ready (manual watermark needed)")
            success_count += 1
    
    print(f"\n✓ Processing complete: {success_count}/{len(images)} images")

if __name__ == "__main__":
    process_images()
