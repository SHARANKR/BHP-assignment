from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import pickle
import pandas as pd
import numpy as np

# Load X feature table (same columns used during training)
X = pd.read_csv(r"csv_files\X_features.csv")

# Load the trained model
with open("Pickle_file.pickle", "rb") as f:
    model = pickle.load(f)

api = FastAPI()


class ValidInput(BaseModel):
    sqft: float = Field(..., description="Enter the total sqft")
    bhk: int = Field(..., gt=0, lt=6, description="Enter BHK count")
    bath_room: int = Field(..., gt=0, lt=6, description="Enter number of bathrooms")
    area: str = Field(..., description="Enter the location name")


@api.post("/predict")
def predict(data: ValidInput):

    location = data.area.strip()

    # Create empty feature vector
    x = np.zeros(len(X.columns))

    # Fill numeric feature values
    try:
        x[X.columns.get_loc("total_sqft")] = data.sqft
        x[X.columns.get_loc("bath")] = data.bath_room
        x[X.columns.get_loc("bhk")] = data.bhk
    except KeyError:
        return JSONResponse(
            status_code=500,
            content={"error": "Your X_features.csv does not contain the required base columns."}
        )

    # Handle location (one-hot encoding)
    if location in X.columns:
        loc_index = X.columns.get_loc(location)
        x[loc_index] = 1
    else:
        return JSONResponse(
            status_code=400,
            content={"error": f"Location '{location}' not found in training columns"}
        )

    # Predict
    prediction = model.predict([x])[0]

    return JSONResponse(
        status_code=200,
        content={
            "location": location,
            "predicted_price_lakhs": float(prediction)
        }
    )
