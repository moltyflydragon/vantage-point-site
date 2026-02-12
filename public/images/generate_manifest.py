#!/usr/bin/env python3
"""
Generate comprehensive manifest of all gathered images
"""

import json
from pathlib import Path
from datetime import datetime
import os

BASE_DIR = Path("/Users/molty/.openclaw/workspace-coder/vantage-capture/assets/images")
PROJECT_ROOT = BASE_DIR.parent

def generate_manifest():
    print("=" * 75)
    print("GENERATING IMAGE MANIFEST")
    print("=" * 75)
    
    # Scan all images
    all_images = sorted(BASE_DIR.rglob("*.jpg"))
    
    manifest_data = {
        "project": "Vantage Capture - Drone Inspection Services",
        "website": "hithisisdan.com",
        "generated": datetime.now().isoformat(),
        "total_images": len(all_images),
        "watermark": "PLACEHOLDER — REPLACE WITH ORIGINAL",
        "status": "ready_for_watermarking",
        "images": []
    }
    
    # Build category counts
    by_category = {}
    
    for img_path in all_images:
        rel_path = img_path.relative_to(BASE_DIR)
        category = str(rel_path.parent)
        
        if category not in by_category:
            by_category[category] = []
        
        size = os.path.getsize(img_path)
        
        img_info = {
            "filename": img_path.name,
            "category": category,
            "path": str(rel_path),
            "full_path": str(img_path),
            "file_size_kb": round(size / 1024, 1),
            "status": "placeholder_watermark_needed",
            "source": "Unsplash (Free Stock Photography)",
            "source_url": "https://unsplash.com",
            "replacement_priority": "high"
        }
        
        by_category[category].append(img_info)
        manifest_data["images"].append(img_info)
    
    # Save JSON manifest
    json_path = PROJECT_ROOT / "image-manifest.json"
    with open(json_path, "w") as f:
        json.dump(manifest_data, f, indent=2)
    
    # Save Markdown manifest
    md_path = PROJECT_ROOT / "image-manifest.md"
    with open(md_path, "w") as f:
        f.write("# Vantage Capture - Image Manifest\n\n")
        f.write(f"**Project:** Vantage Capture Drone Inspection Services\n")
        f.write(f"**Website:** hithisisdan.com\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## Overview\n\n")
        f.write(f"- **Total Images:** {len(all_images)}\n")
        f.write(f"- **Source:** Unsplash (Free Stock Photography)\n")
        f.write(f"- **Watermark:** {manifest_data['watermark']}\n")
        f.write(f"- **Status:** Placeholder images downloaded, sized, and ready for watermarking\n\n")
        
        f.write("## Category Breakdown\n\n")
        
        # Target vs actual
        targets = {
            "hero": 5,
            "services/mapping": 4,
            "services/inspection": 4,
            "services/construction": 4,
            "services/realestate": 4,
            "portfolio": 8,
            "about": 3,
            "testimonials": 2,
            "icons": 3
        }
        
        f.write("| Category | Count | Target | Status |\n")
        f.write("|----------|-------|--------|--------|\n")
        
        for cat in sorted(by_category.keys()):
            count = len(by_category[cat])
            target = targets.get(cat, count)
            status = "✓" if count >= target else "⚠️ Needs more"
            f.write(f"| {cat:25} | {count:>5} | {target:>6} | {status} |\n")
        
        f.write("\n## Image Details\n\n")
        
        for category in sorted(by_category.keys()):
            f.write(f"### {category}\n\n")
            f.write("| Filename | Size | Status |\n")
            f.write("|----------|------|--------|\n")
            
            for img in by_category[category]:
                f.write(f"| `{img['filename']}` | {img['file_size_kb']}KB | {img['status']} |\n")
            
            f.write("\n")
        
        f.write("## Next Steps\n\n")
        f.write("1. **Add Watermarks** - Apply watermark text to each image:\n")
        f.write(f"   - Text: \"{manifest_data['watermark']}\"\n")
        f.write("   - Style: Semi-transparent white, diagonal orientation\n")
        f.write("   - Font size: 48pt\n\n")
        f.write("2. **Supplement Categories** - Add more images to reach targets:\n")
        f.write("   - Consider categories marked '⚠️ Needs more'\n")
        f.write("   - Use original site photography when available\n\n")
        f.write("3. **Quality Check** - Verify all images are:\n")
        f.write("   - Correctly sized and cropped\n")
        f.write("   - Properly watermarked\n")
        f.write("   - Relevant to service/category\n\n")
        f.write("4. **Integration** - Place images in website assets:\n")
        f.write("   - Update image paths in HTML/templates\n")
        f.write("   - Configure CDN/optimization as needed\n")
        f.write("   - Test responsive display\n\n")
        
        f.write("## Target Distribution\n\n")
        f.write("| Category | Purpose | Target Count |\n")
        f.write("|----------|---------|---------------|\n")
        f.write("| hero | Homepage hero sections, before/after | 5-7 |\n")
        f.write("| services/mapping | Orthomosaics, point clouds, 3D renders | 4 |\n")
        f.write("| services/inspection | Infrastructure closeups, roof details | 4 |\n")
        f.write("| services/construction | Progress monitoring, volumetrics | 4 |\n")
        f.write("| services/realestate | Property aerials, neighborhood context | 4 |\n")
        f.write("| portfolio | Finished deliverables, reports, maps | 8-12 |\n")
        f.write("| about | Pilot, equipment, certifications | 3-4 |\n")
        f.write("| testimonials | Client avatars, logos | 2-3 |\n")
        f.write("| icons | Service icons if needed | 3-5 |\n\n")
    
    # Create folder structure summary
    structure_path = PROJECT_ROOT / "FOLDER_STRUCTURE.txt"
    with open(structure_path, "w") as f:
        f.write("VANTAGE CAPTURE - IMAGE ASSET STRUCTURE\n")
        f.write("=" * 60 + "\n\n")
        f.write("vantage-capture/\n")
        f.write("├── assets/\n")
        f.write("│   └── images/\n")
        
        for cat in sorted(by_category.keys()):
            count = len(by_category[cat])
            f.write(f"│       ├── {cat:25} ({count} images)\n")
        
        f.write("│       └── placeholders/\n")
        f.write("├── image-manifest.md      (This file - overview & distribution)\n")
        f.write("├── image-manifest.json    (Machine-readable manifest)\n")
        f.write("└── FOLDER_STRUCTURE.txt   (Directory layout)\n\n")
        f.write("Status: Ready for watermarking and integration\n")
    
    # Report
    print(f"\n📊 IMAGE COLLECTION SUMMARY")
    print(f"=" * 75)
    print(f"\nTotal images collected: {len(all_images)}")
    print(f"\nBreakdown by category:")
    
    total_target = 0
    for cat in sorted(by_category.keys()):
        count = len(by_category[cat])
        target = targets.get(cat, count)
        total_target += target
        status = "✓ OK" if count >= target else f"↑ Need {target - count} more"
        print(f"  • {cat:25} {count:>2} images  ({status})")
    
    print(f"\nTarget total: {total_target} images")
    print(f"Current total: {len(all_images)} images")
    
    if len(all_images) >= 25:
        print(f"\n✓ Minimum target reached (25-35 images)")
    else:
        print(f"\n⚠️  Additional images needed: {25 - len(all_images)}")
    
    print(f"\n📄 Output Files Generated:")
    print(f"  • {json_path.name} - Machine-readable manifest")
    print(f"  • {md_path.name} - Human-readable guide")
    print(f"  • FOLDER_STRUCTURE.txt - Directory layout")
    
    print(f"\n✨ Ready for next steps:")
    print(f"  1. Add watermarks to all images")
    print(f"  2. Supplement missing categories")
    print(f"  3. Integrate into website\n")
    
    return manifest_data

if __name__ == "__main__":
    generate_manifest()
