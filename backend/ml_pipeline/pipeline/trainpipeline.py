import sys
from ml_pipeline.components.dataingestion import DataIngestion
from ml_pipeline.components.datatransformation import DataTransformation
from ml_pipeline.components.modeltrainer import ModelTrainer
from ml_pipeline.logger import logging
from ml_pipeline.exception import CustomException

class TrainPipeline:
    def __init__(self):
        pass

    def run_pipeline(self):
        try:
            logging.info("Starting the training pipeline")
            
            data_ingestion = DataIngestion()
            train_data_path, test_data_path = data_ingestion.initiate_data_ingestion()
            
            data_transformation = DataTransformation()
            train_arr, test_arr, _ = data_transformation.initiate_data_transformation(
                train_data_path, test_data_path
            )
            
            model_trainer = ModelTrainer()
            r2_score = model_trainer.initiate_model_trainer(train_arr, test_arr)
            
            logging.info(f"Training pipeline completed successfully. R2 Score: {r2_score}")
            print(f"Training pipeline completed! Model R2 Score: {r2_score}")
            
        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    pipeline = TrainPipeline()
    pipeline.run_pipeline()
