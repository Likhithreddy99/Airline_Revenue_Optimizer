import os
import sys
from dataclasses import dataclass
from xgboost import XGBRegressor
from sklearn.metrics import r2_score

from ml_pipeline.exception import CustomException
from ml_pipeline.logger import logging
from ml_pipeline.utils import save_object

@dataclass
class ModelTrainerConfig:
    trained_model_file_path: str = os.path.join("backend/artifacts", "model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Splitting training and test input data")
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )

            logging.info("Training XGBoost model")
            model = XGBRegressor(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=42,
                n_jobs=-1
            )
            
            model.fit(X_train, y_train)

            logging.info("Predicting on test data")
            y_pred = model.predict(X_test)
            r2_square = r2_score(y_test, y_pred)
            
            logging.info(f"Model R2 Score: {r2_square}")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=model
            )

            return r2_square

        except Exception as e:
            raise CustomException(e, sys)
