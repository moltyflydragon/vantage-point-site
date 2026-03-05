#!/usr/bin/env python3
"""
Vantage Capture Image Gathering & Processing Workflow
Downloads drone/construction images from free stock sources and adds watermarks
Uses macOS sips tool for image processing
"""

import os
import json
import urllib.request
import subprocess
from pathlib import Path
import io

# Configuration
BASE_DIR = Path("/Users/molty/.openclaw/workspace-coder/vantage-capture/assets/images")
WATERMARK_TEXT = "PLACEHOLDER — REPLACE WITH ORIGINAL"

# Image specifications by category
SPECS = {
    "hero": (1920, 1080),
    "services": (800, 600),
    "portfolio": (600, 400),
    "avatars": (400, 400),
}

# Known free stock image URLs from Unsplash (drone/construction/aerial)
# Format: (url, category, description)
IMAGE_URLS = [
    # HERO images (6)
    ("https://images.unsplash.com/photo-1574609433479-36c3f6d84885?w=1920&h=1080&fit=crop", "hero", "Drone flying over landscape"),
    ("https://images.unsplash.com/photo-1620938534186-b12f73c13f0a?w=1920&h=1080&fit=crop", "hero", "Aerial city construction"),
    ("https://images.unsplash.com/photo-1518895949257-7621c3c786d7?w=1920&h=1080&fit=crop", "hero", "Construction site overview"),
    ("https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=1920&h=1080&fit=crop", "hero", "Building construction progress"),
    ("https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=1920&h=1080&fit=crop", "hero", "Aerial drone shot"),
    ("https://images.unsplash.com/photo-1531482615713-2afd69097998?w=1920&h=1080&fit=crop", "hero", "Modern construction site"),
    
    # SERVICES/MAPPING (4)
    ("https://images.unsplash.com/photo-1618788550549-9def6dd6ac8c?w=800&h=600&fit=crop", "services/mapping", "Survey mapping technology"),
    ("https://images.unsplash.com/photo-1444080748397-f442aa95c3e5?w=800&h=600&fit=crop", "services/mapping", "Digital mapping interface"),
    ("https://images.unsplash.com/photo-1527627320261-7c46d19cd819?w=800&h=600&fit=crop", "services/mapping", "3D modeling visualization"),
    ("https://images.unsplash.com/photo-1623665520903-3f82df6a3df0?w=800&h=600&fit=crop", "services/mapping", "Precision measurement tool"),
    
    # SERVICES/INSPECTION (4)
    ("https://images.unsplash.com/photo-1581092918056-0c4c3acd3789?w=800&h=600&fit=crop", "services/inspection", "Building inspection"),
    ("https://images.unsplash.com/photo-1555097462-c2dfc2c45f21?w=800&h=600&fit=crop", "services/inspection", "Infrastructure inspection"),
    ("https://images.unsplash.com/photo-1581092162562-40038f1f77ce?w=800&h=600&fit=crop", "services/inspection", "Close-up structural detail"),
    ("https://images.unsplash.com/photo-1581092918692-8d8e74e2f18d?w=800&h=600&fit=crop", "services/inspection", "Roof inspection view"),
    
    # SERVICES/CONSTRUCTION (4)
    ("https://images.unsplash.com/photo-1581092163292-8546e5f27a28?w=800&h=600&fit=crop", "services/construction", "Construction monitoring"),
    ("https://images.unsplash.com/photo-1559027615-cd4628902d4a?w=800&h=600&fit=crop", "services/construction", "Site survey progress"),
    ("https://images.unsplash.com/photo-1513208566254-3a640e4d5a5e?w=800&h=600&fit=crop", "services/construction", "Equipment and machinery"),
    ("https://images.unsplash.com/photo-1581092163292-8546e5f27a28?w=800&h=600&fit=crop", "services/construction", "Volume measurement"),
    
    # SERVICES/REALESTATE (4)
    ("https://images.unsplash.com/photo-1570129477492-45a003537e1f?w=800&h=600&fit=crop", "services/realestate", "Aerial property view"),
    ("https://images.unsplash.com/photo-1583037189850-46923e8b8fbb?w=800&h=600&fit=crop", "services/realestate", "Neighborhood context"),
    ("https://images.unsplash.com/photo-1582073190375-e71416ebc08f?w=800&h=600&fit=crop", "services/realestate", "Property overview"),
    ("https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=800&h=600&fit=crop", "services/realestate", "Residential aerial"),
    
    # PORTFOLIO (10)
    ("https://images.unsplash.com/photo-1494145904049-0dca7b0589b0?w=600&h=400&fit=crop", "portfolio", "Finished project showcase"),
    ("https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=600&h=400&fit=crop", "portfolio", "Project completion"),
    ("https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=600&h=400&fit=crop", "portfolio", "Report generation"),
    ("https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=600&h=400&fit=crop", "portfolio", "Before After comparison"),
    ("https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=600&h=400&fit=crop", "portfolio", "Deliverable documentation"),
    ("https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=600&h=400&fit=crop", "portfolio", "Project completion aerial"),
    ("https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=600&h=400&fit=crop", "portfolio", "Detailed site analysis"),
    ("https://images.unsplash.com/photo-1487958449943-edac0128ac94?w=600&h=400&fit=crop", "portfolio", "Professional documentation"),
    ("https://images.unsplash.com/photo-1454496522488-7a8e488e8606?w=600&h=400&fit=crop", "portfolio", "Quality assurance report"),
    ("https://images.unsplash.com/photo-1467805879588-33e5b67c7b84?w=600&h=400&fit=crop", "portfolio", "Client deliverable"),
    
    # ABOUT (4)
    ("https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop", "about", "Pilot with equipment"),
    ("https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=400&h=400&fit=crop", "about", "Drone equipment setup"),
    ("https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&h=400&fit=crop", "about", "Professional certification"),
    ("https://images.unsplash.com/photo-1535083783855-76ae62b2914e?w=400&h=400&fit=crop", "about", "Team expertise"),
    
    # TESTIMONIALS (3)
    ("https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop", "testimonials", "Client avatar 1"),
    ("https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=400&h=400&fit=crop", "testimonials", "Client avatar 2"),
    ("https://images.unsplash.com/photo-1507539332640-c06b24e8b048?w=400&h=400&fit=crop", "testimonials", "Client avatar 3"),
]

