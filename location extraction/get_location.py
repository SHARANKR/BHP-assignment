import pandas as pd

# Read the CSV (change file name)
a = pd.read_csv("unique_locations.csv")

# Step 1: Clean location text
a["clean_location"] = a["0"].apply(lambda x: x.split(",", 1)[-1].strip())

# Step 2: Get unique cleaned locations
unique_locations = a["clean_location"].unique()

# Step 3: Convert to DataFrame and save
pd.DataFrame(unique_locations, columns=["location"]).to_csv("unique_locations_only.csv", index=False)

import json
import pandas as pd

unique_locations = a["clean_location"].unique().tolist()

with open("locations.json", "w") as f:
    json.dump(unique_locations, f, indent=4)
    





