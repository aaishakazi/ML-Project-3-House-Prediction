import json
import pickle
import numpy as np
import os

__locations = None
__data_columns = None
__model = None

base_dir = os.path.dirname(__file__)

file_path = os.path.join(base_dir, "artifacts", "columns.json")
model_path = os.path.join(base_dir, "artifacts", "banglore_home_prices_model.pickle")

def get_estimated_price(location, sqft, bhk, bath):
    global __model
    global __data_columns

    try:
        location = location.lower()

        if location in __data_columns:
            loc_index = __data_columns.index(location)
        else:
            loc_index = -1

        x = np.zeros(len(__data_columns))
        x[0] = sqft
        x[1] = bath
        x[2] = bhk

        if loc_index >= 0:
            x[loc_index] = 1

        return round(__model.predict([x])[0], 2)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise e

def get_location_names():
    global __locations
    return __locations

def load_saved_artifacts():
    print("Loading saved artifacts.. start")
    global __data_columns
    global __locations
    global __model

    with open(file_path, "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]
    print("Loading saved artifacts.. end")

    with open(model_path, "rb") as f:
        __model = pickle.load(f)

if __name__ == '__main__':
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price('1st phase jp nagar',1000, 3, 3))
    print(get_estimated_price('1st phase jp nagar', 1000, 2, 2))
    print(get_estimated_price('kalhalli', 1000, 2, 2))
    print(get_estimated_price('ejipura', 1000, 2, 2))