#!/usr/bin/env python3
"""
Supplement image collection with additional downloads from free stock sources
"""

import os
import urllib.request
import subprocess
from pathlib import Path
import time

BASE_DIR = Path("/Users/molty/.openclaw/workspace-coder/vantage-capture/assets/images")

# Additional working Unsplash image URLs (verified free)
ADDITIONAL_URLS = [
    # Hero images
    ("https://images.unsplash.com/photo-1581092918056-0c4c3acd3789?w=1920&h=1080&fit=crop", "hero", "Modern construction site aerial"),
    ("https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=1920&h=1080&fit=crop", "hero", "Building project overview"),
    
    # Services/Mapping
    ("https://images.unsplash.com/photo-1444080748397-f442aa95c3e5?w=800&h=600&fit=crop", "services/mapping", "Digital analysis interface"),
    ("https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=800&h=600&fit=crop", "services/mapping", "Data visualization dashboard"),
    
    # Services/Inspection  
    ("https://images.unsplash.com/photo-1581092162562-40038f1f77ce?w=800&h=600&fit=crop", "services/inspection", "Detailed inspection closeup"),
    ("https://images.unsplash.com/photo-1581092918692-8d8e74e2f18d?w=800&h=600&fit=crop", "services/inspection", "Structural assessment"),
    
    # Services/Construction
    ("https://images.unsplash.com/photo-1513208566254-3a640e4d5a5e?w=800&h=600&fit=crop", "services/construction", "Site monitoring equipment"),
    ("https://images.unsplash.com/photo-1559027615-cd4628902d4a?w=800&h=600&fit=crop", "services/construction", "Progress tracking"),
    
    # Services/RealEstate
    ("https://images.unsplash.com/photo-1570129477492-45a003537e1f?w=800&h=600&fit=crop", "services/realestate", "Property development view"),
    ("https://images.unsplash.com/photo-1583037189850-46923e8b8fbb?w=800&h=600&fit=crop", "services/realestate", "Aerial neighborhood view"),
    
    # Portfolio
    ("https://images.unsplash.com/photo-1487958449943-edac0128ac94?w=600&h=400&fit=crop", "portfolio", "Delivered project documentation"),
    ("https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=600&h=400&fit=crop", "portfolio", "Site completion report"),
    ("https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=600&h=400&fit=crop", "portfolio", "Final deliverable package"),
]

def download_and_process(url, category, description):
    """Download image and resize with sips"""
    print(f"  ↓ {description[:35]}...", end=" ", flush=True)
    
    # Size mapping
    sizes = {
        "hero": ("1920", "1080"),
        "portfolio": ("600", "400"),
    }
    
    if category.startswith("services"):
        size = ("800", "600")
    elif category in ["about", "testimonials"]:
        size = ("400", "400")
    else:
        size = ("800", "600")
    
    # Create filename
    safe_desc = description.replace(" ", "_").replace("/", "_")[:25]
    filename = f"{category.replace('/', '_')}_{safe_desc}.jpg"
    
    cat_path = BASE_DIR / category
    cat_path.mkdir(parents=True, exist_ok=True)
    file_path = cat_path / filename
    
    # Skip if already exists
    if file_path.exists():
        print("✓ (already exists)")
        return True
    
    # Download to temp
    temp_file = f"/tmp/img_{hash(url) % 10000000}.jpg"
    try:
        urllib.request.urlretrieve(url, temp_file, timeout=30)
    except Exception as e:
        print(f"✗ Download failed")
        return False
    
    # Resize
    try:
        subprocess.run([
            "sips", "-z", size[1], size[0],
            temp_file, "-o", str(file_path)
        ], capture_output=True, check=True, timeout=15)
        print(f"✓ {filename[:30]}")
        os.remove(temp_file)
        return True
    except Exception as e:
        print(f"✗ Resize failed")
        try:
            os.remove(temp_file)
        except:
            pass
        return False

def main():
    print("\n" + "=" * 70)
    print("SUPPLEMENTING IMAGE COLLECTION")
    print("=" * 70)
    print(f"\nTarget: Additional {len(ADDITIONAL_URLS)} images\n")
    
    success = 0
    for url, category, description in ADDITIONAL_URLS:
        if download_and_process(url, category, description):
            success += 1
        time.sleep(0.5)  # Rate limiting
    
    print(f"\n✓ Supplementary download complete: {success}/{len(ADDITIONAL_URLS)} added\n")

if __name__ == "__main__":
    main()
