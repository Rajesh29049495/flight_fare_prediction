import pandas as pd

from ffp.logger import logging
from ffp.exception import ffpException
from ffp.utils import get_collection_as_dataframe
import os, sys
from ffp.entity import config_entity
from ffp.components import data_ingestion, data_validation

if __name__=="__main__":
     try:
          logging.info("just checking th econfig code")
          training_pipeline_config = config_entity.TrainingPipelineConfig()
          data_ingestion_config = config_entity.DataIngestionCofig(training_pipeline_config= training_pipeline_config)
          #print(data_ingestion_config.to_dict())
          data_ingestion = data_ingestion.DataIngestion(data_ingestion_config= data_ingestion_config)
          data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

          data_validation_config = config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
          data_validation = data_validation.DataValidation(data_validation_config= data_validation_config, 
                                        data_ingestion_artifact= data_ingestion_artifact)
          data_validation_artifact = data_validation.initiate_data_validation()
  
     except Exception as e:
          raise ffpException(e,sys)