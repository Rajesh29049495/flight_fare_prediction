import os, sys
from ffp.logger import logging
from ffp.exception import ffpException
from datetime import datetime


TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME= "test.csv"


class TrainingPipelineConfig:

    def __init__(self):
        try:
            self.artifact_dir = os.path.join(os.getcwd(), "artifact",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")
        except Exception as e:
            raise ffpException(e, sys)


class DataIngestionCofig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        try:
            self.database_name = "flight_fare_prediction"
            self.collection_name1 = "train"
            self.collection_name2 = "test"
            self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir, "data_ingestion")
            self.train_file_path = os.path.join(self.data_ingestion_dir, "dataset", TRAIN_FILE_NAME)
            self.test_file_path = os.path.join(self.data_ingestion_dir, "dataset", TEST_FILE_NAME)
        except Exception as e:
            raise ffpException(e, sys)
    
    #function to convert above details w.r.t. data ingestion class into dictionary, although not necessary
    def to_dict(self)->dict:
        try:
            return self.__dict__
        except Exception as e:
            raise ffpException(e, sys)



class DataValidationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        try:
            self.data_validation_dir = os.path.join(training_pipeline_config.artifact_dir, "data_validation")
            self.report_file_path = os.path.join(self.data_validation_dir, "report.yaml")
            self.missing_threshold:float = 0.2
            self.base_file_path = os.path.join("Data_Train.xlsx")         
        except Exception as e:
            raise ffpException(e, sys)



class DataTransformationConfig:...
class ModelTrainingConfig:...
class ModelEvaluationConfig:...
class ModelPusherConfig:...