import pandas as pd

df = pd.read_csv(r"csv_files\unique_locations_only.csv")
locations = df["location"].tolist()

def sanitize(name: str) -> str:
    name = name.lower().strip()

    # Replace unwanted characters
    for ch in [" ", "-", ".", "/", "(", ")", "&"]:
        name = name.replace(ch, "_")

    # If starts with a number → prefix with "loc_"
    if name[0].isdigit():
        name = "loc_" + name

    # Remove double or triple underscores
    while "__" in name:
        name = name.replace("__", "_")

    return name

with open("area_enum.py", "w", encoding="utf-8") as f:
    f.write("from enum import Enum\n\n")
    f.write("class AreaEnum(str, Enum):\n")

    for loc in locations:
        enum_key = sanitize(loc)
        f.write(f"    {enum_key} = \"{loc}\"\n")

    f.write("    other = \"other\"\n")

print("Enum file generated successfully!")