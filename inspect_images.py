import os
from PIL import Image
import hashlib
from pillow_heif import register_heif_opener

register_heif_opener()

image_dir = r"D:\AntiGravity\UrnsCatalogue\Images"
output_dir = r"D:\AntiGravity\UrnsCatalogue\Images_Processed"
os.makedirs(output_dir, exist_ok=True)

all_files = sorted(os.listdir(image_dir))
print(f"Total files in source directory: {len(all_files)}")

valid_images = []
duplicates = {}
errors = []

for filename in all_files:
    file_path = os.path.join(image_dir, filename)
    if os.path.isdir(file_path):
        continue
        
    ext = os.path.splitext(filename)[1].lower()
    
    # Process HEIC or typical image formats
    if ext in ['.heic', '.jpg', '.jpeg', '.png', '.webp']:
        try:
            with Image.open(file_path) as img:
                # Check dimensions and format
                width, height = img.size
                
                # Check md5 of content to skip exact duplicates
                file_hash = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
                
                # Convert HEIC to JPG or keep original format
                out_filename = filename
                if ext == '.heic':
                    out_filename = os.path.splitext(filename)[0] + ".jpg"
                
                out_path = os.path.join(output_dir, out_filename)
                
                # If it's HEIC, save as JPEG
                if ext == '.heic':
                    img.convert('RGB').save(out_path, 'JPEG', quality=90)
                else:
                    # Copy or save to output directory
                    img.save(out_path)
                
                if file_hash in duplicates:
                    duplicates[file_hash].append(filename)
                else:
                    duplicates[file_hash] = [filename]
                    valid_images.append({
                        "original_name": filename,
                        "processed_name": out_filename,
                        "width": width,
                        "height": height,
                        "size": os.path.getsize(file_path),
                        "hash": file_hash
                    })
        except Exception as e:
            errors.append((filename, str(e)))

print(f"Successfully processed {len(valid_images)} unique images.")
print(f"Skipped {sum(len(v)-1 for v in duplicates.values())} exact duplicates.")
print(f"Errors encountered for {len(errors)} files: {errors}")

# Write metadata JSON
import json
metadata_path = r"D:\AntiGravity\UrnsCatalogue\image_metadata.json"
with open(metadata_path, 'w') as f:
    json.dump(valid_images, f, indent=2)
print(f"Metadata saved to {metadata_path}")
