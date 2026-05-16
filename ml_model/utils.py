import pickle
import json
import numpy as np
import os
import sys

# Global variables to hold loaded model and columns
__model = None
__data_columns = None
__locations = None

# Constants for artifact paths (relative to project root)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "price_predictor.pkl")
COLUMNS_PATH = os.path.join(os.path.dirname(__file__), "columns.json")

def load_saved_artifacts():
    """
    Loads the trained model and column information from saved files.
    Populates the global variables __model, __data_columns, and __locations.
    """
    global __model, __data_columns, __locations

    print("Attempting to load saved artifacts...")
    try:
        # Load columns file
        if not os.path.exists(COLUMNS_PATH):
            raise FileNotFoundError(f"Columns file not found at {COLUMNS_PATH}")
        with open(COLUMNS_PATH, 'r') as f:
            contents = json.load(f)
            __data_columns = contents['data_columns']
            # Extract locations (assuming columns after 'total_sqft', 'bath', 'bhk' are locations)
            __locations = __data_columns[3:]  # Adjust index if needed
            print(f"Loaded {len(__locations)} locations from columns.json.")

        # Load model file
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
        if __model is None:  # Load only if not already loaded
            with open(MODEL_PATH, 'rb') as f:
                __model = pickle.load(f)
            print("Loaded prediction model successfully.")

    except FileNotFoundError as e:
        print(f"Error loading artifacts: {e}")
        raise Exception(f"Required artifact file not found. Ensure '{MODEL_PATH}' and '{COLUMNS_PATH}' exist.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {COLUMNS_PATH}: {e}")
        raise Exception(f"Could not parse '{COLUMNS_PATH}'. Check its format.")
    except pickle.UnpicklingError as e:
        print(f"Error unpickling model from {MODEL_PATH}: {e}")
        raise Exception(f"Could not load model from '{MODEL_PATH}'. File might be corrupted or incompatible.")
    except KeyError as e:
        print(f"Key 'data_columns' not found in {COLUMNS_PATH}: {e}")
        raise Exception(f"'{COLUMNS_PATH}' is missing the 'data_columns' key.")
    except Exception as e:
        print(f"An unexpected error occurred during artifact loading: {e}")
        raise Exception(f"Unexpected error loading artifacts: {str(e)}")

def get_location_names():
    """Returns the list of loaded location names."""
    if __locations is None:
        load_saved_artifacts()  # Attempt to load if not already loaded
    return __locations

def get_data_columns():
    """Returns the list of loaded data columns."""
    if __data_columns is None:
        load_saved_artifacts()
    return __data_columns

def get_estimated_price(location, sqft, bhk, bath):
    """
    Predicts the price based on the loaded model and input features.

    Args:
        location (str): The location name.
        sqft (float): Total square feet.
        bhk (int): Number of bedrooms.
        bath (int): Number of bathrooms.

    Returns:
        float: The estimated price in lakhs.
    """
    try:
        if __model is None:
            load_saved_artifacts()

        # Create input array
        x = np.zeros(len(__data_columns))
        x[0] = sqft
        x[1] = bath
        x[2] = bhk

        # Set location
        if location in __data_columns:
            loc_index = __data_columns.index(location)
            x[loc_index] = 1

        # Predict
        prediction = __model.predict([x])[0]

        # Return prediction in lakhs (assuming model outputs in lakhs)
        return round(prediction, 2)

    except Exception as e:
        print(f"Error in prediction: {e}")
        return -1