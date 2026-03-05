#!/usr/bin/env python3
"""
Create simple placeholder images for missing categories
Fills gaps in the portfolio to reach target distribution
"""

import os
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import io

BASE_DIR = Path("/Users/molty/.openclaw/workspace-coder/vantage-capture/assets/images")

# Category placeholders to create
PLACEHOLDERS = [
    ("hero", 1920, 1080, "Hero - Dramatic Aerial View"),
    ("services/mapping", 800, 600, "Mapping - Orthomosaic"),
    ("services/mapping", 800, 600, "Mapping - Point Cloud"),
    ("services/inspection", 800, 600, "Inspection - Tower Detail"),
    ("services/construction", 800, 600, "Construction - Volume Calc"),
    ("services/construction", 800, 600, "Construction - Progress Report"),
    ("services/realestate", 800, 600, "Real Estate - Lot Overview"),
    ("services/realestate", 800, 600, "Real Estate - Neighborhood"),
    ("portfolio", 600, 400, "Portfolio - Mapping Report"),
    ("portfolio", 600, 400, "Portfolio - 3D Model"),
    ("portfolio", 600, 400, "Portfolio - Volume Analysis"),
]

def create_placeholder_image(width, height, text, category):
    """Create a styled placeholder image"""
    # Create image with gradient background
    img = Image.new('RGB', (width, height), color=(240, 240, 245))
    draw = ImageDraw.Draw(img)
    
    # Add gradient effect (simple - multiple rectangles)
    colors = [
        (200, 220, 255),
        (220, 240, 255),
        (240, 245, 255),
    ]
    
    for i, color in enumerate(colors):
        y_start = int(height * i / len(colors))
        y_end = int(height * (i + 1) / len(colors))
        draw.rectangle([(0, y_start), (width, y_end)], fill=color)
    
    # Draw category icon/text
    try:
        font_size = int(width / 12)
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except:
        font = ImageFont.load_default()
    
    # Draw main text
    draw.text((width // 2, height // 3), "PLACEHOLDER", 
              fill=(80, 100, 150), font=font, anchor="mm")
    
    # Draw description
    try:
        font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", int(font_size * 0.6))
    except:
        font_small = ImageFont.load_default()
    
    draw.text((width // 2, height * 2 // 3), text,
              fill=(100, 130, 180), font=font_small, anchor="mm")
    
    # Draw watermark border
    border_width = 2
    draw.rectangle([(0, 0), (width-1, height-1)], outline=(150, 170, 200), width=border_width)
    
    return img

def main():
    try:
        from PIL import Image, ImageDraw, ImageFont
        PIL_AVAILABLE = True
    except ImportError:
        print("⚠️  PIL not available - creating text-based placeholders only")
        PIL_AVAILABLE = False
        return
    
    print("=" * 70)
    print("CREATING PLACEHOLDER IMAGES")
    print("=" * 70)
    
    manifest = []
    created = 0
    
    for category, width, height, description in PLACEHOLDERS:
        # Create directory
        cat_path = BASE_DIR / category
        cat_path.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        count = len(list(cat_path.glob("*.jpg"))) + 1
        filename = f"{category.replace('/', '_')}_placeholder_{count:02d}.jpg"
        filepath = cat_path / filename
        
        if not filepath.exists():
            print(f"  → {filename[:45]}...", end=" ", flush=True)
            
            try:
                # Create image
                img = create_placeholder_image(width, height, description, category)
                
                # Save
                img.save(filepath, "JPEG", quality=85)
                print(f"✓")
                
                manifest.append({
                    "filename": filename,
                    "category": category,
                    "source": "Generated Placeholder",
                    "description": description,
                    "status": "placeholder_needs_replacement",
                    "dimensions": f"{width}x{height}",
                })
                created += 1
            except Exception as e:
                print(f"✗ {str(e)[:30]}")
    
    print(f"\n✓ Created {created} placeholder images\n")
    return manifest

if __name__ == "__main__":
    # Try to create placeholders
    try:
        from PIL import Image, ImageDraw, ImageFont
        main()
    except ImportError:
        print("PIL not available. Skipping placeholder image creation.")
        print("This is OK - we have 21 downloaded images from free stock sources.\n")
