import pandas as pd
from ffp.logger import logging
from ffp.exception import ffpException
from ffp.utils import get_collection_as_dataframe
import os, sys
from ffp.entity import config_entity

from ffp.components.data_ingestion import DataIngestion
from ffp.components.data_validation import DataValidation
from ffp.components.data_transformation import DataTransformation
from ffp.components.model_trainer import ModelTrainer
from ffp.components.model_evaluation import ModelEvaluation 
from ffp.components.model_pusher import ModelPusher 

def start_training_pipeline():
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

          data_transformation_config = config_entity.DataTransformationConfig(training_pipeline_config = training_pipeline_config)
          data_transformation = data_transformation.DataTransformation(data_transformation_config= data_transformation_config,
                                         data_ingestion_artifact= data_ingestion_artifact)
          data_transformation_artifact = data_transformation.initiate_data_transformation()

          model_trainer_config = config_entity.ModelTrainerConfig(training_pipeline_config = training_pipeline_config)
          model_trainer = model_trainer.ModelTrainer(model_trainer_config = model_trainer_config, data_transformation_artifact = data_transformation_artifact)
          model_trainer_artifact = model_trainer.initiate_model_trainer()

          model_eval_config = config_entity.ModelEvaluationConfig(training_pipeline_config = training_pipeline_config)
          model_evaluation = model_evaluation.ModelEvaluation(model_eval_config = model_eval_config,
                    data_ingestion_artifact = data_ingestion_artifact,
                    data_transformation_artifact = data_transformation_artifact,
                    model_trainer_artifact = model_trainer_artifact)
          model_evaluation_artifact = model_evaluation.initiate_model_evaluation()

          model_pusher_config = config_entity.ModelPusherConfig( training_pipeline_config=training_pipeline_config)
          model_pusher = model_pusher.ModelPusher(model_pusher_config= model_pusher_config,
                                                  data_transformation_artifact= data_transformation_artifact,
                                                  model_trainer_artifact = model_trainer_artifact)

          model_pusher_artifact= model_pusher.initiate_model_pusher()
  
     except Exception as e:
          raise ffpException(e,sys)