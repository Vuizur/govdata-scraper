import json
import os

def fuse_all_jsonld_files(dir: str):
    """Fuses all jsonld files in the directory"""
    jsonld_files = [f for f in os.listdir(dir)]
    final_file = []
    for jsonld_file in jsonld_files:
        with open(dir + "/" + jsonld_file, "r", encoding="utf-8") as f:
            # Load json LD data
            try:
                json_file = json.load(f)
                final_file.extend(json_file)
            except:
                print("Exception...")
                print(jsonld_file)

    # Write final file to disc
    with open("catalog_full.jsonld", "w", encoding="utf-8") as f:
        json.dump(final_file, f, indent = 2, ensure_ascii=False)

if __name__ == "__main__":
    fuse_all_jsonld_files("govdata_files")