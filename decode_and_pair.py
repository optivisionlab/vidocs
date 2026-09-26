from pyzbar.pyzbar import decode
from PIL import Image
import sys, os

# Simulates the ingestion step after "print + scan": given a page image,
# decode its corner QR and pair it back to the correct markdown ground truth.

REGISTRY = {
    "sample1_leave_request": "sample1_leave_request.md",
    "sample2_quarterly_report": "sample2_quarterly_report.md",
}

def pair(image_path, uid_to_name):
    img = Image.open(image_path)
    results = decode(img)
    if not results:
        print(f"[FAIL] {image_path}: no QR detected -> send to manual review queue")
        return
    payload = results[0].data.decode("utf-8")
    print(f"[OK] {image_path}: decoded payload = '{payload}'")
    uid = dict(kv.split("=") for kv in payload.split(";"))["uid"]
    name = uid_to_name.get(uid, "UNKNOWN")
    md_file = REGISTRY.get(name)
    if md_file:
        print(f"     -> matched to ground truth: {md_file}")
    else:
        print(f"     -> uid {uid} not found in registry")

if __name__ == "__main__":
    # uid_to_name would normally be looked up in a real database;
    # here we hardcode the mapping printed by generate.py for this demo run.
    import json
    mapping_path = "uid_map.json"
    if not os.path.exists(mapping_path):
        print("Run generate.py (updated to dump uid_map.json) first.")
        sys.exit(1)
    uid_to_name = json.load(open(mapping_path))
    pair("preview1-1.png", uid_to_name)
    pair("preview2-1.png", uid_to_name)