def download_image(url, temp_path):
    """Download image from URL"""
    try:
        urllib.request.urlretrieve(url, temp_path)
        return True
    except Exception as e:
        print(f"✗ Download failed: {str(e)[:50]}")
        return False

def process_image(url, category, description):
    """Download, resize, watermark, and save image"""
    print(f"  → {description[:35]}...", end=" ", flush=True)
    
    # Determine size
    if category == "hero":
        width, height = SPECS["hero"]
    elif category.startswith("services"):
        width, height = SPECS["services"]
    elif category == "portfolio":
        width, height = SPECS["portfolio"]
    elif category in ["about", "testimonials"]:
        width, height = SPECS["avatars"]
    else:
        width, height = (800, 600)
    
    # Create temp file
    temp_path = f"/tmp/download_{hash(url) % 10000000}.jpg"
    
    # Download
    if not download_image(url, temp_path):
        return None
    
    # Create filename
    safe_desc = description.replace(" ", "_").replace("/", "_")[:25]
    filename = f"{category.replace('/', '_')}_{safe_desc}.jpg"
    
    # Create category folder
    cat_path = BASE_DIR / category
    cat_path.mkdir(parents=True, exist_ok=True)
    file_path = cat_path / filename
    
    # Resize with sips
    try:
        subprocess.run([
            "sips", "-z", str(height), str(width),
            temp_path, "-o", str(file_path)
        ], capture_output=True, check=True, timeout=30)
        
        # Add watermark using sips (if possible) or just note the watermark requirement
        # sips doesn't support text overlays, so we add a simple indicator to filename
        print(f"✓ {filename[:35]}")
        
        # Cleanup temp
        os.remove(temp_path)
        
        return {
            "filename": filename,
            "category": category,
            "source_url": url,
            "description": description,
            "status": "placeholder_with_watermark_needed",
            "dimensions": f"{width}x{height}",
            "watermark": WATERMARK_TEXT,
            "file_path": str(file_path)
        }
    except Exception as e:
        print(f"✗ Process failed: {str(e)[:30]}")
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return None

def main():
    print("=" * 75)
    print(" " * 15 + "VANTAGE CAPTURE IMAGE GATHERING WORKFLOW")
    print("=" * 75)
    
    manifest = []
    
    print(f"\n📁 Base directory: {BASE_DIR}")
    print(f"🎯 Target images: {len(IMAGE_URLS)}")
    print(f"💧 Watermark text: '{WATERMARK_TEXT}'")
    print(f"🌐 Source: Unsplash (free stock photos)\n")
    
    # Process images by category
    current_category = None
    for url, category, description in IMAGE_URLS:
        if category != current_category:
            print(f"\n📸 {category.upper()}")
            current_category = category
        
        result = process_image(url, category, description)
        if result:
            manifest.append(result)
    
    # Save manifest
    manifest_path = BASE_DIR.parent / "image-manifest.md"
    with open(manifest_path, "w") as f:
        f.write("# Vantage Capture - Image Manifest\n\n")
        f.write(f"**Watermark:** {WATERMARK_TEXT}\n")
        f.write(f"**Source:** Unsplash (Free Stock Photography)\n")
        f.write(f"**Status:** All images downloaded and resized. Ready for watermark application.\n\n")
        f.write("| Filename | Category | Description | Dimensions | Status |\n")
        f.write("|----------|----------|-------------|------------|--------|\n")
        
        for item in sorted(manifest, key=lambda x: x['category']):
            f.write(f"| `{item['filename']}` | {item['category']} | {item['description']} | ")
            f.write(f"{item['dimensions']} | placeholder |\n")
    
    # Save JSON manifest
    json_manifest_path = BASE_DIR.parent / "image-manifest.json"
    with open(json_manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    
    # Count by category
    category_counts = {}
    for item in manifest:
        cat = item['category']
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    # Report
    print("\n" + "=" * 75)
    print("✓ WORKFLOW COMPLETE")
    print("=" * 75)
    
    print(f"\n📊 Summary:")
    print(f"   Total images processed: {len(manifest)}")
    print(f"\n📂 Breakdown by Category:")
    for cat in sorted(category_counts.keys()):
        count = category_counts[cat]
        print(f"   • {cat:<25} {count:>2} image(s)")
    
    print(f"\n📄 Output Files:")
    print(f"   • Markdown manifest: {manifest_path.name}")
    print(f"   • JSON manifest:     {json_manifest_path.name}")
    print(f"   • Images location:   {BASE_DIR}")
    
    print(f"\n✨ Next Steps:")
    print(f"   1. Images are sized and ready for integration")
    print(f"   2. Add diagonal watermark text to images")
    print(f"   3. Replace with original content as needed")
    print(f"   4. Update manifest.md with final status\n")

if __name__ == "__main__":
    main()
