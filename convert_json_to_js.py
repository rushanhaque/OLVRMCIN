import json

json_path = r"D:\AntiGravity\UrnsCatalogue\catalog_data.json"
js_path = r"D:\AntiGravity\UrnsCatalogue\catalog_data.js"

with open(json_path, 'r') as f:
    data = json.load(f)

# Write to catalog_data.js as a global window object
with open(js_path, 'w') as f:
    f.write("// Auto-generated catalog data\n")
    f.write("window.catalogData = ")
    json.dump(data, f, indent=2)
    f.write(";\n")

print(f"Successfully converted JSON to JS and wrote to {js_path}")
