from ffp import utils
from ffp.entity import config_entity
from ffp.entity import artifact_entity
from ffp.logger import logging
from ffp.exception import ffpException
import os, sys
import pandas as pd
import numpy as np
#from sklearn.model_selection import train_test_split

class DataIngestion:

    def __init__(self, data_ingestion_config: config_entity.DataIngestionCofig):
        try:
            logging.info(f"{'>>'*20} Data Ingestion {'<<'*20}")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise ffpException(e, sys)
    
    def initiate_data_ingestion(self)-> artifact_entity.DataIngestionArtifact:
        try:
            logging.info(f"Exporting train and test collection data as pandas dataframes")
            df_train:pd.DataFrame = utils.get_collection_as_dataframe(
                database_name = self.data_ingestion_config.database_name, 
                collection_name = self.data_ingestion_config.collection_name1)
            df_test:pd.DataFrame = utils.get_collection_as_dataframe(
                database_name = self.data_ingestion_config.database_name, 
                collection_name = self.data_ingestion_config.collection_name2)
            
            logging.info(f"saving data in dataset")

            #replace na with Nan in both dataframes
            df_train.replace(to_replace='na', value = np.NAN, inplace = True)
            df_test.replace(to_replace='na', value = np.NAN, inplace = True)

            #save data in dataset folder
            logging.info("Create dataset directory folder if not available")
            dataset_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir, exist_ok = True)

            logging.info("Save train and test data to dataset folder")
            df_train.to_csv(path_or_buf = self.data_ingestion_config.train_file_path, index = False, header = True)
            df_test.to_csv(path_or_buf = self.data_ingestion_config.test_file_path, index = False, header = True)

            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                train_file_path=self.data_ingestion_config.train_file_path, 
                test_file_path=self.data_ingestion_config.test_file_path)

            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        
        except Exception as e:
            raise ffpException(e, sys)