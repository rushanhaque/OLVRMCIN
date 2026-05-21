import json
import os

metadata_path = r"D:\AntiGravity\UrnsCatalogue\image_metadata.json"
output_catalog_path = r"D:\AntiGravity\UrnsCatalogue\catalog_data.json"

with open(metadata_path, 'r') as f:
    images = json.load(f)

# Keep all images, as they represent the Oliver McInroy catalog
filtered_images = []
for img in images:
    # Relax filter to include small but high-quality reference images
    if img['size'] < 1000 or img['width'] < 100 or img['height'] < 100:
        print(f"Filtering out thumbnail: {img['original_name']} (Size: {img['size']} bytes, Dimensions: {img['width']}x{img['height']})")
    else:
        filtered_images.append(img)

print(f"Remaining high-quality unique images: {len(filtered_images)}")

# Premium names templates for Oliver McInroy & Co. furniture and lighting
adjectives = [
    "Aura", "Celestial", "Elysian", "Serenity", "Majestic", "Eternal", "Solitude", "Infinity",
    "Tranquil", "Royal", "Legacy", "Classic", "Heritage", "Sovereign", "Divine", "Genesis",
    "Absolute", "Verdant", "Imperial", "Noble", "Opulent", "Valiant", "Zenith", "Haven"
]

materials = [
    "Brass", "Marble", "Bronze", "Oak", "Silver", "Rosewood", "Pewter", "Alabaster",
    "Ceramic", "Slate", "Copper", "Gold Leaf", "Mahogany", "Teak", "Granite", "Nickel",
    "Iron", "Walnut", "Ebony", "Glass", "Stone"
]

product_types = [
    "Console Table", "Pendant Light", "Coffee Table", "Lounge Chair", "Chandelier", 
    "Credenza", "Sofa", "Dining Table", "Wall Sconce", "Side Table", "Floor Lamp"
]

descriptions = [
    "A beautifully handcrafted piece with a polished finish and intricate detailing.",
    "Elegant design meets timeless craftsmanship in this premium furniture item.",
    "Crafted from high-grade materials, offering a dignified and luxurious presence.",
    "A modern, minimalist design featuring clean lines and a premium satin finish.",
    "Intricately hand-engraved detailing makes this piece a unique focal point.",
    "Features a secure structure and felt-lined base to protect fine surfaces.",
    "An exquisite piece combining traditional aesthetics with contemporary durability.",
    "Designed to celebrate a beautiful space with grace, honor, and enduring quality.",
    "A sophisticated statement featuring a smooth, hand-polished premium surface.",
    "Meticulously designed with a light-catching finish and elegant contours."
]

catalog_items = []
sku_counter = 101

for idx, img in enumerate(filtered_images):
    adj = adjectives[idx % len(adjectives)]
    mat = materials[idx % len(materials)]
    ptype = product_types[idx % len(product_types)]
    desc = descriptions[idx % len(descriptions)]
    
    # Ensure uniqueness in name by combining indices or using variations
    item_name = f"{adj} {mat} {ptype}"
    if idx >= len(adjectives) * len(materials) * len(product_types):
        item_name += f" - Edition {idx // 100}"
        
    sku = f"OM-FURN-{sku_counter}"
    if "Light" in ptype or "Lamp" in ptype or "Sconce" in ptype or "Chandelier" in ptype:
        sku = f"OM-LITE-{sku_counter}"
        
    sku_counter += 1
    
    catalog_items.append({
        "name": item_name,
        "sku": sku,
        "description": desc,
        "image_path": f"Images_Processed/{img['processed_name']}",
        "width": img['width'],
        "height": img['height'],
        "size_kb": round(img['size'] / 1024, 1)
    })

# Save catalog data
with open(output_catalog_path, 'w') as f:
    json.dump(catalog_items, f, indent=2)

print(f"Generated {len(catalog_items)} catalog items and saved to {output_catalog_path}")
