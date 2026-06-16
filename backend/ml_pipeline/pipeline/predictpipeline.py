import sys
import pandas as pd
from ml_pipeline.exception import CustomException
from ml_pipeline.utils import load_object
import os

class PredictPipeline:
    def __init__(self):
        pass

    def predict(self, features):
        try:
            model_path = os.path.join("backend/artifacts", "model.pkl")
            preprocessor_path = os.path.join("backend/artifacts", "preprocessor.pkl")
            
            print("Loading preprocessor and model...")
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            
            print("Scaling features...")
            data_scaled = preprocessor.transform(features)
            
            print("Predicting...")
            preds = model.predict(data_scaled)
            return preds
        
        except Exception as e:
            raise CustomException(e, sys)

class CustomData:
    def __init__(self,
        days_left: int,
        standard_price: float,
        is_holiday: int,
        is_weekend: int,
        season: str,
        flight_type: str,
        class_type: str):

        self.days_left = days_left
        self.standard_price = standard_price
        self.is_holiday = is_holiday
        self.is_weekend = is_weekend
        self.season = season
        self.flight_type = flight_type
        self.class_type = class_type

    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "days_left": [self.days_left],
                "standard_price": [self.standard_price],
                "is_holiday": [self.is_holiday],
                "is_weekend": [self.is_weekend],
                "season": [self.season],
                "flight_type": [self.flight_type],
                "class": [self.class_type],
            }

            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
