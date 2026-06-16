import sys
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from ml_pipeline.exception import CustomException
from ml_pipeline.logger import logging
from ml_pipeline.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path: str = os.path.join('backend/artifacts', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        try:
            numerical_columns = ['days_left', 'standard_price', 'is_holiday', 'is_weekend']
            categorical_columns = ['season', 'flight_type', 'class']

            num_pipeline = Pipeline(
                steps=[
                    ("scaler", StandardScaler())
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                    ("one_hot_encoder", OneHotEncoder(handle_unknown='ignore'))
                ]
            )

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipeline", cat_pipeline, categorical_columns)
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)

    def clean_data(self, df):
        """Perform custom cleaning steps, e.g., removing bizarre prices and renaming columns."""
        try:
            logging.info("Cleaning data (removing bizarre prices and selecting features)")
            # Remove bizarre prices
            q_high = df['price'].quantile(0.99)
            df_clean = df[(df['price'] > 0) & (df['price'] <= q_high)].copy()
            
            # Rename price to standard_price
            df_clean.rename(columns={'price': 'standard_price'}, inplace=True)
            
            required_columns = [
                'days_left', 'standard_price', 
                'is_holiday', 'is_weekend', 'season', 'flight_type', 'class', 'passenger_demand'
            ]
            
            # Ensure all required columns exist
            for col in required_columns:
                if col not in df_clean.columns:
                    if col == 'flight_type':
                        df_clean[col] = 'Short Haul'
                    else:
                        df_clean[col] = 0
            
            return df_clean[required_columns].copy()
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test data completed")
            
            train_df = self.clean_data(train_df)
            test_df = self.clean_data(test_df)

            logging.info("Obtaining preprocessing object")
            preprocessing_obj = self.get_data_transformer_object()

            target_column_name = "passenger_demand"
            
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info("Applying preprocessing object on training and testing dataframes.")

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info("Saved preprocessing object.")

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            raise CustomException(e, sys)
